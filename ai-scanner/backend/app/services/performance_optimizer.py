"""
Performance Optimizer - Otimização de Performance do Sistema GuardFlow
Monitora e otimiza automaticamente a performance do sistema
"""

import asyncio
import time
import psutil
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import json

logger = logging.getLogger(__name__)

class OptimizationLevel(Enum):
    """Níveis de otimização"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    AGGRESSIVE = "aggressive"

@dataclass
class PerformanceMetrics:
    """Métricas de performance"""
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_io: Dict[str, float]
    response_times: Dict[str, float]
    error_rates: Dict[str, float]
    active_connections: int
    cache_hit_rate: float
    database_connections: int
    timestamp: datetime

@dataclass
class OptimizationAction:
    """Ação de otimização"""
    action_type: str
    description: str
    impact_level: str
    estimated_improvement: float
    executed: bool = False
    execution_time: Optional[datetime] = None
    result: Optional[str] = None

class PerformanceOptimizer:
    """Otimizador de Performance Principal"""
    
    def __init__(self):
        self.metrics_history: List[PerformanceMetrics] = []
        self.optimization_actions: List[OptimizationAction] = []
        self.cache_manager = CacheOptimizer()
        self.database_optimizer = DatabaseOptimizer()
        self.api_optimizer = APIOptimizer()
        self.memory_optimizer = MemoryOptimizer()
        
        # Configurações
        self.monitoring_interval = 30  # segundos
        self.optimization_threshold = {
            "cpu": 80.0,
            "memory": 85.0,
            "response_time": 2.0,  # segundos
            "error_rate": 0.05  # 5%
        }
        
        self.is_monitoring = False
        
    async def start_monitoring(self):
        """Inicia monitoramento contínuo"""
        self.is_monitoring = True
        logger.info("Iniciando monitoramento de performance")
        
        while self.is_monitoring:
            try:
                metrics = await self.collect_metrics()
                self.metrics_history.append(metrics)
                
                # Manter apenas últimas 1000 métricas
                if len(self.metrics_history) > 1000:
                    self.metrics_history = self.metrics_history[-1000:]
                
                # Verificar se otimização é necessária
                if await self.should_optimize(metrics):
                    await self.execute_optimization(metrics)
                
                await asyncio.sleep(self.monitoring_interval)
                
            except Exception as e:
                logger.error(f"Erro no monitoramento: {e}")
                await asyncio.sleep(5)
    
    def stop_monitoring(self):
        """Para monitoramento"""
        self.is_monitoring = False
        logger.info("Monitoramento de performance parado")
    
    async def collect_metrics(self) -> PerformanceMetrics:
        """Coleta métricas atuais do sistema"""
        try:
            # Métricas do sistema
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            network = psutil.net_io_counters()
            
            # Métricas da aplicação (simuladas)
            response_times = await self._get_response_times()
            error_rates = await self._get_error_rates()
            cache_hit_rate = await self.cache_manager.get_hit_rate()
            
            return PerformanceMetrics(
                cpu_usage=cpu_percent,
                memory_usage=memory.percent,
                disk_usage=disk.percent,
                network_io={
                    "bytes_sent": network.bytes_sent,
                    "bytes_recv": network.bytes_recv
                },
                response_times=response_times,
                error_rates=error_rates,
                active_connections=await self._get_active_connections(),
                cache_hit_rate=cache_hit_rate,
                database_connections=await self.database_optimizer.get_connection_count(),
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Erro ao coletar métricas: {e}")
            # Retornar métricas padrão em caso de erro
            return PerformanceMetrics(
                cpu_usage=0.0,
                memory_usage=0.0,
                disk_usage=0.0,
                network_io={},
                response_times={},
                error_rates={},
                active_connections=0,
                cache_hit_rate=0.0,
                database_connections=0,
                timestamp=datetime.now()
            )
    
    async def should_optimize(self, metrics: PerformanceMetrics) -> bool:
        """Verifica se otimização é necessária"""
        conditions = [
            metrics.cpu_usage > self.optimization_threshold["cpu"],
            metrics.memory_usage > self.optimization_threshold["memory"],
            any(rt > self.optimization_threshold["response_time"] 
                for rt in metrics.response_times.values()),
            any(er > self.optimization_threshold["error_rate"] 
                for er in metrics.error_rates.values()),
            metrics.cache_hit_rate < 0.8  # Cache hit rate baixo
        ]
        
        return any(conditions)
    
    async def execute_optimization(self, metrics: PerformanceMetrics):
        """Executa otimizações baseadas nas métricas"""
        logger.info("Executando otimizações de performance")
        
        actions = []
        
        # Otimização de CPU
        if metrics.cpu_usage > self.optimization_threshold["cpu"]:
            actions.extend(await self._optimize_cpu())
        
        # Otimização de Memória
        if metrics.memory_usage > self.optimization_threshold["memory"]:
            actions.extend(await self.memory_optimizer.optimize())
        
        # Otimização de Cache
        if metrics.cache_hit_rate < 0.8:
            actions.extend(await self.cache_manager.optimize())
        
        # Otimização de Database
        if metrics.database_connections > 50:  # Threshold exemplo
            actions.extend(await self.database_optimizer.optimize())
        
        # Otimização de API
        slow_apis = [api for api, time in metrics.response_times.items() 
                    if time > self.optimization_threshold["response_time"]]
        if slow_apis:
            actions.extend(await self.api_optimizer.optimize(slow_apis))
        
        # Executar ações
        for action in actions:
            try:
                await self._execute_action(action)
                self.optimization_actions.append(action)
            except Exception as e:
                logger.error(f"Erro ao executar ação {action.action_type}: {e}")
    
    async def _optimize_cpu(self) -> List[OptimizationAction]:
        """Otimizações específicas para CPU"""
        actions = []
        
        actions.append(OptimizationAction(
            action_type="reduce_worker_processes",
            description="Reduzir processos worker temporariamente",
            impact_level="medium",
            estimated_improvement=15.0
        ))
        
        actions.append(OptimizationAction(
            action_type="enable_cpu_throttling",
            description="Ativar throttling de CPU para requests não críticos",
            impact_level="low",
            estimated_improvement=10.0
        ))
        
        return actions
    
    async def _execute_action(self, action: OptimizationAction):
        """Executa uma ação de otimização específica"""
        logger.info(f"Executando ação: {action.action_type}")
        
        action.execution_time = datetime.now()
        
        try:
            if action.action_type == "clear_cache":
                await self.cache_manager.clear_expired()
                action.result = "Cache limpo com sucesso"
                
            elif action.action_type == "optimize_database_connections":
                await self.database_optimizer.close_idle_connections()
                action.result = "Conexões idle fechadas"
                
            elif action.action_type == "enable_response_compression":
                # Simular ativação de compressão
                action.result = "Compressão de resposta ativada"
                
            elif action.action_type == "reduce_worker_processes":
                # Simular redução de workers
                action.result = "Workers reduzidos temporariamente"
                
            else:
                action.result = f"Ação {action.action_type} simulada"
            
            action.executed = True
            logger.info(f"Ação executada: {action.result}")
            
        except Exception as e:
            action.result = f"Erro: {str(e)}"
            logger.error(f"Erro ao executar ação {action.action_type}: {e}")
    
    async def get_performance_report(self) -> Dict[str, Any]:
        """Gera relatório de performance"""
        if not self.metrics_history:
            return {"error": "Nenhuma métrica coletada ainda"}
        
        latest_metrics = self.metrics_history[-1]
        
        # Calcular médias das últimas 10 métricas
        recent_metrics = self.metrics_history[-10:]
        avg_cpu = sum(m.cpu_usage for m in recent_metrics) / len(recent_metrics)
        avg_memory = sum(m.memory_usage for m in recent_metrics) / len(recent_metrics)
        avg_cache_hit = sum(m.cache_hit_rate for m in recent_metrics) / len(recent_metrics)
        
        return {
            "current_status": {
                "cpu_usage": latest_metrics.cpu_usage,
                "memory_usage": latest_metrics.memory_usage,
                "disk_usage": latest_metrics.disk_usage,
                "cache_hit_rate": latest_metrics.cache_hit_rate,
                "active_connections": latest_metrics.active_connections,
                "database_connections": latest_metrics.database_connections
            },
            "averages_last_10": {
                "cpu_usage": round(avg_cpu, 2),
                "memory_usage": round(avg_memory, 2),
                "cache_hit_rate": round(avg_cache_hit, 2)
            },
            "optimization_actions": {
                "total_executed": len([a for a in self.optimization_actions if a.executed]),
                "recent_actions": [
                    {
                        "type": a.action_type,
                        "description": a.description,
                        "result": a.result,
                        "executed_at": a.execution_time.isoformat() if a.execution_time else None
                    }
                    for a in self.optimization_actions[-5:]  # Últimas 5 ações
                ]
            },
            "recommendations": await self._generate_recommendations(latest_metrics),
            "health_score": await self._calculate_health_score(latest_metrics)
        }
    
    async def _generate_recommendations(self, metrics: PerformanceMetrics) -> List[str]:
        """Gera recomendações baseadas nas métricas"""
        recommendations = []
        
        if metrics.cpu_usage > 70:
            recommendations.append("Considere aumentar recursos de CPU ou otimizar algoritmos")
        
        if metrics.memory_usage > 80:
            recommendations.append("Memória alta detectada - revisar vazamentos e otimizar cache")
        
        if metrics.cache_hit_rate < 0.7:
            recommendations.append("Taxa de cache baixa - revisar estratégia de caching")
        
        if metrics.database_connections > 40:
            recommendations.append("Muitas conexões de banco - implementar connection pooling")
        
        if not recommendations:
            recommendations.append("Sistema operando dentro dos parâmetros normais")
        
        return recommendations
    
    async def _calculate_health_score(self, metrics: PerformanceMetrics) -> float:
        """Calcula score de saúde do sistema (0-100)"""
        scores = []
        
        # Score CPU (invertido - menor uso = melhor score)
        cpu_score = max(0, 100 - metrics.cpu_usage)
        scores.append(cpu_score)
        
        # Score Memória
        memory_score = max(0, 100 - metrics.memory_usage)
        scores.append(memory_score)
        
        # Score Cache
        cache_score = metrics.cache_hit_rate * 100
        scores.append(cache_score)
        
        # Score médio
        return round(sum(scores) / len(scores), 1)
    
    # Métodos auxiliares (simulados)
    async def _get_response_times(self) -> Dict[str, float]:
        """Simula coleta de tempos de resposta das APIs"""
        return {
            "/api/v1/scanner": 0.5,
            "/api/v1/cart": 0.3,
            "/api/v1/esg": 1.2,
            "/api/v1/qr-checkout": 0.8
        }
    
    async def _get_error_rates(self) -> Dict[str, float]:
        """Simula coleta de taxas de erro"""
        return {
            "/api/v1/scanner": 0.01,
            "/api/v1/cart": 0.005,
            "/api/v1/esg": 0.02,
            "/api/v1/qr-checkout": 0.015
        }
    
    async def _get_active_connections(self) -> int:
        """Simula contagem de conexões ativas"""
        return 25

# ==================== OTIMIZADORES ESPECÍFICOS ====================

class CacheOptimizer:
    """Otimizador de Cache"""
    
    async def get_hit_rate(self) -> float:
        """Simula taxa de hit do cache"""
        return 0.85
    
    async def optimize(self) -> List[OptimizationAction]:
        """Otimiza configurações de cache"""
        return [
            OptimizationAction(
                action_type="clear_cache",
                description="Limpar cache expirado",
                impact_level="low",
                estimated_improvement=5.0
            ),
            OptimizationAction(
                action_type="increase_cache_size",
                description="Aumentar tamanho do cache",
                impact_level="medium",
                estimated_improvement=15.0
            )
        ]
    
    async def clear_expired(self):
        """Limpa cache expirado"""
        logger.info("Cache expirado limpo")

class DatabaseOptimizer:
    """Otimizador de Banco de Dados"""
    
    async def get_connection_count(self) -> int:
        """Simula contagem de conexões do banco"""
        return 15
    
    async def optimize(self) -> List[OptimizationAction]:
        """Otimiza configurações do banco"""
        return [
            OptimizationAction(
                action_type="optimize_database_connections",
                description="Otimizar pool de conexões",
                impact_level="high",
                estimated_improvement=25.0
            )
        ]
    
    async def close_idle_connections(self):
        """Fecha conexões idle"""
        logger.info("Conexões idle fechadas")

class APIOptimizer:
    """Otimizador de APIs"""
    
    async def optimize(self, slow_apis: List[str]) -> List[OptimizationAction]:
        """Otimiza APIs lentas"""
        actions = []
        
        for api in slow_apis:
            actions.append(OptimizationAction(
                action_type="enable_response_compression",
                description=f"Ativar compressão para {api}",
                impact_level="medium",
                estimated_improvement=20.0
            ))
        
        return actions

class MemoryOptimizer:
    """Otimizador de Memória"""
    
    async def optimize(self) -> List[OptimizationAction]:
        """Otimiza uso de memória"""
        return [
            OptimizationAction(
                action_type="garbage_collection",
                description="Forçar coleta de lixo",
                impact_level="low",
                estimated_improvement=8.0
            ),
            OptimizationAction(
                action_type="reduce_memory_buffers",
                description="Reduzir buffers de memória",
                impact_level="medium",
                estimated_improvement=12.0
            )
        ]

# Instância global
performance_optimizer = PerformanceOptimizer()
