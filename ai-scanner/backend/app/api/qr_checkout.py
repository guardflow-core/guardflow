import base64
import hmac
import json
import os
import time
from hashlib import sha256
from typing import List, Optional, Dict
from datetime import datetime

from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel, Field


router = APIRouter(prefix="/qr-checkout", tags=["QR Checkout"])


class CartItem(BaseModel):
    sku: str
    name: Optional[str] = None
    unit_price: float = Field(ge=0)
    quantity: int = Field(ge=1)
    expected_weight_kg: float = Field(ge=0)  # peso médio estimado por item
    sensitive: bool = False  # itens de alto risco (ex.: bebidas alcoólicas, eletrônicos)
    esg_score: Optional[float] = Field(None, ge=0, le=10)  # Score ESG do produto
    ncm_code: Optional[str] = None  # Código NCM para ESG Engine


class CartPayload(BaseModel):
    cart_id: str
    store_id: str
    user_id_hash: Optional[str] = None  # pseudonimizado
    items: List[CartItem]
    subtotal: float = Field(ge=0)
    expected_total_weight_kg: float = Field(ge=0)
    timestamp_ms: int
    sector_context: Optional[str] = Field(None, pattern=r"^(retail|industrial|mobility|security|esg)$")  # SYMBEON Personality
    store_type: Optional[str] = None  # supermercado, farmacia, etc.


class SealRequest(BaseModel):
    cart: CartPayload


class SealResponse(BaseModel):
    cart_id: str
    store_id: str
    hash: str
    signature: str
    timestamp_ms: int
    qr_token: str  # base64(cart_id|hash|signature|timestamp)
    agility_tax_applicable: bool = False
    estimated_time_saved_minutes: float = 0.0
    esg_impact_score: Optional[float] = None


class VerifyRequest(BaseModel):
    qr_token: str


class VerifyResponse(BaseModel):
    valid: bool
    reason: Optional[str] = None
    cart_id: Optional[str] = None
    store_id: Optional[str] = None
    timestamp_ms: Optional[int] = None


class WeightCheckRequest(BaseModel):
    cart_id: str
    measured_weight_kg: float = Field(ge=0)
    expected_weight_kg: float = Field(ge=0)


class AnomalyScoreRequest(BaseModel):
    expected_weight_kg: float = Field(ge=0)
    measured_weight_kg: float = Field(ge=0)
    items: List[CartItem]
    scan_duration_sec: Optional[int] = 0
    user_risk_score: Optional[float] = 0.0  # se houver histórico (0–1)
    sector_context: Optional[str] = None  # retail, industrial, etc.
    store_type: Optional[str] = None  # supermercado, farmacia, etc.
    time_of_day: Optional[int] = None  # hora do dia (0-23)
    guardpass_tier: Optional[str] = None  # basic, premium, enterprise


class AnomalyScoreResponse(BaseModel):
    delta_weight_ratio: float
    sensitive_items_flag: bool
    time_factor: float
    user_factor: float
    score: float
    decision: str  # allow / sample / block


def _secret() -> bytes:
    # Segredo HMAC (para PoC). Em produção preferir assinatura assimétrica (RSA/ECDSA)
    secret = os.getenv("GUARDPASS_QR_SECRET", "dev-secret-change-me")
    return secret.encode()


def _hash_cart(cart: CartPayload) -> str:
    # Campos canônicos
    material = {
        "cart_id": cart.cart_id,
        "store_id": cart.store_id,
        "timestamp_ms": cart.timestamp_ms,
        "items": [
            {
                "sku": it.sku,
                "qty": it.quantity,
                "price": it.unit_price,
                "w": it.expected_weight_kg,
                "sens": it.sensitive,
            }
            for it in cart.items
        ],
        "subtotal": cart.subtotal,
        "expected_total_weight_kg": cart.expected_total_weight_kg,
    }
    payload = json.dumps(material, separators=(",", ":"), sort_keys=True)
    return sha256(payload.encode()).hexdigest()


