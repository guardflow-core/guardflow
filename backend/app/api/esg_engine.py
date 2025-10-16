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
