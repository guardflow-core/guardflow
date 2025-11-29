# -*- coding: utf-8 -*-
"""
🌱 GUARDFLOW ESG ENGINE API
Endpoints para cálculo e consulta de scores ESG
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import logging

from app.services.esg_engine import esg_engine, ESGCategory, ESGScore
from app.api.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/esg-engine", tags=["ESG Engine"])

# Schemas
class ESGFactorResponse(BaseModel):
    name: str
    category: str
    weight: float
    impact: str
    description: str
    ncm_codes: List[str]
    calculation_method: str

class ESGScoreRequest(BaseModel):
    ncm_code: str = Field(..., description="Código NCM do produto")
    product_data: Optional[Dict] = Field(None, description="Dados adicionais do produto")

class ESGScoreResponse(BaseModel):
    environmental: float
    social: float
    governance: float
    overall: float
    factors_applied: List[str]
    calculation_timestamp: datetime
    version: str
    insights: Dict[str, str]

class ESGFactorsResponse(BaseModel):
    factors: List[ESGFactorResponse]
    total_count: int

@router.post("/calculate-score", response_model=ESGScoreResponse)
async def calculate_esg_score(
    request: ESGScoreRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Calcula score ESG para um produto baseado no código NCM
    """
    try:
        logger.info(f"Calculando score ESG para NCM {request.ncm_code}")
        
        # Calcular score ESG
        score = esg_engine.calculate_esg_score(
            ncm_code=request.ncm_code,
            product_data=request.product_data
        )
        
        # Gerar insights
        insights = esg_engine.get_esg_insights(score)
        
        return ESGScoreResponse(
            environmental=score.environmental,
            social=score.social,
            governance=score.governance,
            overall=score.overall,
            factors_applied=score.factors_applied,
            calculation_timestamp=score.calculation_timestamp,
            version=score.version,
            insights=insights
        )
        
    except Exception as e:
        logger.error(f"Erro ao calcular score ESG: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/factors", response_model=ESGFactorsResponse)
async def get_esg_factors(
    category: Optional[str] = Query(None, description="Filtrar por categoria ESG"),
    current_user: dict = Depends(get_current_user)
):
    """
    Lista todos os fatores ESG disponíveis
    """
    try:
        factors = esg_engine.factors
        
        # Filtrar por categoria se especificada
        if category:
            try:
                category_enum = ESGCategory(category)
                factors = [f for f in factors if f.category == category_enum]
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Categoria inválida: {category}")
        
        # Converter para response
        factor_responses = [
            ESGFactorResponse(
                name=f.name,
                category=f.category.value,
                weight=f.weight,
                impact=f.impact.name,
                description=f.description,
                ncm_codes=f.ncm_codes,
                calculation_method=f.calculation_method
            )
            for f in factors
        ]
        
        return ESGFactorsResponse(
            factors=factor_responses,
            total_count=len(factor_responses)
        )
        
    except Exception as e:
        logger.error(f"Erro ao listar fatores ESG: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/factors/by-ncm/{ncm_code}")