def _sign(hash_hex: str) -> str:
    sig = hmac.new(_secret(), hash_hex.encode(), sha256).hexdigest()
    return sig


# === INTEGRAÇÃO COM GUARDPASS ===
async def _get_guardpass_profile(guardpass_token: Optional[str]) -> Dict:
    """Integração real com GuardPass"""
    if not guardpass_token:
        from app.services.guardpass_integration import guardpass_service
        return guardpass_service._default_profile()
    
    try:
        from app.services.guardpass_integration import guardpass_service
        profile = await guardpass_service.get_user_profile(guardpass_token)
        return profile
    except Exception as e:
        print(f"Erro na integração GuardPass: {e}")
        # Fallback para perfil básico
        return {"tier": "basic", "risk_score": 0.5, "esg_tier": "basic"}


# === INTEGRAÇÃO COM ESG ENGINE ===
async def _calculate_esg_impact(items: List[CartItem]) -> float:
    """Calcula impacto ESG do carrinho usando ESG Engine real"""
    try:
        from app.services.esg_engine_integration import esg_engine_service
        
        # Converter CartItem para dict para o ESG Engine
        items_dict = []
        for item in items:
            items_dict.append({
                "sku": item.sku,
                "name": item.name,
                "unit_price": item.unit_price,
                "quantity": item.quantity,
                "expected_weight_kg": item.expected_weight_kg,
                "esg_score": item.esg_score,
                "ncm_code": item.ncm_code
            })
        
        # Calcular impacto ESG completo
        esg_result = await esg_engine_service.calculate_cart_esg_impact(items_dict)
        return esg_result.get("overall_score", 0.0)
        
    except Exception as e:
        print(f"Erro na integração ESG Engine: {e}")
        # Fallback para cálculo simples
        total_impact = 0.0
        total_value = 0.0
        
        for item in items:
            item_value = item.unit_price * item.quantity
            total_value += item_value
            
            if item.esg_score:
                total_impact += item.esg_score * item_value
            else:
                # Score médio como fallback
                total_impact += 5.0 * item_value
        
        return total_impact / total_value if total_value > 0 else 0.0


# === THRESHOLDS ADAPTATIVOS ===
def _get_adaptive_thresholds(sector_context: Optional[str], store_type: Optional[str], 
                           time_of_day: Optional[int], guardpass_tier: Optional[str]) -> Dict[str, float]:
    """Calcula thresholds adaptativos baseados no contexto"""
    base_thresholds = {"allow": 0.35, "sample": 0.6}
    
    # Ajustes por setor (SYMBEON Personality)
    sector_adjustments = {
        "retail": {"allow": 0.0, "sample": 0.0},  # Padrão
        "industrial": {"allow": -0.05, "sample": -0.05},  # Mais rigoroso
        "mobility": {"allow": 0.05, "sample": 0.05},  # Mais tolerante
        "security": {"allow": -0.1, "sample": -0.1},  # Muito rigoroso
        "esg": {"allow": 0.1, "sample": 0.1}  # Mais tolerante para ESG
    }
    
    # Ajustes por tipo de loja
    store_adjustments = {
        "supermercado": {"allow": 0.05, "sample": 0.05},  # Produtos a granel
        "farmacia": {"allow": -0.1, "sample": -0.1},  # Produtos controlados
        "eletronicos": {"allow": -0.05, "sample": -0.05},  # Alto valor
        "conveniencia": {"allow": 0.1, "sample": 0.1}  # Mais flexível
    }
    
    # Ajustes por horário
    time_adjustments = {"allow": 0.0, "sample": 0.0}
    if time_of_day:
        if 22 <= time_of_day or time_of_day <= 6:  # Madrugada
            time_adjustments = {"allow": -0.05, "sample": -0.05}
        elif 18 <= time_of_day <= 21:  # Horário de pico
            time_adjustments = {"allow": 0.05, "sample": 0.05}
    
    # Ajustes por tier GuardPass
    guardpass_adjustments = {
        "basic": {"allow": 0.0, "sample": 0.0},
        "premium": {"allow": 0.1, "sample": 0.1},  # Mais tolerante
        "enterprise": {"allow": 0.15, "sample": 0.15}  # Muito tolerante
    }
    
    # Aplicar ajustes
    final_thresholds = base_thresholds.copy()
    
    if sector_context and sector_context in sector_adjustments:
        adj = sector_adjustments[sector_context]
        final_thresholds["allow"] += adj["allow"]
        final_thresholds["sample"] += adj["sample"]
    
    if store_type and store_type in store_adjustments:
        adj = store_adjustments[store_type]
        final_thresholds["allow"] += adj["allow"]
        final_thresholds["sample"] += adj["sample"]
    
    final_thresholds["allow"] += time_adjustments["allow"]
    final_thresholds["sample"] += time_adjustments["sample"]
    
    if guardpass_tier and guardpass_tier in guardpass_adjustments:
        adj = guardpass_adjustments[guardpass_tier]
        final_thresholds["allow"] += adj["allow"]
        final_thresholds["sample"] += adj["sample"]
    
    # Garantir limites válidos
    final_thresholds["allow"] = max(0.1, min(0.8, final_thresholds["allow"]))
    final_thresholds["sample"] = max(0.2, min(0.9, final_thresholds["sample"]))
    
    return final_thresholds


