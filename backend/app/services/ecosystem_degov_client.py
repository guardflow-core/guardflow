# -*- coding: utf-8 -*-
"""
🔗 GUARDFLOW ECOSYSTEM-DEGOV INTEGRATION CLIENT
Cliente para integração com o Ecosystem-Degov para tokenização ESG
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import httpx
from pydantic import BaseModel, Field

from app.config import settings

logger = logging.getLogger("ecosystem_degov_client")

class ESGScore(BaseModel):
    """Modelo para score ESG"""
    overall: float = Field(..., ge=0.0, le=100.0)
    environmental: float = Field(..., ge=0.0, le=100.0)
    social: float = Field(..., ge=0.0, le=100.0)
    governance: float = Field(..., ge=0.0, le=100.0)

class Emitente(BaseModel):
    """Modelo para dados do emitente"""
    cnpj: str
    razao_social: str
    endereco: Optional[str] = None
    uf: Optional[str] = None

class Destinatario(BaseModel):
    """Modelo para dados do destinatário"""
    cnpj_cpf: str
    razao_social: str
    endereco: Optional[str] = None
    uf: Optional[str] = None

class ESGDataRequest(BaseModel):
    """Modelo para requisição de dados ESG"""
    nfe_id: str = Field(..., min_length=44, max_length=44)
    chave_acesso: str = Field(..., min_length=44, max_length=44)
    esg_score: ESGScore
    ncm_codes: List[str] = Field(..., min_items=1)
    valor_total: float = Field(..., gt=0.0)
    emitente: Emitente
    destinatario: Destinatario
    timestamp: str

class TokenResponse(BaseModel):
    """Modelo para resposta de tokenização"""
    success: bool
    transaction_id: Optional[str] = None
    tokens_generated: Optional[Dict[str, float]] = None
    nft_metadata: Optional[Dict[str, Any]] = None
    blockchain_status: Optional[str] = None
    error_message: Optional[str] = None
    timestamp: str

class TokenStatus(BaseModel):
    """Modelo para status dos tokens"""
    nfe_id: str
    token_status: str
    tokens_balance: Optional[Dict[str, float]] = None
    nft_status: Optional[str] = None
    blockchain_confirmations: Optional[int] = None
    last_updated: str

class EcosystemDegovClient:
    """
    Cliente para integração com Ecosystem-Degov
    """
    
    def __init__(self):
        self.base_url = getattr(settings, 'ECOSYSTEM_DEGOV_API_URL', 'http://localhost:8080')
        self.api_key = getattr(settings, 'ECOSYSTEM_DEGOV_API_KEY', '')
        self.timeout = getattr(settings, 'INTEGRATION_TIMEOUT', 30)
        self.retry_attempts = getattr(settings, 'INTEGRATION_RETRY_ATTEMPTS', 3)
        self.enabled = getattr(settings, 'INTEGRATION_ENABLED', True)
        
        logger.info(f"EcosystemDegovClient inicializado - URL: {self.base_url}")
    
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Faz requisição HTTP com retry automático
        """
        if not self.enabled:
            logger.warning("Integração com Ecosystem-Degov desabilitada")
            return {"success": False, "error": "Integration disabled"}
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "GuardFlow-Integration-Client/1.0"
        }
        
        url = f"{self.base_url}{endpoint}"
        
        for attempt in range(self.retry_attempts):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    if method.upper() == "GET":
                        response = await client.get(url, headers=headers, params=params)
                    elif method.upper() == "POST":
                        response = await client.post(url, headers=headers, json=data)
                    else:
                        raise ValueError(f"Método HTTP não suportado: {method}")
                    
                    response.raise_for_status()
                    return response.json()
                    
            except httpx.TimeoutException:
                logger.warning(f"Timeout na tentativa {attempt + 1}/{self.retry_attempts}")
                if attempt == self.retry_attempts - 1:
                    raise
                await asyncio.sleep(2 ** attempt)  # Backoff exponencial
                
            except httpx.HTTPStatusError as e:
                logger.error(f"Erro HTTP {e.response.status_code}: {e.response.text}")
                if e.response.status_code >= 500:  # Erro do servidor, tenta novamente
                    if attempt == self.retry_attempts - 1:
                        raise
                    await asyncio.sleep(2 ** attempt)
                else:  # Erro do cliente, não tenta novamente
                    raise
                    
            except Exception as e:
                logger.error(f"Erro inesperado na tentativa {attempt + 1}: {e}")
                if attempt == self.retry_attempts - 1:
                    raise
                await asyncio.sleep(2 ** attempt)
        
        raise Exception("Todas as tentativas falharam")
    
    async def process_esg_data(self, esg_data: ESGDataRequest) -> TokenResponse:
        """
        Envia dados ESG para tokenização no Ecosystem-Degov
        """
        try:
            logger.info(f"Processando dados ESG para NFe: {esg_data.nfe_id}")
            
            # Converter para dict para serialização
            data = esg_data.model_dump()
            
            response = await self._make_request(
                "POST",
                "/api/v1/ecosystem-degov/process-esg-data",
                data=data
            )
            
            # Validar resposta
            if response.get("success"):
                logger.info(f"Dados ESG processados com sucesso - Transaction ID: {response.get('transaction_id')}")
                return TokenResponse(
                    success=True,
                    transaction_id=response.get("transaction_id"),
                    tokens_generated=response.get("tokens_generated"),
                    nft_metadata=response.get("nft_metadata"),
                    blockchain_status=response.get("blockchain_status"),
                    timestamp=response.get("timestamp", datetime.utcnow().isoformat())
                )
            else:
                logger.error(f"Falha no processamento ESG: {response.get('error_message')}")
                return TokenResponse(
                    success=False,
                    error_message=response.get("error_message", "Erro desconhecido"),
                    timestamp=datetime.utcnow().isoformat()
                )
                
        except Exception as e:
            logger.error(f"Erro ao processar dados ESG: {e}")
            return TokenResponse(
                success=False,
                error_message=str(e),
                timestamp=datetime.utcnow().isoformat()
            )
    
    async def get_token_status(self, nfe_id: str) -> TokenStatus:
        """
        Consulta status dos tokens gerados para uma NFe
        """
        try:
            logger.info(f"Consultando status dos tokens para NFe: {nfe_id}")
            
            response = await self._make_request(
                "GET",
                f"/api/v1/ecosystem-degov/token-status/{nfe_id}"
            )
            
            return TokenStatus(
                nfe_id=nfe_id,
                token_status=response.get("token_status", "unknown"),
                tokens_balance=response.get("tokens_balance"),
                nft_status=response.get("nft_status"),
                blockchain_confirmations=response.get("blockchain_confirmations"),
                last_updated=response.get("last_updated", datetime.utcnow().isoformat())
            )
            
        except Exception as e:
            logger.error(f"Erro ao consultar status dos tokens: {e}")
            return TokenStatus(
                nfe_id=nfe_id,
                token_status="error",
                last_updated=datetime.utcnow().isoformat()
            )
    
    async def batch_process_esg_data(self, esg_data_list: List[ESGDataRequest]) -> List[TokenResponse]:
        """
        Processa múltiplos dados ESG em lote
        """
        logger.info(f"Processando {len(esg_data_list)} dados ESG em lote")
        
        tasks = [self.process_esg_data(data) for data in esg_data_list]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Processar resultados e tratar exceções
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Erro no item {i}: {result}")
                processed_results.append(TokenResponse(
                    success=False,
                    error_message=str(result),
                    timestamp=datetime.utcnow().isoformat()
                ))
            else:
                processed_results.append(result)
        
        return processed_results
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Verifica saúde da integração com Ecosystem-Degov
        """
        try:
            response = await self._make_request("GET", "/health")
            return {
                "status": "healthy",
                "ecosystem_degov_status": response.get("status", "unknown"),
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Health check falhou: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

# Instância global do cliente
ecosystem_degov_client = EcosystemDegovClient()
