# -*- coding: utf-8 -*-
"""
🧾 GUARDFLOW NFE ESG CALCULATOR API
Endpoints para cálculo de scores ESG por NFe e itens
"""

from fastapi import APIRouter, HTTPException, Depends, Query, UploadFile, File
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
import logging

from app.services.nfe_esg_calculator import nfe_esg_calculator, NFeESGResult, NFeItem
from app.api.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/nfe-esg", tags=["NFe ESG Calculator"])

# Schemas
class NFeItemRequest(BaseModel):
    codigo_produto: str = Field(..., description="Código do produto")
    descricao: str = Field(..., description="Descrição do produto")
    ncm: str = Field(..., description="Código NCM")
    cfop: str = Field(..., description="Código CFOP")
    unidade_comercial: str = Field(..., description="Unidade comercial")
    quantidade_comercial: float = Field(..., description="Quantidade comercial")
    valor_unitario: float = Field(..., description="Valor unitário")
    valor_total: float = Field(..., description="Valor total")
    product_data: Optional[Dict] = Field(None, description="Dados adicionais do produto")

class NFeESGResponse(BaseModel):
    chave_acesso: str
    numero_nfe: str
    serie: str
    data_emissao: datetime
    emitente: Dict[str, Any]
    destinatario: Dict[str, Any]
    esg_score_geral: Dict[str, float]
    esg_score_medio: float
    esg_score_ponderado: float
    total_esg_impact: float
    esg_breakdown: Dict[str, float]
    esg_insights: Dict[str, str]
    esg_recommendations: List[Dict[str, str]]
    items_count: int
    calculation_timestamp: datetime
    version: str

class NFeItemESGResponse(BaseModel):
    codigo_produto: str
    descricao: str
    ncm: str
    valor_total: float
    esg_score: Optional[Dict[str, float]]
    esg_factors: Optional[List[str]]
    esg_insights: Optional[Dict[str, str]]
    esg_recommendations: Optional[List[Dict[str, str]]]

class NFeXMLRequest(BaseModel):
    xml_content: str = Field(..., description="Conteúdo XML da NFe")

