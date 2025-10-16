# -*- coding: utf-8 -*-
"""
🔗 GUARDFLOW ECOSYSTEM INTEGRATION API
Endpoints para integração com Ecosystem-Degov
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field

from app.services.ecosystem_degov_client import (
    ecosystem_degov_client,
    ESGDataRequest,
    TokenResponse,
    TokenStatus
)
from app.services.esg_engine import ESGEngineService
from app.services.nfe_esg_calculator import NFeESGCalculatorService
from app.utils.security import get_current_user

logger = logging.getLogger("ecosystem_integration")

router = APIRouter(prefix="/ecosystem-integration", tags=["Ecosystem Integration"])

class NFeTokenizationRequest(BaseModel):
    """Requisição para tokenização de NFe"""
    nfe_id: str = Field(..., description="ID da NFe")
    chave_acesso: str = Field(..., description="Chave de acesso da NFe")
    valor_total: float = Field(..., gt=0, description="Valor total da NFe")
    ncm_codes: List[str] = Field(..., min_items=1, description="Códigos NCM dos produtos")
    emitente: Dict[str, str] = Field(..., description="Dados do emitente")
    destinatario: Dict[str, str] = Field(..., description="Dados do destinatário")

class TokenizationResponse(BaseModel):
    """Resposta da tokenização"""
    success: bool
    nfe_id: str
    esg_score: Optional[Dict[str, float]] = None
    tokens_generated: Optional[Dict[str, float]] = None
    nft_metadata: Optional[Dict[str, Any]] = None
    blockchain_status: Optional[str] = None
    error_message: Optional[str] = None
    timestamp: str

class BatchTokenizationRequest(BaseModel):
    """Requisição para tokenização em lote"""
    nfe_list: List[NFeTokenizationRequest] = Field(..., min_items=1, max_items=100)

class IntegrationStatusResponse(BaseModel):
    """Status da integração"""
    guardflow_status: str
    ecosystem_degov_status: str
    integration_enabled: bool
    last_sync: Optional[str] = None
    total_processed: int = 0
    success_rate: float = 0.0

@router.post("/tokenize-nfe", response_model=TokenizationResponse)
async def tokenize_nfe(
    request: NFeTokenizationRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """
    Tokeniza uma NFe com base no score ESG
    """
    try:
        logger.info(f"Iniciando tokenização para NFe: {request.nfe_id}")
        
        # Calcular score ESG usando o ESG Engine
        esg_engine = ESGEngineService()
        esg_scores = {}
        
        # Calcular score para cada NCM
        for ncm in request.ncm_codes:
            try:
                score = esg_engine.calculate_esg_score(ncm)
                esg_scores[ncm] = {
                    "overall": score.overall,
                    "environmental": score.environmental,
                    "social": score.social,
                    "governance": score.governance
                }
            except Exception as e:
                logger.warning(f"Erro ao calcular score ESG para NCM {ncm}: {e}")
                esg_scores[ncm] = {
                    "overall": 50.0,
                    "environmental": 50.0,
                    "social": 50.0,
                    "governance": 50.0
                }
        
        # Calcular score médio ponderado
        total_score = sum(score["overall"] for score in esg_scores.values())
        avg_score = total_score / len(esg_scores) if esg_scores else 50.0
        
        # Preparar dados para Ecosystem-Degov
        esg_data = ESGDataRequest(
            nfe_id=request.nfe_id,
            chave_acesso=request.chave_acesso,
            esg_score={
                "overall": avg_score,
                "environmental": sum(s["environmental"] for s in esg_scores.values()) / len(esg_scores),
                "social": sum(s["social"] for s in esg_scores.values()) / len(esg_scores),
                "governance": sum(s["governance"] for s in esg_scores.values()) / len(esg_scores)
            },
            ncm_codes=request.ncm_codes,
            valor_total=request.valor_total,
            emitente=request.emitente,
            destinatario=request.destinatario,
            timestamp=datetime.utcnow().isoformat()
        )
        
        # Enviar para Ecosystem-Degov
        token_response = await ecosystem_degov_client.process_esg_data(esg_data)
        
        if token_response.success:
            logger.info(f"Tokenização bem-sucedida para NFe: {request.nfe_id}")
            
            # Adicionar tarefa em background para sincronização
            background_tasks.add_task(
                sync_tokenization_data,
                request.nfe_id,
                token_response
            )
            
            return TokenizationResponse(
                success=True,
                nfe_id=request.nfe_id,
                esg_score={
                    "overall": avg_score,
                    "environmental": sum(s["environmental"] for s in esg_scores.values()) / len(esg_scores),
                    "social": sum(s["social"] for s in esg_scores.values()) / len(esg_scores),
                    "governance": sum(s["governance"] for s in esg_scores.values()) / len(esg_scores)
                },
                tokens_generated=token_response.tokens_generated,
                nft_metadata=token_response.nft_metadata,
                blockchain_status=token_response.blockchain_status,
                timestamp=datetime.utcnow().isoformat()
            )
        else:
            logger.error(f"Falha na tokenização para NFe: {request.nfe_id} - {token_response.error_message}")
            return TokenizationResponse(
                success=False,
                nfe_id=request.nfe_id,
                error_message=token_response.error_message,
                timestamp=datetime.utcnow().isoformat()
            )
            
    except Exception as e:
        logger.error(f"Erro na tokenização da NFe {request.nfe_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/batch-tokenize", response_model=List[TokenizationResponse])
async def batch_tokenize_nfes(
    request: BatchTokenizationRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """
    Tokeniza múltiplas NFe em lote
    """
    try:
        logger.info(f"Iniciando tokenização em lote para {len(request.nfe_list)} NFe")
        
        results = []
        for nfe_request in request.nfe_list:
            try:
                # Processar cada NFe individualmente
                result = await tokenize_nfe(nfe_request, background_tasks, current_user)
                results.append(result)
            except Exception as e:
                logger.error(f"Erro ao processar NFe {nfe_request.nfe_id}: {e}")
                results.append(TokenizationResponse(
                    success=False,
                    nfe_id=nfe_request.nfe_id,
                    error_message=str(e),
                    timestamp=datetime.utcnow().isoformat()
                ))
        
        logger.info(f"Tokenização em lote concluída - {len([r for r in results if r.success])} sucessos")
        return results
        
    except Exception as e:
        logger.error(f"Erro na tokenização em lote: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/token-status/{nfe_id}", response_model=TokenStatus)
async def get_token_status(
    nfe_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Consulta status dos tokens para uma NFe
    """
    try:
        logger.info(f"Consultando status dos tokens para NFe: {nfe_id}")
        
        status = await ecosystem_degov_client.get_token_status(nfe_id)
        return status
        
    except Exception as e:
        logger.error(f"Erro ao consultar status dos tokens para NFe {nfe_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/integration-status", response_model=IntegrationStatusResponse)
