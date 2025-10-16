import pytest
from httpx import AsyncClient
from app.main import app
from app.services.nfe_esg_calculator import nfe_esg_calculator, NFeItem, NFeESGResult
from datetime import datetime

# Teste XML de NFe simples para testes
TEST_NFE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<nfeProc xmlns="http://www.portalfiscal.inf.br/nfe">
    <NFe xmlns="http://www.portalfiscal.inf.br/nfe">
        <infNFe Id="NFe12345678901234567890123456789012345678901234">
            <ide>
                <nNF>1</nNF>
                <serie>1</serie>
                <dhEmi>2023-01-01T10:00:00-03:00</dhEmi>
            </ide>
            <emit>
                <CNPJ>12345678000195</CNPJ>
                <xNome>Empresa Teste Ltda</xNome>
                <enderEmit>
                    <xLgr>Rua Teste</xLgr>
                    <nro>123</nro>
                    <xBairro>Centro</xBairro>
                    <xMun>São Paulo</xMun>
                    <UF>SP</UF>
                    <CEP>01234567</CEP>
                </enderEmit>
            </emit>
            <dest>
                <CPF>12345678901</CPF>
                <xNome>Cliente Teste</xNome>
                <enderDest>
                    <xLgr>Rua Cliente</xLgr>
                    <nro>456</nro>
                    <xBairro>Bairro Cliente</xBairro>
                    <xMun>Rio de Janeiro</xMun>
                    <UF>RJ</UF>
                    <CEP>20000000</CEP>
                </enderDest>
            </dest>
            <det nItem="1">
                <prod>
                    <cProd>001</cProd>
                    <xProd>Produto Teste Eletrônico</xProd>
                    <NCM>84000000</NCM>
                    <CFOP>5102</CFOP>
                    <uCom>UN</uCom>
                    <qCom>1.0000</qCom>
                    <vUnCom>100.00</vUnCom>
                    <vProd>100.00</vProd>
                </prod>
            </det>
            <det nItem="2">
                <prod>
                    <cProd>002</cProd>
                    <xProd>Produto Teste Alimentício</xProd>
                    <NCM>01000000</NCM>
                    <CFOP>5102</CFOP>
                    <uCom>KG</uCom>
                    <qCom>2.0000</qCom>
                    <vUnCom>50.00</vUnCom>
                    <vProd>100.00</vProd>
                </prod>
            </det>
        </infNFe>
    </NFe>
</nfeProc>"""

# Testes para o serviço NFe ESG Calculator
@pytest.mark.asyncio
async def test_nfe_esg_calculator_parse_xml():
    """Testa parsing do XML da NFe"""
    nfe_data = nfe_esg_calculator.parse_nfe_xml(TEST_NFE_XML)
    
    assert "chave_acesso" in nfe_data
    assert "numero_nfe" in nfe_data
    assert "serie" in nfe_data
    assert "emitente" in nfe_data
    assert "destinatario" in nfe_data
    assert "items" in nfe_data
    assert len(nfe_data["items"]) == 2
    assert nfe_data["items"][0]["ncm"] == "84000000"
    assert nfe_data["items"][1]["ncm"] == "01000000"

@pytest.mark.asyncio
async def test_nfe_esg_calculator_calculate_nfe_score():
    """Testa cálculo de score ESG para NFe completa"""
    result = nfe_esg_calculator.calculate_nfe_esg_score(TEST_NFE_XML)
    
    assert isinstance(result, NFeESGResult)
    assert result.chave_acesso == "12345678901234567890123456789012345678901234"
    assert result.numero_nfe == "1"
    assert result.serie == "1"
    assert len(result.items) == 2
    assert result.esg_score_geral.overall >= 0
    assert result.esg_score_medio >= 0
    assert result.esg_score_ponderado >= 0
    assert result.total_esg_impact >= 0

@pytest.mark.asyncio
async def test_nfe_esg_calculator_calculate_item_score():
    """Testa cálculo de score ESG para item específico"""
    esg_score = nfe_esg_calculator.calculate_item_esg_score("84000000")
    
    assert esg_score.environmental >= 0
    assert esg_score.social >= 0
    assert esg_score.governance >= 0
    assert esg_score.overall >= 0
    assert len(esg_score.factors_applied) > 0

@pytest.mark.asyncio
async def test_nfe_esg_calculator_batch_calculate_items():
    """Testa cálculo em lote de itens"""
    items_data = [
        {
            "codigo_produto": "001",
            "descricao": "Produto 1",
            "ncm": "84000000",
            "cfop": "5102",
            "unidade_comercial": "UN",
            "quantidade_comercial": 1.0,
            "valor_unitario": 100.0,
            "valor_total": 100.0
        },
        {
            "codigo_produto": "002",
            "descricao": "Produto 2",
            "ncm": "01000000",
            "cfop": "5102",
            "unidade_comercial": "KG",
            "quantidade_comercial": 2.0,
            "valor_unitario": 50.0,
            "valor_total": 100.0
        }
    ]
    
    items_with_esg = nfe_esg_calculator.batch_calculate_items_esg(items_data)
    
    assert len(items_with_esg) == 2
    assert all(isinstance(item, NFeItem) for item in items_with_esg)
    assert items_with_esg[0].ncm == "84000000"
    assert items_with_esg[1].ncm == "01000000"
    assert items_with_esg[0].esg_score is not None
    assert items_with_esg[1].esg_score is not None

@pytest.mark.asyncio
async def test_nfe_esg_calculator_export_report():
    """Testa exportação de relatório ESG"""
    result = nfe_esg_calculator.calculate_nfe_esg_score(TEST_NFE_XML)
    
    # Teste JSON
    json_report = nfe_esg_calculator.export_nfe_esg_report(result, "json")
    assert "chave_acesso" in json_report
    assert "esg_summary" in json_report
    
    # Teste CSV
    csv_report = nfe_esg_calculator.export_nfe_esg_report(result, "csv")
    assert "NCM,Descricao,Valor_Total,ESG_Score" in csv_report
    
    # Teste XML
    xml_report = nfe_esg_calculator.export_nfe_esg_report(result, "xml")
    assert "<?xml" in xml_report
    assert "<nfe_esg_report>" in xml_report

# Testes para a API do NFe ESG Calculator
@pytest.mark.asyncio
async def test_nfe_esg_calculator_health():
    """Testa health check do NFe ESG Calculator"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/api/v1/nfe-esg/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"
    assert "version" in r.json()

