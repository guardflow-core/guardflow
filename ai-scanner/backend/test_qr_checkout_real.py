#!/usr/bin/env python3
"""
Teste da API QR Checkout com dados reais
Simula cenários de supermercado, farmácia e eletrônicos
"""

import asyncio
import json
import time
from typing import Dict, List
import httpx

# Configuração da API
API_BASE = "http://localhost:8002/api/v1/qr-checkout"
GUARDPASS_TOKEN = "test_premium_user_token_123"

# Dados reais de produtos
REAL_PRODUCTS = {
    "supermercado": [
        {"sku": "7891000100103", "name": "Leite Integral 1L", "price": 4.50, "weight": 1.03, "esg_score": 6.5, "ncm": "04011010"},
        {"sku": "7891000315507", "name": "Açúcar Cristal 1kg", "price": 3.20, "weight": 1.0, "esg_score": 4.0, "ncm": "17019900"},
        {"sku": "7891000053508", "name": "Arroz Branco 5kg", "price": 18.90, "weight": 5.0, "esg_score": 5.5, "ncm": "10063021"},
        {"sku": "7891000244203", "name": "Feijão Preto 1kg", "price": 7.80, "weight": 1.0, "esg_score": 7.2, "ncm": "07133390"},
        {"sku": "7891991010016", "name": "Cerveja Lata 350ml", "price": 2.80, "weight": 0.35, "esg_score": 3.0, "ncm": "22030000", "sensitive": True}
    ],
    "farmacia": [
        {"sku": "7896658003912", "name": "Dipirona 500mg", "price": 8.50, "weight": 0.05, "esg_score": 8.0, "ncm": "30049099", "sensitive": True},
        {"sku": "7896112108721", "name": "Vitamina C 1g", "price": 15.20, "weight": 0.08, "esg_score": 7.5, "ncm": "21069090"},
        {"sku": "7896658001123", "name": "Protetor Solar FPS60", "price": 28.90, "weight": 0.12, "esg_score": 6.8, "ncm": "33049900"}
    ],
    "eletronicos": [
        {"sku": "7899619404567", "name": "Cabo USB-C 1m", "price": 25.90, "weight": 0.15, "esg_score": 4.5, "ncm": "85444290"},
        {"sku": "7891234567890", "name": "Fone Bluetooth", "price": 89.90, "weight": 0.25, "esg_score": 5.2, "ncm": "85183000", "sensitive": True},
        {"sku": "7891234567891", "name": "Carregador Wireless", "price": 45.50, "weight": 0.18, "esg_score": 6.0, "ncm": "85044030"}
    ]
}

# Cenários de teste
TEST_SCENARIOS = [
    {
        "name": "Supermercado - Compra Família",
        "store_type": "supermercado",
        "sector_context": "retail",
        "products": ["7891000100103", "7891000315507", "7891000053508", "7891000244203"],
        "quantities": [2, 1, 1, 2],
        "guardpass_tier": "premium"
    },
    {
        "name": "Farmácia - Medicamentos",
        "store_type": "farmacia", 
        "sector_context": "security",
        "products": ["7896658003912", "7896112108721"],
        "quantities": [1, 2],
        "guardpass_tier": "basic"
    },
    {
        "name": "Eletrônicos - Acessórios",
        "store_type": "eletronicos",
        "sector_context": "retail", 
        "products": ["7899619404567", "7891234567890", "7891234567891"],
        "quantities": [1, 1, 1],
        "guardpass_tier": "enterprise"
    },
    {
        "name": "Supermercado - Com Álcool",
        "store_type": "supermercado",
        "sector_context": "retail",
        "products": ["7891000100103", "7891991010016"],
        "quantities": [1, 6],
        "guardpass_tier": "basic"
    }
]

async def create_cart_from_scenario(scenario: Dict) -> Dict:
    """Cria carrinho baseado no cenário"""
    store_products = REAL_PRODUCTS[scenario["store_type"]]
    product_map = {p["sku"]: p for p in store_products}
    
    items = []
    total_price = 0.0
    total_weight = 0.0
    
    for sku, qty in zip(scenario["products"], scenario["quantities"]):
        if sku in product_map:
            product = product_map[sku]
            item_price = product["price"] * qty
            item_weight = product["weight"] * qty
            
            items.append({
                "sku": sku,
                "name": product["name"],
                "unit_price": product["price"],
                "quantity": qty,
                "expected_weight_kg": product["weight"],
                "sensitive": product.get("sensitive", False),
                "esg_score": product["esg_score"],
                "ncm_code": product["ncm"]
            })
            
            total_price += item_price
            total_weight += item_weight
    
    cart_id = f"cart_{scenario['name'].lower().replace(' ', '_')}_{int(time.time())}"
    
    return {
        "cart_id": cart_id,
        "store_id": f"store_{scenario['store_type']}_001",
        "user_id_hash": "user_hash_12345",
        "items": items,
        "subtotal": round(total_price, 2),
        "expected_total_weight_kg": round(total_weight, 3),
        "timestamp_ms": int(time.time() * 1000),
        "sector_context": scenario["sector_context"],
        "store_type": scenario["store_type"]
    }

