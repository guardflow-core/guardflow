"""
API de Performance - Monitoramento e Otimização
Endpoints para monitorar e otimizar performance do sistema
"""

from fastapi import APIRouter, HTTPException, Depends, Request, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.services.performance_optimizer import performance_optimizer, OptimizationLevel

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
router = APIRouter()
router.state.limiter = limiter
router.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ==================== MODELS ====================

class PerformanceStatus(BaseModel):
    """Status atual de performance"""
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    cache_hit_rate: float
    active_connections: int
    database_connections: int
    health_score: float
    status: str
    timestamp: datetime

class OptimizationRequest(BaseModel):
    """Request para otimização manual"""
    level: OptimizationLevel = Field(default=OptimizationLevel.MEDIUM)
    target_areas: List[str] = Field(default_factory=lambda: ["cpu", "memory", "cache"])
    force: bool = Field(default=False, description="Forçar otimização mesmo se não necessária")

class OptimizationResult(BaseModel):
    """Resultado da otimização"""
    success: bool
    actions_executed: int
    estimated_improvement: float
    execution_time: float
    details: List[Dict[str, Any]]

class MonitoringConfig(BaseModel):
    """Configuração de monitoramento"""
    interval_seconds: int = Field(default=30, ge=10, le=300)
    cpu_threshold: float = Field(default=80.0, ge=50.0, le=95.0)
    memory_threshold: float = Field(default=85.0, ge=60.0, le=95.0)
    response_time_threshold: float = Field(default=2.0, ge=0.5, le=10.0)
    auto_optimize: bool = Field(default=True)

# ==================== ENDPOINTS ====================