# === MÉTRICAS PARA AGILITY TAX ===
async def _record_checkout_metrics(cart: CartPayload, checkout_time_seconds: float):
    """Registra métricas para cálculo de Agility Tax ROI"""
    # TODO: Integrar com sistema de métricas real (Prometheus/InfluxDB)
    metrics = {
        "store_id": cart.store_id,
        "checkout_time_seconds": checkout_time_seconds,
        "items_count": len(cart.items),
        "total_value": cart.subtotal,
        "method": "qr_checkout",
        "timestamp": datetime.now().isoformat(),
        "sector_context": cart.sector_context
    }
    
    # Simular registro de métricas
    print(f"📊 Métricas registradas: {metrics}")
    return metrics


@router.post("/seal", response_model=SealResponse)
async def seal_cart(
    req: SealRequest, 
    guardpass_token: Optional[str] = Header(None),
    seve_anonymous_id: Optional[str] = Header(None)
):
    start_time = time.time()
    
    # Integração com SEVE Personalization (se disponível)
    seve_context = None
    if seve_anonymous_id:
        try:
            from app.services.seve_personalization import seve_personalization
            # Atualizar perfil SEVE com dados da compra
            seve_interaction = {
                "purchased_esg_products": any(item.esg_score and item.esg_score > 7.0 for item in req.cart.items),
                "viewed_brands": [item.name.split()[0] if item.name else "Unknown" for item in req.cart.items],
                "viewed_categories": list(set([item.ncm_code[:2] if item.ncm_code else "00" for item in req.cart.items])),
                "premium_product_views": any(item.unit_price > 20.0 for item in req.cart.items)
            }
            seve_context = await seve_personalization.update_profile_interaction(
                seve_anonymous_id, seve_interaction
            )
        except Exception as e:
            print(f"Erro na integração SEVE: {e}")
    
    # Integração com GuardPass
    guardpass_profile = await _get_guardpass_profile(guardpass_token)
    
    # Calcular impacto ESG (enriquecido com dados SEVE)
    esg_impact = await _calculate_esg_impact(req.cart.items)
    
    # Gerar hash e assinatura
    h = _hash_cart(req.cart)
    sig = _sign(h)
    ts = req.cart.timestamp_ms
    token_raw = f"{req.cart.cart_id}|{h}|{sig}|{ts}"
    token = base64.urlsafe_b64encode(token_raw.encode()).decode()
    
    # Calcular tempo economizado (estimativa)
    traditional_time = len(req.cart.items) * 0.5  # 30s por item tradicional
    qr_time = len(req.cart.items) * 0.1  # 6s por item com QR
    time_saved = max(0, traditional_time - qr_time)
    
    # Registrar métricas para Agility Tax
    checkout_time = time.time() - start_time
    await _record_checkout_metrics(req.cart, checkout_time)
    
    return SealResponse(
        cart_id=req.cart.cart_id,
        store_id=req.cart.store_id,
        hash=h,
        signature=sig,
        timestamp_ms=ts,
        qr_token=token,
        agility_tax_applicable=True,
        estimated_time_saved_minutes=round(time_saved, 2),
        esg_impact_score=round(esg_impact, 2) if esg_impact > 0 else None
    )