async def test_seal_endpoint(client: httpx.AsyncClient, cart: Dict, guardpass_token: str = None) -> Dict:
    """Testa endpoint de selagem"""
    headers = {}
    if guardpass_token:
        headers["guardpass_token"] = guardpass_token
    
    response = await client.post(
        f"{API_BASE}/seal",
        json={"cart": cart},
        headers=headers
    )
    
    return response.json() if response.status_code == 200 else {"error": response.text}

async def test_verify_endpoint(client: httpx.AsyncClient, qr_token: str) -> Dict:
    """Testa endpoint de verificação"""
    response = await client.post(
        f"{API_BASE}/verify",
        json={"qr_token": qr_token}
    )
    
    return response.json() if response.status_code == 200 else {"error": response.text}

async def test_anomaly_score(client: httpx.AsyncClient, cart: Dict, measured_weight: float, guardpass_token: str = None) -> Dict:
    """Testa cálculo de score de anomalia"""
    headers = {}
    if guardpass_token:
        headers["guardpass_token"] = guardpass_token
    
    current_hour = time.localtime().tm_hour
    
    request_data = {
        "expected_weight_kg": cart["expected_total_weight_kg"],
        "measured_weight_kg": measured_weight,
        "items": cart["items"],
        "scan_duration_sec": 45,  # Tempo realista de escaneamento
        "sector_context": cart.get("sector_context"),
        "store_type": cart.get("store_type"),
        "time_of_day": current_hour,
        "guardpass_tier": "premium" if guardpass_token else "basic"
    }
    
    response = await client.post(
        f"{API_BASE}/anomaly-score",
        json=request_data,
        headers=headers
    )
    
    return response.json() if response.status_code == 200 else {"error": response.text}

async def run_comprehensive_test():
    """Executa teste abrangente da API"""
    print("🧪 INICIANDO TESTES DA API QR CHECKOUT COM DADOS REAIS")
    print("=" * 60)
    
    async with httpx.AsyncClient() as client:
        for i, scenario in enumerate(TEST_SCENARIOS, 1):
            print(f"\n📋 CENÁRIO {i}: {scenario['name']}")
            print("-" * 40)
            
            # Criar carrinho
            cart = await create_cart_from_scenario(scenario)
            print(f"🛒 Carrinho: {len(cart['items'])} itens, R$ {cart['subtotal']}, {cart['expected_total_weight_kg']}kg")
            
            # Testar selagem
            guardpass_token = GUARDPASS_TOKEN if scenario["guardpass_tier"] != "basic" else None
            seal_result = await test_seal_endpoint(client, cart, guardpass_token)
            
            if "error" in seal_result:
                print(f"❌ Erro na selagem: {seal_result['error']}")
                continue
                
            print(f"✅ Selagem: QR gerado, tempo economizado: {seal_result.get('estimated_time_saved_minutes', 0)}min")
            if seal_result.get("esg_impact_score"):
                print(f"🌱 ESG Score: {seal_result['esg_impact_score']}")
            
            # Testar verificação
            verify_result = await test_verify_endpoint(client, seal_result["qr_token"])
            if verify_result.get("valid"):
                print(f"✅ Verificação: QR válido")
            else:
                print(f"❌ Verificação falhou: {verify_result.get('reason')}")
            
            # Testar cenários de peso
            expected_weight = cart["expected_total_weight_kg"]
            test_weights = [
                ("Peso correto", expected_weight),
                ("5% a mais", expected_weight * 1.05),
                ("15% a menos", expected_weight * 0.85),
                ("30% a mais", expected_weight * 1.30)
            ]
            
            for weight_desc, test_weight in test_weights:
                anomaly_result = await test_anomaly_score(client, cart, test_weight, guardpass_token)
                
                if "error" not in anomaly_result:
                    score = anomaly_result["score"]
                    decision = anomaly_result["decision"]
                    delta = anomaly_result["delta_weight_ratio"]
                    
                    decision_emoji = {"allow": "✅", "sample": "⚠️", "block": "❌"}[decision]
                    print(f"  {decision_emoji} {weight_desc}: Score {score:.3f}, Δ {delta:.1%} → {decision.upper()}")
                else:
                    print(f"  ❌ Erro no teste de peso: {anomaly_result['error']}")
            
            print()
    
    print("🎯 TESTE DE MÉTRICAS")
    print("-" * 20)
    
    async with httpx.AsyncClient() as client:
        metrics_response = await client.get(f"{API_BASE}/metrics/store_supermercado_001")
        if metrics_response.status_code == 200:
            metrics = metrics_response.json()
            print(f"📊 Checkouts totais: {metrics['total_checkouts']}")
            print(f"⚡ QR Checkouts: {metrics['qr_checkouts']}")
            print(f"⏱️ Tempo médio tradicional: {metrics['average_time_traditional']}s")
            print(f"🚀 Tempo médio QR: {metrics['average_time_qr']}s")
            print(f"💰 ROI estimado: {metrics['roi_estimate']}%")
        else:
            print(f"❌ Erro ao obter métricas: {metrics_response.text}")

if __name__ == "__main__":
    asyncio.run(run_comprehensive_test())