@router.post("/calculate-nfe", response_model=NFeESGResponse)
async def calculate_nfe_esg_score(
    request: NFeXMLRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Calcula score ESG para uma NFe completa baseada no XML
    """
    try:
        logger.info(f"Calculando score ESG para NFe")
        
        # Calcular score ESG da NFe
        result = nfe_esg_calculator.calculate_nfe_esg_score(request.xml_content)
        
        return NFeESGResponse(
            chave_acesso=result.chave_acesso,
            numero_nfe=result.numero_nfe,
            serie=result.serie,
            data_emissao=result.data_emissao,
            emitente=result.emitente,
            destinatario=result.destinatario,
            esg_score_geral={
                "environmental": result.esg_score_geral.environmental,
                "social": result.esg_score_geral.social,
                "governance": result.esg_score_geral.governance,
                "overall": result.esg_score_geral.overall
            },
            esg_score_medio=result.esg_score_medio,
            esg_score_ponderado=result.esg_score_ponderado,
            total_esg_impact=result.total_esg_impact,
            esg_breakdown=result.esg_breakdown,
            esg_insights=result.esg_insights,
            esg_recommendations=result.esg_recommendations,
            items_count=len(result.items),
            calculation_timestamp=result.calculation_timestamp,
            version=result.version
        )
        
    except Exception as e:
        logger.error(f"Erro ao calcular score ESG da NFe: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/upload-nfe", response_model=NFeESGResponse)
async def upload_nfe_xml(
    file: UploadFile = File(..., description="Arquivo XML da NFe"),
    current_user: dict = Depends(get_current_user)
):
    """
    Upload e cálculo de score ESG para arquivo XML da NFe
    """
    try:
        if not file.filename.endswith('.xml'):
            raise HTTPException(status_code=400, detail="Arquivo deve ser XML")
        
        # Ler conteúdo do arquivo
        xml_content = await file.read()
        xml_content_str = xml_content.decode('utf-8')
        
        logger.info(f"Processando arquivo NFe: {file.filename}")
        
        # Calcular score ESG
        result = nfe_esg_calculator.calculate_nfe_esg_score(xml_content_str)
        
        return NFeESGResponse(
            chave_acesso=result.chave_acesso,
            numero_nfe=result.numero_nfe,
            serie=result.serie,
            data_emissao=result.data_emissao,
            emitente=result.emitente,
            destinatario=result.destinatario,
            esg_score_geral={
                "environmental": result.esg_score_geral.environmental,
                "social": result.esg_score_geral.social,
                "governance": result.esg_score_geral.governance,
                "overall": result.esg_score_geral.overall
            },
            esg_score_medio=result.esg_score_medio,
            esg_score_ponderado=result.esg_score_ponderado,
            total_esg_impact=result.total_esg_impact,
            esg_breakdown=result.esg_breakdown,
            esg_insights=result.esg_insights,
            esg_recommendations=result.esg_recommendations,
            items_count=len(result.items),
            calculation_timestamp=result.calculation_timestamp,
            version=result.version
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao processar arquivo NFe: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/calculate-item", response_model=NFeItemESGResponse)
async def calculate_item_esg_score(
    request: NFeItemRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Calcula score ESG para um item específico
    """
    try:
        logger.info(f"Calculando score ESG para item NCM: {request.ncm}")
        
        # Calcular score ESG do item
        esg_score = nfe_esg_calculator.calculate_item_esg_score(
            ncm=request.ncm,
            product_data=request.product_data
        )
        
        # Gerar insights e recomendações
        from app.services.esg_engine import esg_engine
        insights = esg_engine.get_esg_insights(esg_score)
        recommendations = esg_engine.get_esg_recommendations(esg_score)
        
        return NFeItemESGResponse(
            codigo_produto=request.codigo_produto,
            descricao=request.descricao,
            ncm=request.ncm,
            valor_total=request.valor_total,
            esg_score={
                "environmental": esg_score.environmental,
                "social": esg_score.social,
                "governance": esg_score.governance,
                "overall": esg_score.overall
            },
            esg_factors=esg_score.factors_applied,
            esg_insights=insights,
            esg_recommendations=recommendations
        )
        
    except Exception as e:
        logger.error(f"Erro ao calcular score ESG do item: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/batch-calculate-items")
async def batch_calculate_items_esg(
    items: List[NFeItemRequest],
    current_user: dict = Depends(get_current_user)
):
    """
    Calcula scores ESG para múltiplos itens
    """
    try:
        if len(items) > 100:
            raise HTTPException(status_code=400, detail="Máximo de 100 itens por lote")
        
        logger.info(f"Calculando scores ESG para {len(items)} itens")
        
        # Converter para formato esperado
        items_data = [
            {
                "codigo_produto": item.codigo_produto,
                "descricao": item.descricao,
                "ncm": item.ncm,
                "cfop": item.cfop,
                "unidade_comercial": item.unidade_comercial,
                "quantidade_comercial": item.quantidade_comercial,
                "valor_unitario": item.valor_unitario,
                "valor_total": item.valor_total,
                "product_data": item.product_data
            }
            for item in items
        ]
        
        # Calcular scores ESG
        items_with_esg = nfe_esg_calculator.batch_calculate_items_esg(items_data)
        
        # Converter para resposta
        results = []
        for item in items_with_esg:
            results.append({
                "codigo_produto": item.codigo_produto,
                "descricao": item.descricao,
                "ncm": item.ncm,
                "valor_total": item.valor_total,
                "esg_score": {
                    "environmental": item.esg_score.environmental,
                    "social": item.esg_score.social,
                    "governance": item.esg_score.governance,
                    "overall": item.esg_score.overall
                } if item.esg_score else None,
                "esg_factors": item.esg_factors,
                "esg_insights": item.esg_insights,
                "esg_recommendations": item.esg_recommendations,
                "status": "success" if item.esg_score else "error"
            })
        
        return {
            "results": results,
            "total_processed": len(items),
            "successful": len([r for r in results if r["status"] == "success"]),
            "failed": len([r for r in results if r["status"] == "error"]),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro no cálculo em lote de itens: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/export-nfe-report")
async def export_nfe_esg_report(
    request: NFeXMLRequest,
    format: str = Query("json", description="Formato do relatório (json, csv, xml)"),
    current_user: dict = Depends(get_current_user)
):
    """
    Exporta relatório ESG da NFe em formato específico
    """
    try:
        if format.lower() not in ["json", "csv", "xml"]:
            raise HTTPException(status_code=400, detail="Formato inválido. Use: json, csv, xml")
        
        # Calcular score ESG da NFe
        result = nfe_esg_calculator.calculate_nfe_esg_score(request.xml_content)
        
        # Exportar relatório
        report = nfe_esg_calculator.export_nfe_esg_report(result, format)
        
        return {
            "chave_acesso": result.chave_acesso,
            "format": format,
            "report": report,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao exportar relatório ESG da NFe: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/health")
async def nfe_esg_calculator_health():
    """
    Health check do NFe ESG Calculator
    """
    try:
        # Testar parsing básico
        test_xml = """<?xml version="1.0" encoding="UTF-8"?>
        <nfeProc xmlns="http://www.portalfiscal.inf.br/nfe">
            <NFe xmlns="http://www.portalfiscal.inf.br/nfe">
                <infNFe Id="NFe123456789">
                    <ide>
                        <nNF>1</nNF>
                        <serie>1</serie>
                        <dhEmi>2023-01-01T10:00:00-03:00</dhEmi>
                    </ide>
                    <emit>
                        <CNPJ>12345678000195</CNPJ>
                        <xNome>Empresa Teste</xNome>
                    </emit>
                    <dest>
                        <CPF>12345678901</CPF>
                        <xNome>Cliente Teste</xNome>
                    </dest>
                    <det nItem="1">
                        <prod>
                            <cProd>001</cProd>
                            <xProd>Produto Teste</xProd>
                            <NCM>84000000</NCM>
                            <CFOP>5102</CFOP>
                            <uCom>UN</uCom>
                            <qCom>1.0000</qCom>
                            <vUnCom>100.00</vUnCom>
                            <vProd>100.00</vProd>
                        </prod>
                    </det>
                </infNFe>
            </NFe>
        </nfeProc>"""
        
        # Testar parsing
        nfe_data = nfe_esg_calculator.parse_nfe_xml(test_xml)
        
        return {
            "status": "healthy",
            "version": nfe_esg_calculator.version,
            "test_parsing": "success",
            "nfe_data_keys": list(nfe_data.keys()),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Erro no health check do NFe ESG Calculator: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

@router.get("/version")
async def get_nfe_esg_calculator_version():
    """
    Retorna informações da versão do NFe ESG Calculator
    """
    return {
        "version": nfe_esg_calculator.version,
        "calculator": "GuardFlow NFe ESG Calculator",
        "description": "Sistema de cálculo de scores ESG para NFe e itens",
        "features": [
            "Parsing de XML de NFe",
            "Cálculo ESG por item",
            "Cálculo ESG por NFe completa",
            "Upload de arquivos XML",
            "Exportação de relatórios",
            "Cálculo em lote"
        ],
        "timestamp": datetime.utcnow().isoformat()
    }
