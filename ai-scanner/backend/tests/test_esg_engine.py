import pytest
from httpx import AsyncClient
from app.main import app
from app.services.esg_engine import esg_engine, ESGCategory, ESGScore
from datetime import datetime

# Testes para o serviço ESG Engine
@pytest.mark.asyncio
async def test_esg_engine_service_single_ncm():
    """Testa cálculo de score ESG para um NCM específico"""
    score = esg_engine.calculate_esg_score("84000000")
    assert isinstance(score, ESGScore)
    assert score.environmental >= 0
    assert score.social >= 0
    assert score.governance >= 0
    assert score.overall >= 0
    assert len(score.factors_applied) > 0

@pytest.mark.asyncio
async def test_esg_engine_service_batch_ncm():
    """Testa cálculo em lote de scores ESG"""
    ncm_codes = ["84000000", "01000000", "99999999"]  # Último para testar fallback
    scores = esg_engine.batch_calculate_esg_scores(ncm_codes)
    assert len(scores) == 3
    assert all(isinstance(s, ESGScore) for s in scores)
    assert scores[0].overall > 0
    assert scores[2].overall == 50.0  # Fallback score

@pytest.mark.asyncio
async def test_esg_engine_with_product_data():
    """Testa cálculo ESG com dados do produto"""
    product_data = {
        "organic": True,
        "certified": True,
        "sustainable": True
    }
    score = esg_engine.calculate_esg_score("84000000", product_data)
    assert score.overall > 50  # Deve ser maior que o score padrão

@pytest.mark.asyncio
async def test_esg_engine_insights():
    """Testa geração de insights ESG"""
    score = esg_engine.calculate_esg_score("84000000")
    insights = esg_engine.get_esg_insights(score)
    assert "environmental" in insights
    assert "social" in insights
    assert "governance" in insights
    assert "overall" in insights

@pytest.mark.asyncio
async def test_esg_engine_recommendations():
    """Testa geração de recomendações ESG"""
    score = esg_engine.calculate_esg_score("84000000")
    recommendations = esg_engine.get_esg_recommendations(score)
    assert isinstance(recommendations, list)
    if recommendations:
        assert "category" in recommendations[0]
        assert "priority" in recommendations[0]
        assert "recommendation" in recommendations[0]

@pytest.mark.asyncio
async def test_esg_engine_benchmarks():
    """Testa obtenção de benchmarks ESG"""
    benchmark = esg_engine.get_esg_benchmark(ESGCategory.ENVIRONMENTAL)
    assert "average" in benchmark
    assert "median" in benchmark
    assert "excellent" in benchmark

@pytest.mark.asyncio
async def test_esg_engine_export_report():
    """Testa exportação de relatório ESG"""
    score = esg_engine.calculate_esg_score("84000000")
    
    # Teste JSON
    json_report = esg_engine.export_esg_report(score, "json")
    assert "environmental" in json_report
    
    # Teste CSV
    csv_report = esg_engine.export_esg_report(score, "csv")
    assert "Environmental,Social,Governance,Overall" in csv_report
    
    # Teste XML
    xml_report = esg_engine.export_esg_report(score, "xml")
    assert "<?xml" in xml_report
    assert "<esg_report>" in xml_report

@pytest.mark.asyncio
async def test_esg_engine_trends():
    """Testa análise de tendências ESG"""
    # Criar histórico de scores
    scores_history = [
        esg_engine.calculate_esg_score("84000000"),
        esg_engine.calculate_esg_score("84000000"),
        esg_engine.calculate_esg_score("84000000")
    ]
    
    trends = esg_engine.get_esg_trends(scores_history)
    assert "trend" in trends
    assert "direction" in trends

