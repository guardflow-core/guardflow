#!/usr/bin/env python3
"""
GuardFlow Taskmash - Sistema de Orquestração de Tarefas
Integração com ARKITECT para desenvolvimento paralelo acelerado
"""

import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("guardflow.taskmash")

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"

class TaskPriority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

@dataclass
class Task:
    id: str
    name: str
    description: str
    category: str
    priority: TaskPriority
    status: TaskStatus
    dependencies: List[str]
    assignee: Optional[str] = None
    estimated_hours: Optional[float] = None
    actual_hours: Optional[float] = None
    created_at: datetime = None
    updated_at: datetime = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
        if self.metadata is None:
            self.metadata = {}

class TaskmashOrchestrator:
    """Orquestrador principal do Taskmash GuardFlow"""
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.categories = {
            "backend": "Backend Development",
            "mobile": "Mobile Development", 
            "web": "Web Development",
            "infra": "Infrastructure",
            "docs": "Documentation",
            "security": "Security",
            "data": "Data Management",
            "perf": "Performance",
            "governance": "Governance",
            "release": "Release Management"
        }
        self.metrics = {
            "total_tasks": 0,
            "completed_tasks": 0,
            "in_progress_tasks": 0,
            "blocked_tasks": 0,
            "avg_completion_time": 0.0
        }
    
    def create_task(self, 
                   name: str, 
                   description: str, 
                   category: str,
                   priority: TaskPriority = TaskPriority.MEDIUM,
                   dependencies: List[str] = None,
                   assignee: str = None,
                   estimated_hours: float = None) -> Task:
        """Cria uma nova tarefa"""
        
        task_id = str(uuid.uuid4())
        task = Task(
            id=task_id,
            name=name,
            description=description,
            category=category,
            priority=priority,
            status=TaskStatus.PENDING,
            dependencies=dependencies or [],
            assignee=assignee,
            estimated_hours=estimated_hours
        )
        
        self.tasks[task_id] = task
        self.metrics["total_tasks"] += 1
        
        logger.info(f"Tarefa criada: {name} (ID: {task_id})")
        return task
    
    def update_task_status(self, task_id: str, status: TaskStatus):
        """Atualiza status de uma tarefa"""
        if task_id in self.tasks:
            self.tasks[task_id].status = status
            self.tasks[task_id].updated_at = datetime.now()
            self._update_metrics()
            logger.info(f"Status atualizado para {task_id}: {status.value}")
    
    def get_ready_tasks(self) -> List[Task]:
        """Retorna tarefas prontas para execução (sem dependências pendentes)"""
        ready_tasks = []
        
        for task in self.tasks.values():
            if task.status == TaskStatus.PENDING:
                # Verifica se todas as dependências estão completas
                dependencies_met = True
                for dep_id in task.dependencies:
                    if dep_id not in self.tasks or self.tasks[dep_id].status != TaskStatus.COMPLETED:
                        dependencies_met = False
                        break
                
                if dependencies_met:
                    ready_tasks.append(task)
        
        return sorted(ready_tasks, key=lambda t: t.priority.value)
    
    def get_tasks_by_category(self, category: str) -> List[Task]:
        """Retorna tarefas por categoria"""
        return [task for task in self.tasks.values() if task.category == category]
    
    def get_critical_path(self) -> List[Task]:
        """Calcula caminho crítico das tarefas"""
        # Implementação simplificada - retorna tarefas de alta prioridade
        return sorted(
            [task for task in self.tasks.values() if task.priority == TaskPriority.CRITICAL],
            key=lambda t: t.created_at
        )
    
    def _update_metrics(self):
        """Atualiza métricas do sistema"""
        self.metrics["completed_tasks"] = len([t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED])
        self.metrics["in_progress_tasks"] = len([t for t in self.tasks.values() if t.status == TaskStatus.IN_PROGRESS])
        self.metrics["blocked_tasks"] = len([t for t in self.tasks.values() if t.status == TaskStatus.BLOCKED])
    
    def export_tasks(self, format: str = "json") -> str:
        """Exporta tarefas em formato específico"""
        if format == "json":
            tasks_data = {
                "metadata": {
                    "exported_at": datetime.now().isoformat(),
                    "total_tasks": len(self.tasks),
                    "metrics": self.metrics
                },
                "tasks": [asdict(task) for task in self.tasks.values()]
            }
            return json.dumps(tasks_data, indent=2, default=str)
        return ""
    
    def import_tasks(self, data: str):
        """Importa tarefas de formato JSON"""
        try:
            tasks_data = json.loads(data)
            for task_data in tasks_data.get("tasks", []):
                # Converte strings de volta para enums
                task_data["priority"] = TaskPriority(task_data["priority"])
                task_data["status"] = TaskStatus(task_data["status"])
                task_data["created_at"] = datetime.fromisoformat(task_data["created_at"])
                task_data["updated_at"] = datetime.fromisoformat(task_data["updated_at"])
                
                task = Task(**task_data)
                self.tasks[task.id] = task
        except Exception as e:
            logger.error(f"Erro ao importar tarefas: {e}")