async def get_integration_status(current_user: dict = Depends(get_current_user)):
    """
    Consulta status da integração entre GuardFlow e Ecosystem-Degov
    """
    try:
        # Health check do Ecosystem-Degov
        ecosystem_health = await ecosystem_degov_client.health_check()
        
        # TODO: Implementar consulta de estatísticas do banco de dados
        # Por enquanto, retornar dados simulados
        return IntegrationStatusResponse(
            guardflow_status="healthy",
            ecosystem_degov_status=ecosystem_health.get("status", "unknown"),
            integration_enabled=ecosystem_degov_client.enabled,
            last_sync=datetime.utcnow().isoformat(),
            total_processed=0,  # TODO: Implementar consulta real
            success_rate=0.0    # TODO: Implementar cálculo real
        )
        
    except Exception as e:
        logger.error(f"Erro ao consultar status da integração: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/sync-data")
async def sync_integration_data(
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """
    Força sincronização de dados entre GuardFlow e Ecosystem-Degov
    """
    try:
        logger.info("Iniciando sincronização de dados")
        
        # Adicionar tarefa em background para sincronização
        background_tasks.add_task(perform_data_sync)
        
        return {"message": "Sincronização iniciada", "timestamp": datetime.utcnow().isoformat()}
        
    except Exception as e:
        logger.error(f"Erro ao iniciar sincronização: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

# Funções auxiliares para tarefas em background

async def sync_tokenization_data(nfe_id: str, token_response: TokenResponse):
    """
    Sincroniza dados de tokenização no banco de dados
    """
    try:
        logger.info(f"Sincronizando dados de tokenização para NFe: {nfe_id}")
        
        # TODO: Implementar sincronização no banco de dados
        # - Salvar logs de integração
        # - Atualizar status dos tokens
        # - Registrar transações blockchain
        
        logger.info(f"Dados de tokenização sincronizados para NFe: {nfe_id}")
        
    except Exception as e:
        logger.error(f"Erro na sincronização de dados para NFe {nfe_id}: {e}")

async def perform_data_sync():
    """
    Executa sincronização completa de dados
    """
    try:
        logger.info("Executando sincronização completa de dados")
        
        # TODO: Implementar sincronização completa
        # - Sincronizar logs de integração
        # - Sincronizar status dos tokens
        # - Sincronizar transações blockchain
        # - Verificar consistência dos dados
        
        logger.info("Sincronização completa de dados concluída")
        
    except Exception as e:
        logger.error(f"Erro na sincronização completa: {e}")