# Testes para a API do ESG Engine
@pytest.mark.asyncio
async def test_esg_engine_health():
    """Testa health check do ESG Engine"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/api/v1/esg-engine/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"
    assert "version" in r.json()
    assert "factors_count" in r.json()

@pytest.mark.asyncio
async def test_esg_calculate_score_success():
    """Testa cálculo de score ESG via API"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/api/v1/esg-engine/calculate-score", json={"ncm_code": "84000000"})
    assert r.status_code in (200, 401)  # pode exigir auth
    if r.status_code == 200:
        assert "environmental" in r.json()
        assert "social" in r.json()
        assert "governance" in r.json()
        assert "overall" in r.json()

@pytest.mark.asyncio
async def test_esg_calculate_score_with_product_data():
    """Testa cálculo ESG com dados do produto via API"""
    payload = {
        "ncm_code": "84000000",
        "product_data": {
            "organic": True,
            "certified": True
        }
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/api/v1/esg-engine/calculate-score", json=payload)
    assert r.status_code in (200, 401)  # pode exigir auth

@pytest.mark.asyncio
async def test_esg_calculate_score_invalid_ncm():
    """Testa cálculo ESG com NCM inválido"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/api/v1/esg-engine/calculate-score", json={"ncm_code": ""})
    assert r.status_code in (400, 401)  # pode exigir auth

@pytest.mark.asyncio
async def test_esg_batch_calculate_scores_success():
    """Testa cálculo em lote via API"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/api/v1/esg-engine/batch-calculate", json=["84000000", "01000000"])
    assert r.status_code in (200, 401)  # pode exigir auth

@pytest.mark.asyncio
async def test_esg_factors_endpoint():
    """Testa endpoint de fatores ESG"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/api/v1/esg-engine/factors")
    assert r.status_code in (200, 401)  # pode exigir auth

@pytest.mark.asyncio
async def test_esg_factors_by_category():
    """Testa filtro de fatores por categoria"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/api/v1/esg-engine/factors?category=environmental")
    assert r.status_code in (200, 401)  # pode exigir auth

@pytest.mark.asyncio
async def test_esg_factors_by_ncm():
    """Testa fatores ESG por NCM"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/api/v1/esg-engine/factors/by-ncm/84000000")
    assert r.status_code in (200, 401)  # pode exigir auth

@pytest.mark.asyncio
async def test_esg_categories_endpoint():
    """Testa endpoint de categorias ESG"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/api/v1/esg-engine/categories")
    assert r.status_code in (200, 401)  # pode exigir auth

@pytest.mark.asyncio
async def test_esg_benchmarks_endpoint():
    """Testa endpoint de benchmarks ESG"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/api/v1/esg-engine/benchmarks/environmental")
    assert r.status_code in (200, 401)  # pode exigir auth

@pytest.mark.asyncio
async def test_esg_recommendations_endpoint():
    """Testa endpoint de recomendações ESG"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/api/v1/esg-engine/recommendations", json={"ncm_code": "84000000"})
    assert r.status_code in (200, 401)  # pode exigir auth

@pytest.mark.asyncio
async def test_esg_export_report_endpoint():
    """Testa endpoint de exportação de relatório"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/api/v1/esg-engine/export-report", 
                         json={"ncm_code": "84000000"}, 
                         params={"format": "json"})
    assert r.status_code in (200, 401)  # pode exigir auth

@pytest.mark.asyncio
async def test_esg_ncm_coverage_endpoint():
    """Testa endpoint de cobertura NCM"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/api/v1/esg-engine/ncm-coverage")
    assert r.status_code in (200, 401)  # pode exigir auth

@pytest.mark.asyncio
async def test_esg_version_endpoint():
    """Testa endpoint de versão"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/api/v1/esg-engine/version")
    assert r.status_code == 200
    assert "version" in r.json()
    assert "engine" in r.json()
    assert "features" in r.json()

@pytest.mark.asyncio
async def test_esg_engine_core_direct():
    """Teste direto do core sem HTTP"""
    score = esg_engine.calculate_esg_score("84")
    assert 0.0 <= score.overall <= 100.0
    assert isinstance(score, ESGScore)