@router.post("/verify", response_model=VerifyResponse)
async def verify_qr(req: VerifyRequest):
    try:
        decoded = base64.urlsafe_b64decode(req.qr_token.encode()).decode()
        cart_id, hash_hex, signature, ts_str = decoded.split("|")
    except Exception:
        return VerifyResponse(valid=False, reason="invalid_token")

    expected_sig = _sign(hash_hex)
    if not hmac.compare_digest(expected_sig, signature):
        return VerifyResponse(valid=False, reason="invalid_signature")

    # tolerância de tempo (ex.: 2h)
    now_ms = int(time.time() * 1000)
    if now_ms - int(ts_str) > 2 * 60 * 60 * 1000:
        return VerifyResponse(valid=False, reason="expired", cart_id=cart_id, timestamp_ms=int(ts_str))

    return VerifyResponse(valid=True, cart_id=cart_id, timestamp_ms=int(ts_str))


@router.post("/weight-check")
async def weight_check(req: WeightCheckRequest) -> Dict[str, float]:
    diff = req.measured_weight_kg - req.expected_weight_kg
    ratio = (diff / req.expected_weight_kg) if req.expected_weight_kg > 0 else 0.0
    return {"delta_weight_kg": round(diff, 3), "delta_ratio": round(ratio, 4)}


@router.post("/anomaly-score", response_model=AnomalyScoreResponse)
async def anomaly_score(req: AnomalyScoreRequest, guardpass_token: Optional[str] = Header(None)):
    # Integração com GuardPass
    guardpass_profile = await _get_guardpass_profile(guardpass_token)
    
    # Thresholds adaptativos baseados no contexto
    thresholds = _get_adaptive_thresholds(
        req.sector_context, 
        req.store_type, 
        req.time_of_day, 
        req.guardpass_tier or guardpass_profile.get("tier")
    )
    
    # Pesos ajustados por contexto
    base_weights = {"weight": 0.5, "sensitive": 0.2, "time": 0.15, "user": 0.15}
    
    # Ajustar pesos por setor (SYMBEON Personality)
    if req.sector_context == "esg":
        # ESG: menos peso para itens sensíveis, mais para usuário
        base_weights.update({"sensitive": 0.1, "user": 0.25})
    elif req.sector_context == "security":
        # Segurança: mais peso para itens sensíveis
        base_weights.update({"sensitive": 0.3, "weight": 0.4})
    
    # Delta peso relativo
    exp = max(req.expected_weight_kg, 0.0001)
    delta_ratio = abs(req.measured_weight_kg - exp) / exp
    
    # Flag de itens sensíveis
    sensitive_flag = any(i.sensitive for i in req.items)
    
    # Fator de tempo (scan muito rápido pode indicar risco)
    time_factor = 1.0 if (req.scan_duration_sec or 0) < 20 else 0.3
    
    # Fator de usuário melhorado com GuardPass
    user_risk = req.user_risk_score or guardpass_profile.get("risk_score", 0.5)
    user_factor = min(max(user_risk, 0.0), 1.0)
    
    # Ajuste por tier GuardPass
    if guardpass_profile.get("tier") == "premium":
        user_factor *= 0.7  # Reduz risco para usuários premium
    elif guardpass_profile.get("tier") == "enterprise":
        user_factor *= 0.5  # Reduz ainda mais para enterprise
    
    # Calcular score com pesos adaptativos
    score = (
        base_weights["weight"] * min(delta_ratio, 1.0)
        + base_weights["sensitive"] * (1.0 if sensitive_flag else 0.0)
        + base_weights["time"] * time_factor
        + base_weights["user"] * user_factor
    )
    
    # Decisão com thresholds adaptativos
    if score < thresholds["allow"]:
        decision = "allow"
    elif score < thresholds["sample"]:
        decision = "sample"
    else:
        decision = "block"
    
    return AnomalyScoreResponse(
        delta_weight_ratio=round(delta_ratio, 4),
        sensitive_items_flag=sensitive_flag,
        time_factor=round(time_factor, 2),
        user_factor=round(user_factor, 2),
        score=round(score, 3),
        decision=decision,
    )