@router.get("/status", response_model=PerformanceStatus)
@limiter.limit("60/minute")
async def get_performance_status(request: Request):
    """
    Retorna status atual de performance do sistema
    """
    try:
        # Coletar métricas atuais
        metrics = await performance_optimizer.collect_metrics()
        health_score = await performance_optimizer._calculate_health_score(metrics)
        
        # Determinar status baseado no health score
        if health_score >= 80:
            status = "excellent"
        elif health_score >= 60:
            status = "good"
        elif health_score >= 40:
            status = "warning"
        else:
            status = "critical"
        
        return PerformanceStatus(
            cpu_usage=metrics.cpu_usage,
            memory_usage=metrics.memory_usage,
            disk_usage=metrics.disk_usage,
            cache_hit_rate=metrics.cache_hit_rate,
            active_connections=metrics.active_connections,
            database_connections=metrics.database_connections,
            health_score=health_score,
            status=status,
            timestamp=metrics.timestamp
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter status: {str(e)}")

@router.get("/report")
@limiter.limit("30/minute")
async def get_performance_report(request: Request):
    """
    Retorna relatório detalhado de performance
    """
    try:
        report = await performance_optimizer.get_performance_report()
        return report
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar relatório: {str(e)}")

@router.post("/optimize", response_model=OptimizationResult)
@limiter.limit("10/minute")
async def optimize_performance(
    request: Request,
    optimization_request: OptimizationRequest,
    background_tasks: BackgroundTasks
):
    """
    Executa otimização manual do sistema
    """
    try:
        import time
        start_time = time.time()
        
        # Coletar métricas atuais
        metrics = await performance_optimizer.collect_metrics()
        
        # Verificar se otimização é necessária (a menos que forçada)
        if not optimization_request.force:
            needs_optimization = await performance_optimizer.should_optimize(metrics)
            if not needs_optimization:
                return OptimizationResult(
                    success=True,
                    actions_executed=0,
                    estimated_improvement=0.0,
                    execution_time=time.time() - start_time,
                    details=[{"message": "Sistema já está otimizado"}]
                )
        
        # Executar otimização
        actions_before = len(performance_optimizer.optimization_actions)
        await performance_optimizer.execute_optimization(metrics)
        actions_after = len(performance_optimizer.optimization_actions)
        
        actions_executed = actions_after - actions_before
        recent_actions = performance_optimizer.optimization_actions[-actions_executed:] if actions_executed > 0 else []
        
        # Calcular melhoria estimada
        estimated_improvement = sum(action.estimated_improvement for action in recent_actions)
        
        execution_time = time.time() - start_time
        
        return OptimizationResult(
            success=True,
            actions_executed=actions_executed,
            estimated_improvement=estimated_improvement,
            execution_time=execution_time,
            details=[
                {
                    "action": action.action_type,
                    "description": action.description,
                    "impact": action.impact_level,
                    "improvement": action.estimated_improvement,
                    "result": action.result
                }
                for action in recent_actions
            ]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na otimização: {str(e)}")

@router.post("/monitoring/start")
@limiter.limit("5/minute")
async def start_monitoring(
    request: Request,
    config: Optional[MonitoringConfig] = None,
    background_tasks: BackgroundTasks = None
):
    """
    Inicia monitoramento automático de performance
    """
    try:
        if performance_optimizer.is_monitoring:
            return {"message": "Monitoramento já está ativo", "status": "already_running"}
        
        # Aplicar configurações se fornecidas
        if config:
            performance_optimizer.monitoring_interval = config.interval_seconds
            performance_optimizer.optimization_threshold.update({
                "cpu": config.cpu_threshold,
                "memory": config.memory_threshold,
                "response_time": config.response_time_threshold
            })
        
        # Iniciar monitoramento em background
        background_tasks.add_task(performance_optimizer.start_monitoring)
        
        return {
            "message": "Monitoramento iniciado com sucesso",
            "status": "started",
            "config": {
                "interval": performance_optimizer.monitoring_interval,
                "thresholds": performance_optimizer.optimization_threshold
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao iniciar monitoramento: {str(e)}")

@router.post("/monitoring/stop")
@limiter.limit("5/minute")
async def stop_monitoring(request: Request):
    """
    Para monitoramento automático de performance
    """
    try:
        if not performance_optimizer.is_monitoring:
            return {"message": "Monitoramento não está ativo", "status": "not_running"}
        
        performance_optimizer.stop_monitoring()
        
        return {
            "message": "Monitoramento parado com sucesso",
            "status": "stopped"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao parar monitoramento: {str(e)}")

@router.get("/monitoring/status")
@limiter.limit("60/minute")
async def get_monitoring_status(request: Request):
    """
    Retorna status do monitoramento
    """
    try:
        return {
            "is_active": performance_optimizer.is_monitoring,
            "interval_seconds": performance_optimizer.monitoring_interval,
            "thresholds": performance_optimizer.optimization_threshold,
            "metrics_collected": len(performance_optimizer.metrics_history),
            "actions_executed": len([a for a in performance_optimizer.optimization_actions if a.executed]),
            "last_optimization": (
                performance_optimizer.optimization_actions[-1].execution_time.isoformat()
                if performance_optimizer.optimization_actions and performance_optimizer.optimization_actions[-1].executed
                else None
            )
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter status: {str(e)}")

@router.get("/metrics/history")
@limiter.limit("30/minute")
async def get_metrics_history(
    request: Request,
    limit: int = 100,
    hours: Optional[int] = None
):
    """
    Retorna histórico de métricas
    """
    try:
        metrics_history = performance_optimizer.metrics_history
        
        # Filtrar por tempo se especificado
        if hours:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            metrics_history = [m for m in metrics_history if m.timestamp >= cutoff_time]
        
        # Limitar quantidade
        metrics_history = metrics_history[-limit:]
        
        return {
            "total_metrics": len(metrics_history),
            "time_range": {
                "start": metrics_history[0].timestamp.isoformat() if metrics_history else None,
                "end": metrics_history[-1].timestamp.isoformat() if metrics_history else None
            },
            "metrics": [
                {
                    "timestamp": m.timestamp.isoformat(),
                    "cpu_usage": m.cpu_usage,
                    "memory_usage": m.memory_usage,
                    "cache_hit_rate": m.cache_hit_rate,
                    "active_connections": m.active_connections,
                    "database_connections": m.database_connections
                }
                for m in metrics_history
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter histórico: {str(e)}")

@router.get("/actions/history")
@limiter.limit("30/minute")
async def get_actions_history(
    request: Request,
    limit: int = 50
):
    """
    Retorna histórico de ações de otimização
    """
    try:
        actions = performance_optimizer.optimization_actions[-limit:]
        
        return {
            "total_actions": len(performance_optimizer.optimization_actions),
            "showing": len(actions),
            "actions": [
                {
                    "action_type": action.action_type,
                    "description": action.description,
                    "impact_level": action.impact_level,
                    "estimated_improvement": action.estimated_improvement,
                    "executed": action.executed,
                    "execution_time": action.execution_time.isoformat() if action.execution_time else None,
                    "result": action.result
                }
                for action in actions
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter histórico de ações: {str(e)}")

@router.get("/health")
@limiter.limit("120/minute")
async def health_check(request: Request):
    """
    Health check rápido do sistema de performance
    """
    try:
        # Verificação básica
        is_monitoring = performance_optimizer.is_monitoring
        metrics_count = len(performance_optimizer.metrics_history)
        
        # Status simplificado
        if metrics_count > 0:
            latest_metric = performance_optimizer.metrics_history[-1]
            health_score = await performance_optimizer._calculate_health_score(latest_metric)
        else:
            health_score = 0.0
        
        return {
            "status": "healthy" if health_score > 50 else "degraded",
            "monitoring_active": is_monitoring,
            "health_score": health_score,
            "metrics_available": metrics_count > 0,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
