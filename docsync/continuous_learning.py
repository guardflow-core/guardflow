#!/usr/bin/env python3
"""
🧠 ESG Token Ecosystem - Continuous Learning System
Sistema de Aprendizado Contínuo para Melhoria da Organização
"""

import os
import json
import yaml
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Tuple
import logging
from collections import defaultdict, Counter
import hashlib
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('continuous_learning.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ContinuousLearningSystem:
    """Sistema de Aprendizado Contínuo ESG Token Ecosystem"""
    
    def __init__(self, learning_data_path: str = "learning_data.json"):
        self.learning_data_path = learning_data_path
        self.learning_data = self.load_learning_data()
        self.patterns_learned = defaultdict(list)
        self.optimization_history = []
        self.success_metrics = {}
        
    def load_learning_data(self) -> Dict[str, Any]:
        """Carrega dados de aprendizado"""
        if Path(self.learning_data_path).exists():
            try:
                with open(self.learning_data_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"⚠️ Erro ao carregar dados de aprendizado: {e}")
        
        return {
            'file_patterns': {},
            'directory_structures': {},
            'content_patterns': {},
            'optimization_history': [],
            'success_metrics': {},
            'learning_models': {},
            'adaptation_rules': []
        }
    
    def save_learning_data(self):
        """Salva dados de aprendizado"""
        try:
            with open(self.learning_data_path, 'w', encoding='utf-8') as f:
                json.dump(self.learning_data, f, indent=2, ensure_ascii=False)
            logger.info("💾 Dados de aprendizado salvos")
        except Exception as e:
            logger.error(f"❌ Erro ao salvar dados de aprendizado: {e}")
    
    def analyze_historical_patterns(self) -> Dict[str, Any]:
        """Analisa padrões históricos"""
        logger.info("📊 Analisando padrões históricos...")
        
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'file_pattern_evolution': {},
            'directory_structure_evolution': {},
            'content_evolution': {},
            'optimization_effectiveness': {},
            'learning_insights': []
        }
        
        # Análise de evolução de padrões de arquivos
        if 'file_patterns' in self.learning_data:
            analysis['file_pattern_evolution'] = self.analyze_file_pattern_evolution()
        
        # Análise de evolução de estrutura de diretórios
        if 'directory_structures' in self.learning_data:
            analysis['directory_structure_evolution'] = self.analyze_directory_evolution()
        
        # Análise de evolução de conteúdo
        if 'content_patterns' in self.learning_data:
            analysis['content_evolution'] = self.analyze_content_evolution()
        
        # Análise de efetividade de otimizações
        if 'optimization_history' in self.learning_data:
            analysis['optimization_effectiveness'] = self.analyze_optimization_effectiveness()
        
        # Gerar insights de aprendizado
        analysis['learning_insights'] = self.generate_learning_insights(analysis)
        
        return analysis
    
    def analyze_file_pattern_evolution(self) -> Dict[str, Any]:
        """Analisa evolução de padrões de arquivos"""
        evolution = {
            'naming_conventions': Counter(),
            'file_types': Counter(),
            'directory_depth_trends': [],
            'organization_improvements': []
        }
        
        file_patterns = self.learning_data.get('file_patterns', {})
        
        for timestamp, patterns in file_patterns.items():
            # Analisar convenções de nomenclatura
            for pattern in patterns.get('naming_conventions', []):
                evolution['naming_conventions'][pattern] += 1
            
            # Analisar tipos de arquivos
            for file_type, count in patterns.get('file_types', {}).items():
                evolution['file_types'][file_type] += count
            
            # Analisar tendências de profundidade
            depth = patterns.get('average_depth', 0)
            evolution['directory_depth_trends'].append({
                'timestamp': timestamp,
                'depth': depth
            })
        
        return evolution
    
    def analyze_directory_evolution(self) -> Dict[str, Any]:
        """Analisa evolução de estrutura de diretórios"""
        evolution = {
            'structure_complexity': [],
            'organization_scores': [],
            'optimization_impact': []
        }
        
        directory_structures = self.learning_data.get('directory_structures', {})
        
        for timestamp, structure in directory_structures.items():
            # Analisar complexidade da estrutura
            complexity = self.calculate_structure_complexity(structure)
            evolution['structure_complexity'].append({
                'timestamp': timestamp,
                'complexity': complexity
            })
            
            # Analisar scores de organização
            if 'organization_score' in structure:
                evolution['organization_scores'].append({
                    'timestamp': timestamp,
                    'score': structure['organization_score']
                })
        
        return evolution
    
    def analyze_content_evolution(self) -> Dict[str, Any]:
        """Analisa evolução de conteúdo"""
        evolution = {
            'esg_keywords_trends': Counter(),
            'documentation_quality_trends': [],
            'technical_terms_evolution': Counter(),
            'content_consistency_improvements': []
        }
        
        content_patterns = self.learning_data.get('content_patterns', {})
        
        for timestamp, patterns in content_patterns.items():
            # Analisar tendências de palavras-chave ESG
            for keyword, count in patterns.get('esg_keywords', {}).items():
                evolution['esg_keywords_trends'][keyword] += count
            
            # Analisar evolução da qualidade da documentação
            if 'documentation_quality' in patterns:
                evolution['documentation_quality_trends'].append({
                    'timestamp': timestamp,
                    'quality': patterns['documentation_quality']
                })
            
            # Analisar evolução de termos técnicos
            for term, count in patterns.get('technical_terms', {}).items():
                evolution['technical_terms_evolution'][term] += count
        
        return evolution
    
    def analyze_optimization_effectiveness(self) -> Dict[str, Any]:
        """Analisa efetividade das otimizações"""
        effectiveness = {
            'success_rate': 0.0,
            'improvement_trends': [],
            'failed_optimizations': [],
            'best_practices': []
        }
        
        optimization_history = self.learning_data.get('optimization_history', [])
        
        if not optimization_history:
            return effectiveness
        
        # Calcular taxa de sucesso
        successful_optimizations = 0
        total_optimizations = len(optimization_history)
        
        for optimization in optimization_history:
            if optimization.get('success', False):
                successful_optimizations += 1
            else:
                effectiveness['failed_optimizations'].append(optimization)
        
        effectiveness['success_rate'] = successful_optimizations / total_optimizations if total_optimizations > 0 else 0
        
        # Analisar tendências de melhoria
        for optimization in optimization_history:
            if 'improvement_score' in optimization:
                effectiveness['improvement_trends'].append({
                    'timestamp': optimization.get('timestamp', ''),
                    'score': optimization['improvement_score']
                })
        
        # Identificar melhores práticas
        effectiveness['best_practices'] = self.identify_best_practices(optimization_history)
        
        return effectiveness
    
    def generate_learning_insights(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Gera insights de aprendizado"""
        insights = []
        
        # Insight sobre padrões de nomenclatura
        naming_conventions = analysis.get('file_pattern_evolution', {}).get('naming_conventions', Counter())
        if naming_conventions:
            most_common = naming_conventions.most_common(1)[0]
            insights.append({
                'type': 'naming_convention',
                'insight': f"Padrão de nomenclatura mais comum: {most_common[0]} ({most_common[1]} ocorrências)",
                'recommendation': f"Padronizar nomenclatura usando {most_common[0]}",
                'confidence': min(most_common[1] / sum(naming_conventions.values()), 1.0)
            })
        
        # Insight sobre tipos de arquivos
        file_types = analysis.get('file_pattern_evolution', {}).get('file_types', Counter())
        if file_types:
            most_common_type = file_types.most_common(1)[0]
            insights.append({
                'type': 'file_type_distribution',
                'insight': f"Tipo de arquivo mais comum: {most_common_type[0]} ({most_common_type[1]} arquivos)",
                'recommendation': f"Otimizar estrutura para {most_common_type[0]}",
                'confidence': min(most_common_type[1] / sum(file_types.values()), 1.0)
            })
        
        # Insight sobre efetividade de otimizações
        optimization_effectiveness = analysis.get('optimization_effectiveness', {})
        success_rate = optimization_effectiveness.get('success_rate', 0)
        
        if success_rate > 0.8:
            insights.append({
                'type': 'optimization_success',
                'insight': f"Taxa de sucesso das otimizações: {success_rate:.1%}",
                'recommendation': "Continuar com estratégias atuais de otimização",
                'confidence': success_rate
            })
        elif success_rate < 0.5:
            insights.append({
                'type': 'optimization_improvement',
                'insight': f"Taxa de sucesso das otimizações: {success_rate:.1%}",
                'recommendation': "Revisar e melhorar estratégias de otimização",
                'confidence': 1.0 - success_rate
            })
        
        return insights
    
    def identify_best_practices(self, optimization_history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identifica melhores práticas"""
        best_practices = []
        
        # Agrupar otimizações por tipo
        optimization_types = defaultdict(list)
        for optimization in optimization_history:
            if optimization.get('success', False):
                opt_type = optimization.get('type', 'unknown')
                optimization_types[opt_type].append(optimization)
        
        # Identificar práticas mais bem-sucedidas
        for opt_type, optimizations in optimization_types.items():
            if len(optimizations) >= 3:  # Pelo menos 3 otimizações bem-sucedidas
                avg_improvement = np.mean([opt.get('improvement_score', 0) for opt in optimizations])
                
                best_practices.append({
                    'type': opt_type,
                    'success_count': len(optimizations),
                    'average_improvement': avg_improvement,
                    'recommendation': f"Continuar usando estratégias de {opt_type}",
                    'confidence': min(len(optimizations) / 10, 1.0)
                })
        
        return best_practices
    
    def calculate_structure_complexity(self, structure: Dict[str, Any]) -> float:
        """Calcula complexidade da estrutura"""
        complexity = 0.0
        
        # Fator de profundidade
        max_depth = structure.get('max_depth', 0)
        complexity += max_depth * 0.1
        
        # Fator de número de diretórios
        total_dirs = structure.get('total_directories', 0)
        complexity += total_dirs * 0.01
        
        # Fator de número de arquivos
        total_files = structure.get('total_files', 0)
        complexity += total_files * 0.001
        
        # Fator de diversidade de tipos
        file_types = structure.get('file_types', {})
        type_diversity = len(file_types)
        complexity += type_diversity * 0.05
        
        return min(complexity, 10.0)  # Cap em 10
    
    def learn_from_patterns(self, current_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Aprende com padrões atuais"""
        logger.info("🧠 Aprendendo com padrões atuais...")
        
        learning_insights = {
            'timestamp': datetime.now().isoformat(),
            'new_patterns_discovered': [],
            'pattern_improvements': [],
            'adaptation_suggestions': []
        }
        
        # Aprender padrões de arquivos
        file_patterns = self.extract_file_patterns(current_analysis)
        learning_insights['new_patterns_discovered'].extend(file_patterns)
        
        # Aprender padrões de diretórios
        directory_patterns = self.extract_directory_patterns(current_analysis)
        learning_insights['new_patterns_discovered'].extend(directory_patterns)
        
        # Aprender padrões de conteúdo
        content_patterns = self.extract_content_patterns(current_analysis)
        learning_insights['new_patterns_discovered'].extend(content_patterns)
        
        # Gerar sugestões de adaptação
        learning_insights['adaptation_suggestions'] = self.generate_adaptation_suggestions(learning_insights)
        
        # Atualizar dados de aprendizado
        self.update_learning_data(learning_insights)
        
        return learning_insights
    
    def extract_file_patterns(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extrai padrões de arquivos"""
        patterns = []
        
        for dir_name, dir_analysis in analysis.get('directories', {}).items():
            # Padrões de nomenclatura
            naming_conventions = dir_analysis.get('naming_conventions', [])
            if naming_conventions:
                most_common = Counter(naming_conventions).most_common(1)[0]
                patterns.append({
                    'type': 'naming_convention',
                    'directory': dir_name,
                    'pattern': most_common[0],
                    'frequency': most_common[1],
                    'confidence': most_common[1] / len(naming_conventions)
                })
            
            # Padrões de tipos de arquivos
            file_types = dir_analysis.get('file_types', Counter())
            if file_types:
                most_common_type = file_types.most_common(1)[0]
                patterns.append({
                    'type': 'file_type',
                    'directory': dir_name,
                    'pattern': most_common_type[0],
                    'frequency': most_common_type[1],
                    'confidence': most_common_type[1] / sum(file_types.values())
                })
        
        return patterns
    
    def extract_directory_patterns(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extrai padrões de diretórios"""
        patterns = []
        
        for dir_name, dir_analysis in analysis.get('directories', {}).items():
            # Padrões de organização
            org_score = dir_analysis.get('organization_score', 0)
            patterns.append({
                'type': 'organization_score',
                'directory': dir_name,
                'pattern': f"score_{org_score}",
                'value': org_score,
                'confidence': org_score / 100
            })
            
            # Padrões de profundidade
            depth_levels = dir_analysis.get('depth_levels', [])
            if depth_levels:
                avg_depth = np.mean(depth_levels)
                patterns.append({
                    'type': 'depth_pattern',
                    'directory': dir_name,
                    'pattern': f"avg_depth_{avg_depth:.1f}",
                    'value': avg_depth,
                    'confidence': 1.0 if len(depth_levels) > 5 else 0.5
                })
        
        return patterns
    
    def extract_content_patterns(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extrai padrões de conteúdo"""
        patterns = []
        
        for dir_name, content_analysis in analysis.get('content_analysis', {}).items():
            # Padrões de palavras-chave ESG
            esg_keywords = content_analysis.get('esg_keywords', Counter())
            if esg_keywords:
                most_common = esg_keywords.most_common(1)[0]
                patterns.append({
                    'type': 'esg_keyword',
                    'directory': dir_name,
                    'pattern': most_common[0],
                    'frequency': most_common[1],
                    'confidence': most_common[1] / sum(esg_keywords.values())
                })
            
            # Padrões de qualidade de documentação
            doc_quality = content_analysis.get('documentation_quality', {})
            if doc_quality:
                avg_quality = np.mean(list(doc_quality.values()))
                patterns.append({
                    'type': 'documentation_quality',
                    'directory': dir_name,
                    'pattern': f"quality_{avg_quality:.1f}",
                    'value': avg_quality,
                    'confidence': 1.0 if len(doc_quality) > 3 else 0.5
                })
        
        return patterns
    
    def generate_adaptation_suggestions(self, learning_insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Gera sugestões de adaptação"""
        suggestions = []
        
        new_patterns = learning_insights.get('new_patterns_discovered', [])
        
        # Agrupar padrões por tipo
        pattern_groups = defaultdict(list)
        for pattern in new_patterns:
            pattern_groups[pattern['type']].append(pattern)
        
        # Gerar sugestões baseadas em padrões
        for pattern_type, patterns in pattern_groups.items():
            if len(patterns) >= 2:  # Pelo menos 2 padrões do mesmo tipo
                # Calcular confiança média
                avg_confidence = np.mean([p['confidence'] for p in patterns])
                
                if avg_confidence > 0.7:
                    suggestions.append({
                        'type': f'standardize_{pattern_type}',
                        'description': f"Padronizar {pattern_type} baseado em padrões identificados",
                        'confidence': avg_confidence,
                        'patterns': patterns,
                        'action': f"Implementar padrão mais comum para {pattern_type}"
                    })
        
        return suggestions
    
    def update_learning_data(self, learning_insights: Dict[str, Any]):
        """Atualiza dados de aprendizado"""
        timestamp = learning_insights['timestamp']
        
        # Atualizar padrões de arquivos
        if 'file_patterns' not in self.learning_data:
            self.learning_data['file_patterns'] = {}
        
        self.learning_data['file_patterns'][timestamp] = {
            'patterns': learning_insights['new_patterns_discovered'],
            'suggestions': learning_insights['adaptation_suggestions']
        }
        
        # Atualizar histórico de otimização
        if 'optimization_history' not in self.learning_data:
            self.learning_data['optimization_history'] = []
        
        self.learning_data['optimization_history'].append({
            'timestamp': timestamp,
            'type': 'learning_cycle',
            'insights': learning_insights,
            'success': True
        })
        
        # Salvar dados atualizados
        self.save_learning_data()
    
    def predict_optimal_structure(self, current_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Prediz estrutura ótima baseada no aprendizado"""
        logger.info("🔮 Predizendo estrutura ótima...")
        
        prediction = {
            'timestamp': datetime.now().isoformat(),
            'predicted_improvements': [],
            'confidence_scores': {},
            'implementation_plan': []
        }
        
        # Analisar padrões históricos
        historical_analysis = self.analyze_historical_patterns()
        
        # Predizer melhorias baseadas em padrões bem-sucedidos
        best_practices = historical_analysis.get('optimization_effectiveness', {}).get('best_practices', [])
        
        for practice in best_practices:
            if practice['confidence'] > 0.8:
                prediction['predicted_improvements'].append({
                    'type': practice['type'],
                    'expected_improvement': practice['average_improvement'],
                    'confidence': practice['confidence'],
                    'description': practice['recommendation']
                })
        
        # Gerar plano de implementação
        prediction['implementation_plan'] = self.generate_implementation_plan(prediction['predicted_improvements'])
        
        return prediction
    
    def generate_implementation_plan(self, improvements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Gera plano de implementação"""
        plan = []
        
        # Ordenar melhorias por confiança e impacto esperado
        sorted_improvements = sorted(improvements, key=lambda x: x['confidence'] * x['expected_improvement'], reverse=True)
        
        for i, improvement in enumerate(sorted_improvements[:5]):  # Top 5 melhorias
            plan.append({
                'step': i + 1,
                'action': improvement['description'],
                'type': improvement['type'],
                'priority': 'high' if improvement['confidence'] > 0.9 else 'medium',
                'expected_impact': improvement['expected_improvement'],
                'confidence': improvement['confidence']
            })
        
        return plan
    
    def run_continuous_learning_cycle(self, current_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Executa ciclo de aprendizado contínuo"""
        logger.info("🔄 Executando ciclo de aprendizado contínuo...")
        
        # Aprender com padrões atuais
        learning_insights = self.learn_from_patterns(current_analysis)
        
        # Analisar padrões históricos
        historical_analysis = self.analyze_historical_patterns()
        
        # Predizer estrutura ótima
        optimal_structure = self.predict_optimal_structure(current_analysis)
        
        # Relatório completo
        report = {
            'timestamp': datetime.now().isoformat(),
            'learning_insights': learning_insights,
            'historical_analysis': historical_analysis,
            'optimal_structure': optimal_structure,
            'learning_effectiveness': self.calculate_learning_effectiveness(learning_insights, historical_analysis)
        }
        
        # Salvar relatório
        with open('continuous_learning_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info("✅ Ciclo de aprendizado contínuo concluído!")
        return report
    
    def calculate_learning_effectiveness(self, learning_insights: Dict[str, Any], historical_analysis: Dict[str, Any]) -> float:
        """Calcula efetividade do aprendizado"""
        # Fator de novos padrões descobertos
        new_patterns = len(learning_insights.get('new_patterns_discovered', []))
        pattern_factor = min(new_patterns / 10, 1.0)  # Normalizar para 0-1
        
        # Fator de sugestões de adaptação
        adaptation_suggestions = len(learning_insights.get('adaptation_suggestions', []))
        adaptation_factor = min(adaptation_suggestions / 5, 1.0)  # Normalizar para 0-1
        
        # Fator de análise histórica
        historical_insights = len(historical_analysis.get('learning_insights', []))
        historical_factor = min(historical_insights / 5, 1.0)  # Normalizar para 0-1
        
        # Calcular efetividade geral
        effectiveness = (pattern_factor * 0.4 + adaptation_factor * 0.3 + historical_factor * 0.3)
        
        return min(effectiveness, 1.0)

def main():
    """Função principal"""
    print("🧠 ESG Token Ecosystem - Continuous Learning System")
    print("=" * 60)
    
    # Inicializar sistema de aprendizado contínuo
    learning_system = ContinuousLearningSystem()
    
    # Simular análise atual (em produção, viria do sistema principal)
    current_analysis = {
        'directories': {
            'guardflow': {
                'organization_score': 75,
                'file_types': Counter({'.py': 10, '.md': 5, '.yaml': 3}),
                'naming_conventions': ['snake_case', 'kebab-case', 'snake_case']
            }
        },
        'content_analysis': {
            'guardflow': {
                'esg_keywords': Counter({'sustainability': 5, 'carbon': 3, 'environment': 2}),
                'documentation_quality': {'README.md': 80, 'CONTRIBUTING.md': 70}
            }
        }
    }
    
    # Executar ciclo de aprendizado contínuo
    report = learning_system.run_continuous_learning_cycle(current_analysis)
    
    print("✅ Aprendizado contínuo concluído!")
    print(f"📊 Efetividade do aprendizado: {report['learning_effectiveness']:.1%}")
    print(f"🔍 Novos padrões descobertos: {len(report['learning_insights']['new_patterns_discovered'])}")
    print(f"💡 Sugestões de adaptação: {len(report['learning_insights']['adaptation_suggestions'])}")
    print("📄 Relatório salvo em: continuous_learning_report.json")

if __name__ == "__main__":
    main()