@router.post("/seal-with-guardpass", response_model=SealResponse)
async def seal_with_guardpass(req: SealRequest, guardpass_token: str = Header(...)):
    """Endpoint otimizado para integração com GuardPass"""
    start_time = time.time()
    
    # Validar e obter perfil GuardPass
    guardpass_profile = await _get_guardpass_profile(guardpass_token)
    if not guardpass_profile:
        raise HTTPException(status_code=401, detail="Token GuardPass inválido")
    
    # Aplicar benefícios ESG se usuário for premium
    esg_impact = await _calculate_esg_impact(req.cart.items)
    esg_bonus = 0.0
    if guardpass_profile.get("esg_tier") == "premium" and esg_impact > 7.0:
        esg_bonus = 2.0  # Bônus de tempo para compras ESG premium
    
    # Gerar hash e assinatura
    h = _hash_cart(req.cart)
    sig = _sign(h)
    ts = req.cart.timestamp_ms
    token_raw = f"{req.cart.cart_id}|{h}|{sig}|{ts}"
    token = base64.urlsafe_b64encode(token_raw.encode()).decode()
    
    # Calcular tempo economizado com bônus ESG
    traditional_time = len(req.cart.items) * 0.5
    qr_time = len(req.cart.items) * 0.1
    time_saved = max(0, traditional_time - qr_time + esg_bonus)
    
    # Registrar métricas enriquecidas
    checkout_time = time.time() - start_time
    metrics = await _record_checkout_metrics(req.cart, checkout_time)
    metrics.update({
        "guardpass_tier": guardpass_profile.get("tier"),
        "esg_impact": esg_impact,
        "esg_bonus": esg_bonus
    })
    
    return SealResponse(
        cart_id=req.cart.cart_id,
        store_id=req.cart.store_id,
        hash=h,
        signature=sig,
        timestamp_ms=ts,
        qr_token=token,
        agility_tax_applicable=True,
        estimated_time_saved_minutes=round(time_saved, 2),
        esg_impact_score=round(esg_impact, 2) if esg_impact > 0 else None
    )


@router.get("/metrics/{store_id}")
async def get_checkout_metrics(store_id: str):
    """Endpoint para obter métricas de checkout para Agility Tax"""
    # TODO: Integrar com sistema de métricas real
    return {
        "store_id": store_id,
        "total_checkouts": 1250,
        "qr_checkouts": 890,
        "average_time_traditional": 180.5,  # segundos
        "average_time_qr": 45.2,  # segundos
        "time_saved_total": 120397.0,  # segundos totais economizados
        "conversion_boost": 6.8,
        "abandonment_reduction": 0.73,
        "agility_tax_justified": True,
        "roi_estimate": 425.6  # % ROI
    }


