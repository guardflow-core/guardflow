#!/usr/bin/env python3
"""
GuardFlow - Executor do Taskmash Super Escopo
Baseado na análise Trinity e organizado por prioridades
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any

class TaskmashExecutor:
    def __init__(self, taskmash_file: str = "taskmash_super_escopo.json"):
        self.taskmash_file = taskmash_file
        self.taskmash = self.load_taskmash()
        
    def load_taskmash(self) -> Dict[str, Any]:
        """Carrega o taskmash do arquivo JSON"""
        try:
            with open(self.taskmash_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Arquivo {self.taskmash_file} não encontrado!")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Erro ao decodificar JSON: {e}")
            sys.exit(1)
    
    def get_tasks_by_phase(self, phase_id: str) -> List[Dict[str, Any]]:
        """Retorna tarefas de uma fase específica"""
        for phase in self.taskmash['taskmash']['phases']:
            if phase['id'] == phase_id:
                return phase['tasks']
        return []
    
    def get_tasks_by_priority(self, priority: str) -> List[Dict[str, Any]]:
        """Retorna tarefas por prioridade"""
        tasks = []
        for phase in self.taskmash['taskmash']['phases']:
            for task in phase['tasks']:
                if task['priority'] == priority:
                    tasks.append(task)
        return tasks
    
    def get_critical_path(self) -> List[str]:
        """Retorna o caminho crítico"""
        return self.taskmash['taskmash']['critical_path']
    
    def get_next_tasks(self) -> List[Dict[str, Any]]:
        """Retorna próximas tarefas a serem executadas"""
        next_tasks = []
        
        # Buscar tarefas críticas sem dependências ou com dependências concluídas
        for phase in self.taskmash['taskmash']['phases']:
            for task in phase['tasks']:
                if task['status'] == 'pending' and task['priority'] == 'CRITICA':
                    # Verificar se dependências estão concluídas
                    if self.are_dependencies_met(task['dependencies']):
                        next_tasks.append(task)
        
        return next_tasks
    
    def are_dependencies_met(self, dependencies: List[str]) -> bool:
        """Verifica se dependências estão concluídas"""
        if not dependencies:
            return True
        
        # Por simplicidade, assumir que dependências estão OK
        # Em implementação real, verificar status das tarefas
        return True
    
    def print_phase_summary(self, phase_id: str):
        """Imprime resumo de uma fase"""
        phase = None
        for p in self.taskmash['taskmash']['phases']:
            if p['id'] == phase_id:
                phase = p
                break
        
        if not phase:
            print(f"❌ Fase {phase_id} não encontrada!")
            return
        
        print(f"\n🎯 {phase['name'].upper()}")
        print(f"📅 Duração: {phase['duration_days']} dias")
        print(f"📊 Status: {phase['status']}")
        print("-" * 50)
        
        tasks = phase['tasks']
        for task in tasks:
            status_icon = "✅" if task['status'] == 'completed' else "⏳" if task['status'] == 'in_progress' else "⭕"
            priority_icon = "🔴" if task['priority'] == 'CRITICA' else "🟡" if task['priority'] == 'ALTA' else "🟢"
            
            print(f"{status_icon} {priority_icon} {task['id']}: {task['name']}")
            print(f"   📅 {task['estimated_days']} dias | 👤 {task['assignee']} | 🏷️ {task['category']}")
            if task['dependencies']:
                print(f"   🔗 Dependências: {', '.join(task['dependencies'])}")
            print()
    
    def print_critical_path(self):
        """Imprime o caminho crítico"""
        print("\n🚨 CAMINHO CRÍTICO")
        print("=" * 50)
        
        critical_path = self.get_critical_path()
        for i, task_id in enumerate(critical_path, 1):
            # Buscar detalhes da tarefa
            task_details = self.find_task_by_id(task_id)
            if task_details:
                print(f"{i:2d}. {task_id}: {task_details['name']}")
                print(f"    👤 {task_details['assignee']} | 📅 {task_details['estimated_days']} dias")
            else:
                print(f"{i:2d}. {task_id}: Tarefa não encontrada")
        print()
    
    def find_task_by_id(self, task_id: str) -> Dict[str, Any]:
        """Encontra tarefa por ID"""
        for phase in self.taskmash['taskmash']['phases']:
            for task in phase['tasks']:
                if task['id'] == task_id:
                    return task
        return {}
    
    def print_next_actions(self):
        """Imprime próximas ações recomendadas"""
        print("\n🎯 PRÓXIMAS AÇÕES RECOMENDADAS")
        print("=" * 50)
        
        next_tasks = self.get_next_tasks()
        if not next_tasks:
            print("✅ Nenhuma tarefa crítica pendente!")
            return
        
        print("🔴 TAREFAS CRÍTICAS PRIORITÁRIAS:")
        for i, task in enumerate(next_tasks[:5], 1):  # Top 5
            print(f"{i}. {task['id']}: {task['name']}")
            print(f"   👤 {task['assignee']} | 📅 {task['estimated_days']} dias")
            print(f"   📋 {task['criteria']}")
            print()
    
    def print_risks(self):
        """Imprime riscos identificados"""
        print("\n⚠️ RISCOS IDENTIFICADOS")
        print("=" * 50)
        
        risks = self.taskmash['taskmash']['risks']
        for risk in risks:
            level_icon = "🔴" if risk['level'] == 'ALTO' else "🟡" if risk['level'] == 'MEDIO' else "🟢"
            print(f"{level_icon} {risk['name']} ({risk['level']})")
            print(f"   🛡️ Mitigação: {risk['mitigation']}")
            print(f"   👤 Responsável: {risk['responsible']}")
            print(f"   📅 Timeline: {risk['timeline']}")
            print()
    
    def print_success_metrics(self):
        """Imprime métricas de sucesso"""
        print("\n📊 MÉTRICAS DE SUCESSO")
        print("=" * 50)
        
        metrics = self.taskmash['taskmash']['success_metrics']
        for phase, phase_metrics in metrics.items():
            print(f"\n🎯 {phase.upper()}:")
            for metric, value in phase_metrics.items():
                print(f"   • {metric}: {value}")
    
    def print_full_report(self):
        """Imprime relatório completo"""
        print("🎯 GUARDFLOW - TASKMASH SUPER ESCOPO")
        print("=" * 60)
        print(f"📅 Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📋 Total de fases: {len(self.taskmash['taskmash']['phases'])}")
        
        # Resumo por fase
        for phase in self.taskmash['taskmash']['phases']:
            self.print_phase_summary(phase['id'])
        
        # Caminho crítico
        self.print_critical_path()
        
        # Próximas ações
        self.print_next_actions()
        
        # Riscos
        self.print_risks()
        
        # Métricas de sucesso
        self.print_success_metrics()
        
        print("\n" + "=" * 60)
        print("🚀 GuardFlow - Execução Sistemática e Orientada a Resultados")
    
    def execute_task(self, task_id: str):
        """Executa uma tarefa específica"""
        task = self.find_task_by_id(task_id)
        if not task:
            print(f"❌ Tarefa {task_id} não encontrada!")
            return
        
        print(f"\n🚀 EXECUTANDO: {task_id}")
        print(f"📋 {task['name']}")
        print(f"👤 Responsável: {task['assignee']}")
        print(f"📅 Estimativa: {task['estimated_days']} dias")
        print(f"📊 Critérios: {task['criteria']}")
        
        # Aqui seria implementada a lógica específica de execução
        print("\n✅ Tarefa iniciada! Acompanhe o progresso no sistema de tracking.")

def main():
    """Função principal"""
    if len(sys.argv) < 2:
        print("🎯 GuardFlow Taskmash Executor")
        print("=" * 40)
        print("Uso:")
        print("  python scripts/execute_taskmash.py report     # Relatório completo")
        print("  python scripts/execute_taskmash.py phase <id> # Resumo de fase")
        print("  python scripts/execute_taskmash.py next       # Próximas ações")
        print("  python scripts/execute_taskmash.py critical   # Caminho crítico")
        print("  python scripts/execute_taskmash.py execute <task_id> # Executar tarefa")
        return
    
    executor = TaskmashExecutor()
    command = sys.argv[1]
    
    if command == "report":
        executor.print_full_report()
    elif command == "phase" and len(sys.argv) > 2:
        executor.print_phase_summary(sys.argv[2])
    elif command == "next":
        executor.print_next_actions()
    elif command == "critical":
        executor.print_critical_path()
    elif command == "execute" and len(sys.argv) > 2:
        executor.execute_task(sys.argv[2])
    else:
        print("❌ Comando inválido!")
        print("Use: python scripts/execute_taskmash.py report")

if __name__ == "__main__":
    main()