async def get_esg_factors_by_ncm(
    ncm_code: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Lista fatores ESG aplicáveis a um código NCM específico
    """
    try:
        factors = esg_engine.get_esg_factors_by_ncm(ncm_code)
        
        factor_responses = [
            ESGFactorResponse(
                name=f.name,
                category=f.category.value,
                weight=f.weight,
                impact=f.impact.name,
                description=f.description,
                ncm_codes=f.ncm_codes,
                calculation_method=f.calculation_method
            )
            for f in factors
        ]
        
        return {
            "ncm_code": ncm_code,
            "factors": factor_responses,
            "total_count": len(factor_responses)
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter fatores ESG para NCM {ncm_code}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/categories")
async def get_esg_categories(current_user: dict = Depends(get_current_user)):
    """
    Lista todas as categorias ESG disponíveis
    """
    try:
        categories = [
            {
                "name": category.value,
                "display_name": category.value.title(),
                "description": f"Fatores relacionados a {category.value}"
            }
            for category in ESGCategory
        ]
        
        return {
            "categories": categories,
            "total_count": len(categories)
        }
        
    except Exception as e:
        logger.error(f"Erro ao listar categorias ESG: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/health")
async def esg_engine_health():
    """
    Health check do ESG Engine
    """
    try:
        # Testar cálculo básico
        test_score = esg_engine.calculate_esg_score("84")
        
        return {
            "status": "healthy",
            "version": esg_engine.version,
            "factors_count": len(esg_engine.factors),
            "ncm_mappings_count": len(esg_engine.ncm_mapping),
            "test_score": test_score.overall,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Erro no health check do ESG Engine: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

@router.post("/batch-calculate")
async def batch_calculate_esg_scores(
    ncm_codes: List[str],
    current_user: dict = Depends(get_current_user)
):
    """
    Calcula scores ESG para múltiplos códigos NCM
    """
    try:
        if len(ncm_codes) > 100:
            raise HTTPException(status_code=400, detail="Máximo de 100 códigos NCM por lote")
        
        results = []
        for ncm_code in ncm_codes:
            try:
                score = esg_engine.calculate_esg_score(ncm_code)
                insights = esg_engine.get_esg_insights(score)
                
                results.append({
                    "ncm_code": ncm_code,
                    "score": {
                        "environmental": score.environmental,
                        "social": score.social,
                        "governance": score.governance,
                        "overall": score.overall
                    },
                    "insights": insights,
                    "factors_applied": score.factors_applied,
                    "status": "success"
                })
                
            except Exception as e:
                results.append({
                    "ncm_code": ncm_code,
                    "error": str(e),
                    "status": "error"
                })
        
        return {
            "results": results,
            "total_processed": len(ncm_codes),
            "successful": len([r for r in results if r["status"] == "success"]),
            "failed": len([r for r in results if r["status"] == "error"])
        }
        
    except Exception as e:
        logger.error(f"Erro no cálculo em lote: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/benchmarks/{category}")
async def get_esg_benchmarks(
    category: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Retorna benchmarks ESG para uma categoria específica
    """
    try:
        try:
            category_enum = ESGCategory(category)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Categoria inválida: {category}")
        
        benchmarks = esg_engine.get_esg_benchmark(category_enum)
        
        return {
            "category": category,
            "benchmarks": benchmarks,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter benchmarks ESG: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/recommendations")
async def get_esg_recommendations(
    request: ESGScoreRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Gera recomendações ESG baseadas no score calculado
    """
    try:
        # Calcular score ESG
        score = esg_engine.calculate_esg_score(
            ncm_code=request.ncm_code,
            product_data=request.product_data
        )
        
        # Gerar recomendações
        recommendations = esg_engine.get_esg_recommendations(score)
        
        return {
            "ncm_code": request.ncm_code,
            "score": {
                "environmental": score.environmental,
                "social": score.social,
                "governance": score.governance,
                "overall": score.overall
            },
            "recommendations": recommendations,
            "total_recommendations": len(recommendations),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Erro ao gerar recomendações ESG: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/export-report")
async def export_esg_report(
    request: ESGScoreRequest,
    format: str = Query("json", description="Formato do relatório (json, csv, xml)"),
    current_user: dict = Depends(get_current_user)
):
    """
    Exporta relatório ESG em formato específico
    """
    try:
        if format.lower() not in ["json", "csv", "xml"]:
            raise HTTPException(status_code=400, detail="Formato inválido. Use: json, csv, xml")
        
        # Calcular score ESG
        score = esg_engine.calculate_esg_score(
            ncm_code=request.ncm_code,
            product_data=request.product_data
        )
        
        # Exportar relatório
        report = esg_engine.export_esg_report(score, format)
        
        return {
            "ncm_code": request.ncm_code,
            "format": format,
            "report": report,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao exportar relatório ESG: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/ncm-coverage")
async def get_ncm_coverage(current_user: dict = Depends(get_current_user)):
    """
    Retorna estatísticas de cobertura NCM do ESG Engine
    """
    try:
        total_ncm_codes = len(esg_engine.ncm_mapping)
        total_factors = len(esg_engine.factors)
        
        # Estatísticas por categoria
        category_stats = {}
        for category in ESGCategory:
            factors = esg_engine.get_esg_factors_by_category(category)
            category_stats[category.value] = {
                "factors_count": len(factors),
                "avg_weight": sum(f.weight for f in factors) / len(factors) if factors else 0
            }
        
        return {
            "total_ncm_codes": total_ncm_codes,
            "total_factors": total_factors,
            "category_stats": category_stats,
            "coverage_percentage": (total_ncm_codes / 99) * 100,  # Assumindo 99 códigos NCM principais
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas de cobertura: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/version")
async def get_esg_engine_version():
    """
    Retorna informações da versão do ESG Engine
    """
    return {
        "version": esg_engine.version,
        "engine": "GuardFlow ESG Engine",
        "description": "Sistema de cálculo de scores ESG baseado em NCM",
        "features": [
            "Cálculo de scores ESG por NCM",
            "Análise de fatores ambientais, sociais e de governança",
            "Benchmarks e recomendações",
            "Exportação de relatórios",
            "Cálculo em lote"
        ],
        "timestamp": datetime.utcnow().isoformat()
    }