@router.get("/esg-insights/{store_id}")
async def get_esg_insights(store_id: str, period_days: int = 30):
    """Endpoint para obter insights ESG da loja"""
    try:
        from app.services.esg_engine_integration import esg_engine_service
        insights = await esg_engine_service.get_esg_insights(store_id, period_days)
        return insights
    except Exception as e:
        return {
            "error": f"Erro ao obter insights ESG: {str(e)}",
            "store_id": store_id,
            "period_days": period_days
        }


@router.post("/record-transaction")
async def record_transaction(
    cart_id: str,
    store_id: str,
    esg_impact: float,
    guardpass_token: Optional[str] = Header(None)
):
    """Registra transação nos sistemas GuardPass e ESG Engine"""
    results = {"guardpass": False, "esg_engine": False}
    
    # Registrar no GuardPass se token fornecido
    if guardpass_token:
        try:
            from app.services.guardpass_integration import guardpass_service
            profile = await guardpass_service.get_user_profile(guardpass_token)
            
            if profile.get("user_id"):
                success = await guardpass_service.record_transaction(
                    profile["user_id"],
                    {
                        "cart_id": cart_id,
                        "store_id": store_id,
                        "esg_score": esg_impact,
                        "amount": 0  # Seria passado do carrinho real
                    }
                )
                results["guardpass"] = success
        except Exception as e:
            print(f"Erro ao registrar no GuardPass: {e}")
    
    # Registrar no ESG Engine
    try:
        from app.services.esg_engine_integration import esg_engine_service
        success = await esg_engine_service.register_esg_transaction({
            "cart_id": cart_id,
            "store_id": store_id,
            "esg_impact": {"overall_score": esg_impact}
        })
        results["esg_engine"] = success
    except Exception as e:
        print(f"Erro ao registrar no ESG Engine: {e}")
    
    return {
        "cart_id": cart_id,
        "registration_results": results,
        "success": any(results.values())
    }


@router.get("/calibration/analyze")
async def analyze_threshold_calibration():
    """Analisa dados de piloto e sugere calibração de thresholds"""
    try:
        from app.services.threshold_calibration import threshold_calibrator
        analysis = threshold_calibrator.get_calibration_by_context()
        return {
            "status": "success",
            "analysis": analysis,
            "summary": {
                "contexts_analyzed": len(analysis),
                "recommendations": [
                    {
                        "context": k,
                        "action": v.get("recommendation", {}).get("action", "UNKNOWN"),
                        "confidence": v.get("validation", {}).get("f1_score", 0)
                    }
                    for k, v in analysis.items()
                    if "recommendation" in v
                ]
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.post("/calibration/apply")
async def apply_threshold_calibration():
    """Aplica thresholds calibrados para produção"""
    try:
        from app.services.threshold_calibration import threshold_calibrator
        result = threshold_calibrator.export_calibrated_thresholds()
        return {
            "status": "success",
            "message": "Thresholds calibrados aplicados com sucesso",
            "result": result
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/calibration/status")
async def get_calibration_status():
    """Obtém status atual da calibração"""
    try:
        import os
        from datetime import datetime
        
        # Verificar se existem arquivos de calibração
        calibration_file = "threshold_calibration_data.json"
        production_file = "production_thresholds.json"
        
        status = {
            "calibration_data_exists": os.path.exists(calibration_file),
            "production_config_exists": os.path.exists(production_file),
            "last_calibration": None,
            "current_thresholds": {"allow": 0.35, "sample": 0.6}
        }
        
        if os.path.exists(production_file):
            try:
                import json
                with open(production_file, 'r') as f:
                    config = json.load(f)
                    status["last_calibration"] = config.get("calibrated_at")
                    status["calibrated_contexts"] = list(config.get("thresholds", {}).keys())
            except:
                pass
        
        return status
    except Exception as e:
        return {"status": "error", "message": str(e)}


