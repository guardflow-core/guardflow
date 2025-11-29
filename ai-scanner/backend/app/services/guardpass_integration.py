"""
Integração real com GuardPass
Substitui a simulação por cliente HTTP real
"""

import httpx
import os
from typing import Dict, Optional
from datetime import datetime, timedelta
import jwt
import logging

logger = logging.getLogger(__name__)

class GuardPassService:
    def __init__(self):
        self.base_url = os.getenv("GUARDPASS_API_URL", "https://api.guardpass.com")
        self.api_key = os.getenv("GUARDPASS_API_KEY", "")
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            timeout=10.0
        )
    
    async def validate_token(self, token: str) -> Dict:
        """Valida token GuardPass e retorna dados do usuário"""
        try:
            # Tentar decodificar JWT localmente primeiro
            payload = jwt.decode(token, options={"verify_signature": False})
            user_id = payload.get("user_id")
            
            if not user_id:
                return {"valid": False, "reason": "invalid_token"}
            
            # Buscar perfil completo na API
            response = await self.client.get(f"/users/{user_id}/profile")
            
            if response.status_code == 200:
                profile_data = response.json()
                return {
                    "valid": True,
                    "user_id": user_id,
                    "profile": profile_data
                }
            else:
                logger.warning(f"GuardPass API error: {response.status_code}")
                return {"valid": False, "reason": "api_error"}
                
        except jwt.InvalidTokenError:
            return {"valid": False, "reason": "invalid_jwt"}
        except httpx.RequestError as e:
            logger.error(f"GuardPass connection error: {e}")
            # Fallback para modo offline
            return await self._offline_validation(token)
        except Exception as e:
            logger.error(f"GuardPass validation error: {e}")
            return {"valid": False, "reason": "validation_error"}
    
    async def get_user_profile(self, token: str) -> Dict:
        """Obtém perfil completo do usuário"""
        validation = await self.validate_token(token)
        
        if not validation.get("valid"):
            return self._default_profile()
        
        profile = validation.get("profile", {})
        
        # Mapear dados do GuardPass para formato interno
        return {
            "user_id": validation.get("user_id"),
            "tier": profile.get("subscription_tier", "basic"),
            "risk_score": self._calculate_risk_score(profile),
            "esg_tier": profile.get("esg_tier", "basic"),
            "transaction_history": profile.get("transaction_count", 0),
            "fraud_incidents": profile.get("fraud_incidents", 0),
            "kyc_verified": profile.get("kyc_verified", False),
            "created_at": profile.get("created_at"),
            "last_activity": profile.get("last_activity")
        }
    
    async def record_transaction(self, user_id: str, transaction_data: Dict) -> bool:
        """Registra transação no GuardPass para histórico"""
        try:
            payload = {
                "user_id": user_id,
                "transaction_type": "qr_checkout",
                "amount": transaction_data.get("amount", 0),
                "store_id": transaction_data.get("store_id"),
                "items_count": len(transaction_data.get("items", [])),
                "esg_score": transaction_data.get("esg_score"),
                "timestamp": datetime.now().isoformat()
            }
            
            response = await self.client.post("/transactions", json=payload)
            return response.status_code == 201
            
        except Exception as e:
            logger.error(f"Error recording transaction: {e}")
            return False
    
    async def update_risk_score(self, user_id: str, incident_type: str, severity: float) -> bool:
        """Atualiza score de risco baseado em incidentes"""
        try:
            payload = {
                "user_id": user_id,
                "incident_type": incident_type,  # fraud_attempt, anomaly_detected, etc.
                "severity": severity,  # 0.0 - 1.0
                "timestamp": datetime.now().isoformat()
            }
            
            response = await self.client.post("/risk-incidents", json=payload)
            return response.status_code == 201
            
        except Exception as e:
            logger.error(f"Error updating risk score: {e}")
            return False
    
    def _calculate_risk_score(self, profile: Dict) -> float:
        """Calcula score de risco baseado no perfil"""
        base_risk = 0.5  # Risco neutro
        
        # Fatores que reduzem risco
        if profile.get("kyc_verified"):
            base_risk -= 0.2
        
        if profile.get("transaction_count", 0) > 100:
            base_risk -= 0.1
        
        if profile.get("subscription_tier") in ["premium", "enterprise"]:
            base_risk -= 0.15
        
        # Fatores que aumentam risco
        fraud_incidents = profile.get("fraud_incidents", 0)
        if fraud_incidents > 0:
            base_risk += min(fraud_incidents * 0.1, 0.3)
        
        # Inatividade recente
        last_activity = profile.get("last_activity")
        if last_activity:
            try:
                last_date = datetime.fromisoformat(last_activity.replace('Z', '+00:00'))
                days_inactive = (datetime.now() - last_date).days
                if days_inactive > 30:
                    base_risk += 0.1
            except:
                pass
        
        return max(0.0, min(1.0, base_risk))
    
    async def _offline_validation(self, token: str) -> Dict:
        """Validação offline quando API não está disponível"""
        try:
            # Decodificar JWT sem verificar assinatura (modo degradado)
            payload = jwt.decode(token, options={"verify_signature": False})
            
            # Verificar expiração
            exp = payload.get("exp")
            if exp and datetime.fromtimestamp(exp) < datetime.now():
                return {"valid": False, "reason": "token_expired"}
            
            return {
                "valid": True,
                "user_id": payload.get("user_id"),
                "profile": {
                    "subscription_tier": payload.get("tier", "basic"),
                    "esg_tier": payload.get("esg_tier", "basic"),
                    "offline_mode": True
                }
            }
        except:
            return {"valid": False, "reason": "offline_validation_failed"}
    
    def _default_profile(self) -> Dict:
        """Perfil padrão para usuários não autenticados"""
        return {
            "user_id": None,
            "tier": "basic",
            "risk_score": 0.5,
            "esg_tier": "basic",
            "transaction_history": 0,
            "fraud_incidents": 0,
            "kyc_verified": False
        }
    
    async def close(self):
        """Fechar cliente HTTP"""
        await self.client.aclose()

# Instância global do serviço
guardpass_service = GuardPassService()