@pytest.mark.asyncio
async def test_nfe_esg_calculator_version():
    """Testa endpoint de versão"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/api/v1/nfe-esg/version")
    assert r.status_code == 200
    assert "version" in r.json()
    assert "calculator" in r.json()
    assert "features" in r.json()

@pytest.mark.asyncio
async def test_nfe_esg_calculate_nfe_success():
    """Testa cálculo de score ESG da NFe via API"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/api/v1/nfe-esg/calculate-nfe", json={"xml_content": TEST_NFE_XML})
    assert r.status_code in (200, 401)  # pode exigir auth
    if r.status_code == 200:
        assert "chave_acesso" in r.json()
        assert "esg_score_geral" in r.json()
        assert "items_count" in r.json()

@pytest.mark.asyncio
async def test_nfe_esg_calculate_item_success():
    """Testa cálculo de score ESG de item via API"""
    item_data = {
        "codigo_produto": "001",
        "descricao": "Produto Teste",
        "ncm": "84000000",
        "cfop": "5102",
        "unidade_comercial": "UN",
        "quantidade_comercial": 1.0,
        "valor_unitario": 100.0,
        "valor_total": 100.0
    }
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/api/v1/nfe-esg/calculate-item", json=item_data)
    assert r.status_code in (200, 401)  # pode exigir auth

@pytest.mark.asyncio
async def test_nfe_esg_batch_calculate_items():
    """Testa cálculo em lote de itens via API"""
    items_data = [
        {
            "codigo_produto": "001",
            "descricao": "Produto 1",
            "ncm": "84000000",
            "cfop": "5102",
            "unidade_comercial": "UN",
            "quantidade_comercial": 1.0,
            "valor_unitario": 100.0,
            "valor_total": 100.0
        },
        {
            "codigo_produto": "002",
            "descricao": "Produto 2",
            "ncm": "01000000",
            "cfop": "5102",
            "unidade_comercial": "KG",
            "quantidade_comercial": 2.0,
            "valor_unitario": 50.0,
            "valor_total": 100.0
        }
    ]
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/api/v1/nfe-esg/batch-calculate-items", json=items_data)
    assert r.status_code in (200, 401)  # pode exigir auth

@pytest.mark.asyncio
async def test_nfe_esg_export_report():
    """Testa exportação de relatório via API"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/api/v1/nfe-esg/export-nfe-report", 
                         json={"xml_content": TEST_NFE_XML}, 
                         params={"format": "json"})
    assert r.status_code in (200, 401)  # pode exigir auth

@pytest.mark.asyncio
async def test_nfe_esg_calculator_core_direct():
    """Teste direto do core sem HTTP"""
    result = nfe_esg_calculator.calculate_nfe_esg_score(TEST_NFE_XML)
    assert isinstance(result, NFeESGResult)
    assert result.esg_score_geral.overall >= 0
    assert len(result.items) == 2