def create_guardflow_taskmash() -> TaskmashOrchestrator:
    """Cria o taskmash completo do GuardFlow"""
    
    orchestrator = TaskmashOrchestrator()
    
    # Backend Tasks
    backend_tasks = [
        ("Backend: reforçar segurança (OAuth2/JWT, escopos, RBAC por rota)", 
         "Implementar autenticação robusta com OAuth2, JWT tokens, controle de escopos e RBAC granular por rota", 
         "backend", TaskPriority.CRITICAL, None, None, 16.0),
        
        ("Backend: cobertura de testes 60%+ (auth, cart, payment, store)", 
         "Expandir suite de testes para atingir 60%+ de cobertura, focando em endpoints críticos", 
         "backend", TaskPriority.HIGH, None, None, 12.0),
        
        ("Backend: contratos Pydantic padronizados e validação de resposta", 
         "Padronizar schemas Pydantic e implementar validação consistente de requests/responses", 
         "backend", TaskPriority.MEDIUM, None, None, 8.0),
        
        ("Backend: observabilidade (Prometheus labels, traces, logs com trace_id)", 
         "Implementar observabilidade completa com métricas, traces distribuídos e logging estruturado", 
         "backend", TaskPriority.MEDIUM, None, None, 10.0)
    ]
    
    # Mobile Tasks
    mobile_tasks = [
        ("Mobile: alinhar API_BASE_URL e contratos, telas de login/cart/checkout", 
         "Sincronizar mobile app com contratos da API e implementar telas principais", 
         "mobile", TaskPriority.HIGH, None, None, 20.0)
    ]
    
    # Web Tasks
    web_tasks = [
        ("Web: consolidar demo única e remover dívidas (scripts, env, README)", 
         "Consolidar demos web em uma única versão canônica e limpar dívidas técnicas", 
         "web", TaskPriority.MEDIUM, None, None, 6.0)
    ]
    
    # Infrastructure Tasks
    infra_tasks = [
        ("Infra: dockerizar backend + compose (DB/Redis) e perfis dev/prod", 
         "Containerizar aplicação e configurar ambientes de desenvolvimento e produção", 
         "infra", TaskPriority.HIGH, None, None, 8.0),
        
        ("CI/CD: quality gate (flake8/mypy), cobertura mínima e cache build", 
         "Implementar pipeline CI/CD com quality gates e otimizações de build", 
         "infra", TaskPriority.MEDIUM, None, None, 6.0)
    ]
    
    # Documentation Tasks
    docs_tasks = [
        ("Docs: OPERACAO_REPO, SETUP_DEV, API_REFERENCE (OpenAPI), CHANGELOG", 
         "Criar documentação completa: operação, setup, referência da API e changelog", 
         "docs", TaskPriority.LOW, None, None, 8.0)
    ]
    
    # Security Tasks
    security_tasks = [
        ("Segurança: política de secrets, rotação de chaves, rate limit granular", 
         "Implementar políticas de segurança robustas para secrets e rate limiting", 
         "security", TaskPriority.HIGH, None, None, 6.0)
    ]
    
    # Data Tasks
    data_tasks = [
        ("Dados: migração para PostgreSQL, modelos e seeds iniciais", 
         "Migrar para PostgreSQL e criar modelos de dados com seeds iniciais", 
         "data", TaskPriority.MEDIUM, None, None, 10.0)
    ]
    
    # Performance Tasks
    perf_tasks = [
        ("Performance: profiling endpoints críticos e caching seletivo", 
         "Otimizar performance de endpoints críticos e implementar estratégias de cache", 
         "perf", TaskPriority.LOW, None, None, 8.0)
    ]
    
    # Governance Tasks
    governance_tasks = [
        ("Governança: convenções de branches, SemVer, PR template e CODEOWNERS", 
         "Estabelecer padrões de governança para desenvolvimento colaborativo", 
         "governance", TaskPriority.LOW, None, None, 4.0)
    ]
    
    # Release Tasks
    release_tasks = [
        ("Release: checklist de release e plano de rollback", 
         "Criar processos de release e planos de contingência", 
         "release", TaskPriority.LOW, None, None, 4.0)
    ]
    
    # Criar todas as tarefas
    all_tasks = (backend_tasks + mobile_tasks + web_tasks + infra_tasks + 
                docs_tasks + security_tasks + data_tasks + perf_tasks + 
                governance_tasks + release_tasks)
    
    for task_data in all_tasks:
        orchestrator.create_task(*task_data)
    
    logger.info(f"Taskmash GuardFlow criado com {len(all_tasks)} tarefas")
    return orchestrator

async def main():
    """Função principal para demonstrar o Taskmash"""
    print("🚀 Iniciando GuardFlow Taskmash...")
    
    # Criar taskmash
    taskmash = create_guardflow_taskmash()
    
    # Mostrar estatísticas
    print(f"\n📊 Estatísticas do Taskmash:")
    print(f"Total de tarefas: {taskmash.metrics['total_tasks']}")
    
    # Mostrar tarefas por categoria
    for category, description in taskmash.categories.items():
        tasks = taskmash.get_tasks_by_category(category)
        if tasks:
            print(f"\n📁 {description}: {len(tasks)} tarefas")
            for task in tasks[:3]:  # Mostra apenas as primeiras 3
                print(f"  • {task.name}")
    
    # Mostrar tarefas prontas para execução
    ready_tasks = taskmash.get_ready_tasks()
    print(f"\n✅ Tarefas prontas para execução: {len(ready_tasks)}")
    for task in ready_tasks[:5]:  # Mostra apenas as primeiras 5
        print(f"  • {task.name} (Prioridade: {task.priority.name})")
    
    # Exportar taskmash
    export_data = taskmash.export_tasks("json")
    with open("guardflow_taskmash.json", "w", encoding="utf-8") as f:
        f.write(export_data)
    
    print(f"\n💾 Taskmash exportado para: guardflow_taskmash.json")
    print("🎯 Taskmash GuardFlow configurado com sucesso!")

if __name__ == "__main__":
    asyncio.run(main())
