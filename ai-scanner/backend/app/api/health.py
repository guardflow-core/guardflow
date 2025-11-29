"""
Health Check API Endpoints
Monitoramento e saúde do sistema
DIA 1 MVP - Monitoramento completo
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from datetime import datetime
import psutil
import asyncio
from typing import Dict, Any

from app.database import get_db, DatabaseUtils
from app.config import settings

# Logger
logger = logging.getLogger("guardflow.health")

# Router
router = APIRouter()

@router.get("/")
async def basic_health_check():
    """
    Health check básico
    """
    return {
        "status": "healthy",
        "message": "GuardFlow agilizando perfeitamente! ✅",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.utcnow().isoformat(),
        "slogan": "Agiliza aí! ⚡"
    }

@router.get("/detailed")
async def detailed_health_check(db: AsyncSession = Depends(get_db)):
    """
    Health check detalhado com métricas do sistema
    """
    try:
        start_time = datetime.utcnow()
        
        # Verificar banco de dados
        db_health = await DatabaseUtils.health_check()
        
        # Métricas do sistema
        system_metrics = _get_system_metrics()
        
        # Verificar APIs externas (mock para MVP)
        external_apis = await _check_external_apis()
        
        # Calcular tempo de resposta
        response_time = (datetime.utcnow() - start_time).total_seconds() * 1000
        
        # Status geral
        overall_status = "healthy"
        if db_health["status"] != "healthy":
            overall_status = "unhealthy"
        elif any(api["status"] != "healthy" for api in external_apis.values()):
            overall_status = "degraded"
        elif system_metrics["memory_usage_percent"] > 90:
            overall_status = "degraded"
        
        health_data = {
            "status": overall_status,
            "message": f"Sistema {overall_status} - Agilizando {'perfeitamente' if overall_status == 'healthy' else 'com atenção'}! 🔍",
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
            "response_time_ms": round(response_time, 2),
            "timestamp": datetime.utcnow().isoformat(),
            "components": {
                "database": db_health,
                "system": system_metrics,
                "external_apis": external_apis
            }
        }
        
        logger.info(f"🔍 Health check: {overall_status} em {response_time:.2f}ms")
        
        return health_data
        
    except Exception as e:
        logger.error(f"❌ Erro no health check: {str(e)}")
        return {
            "status": "unhealthy",
            "message": f"Erro no health check: {str(e)} ❌",
            "version": settings.APP_VERSION,
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }

@router.get("/database")
async def database_health_check(db: AsyncSession = Depends(get_db)):
    """
    Health check específico do banco de dados
    """
    try:
        db_health = await DatabaseUtils.health_check()
        table_counts = await DatabaseUtils.get_table_counts()
        
        return {
            "status": db_health["status"],
            "message": db_health["message"],
            "connection_info": {
                "version": db_health.get("version"),
                "pool_size": db_health.get("pool_size"),
                "checked_out": db_health.get("checked_out")
            },
            "table_counts": table_counts.get("counts", {}),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Erro no health check do banco: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao verificar saúde do banco: {str(e)}"
        )

@router.get("/system")
async def system_health_check():
    """
    Health check do sistema operacional
    """
    try:
        metrics = _get_system_metrics()
        
        # Determinar status baseado nas métricas
        status_health = "healthy"
        warnings = []
        
        if metrics["memory_usage_percent"] > 90:
            status_health = "degraded"
            warnings.append("Uso de memória alto")
        
        if metrics["cpu_usage_percent"] > 90:
            status_health = "degraded"
            warnings.append("Uso de CPU alto")
        
        if metrics["disk_usage_percent"] > 90:
            status_health = "degraded"
            warnings.append("Uso de disco alto")
        
        return {
            "status": status_health,
            "message": f"Sistema {status_health} - {'Recursos agilizados!' if status_health == 'healthy' else 'Atenção aos recursos!'} 💻",
            "metrics": metrics,
            "warnings": warnings,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Erro no health check do sistema: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao verificar sistema: {str(e)}"
        )

@router.get("/apis")
async def external_apis_health_check():
    """
    Health check das APIs externas
    """
    try:
        apis_status = await _check_external_apis()
        
        # Status geral
        overall_status = "healthy"
        if any(api["status"] != "healthy" for api in apis_status.values()):
            overall_status = "degraded"
        
        return {
            "status": overall_status,
            "message": f"APIs externas {overall_status} - {'Integrações agilizadas!' if overall_status == 'healthy' else 'Algumas integrações com problemas!'} 🔗",
            "apis": apis_status,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Erro no health check das APIs: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao verificar APIs externas: {str(e)}"
        )

@router.get("/metrics")
async def get_application_metrics(db: AsyncSession = Depends(get_db)):
    """
    Métricas da aplicação GuardFlow
    """
    try:
        # Contar registros principais
        table_counts = await DatabaseUtils.get_table_counts()
        
        # Métricas de negócio (mock para MVP)
        business_metrics = {
            "active_users_today": 42,  # Mock
            "transactions_today": 128,  # Mock
            "total_revenue_today": "R$ 3.240,50",  # Mock
            "avg_checkout_time_seconds": 28.5,  # Mock
            "success_rate_percent": 96.8,  # Mock
            "stores_online": 15  # Mock
        }
        
        # Métricas técnicas
        system_metrics = _get_system_metrics()
        
        return {
            "success": True,
            "message": "Métricas agilizadas! 📊",
            "data": {
                "business": business_metrics,
                "database": table_counts.get("counts", {}),
                "system": system_metrics,
                "application": {
                    "version": settings.APP_VERSION,
                    "environment": settings.ENVIRONMENT,
                    "uptime_hours": _get_uptime_hours(),
                    "features_enabled": {
                        "product_recommendations": settings.ENABLE_PRODUCT_RECOMMENDATIONS,
                        "loyalty_program": settings.ENABLE_LOYALTY_PROGRAM,
                        "esg_tracking": settings.ENABLE_ESG_TRACKING,
                        "analytics": settings.ENABLE_ANALYTICS
                    }
                }
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter métricas: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter métricas da aplicação"
        )

@router.post("/cleanup")
async def cleanup_expired_data(db: AsyncSession = Depends(get_db)):
    """
    Limpeza de dados expirados
    """
    try:
        # Limpar carrinhos expirados
        cleanup_result = await DatabaseUtils.cleanup_expired_carts()
        
        logger.info(f"🧹 Limpeza executada: {cleanup_result.get('affected_rows', 0)} carrinhos")
        
        return {
            "success": True,
            "message": f"Limpeza agilizada! {cleanup_result.get('message', 'Dados limpos')} 🧹",
            "data": cleanup_result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Erro na limpeza: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao executar limpeza"
        )

# Funções auxiliares

def _get_system_metrics() -> Dict[str, Any]:
    """
    Obter métricas do sistema
    """
    try:
        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Memória
        memory = psutil.virtual_memory()
        
        # Disco
        disk = psutil.disk_usage('/')
        
        # Rede (se disponível)
        try:
            network = psutil.net_io_counters()
            network_stats = {
                "bytes_sent": network.bytes_sent,
                "bytes_recv": network.bytes_recv,
                "packets_sent": network.packets_sent,
                "packets_recv": network.packets_recv
            }
        except:
            network_stats = None
        
        return {
            "cpu_usage_percent": round(cpu_percent, 2),
            "memory_total_gb": round(memory.total / (1024**3), 2),
            "memory_used_gb": round(memory.used / (1024**3), 2),
            "memory_usage_percent": round(memory.percent, 2),
            "disk_total_gb": round(disk.total / (1024**3), 2),
            "disk_used_gb": round(disk.used / (1024**3), 2),
            "disk_usage_percent": round((disk.used / disk.total) * 100, 2),
            "network": network_stats,
            "load_average": psutil.getloadavg() if hasattr(psutil, 'getloadavg') else None
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter métricas do sistema: {str(e)}")
        return {
            "error": str(e),
            "cpu_usage_percent": 0,
            "memory_usage_percent": 0,
            "disk_usage_percent": 0
        }

async def _check_external_apis() -> Dict[str, Dict[str, Any]]:
    """
    Verificar status das APIs externas (mock para MVP)
    """
    try:
        # Simular verificação das APIs
        apis = {
            "mercado_pago": {
                "status": "healthy",
                "response_time_ms": 245,
                "last_check": datetime.utcnow().isoformat(),
                "message": "PIX agilizando! 💳"
            },
            "google_vision": {
                "status": "healthy", 
                "response_time_ms": 890,
                "last_check": datetime.utcnow().isoformat(),
                "message": "Scanner agilizando! 📸"
            },
            "guardpass": {
                "status": "healthy",
                "response_time_ms": 156,
                "last_check": datetime.utcnow().isoformat(),
                "message": "Auth agilizando! 🔐"
            }
        }
        
        # Simular delay de rede
        await asyncio.sleep(0.1)
        
        return apis
        
    except Exception as e:
        logger.error(f"❌ Erro ao verificar APIs externas: {str(e)}")
        return {
            "error": {
                "status": "unhealthy",
                "message": f"Erro na verificação: {str(e)}",
                "last_check": datetime.utcnow().isoformat()
            }
        }

def _get_uptime_hours() -> float:
    """
    Calcular uptime da aplicação (mock para MVP)
    """
    try:
        # Em produção, usar timestamp de inicialização real
        import time
        boot_time = psutil.boot_time()
        uptime_seconds = time.time() - boot_time
        return round(uptime_seconds / 3600, 2)
    except:
        return 24.5  # Mock: 24.5 horas

# Endpoint de desenvolvimento
if settings.DEBUG:
    @router.get("/debug")
    async def debug_info():
        """
        Informações de debug (apenas desenvolvimento)
        """
        try:
            import platform
            import sys
            
            return {
                "success": True,
                "message": "Debug info agilizado! 🔧",
                "data": {
                    "python_version": sys.version,
                    "platform": platform.platform(),
                    "architecture": platform.architecture(),
                    "processor": platform.processor(),
                    "hostname": platform.node(),
                    "settings": {
                        "debug": settings.DEBUG,
                        "environment": settings.ENVIRONMENT,
                        "database_url": settings.DATABASE_URL.split("@")[0] + "@***",
                        "redis_url": settings.REDIS_URL.split("@")[0] + "@***" if "@" in settings.REDIS_URL else settings.REDIS_URL,
                        "log_level": settings.LOG_LEVEL
                    }
                },
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro no debug: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
