#!/usr/bin/env python3
"""
🧠 ESG Token Ecosystem - Adaptive Structure System
Sistema de Estrutura Adaptativa para Melhoria Contínua da Organização
"""

import os
import yaml
import json
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Tuple
import logging
from collections import defaultdict, Counter
import hashlib
import re

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('adaptive_structure.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AdaptiveStructureManager:
    """Gerenciador de Estrutura Adaptativa ESG Token Ecosystem"""
    
    def __init__(self, config_path: str = "esg-token-docsync.yaml"):
        self.config_path = config_path
        self.config = self.load_config()
        self.learning_data = self.load_learning_data()
        self.adaptation_history = []
        self.structure_patterns = defaultdict(list)
        self.optimization_suggestions = []
        
    def load_config(self) -> Dict[str, Any]:
        """Carrega configuração do docsync"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
                logger.info(f"✅ Configuração adaptativa carregada: {self.config_path}")
                return config
        except Exception as e:
            logger.error(f"❌ Erro ao carregar configuração: {e}")
            return {}
    
    def load_learning_data(self) -> Dict[str, Any]:
        """Carrega dados de aprendizado"""
        learning_file = Path("adaptive_learning.json")
        if learning_file.exists():
            try:
                with open(learning_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"⚠️ Erro ao carregar dados de aprendizado: {e}")
        return {
            'file_patterns': {},
            'directory_structures': {},
            'content_analysis': {},
            'optimization_history': [],
            'success_metrics': {}
        }
    
    def save_learning_data(self):
        """Salva dados de aprendizado"""
        try:
            learning_file = Path("adaptive_learning.json")
            with open(learning_file, 'w', encoding='utf-8') as f:
                json.dump(self.learning_data, f, indent=2, ensure_ascii=False)
            logger.info("💾 Dados de aprendizado salvos")
        except Exception as e:
            logger.error(f"❌ Erro ao salvar dados de aprendizado: {e}")
    
    def analyze_project_structure(self) -> Dict[str, Any]:
        """Analisa estrutura atual do projeto"""
        logger.info("🔍 Analisando estrutura do projeto...")
        
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'directories': {},
            'file_patterns': {},
            'content_analysis': {},
            'structure_metrics': {},
            'optimization_opportunities': []
        }
        
        directories = self.config.get('directories', {})
        
        for dir_name, dir_config in directories.items():
            if not dir_config.get('sync_enabled', False):
                continue
                
            path = Path(dir_config['path'])
            if not path.exists():
                continue
            
            logger.info(f"📁 Analisando: {dir_name}")
            
            # Análise de estrutura de diretórios
            dir_analysis = self.analyze_directory_structure(path, dir_name)
            analysis['directories'][dir_name] = dir_analysis
            
            # Análise de padrões de arquivos
            file_patterns = self.analyze_file_patterns(path, dir_config)
            analysis['file_patterns'][dir_name] = file_patterns
            
            # Análise de conteúdo
            content_analysis = self.analyze_content_patterns(path)
            analysis['content_analysis'][dir_name] = content_analysis
        
        # Análise de métricas de estrutura
        analysis['structure_metrics'] = self.calculate_structure_metrics(analysis)
        
        # Identificar oportunidades de otimização
        analysis['optimization_opportunities'] = self.identify_optimization_opportunities(analysis)
        
        return analysis
    
    def analyze_directory_structure(self, path: Path, dir_name: str) -> Dict[str, Any]:
        """Analisa estrutura de diretórios"""
        structure = {
            'total_directories': 0,
            'total_files': 0,
            'depth_levels': [],
            'file_types': Counter(),
            'directory_patterns': [],
            'naming_conventions': [],
            'organization_score': 0
        }
        
        for root, dirs, files in os.walk(path):
            level = root.replace(str(path), '').count(os.sep)
            structure['depth_levels'].append(level)
            structure['total_directories'] += len(dirs)
            structure['total_files'] += len(files)
            
            # Analisar tipos de arquivos
            for file in files:
                ext = Path(file).suffix.lower()
                structure['file_types'][ext] += 1
            
            # Analisar padrões de nomenclatura
            for dir_name in dirs:
                structure['naming_conventions'].append(self.analyze_naming_pattern(dir_name))
        
        # Calcular score de organização
        structure['organization_score'] = self.calculate_organization_score(structure)
        
        return structure
    
    def analyze_file_patterns(self, path: Path, dir_config: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa padrões de arquivos"""
        patterns = {
            'esg_files': [],
            'documentation_files': [],
            'code_files': [],
            'config_files': [],
            'pattern_violations': [],
            'optimization_suggestions': []
        }
        
        sections = dir_config.get('sections', [])
        
        for section in sections:
            section_name = section['name']
            section_patterns = section.get('patterns', [])
            
            for pattern in section_patterns:
                matching_files = list(path.rglob(pattern))
                
                for file_path in matching_files:
                    file_analysis = self.analyze_file_structure(file_path, section_name)
                    
                    # Categorizar arquivos
                    if self.is_esg_file(file_path):
                        patterns['esg_files'].append(str(file_path))
                    elif self.is_documentation_file(file_path):
                        patterns['documentation_files'].append(str(file_path))
                    elif self.is_code_file(file_path):
                        patterns['code_files'].append(str(file_path))
                    elif self.is_config_file(file_path):
                        patterns['config_files'].append(str(file_path))
                    
                    # Verificar violações de padrão
                    violations = self.check_pattern_violations(file_path, section_name)
                    if violations:
                        patterns['pattern_violations'].extend(violations)
        
        # Gerar sugestões de otimização
        patterns['optimization_suggestions'] = self.generate_file_optimization_suggestions(patterns)
        
        return patterns
    
    def analyze_content_patterns(self, path: Path) -> Dict[str, Any]:
        """Analisa padrões de conteúdo"""
        content_analysis = {
            'esg_keywords': Counter(),
            'technical_terms': Counter(),
            'documentation_quality': {},
            'consistency_issues': [],
            'improvement_suggestions': []
        }
        
        # Analisar arquivos de documentação
        doc_files = list(path.rglob("*.md")) + list(path.rglob("*.rst"))
        
        for doc_file in doc_files:
            try:
                with open(doc_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Análise de palavras-chave ESG
                esg_keywords = self.extract_esg_keywords(content)
                for keyword in esg_keywords:
                    content_analysis['esg_keywords'][keyword] += 1
                
                # Análise de termos técnicos
                tech_terms = self.extract_technical_terms(content)
                for term in tech_terms:
                    content_analysis['technical_terms'][term] += 1
                
                # Análise de qualidade da documentação
                quality_score = self.analyze_documentation_quality(content, doc_file)
                content_analysis['documentation_quality'][str(doc_file)] = quality_score
                
            except Exception as e:
                logger.warning(f"⚠️ Erro ao analisar conteúdo de {doc_file}: {e}")
        
        # Identificar problemas de consistência
        content_analysis['consistency_issues'] = self.identify_consistency_issues(content_analysis)
        
        # Gerar sugestões de melhoria
        content_analysis['improvement_suggestions'] = self.generate_content_improvement_suggestions(content_analysis)
        
        return content_analysis
    
    def calculate_structure_metrics(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula métricas de estrutura"""
        metrics = {
            'total_directories': 0,
            'total_files': 0,
            'average_organization_score': 0,
            'esg_coverage': 0,
            'documentation_quality': 0,
            'consistency_score': 0,
            'optimization_potential': 0
        }
        
        total_dirs = 0
        total_files = 0
        org_scores = []
        esg_files = 0
        total_doc_files = 0
        quality_scores = []
        
        for dir_name, dir_analysis in analysis['directories'].items():
            total_dirs += dir_analysis['total_directories']
            total_files += dir_analysis['total_files']
            org_scores.append(dir_analysis['organization_score'])
            
            # Análise ESG
            file_patterns = analysis['file_patterns'].get(dir_name, {})
            esg_files += len(file_patterns.get('esg_files', []))
            
            # Análise de documentação
            content_analysis = analysis['content_analysis'].get(dir_name, {})
            doc_quality = content_analysis.get('documentation_quality', {})
            for quality in doc_quality.values():
                quality_scores.append(quality)
        
        metrics['total_directories'] = total_dirs
        metrics['total_files'] = total_files
        metrics['average_organization_score'] = sum(org_scores) / len(org_scores) if org_scores else 0
        metrics['esg_coverage'] = (esg_files / total_files * 100) if total_files > 0 else 0
        metrics['documentation_quality'] = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        return metrics
    
    def identify_optimization_opportunities(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identifica oportunidades de otimização"""
        opportunities = []
        
        # Análise de estrutura
        for dir_name, dir_analysis in analysis['directories'].items():
            if dir_analysis['organization_score'] < 70:
                opportunities.append({
                    'type': 'structure_optimization',
                    'directory': dir_name,
                    'issue': 'Low organization score',
                    'current_score': dir_analysis['organization_score'],
                    'suggestion': 'Reorganize directory structure and naming conventions',
                    'priority': 'high' if dir_analysis['organization_score'] < 50 else 'medium'
                })
        
        # Análise de padrões de arquivos
        for dir_name, file_patterns in analysis['file_patterns'].items():
            violations = file_patterns.get('pattern_violations', [])
            if violations:
                opportunities.append({
                    'type': 'pattern_optimization',
                    'directory': dir_name,
                    'issue': f'{len(violations)} pattern violations found',
                    'violations': violations[:5],  # Primeiros 5
                    'suggestion': 'Standardize file patterns and naming conventions',
                    'priority': 'high' if len(violations) > 10 else 'medium'
                })
        
        # Análise de conteúdo
        for dir_name, content_analysis in analysis['content_analysis'].items():
            consistency_issues = content_analysis.get('consistency_issues', [])
            if consistency_issues:
                opportunities.append({
                    'type': 'content_optimization',
                    'directory': dir_name,
                    'issue': f'{len(consistency_issues)} consistency issues found',
                    'suggestion': 'Standardize documentation and improve consistency',
                    'priority': 'medium'
                })
        
        return opportunities
    
    def generate_adaptive_recommendations(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Gera recomendações adaptativas"""
        recommendations = []
        
        # Recomendações baseadas em métricas
        metrics = analysis['structure_metrics']
        
        if metrics['average_organization_score'] < 70:
            recommendations.append({
                'category': 'structure',
                'priority': 'high',
                'title': 'Improve Directory Organization',
                'description': 'Reorganize directory structure for better maintainability',
                'actions': [
                    'Create standardized directory structure',
                    'Implement consistent naming conventions',
                    'Group related files together'
                ],
                'expected_improvement': '20-30% better organization score'
            })
        
        if metrics['esg_coverage'] < 50:
            recommendations.append({
                'category': 'esg_integration',
                'priority': 'high',
                'title': 'Increase ESG Content Coverage',
                'description': 'Add more ESG-related content and documentation',
                'actions': [
                    'Create ESG-specific documentation templates',
                    'Add ESG metrics to existing files',
                    'Implement ESG validation in CI/CD'
                ],
                'expected_improvement': '40-60% better ESG coverage'
            })
        
        if metrics['documentation_quality'] < 70:
            recommendations.append({
                'category': 'documentation',
                'priority': 'medium',
                'title': 'Improve Documentation Quality',
                'description': 'Enhance documentation quality and consistency',
                'actions': [
                    'Standardize documentation format',
                    'Add missing documentation',
                    'Improve content clarity and structure'
                ],
                'expected_improvement': '25-40% better documentation quality'
            })
        
        # Recomendações baseadas em oportunidades
        for opportunity in analysis['optimization_opportunities']:
            if opportunity['priority'] == 'high':
                recommendations.append({
                    'category': 'optimization',
                    'priority': 'high',
                    'title': f"Fix {opportunity['type'].replace('_', ' ').title()}",
                    'description': opportunity['suggestion'],
                    'actions': [
                        f"Address {opportunity['issue']}",
                        "Implement automated validation",
                        "Monitor improvements"
                    ],
                    'expected_improvement': 'Significant improvement in project organization'
                })
        
        return recommendations
    
    def apply_adaptive_improvements(self, recommendations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aplica melhorias adaptativas"""
        logger.info("🔧 Aplicando melhorias adaptativas...")
        
        improvements_applied = {
            'timestamp': datetime.now().isoformat(),
            'recommendations_applied': [],
            'files_modified': [],
            'directories_created': [],
            'templates_updated': [],
            'config_updated': False
        }
        
        for recommendation in recommendations:
            if recommendation['priority'] == 'high':
                logger.info(f"🚀 Aplicando: {recommendation['title']}")
                
                try:
                    if recommendation['category'] == 'structure':
                        self.apply_structure_improvements(recommendation, improvements_applied)
                    elif recommendation['category'] == 'esg_integration':
                        self.apply_esg_improvements(recommendation, improvements_applied)
                    elif recommendation['category'] == 'documentation':
                        self.apply_documentation_improvements(recommendation, improvements_applied)
                    elif recommendation['category'] == 'optimization':
                        self.apply_optimization_improvements(recommendation, improvements_applied)
                    
                    improvements_applied['recommendations_applied'].append(recommendation['title'])
                    
                except Exception as e:
                    logger.error(f"❌ Erro ao aplicar {recommendation['title']}: {e}")
        
        # Salvar dados de aprendizado
        self.learning_data['optimization_history'].append(improvements_applied)
        self.save_learning_data()
        
        return improvements_applied
    
    def apply_structure_improvements(self, recommendation: Dict[str, Any], improvements: Dict[str, Any]):
        """Aplica melhorias de estrutura"""
        # Criar estrutura de diretórios padronizada
        standard_structure = {
            'docs/': ['README.md', 'CONTRIBUTING.md', 'CHANGELOG.md'],
            'src/': ['main.py', 'utils.py', 'config.py'],
            'tests/': ['test_main.py', 'test_utils.py'],
            'templates/': ['project/', 'integration/', 'service/'],
            'config/': ['config.yaml', 'settings.json']
        }
        
        for dir_path, files in standard_structure.items():
            dir_path_obj = Path(dir_path)
            if not dir_path_obj.exists():
                dir_path_obj.mkdir(parents=True, exist_ok=True)
                improvements['directories_created'].append(str(dir_path_obj))
                
                # Criar arquivos padrão se não existirem
                for file_name in files:
                    file_path = dir_path_obj / file_name
                    if not file_path.exists():
                        self.create_standard_file(file_path, file_name)
                        improvements['files_modified'].append(str(file_path))
    
    def apply_esg_improvements(self, recommendation: Dict[str, Any], improvements: Dict[str, Any]):
        """Aplica melhorias ESG"""
        # Criar templates ESG específicos
        esg_templates = {
            'templates/esg/': [
                'esg-metrics-template.md',
                'sustainability-report-template.md',
                'carbon-footprint-template.md'
            ]
        }
        
        for dir_path, files in esg_templates.items():
            dir_path_obj = Path(dir_path)
            dir_path_obj.mkdir(parents=True, exist_ok=True)
            improvements['directories_created'].append(str(dir_path_obj))
            
            for file_name in files:
                file_path = dir_path_obj / file_name
                if not file_path.exists():
                    self.create_esg_template(file_path, file_name)
                    improvements['files_modified'].append(str(file_path))
                    improvements['templates_updated'].append(str(file_path))
    
    def apply_documentation_improvements(self, recommendation: Dict[str, Any], improvements: Dict[str, Any]):
        """Aplica melhorias de documentação"""
        # Atualizar templates de documentação
        doc_improvements = [
            'docs/README.md',
            'docs/CONTRIBUTING.md',
            'docs/CHANGELOG.md'
        ]
        
        for doc_path in doc_improvements:
            doc_path_obj = Path(doc_path)
            if not doc_path_obj.exists():
                self.create_standard_documentation(doc_path_obj)
                improvements['files_modified'].append(str(doc_path_obj))
    
    def apply_optimization_improvements(self, recommendation: Dict[str, Any], improvements: Dict[str, Any]):
        """Aplica melhorias de otimização"""
        # Atualizar configuração do docsync
        if not improvements['config_updated']:
            self.update_docsync_config()
            improvements['config_updated'] = True
    
    def create_standard_file(self, file_path: Path, file_name: str):
        """Cria arquivo padrão"""
        if file_name == 'README.md':
            content = f"""# {file_path.parent.name}

## Visão Geral
Descrição do projeto.

## Instalação
```bash
pip install -r requirements.txt
```

## Uso
```bash
python main.py
```

## Contribuição
Veja CONTRIBUTING.md para detalhes.
"""
        elif file_name == 'config.py':
            content = """# Configurações do projeto
import os
from pathlib import Path

# Diretório base
BASE_DIR = Path(__file__).parent

# Configurações de ambiente
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Configurações ESG Token
ESG_TOKEN_CONFIG = {
    'enabled': True,
    'validation': True,
    'sync_frequency': 'realtime'
}
"""
        else:
            content = f"# {file_name}\n\nConteúdo padrão para {file_name}"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def create_esg_template(self, file_path: Path, file_name: str):
        """Cria template ESG"""
        if 'esg-metrics' in file_name:
            content = """# ESG Metrics Template

## Environmental Metrics
- Carbon Footprint: {{CARBON_FOOTPRINT}} kg CO₂
- Energy Consumption: {{ENERGY_CONSUMPTION}} kWh
- Water Usage: {{WATER_USAGE}} L
- Waste Generated: {{WASTE_GENERATED}} kg

## Social Metrics
- Employee Satisfaction: {{EMPLOYEE_SATISFACTION}}/100
- Community Impact: {{COMMUNITY_IMPACT}}/100
- Safety Score: {{SAFETY_SCORE}}/100

## Governance Metrics
- Transparency Score: {{TRANSPARENCY_SCORE}}/100
- Compliance Rate: {{COMPLIANCE_RATE}}%
- Ethics Score: {{ETHICS_SCORE}}/100
"""
        elif 'sustainability-report' in file_name:
            content = """# Sustainability Report Template

## Executive Summary
{{EXECUTIVE_SUMMARY}}

## ESG Performance
### Environmental
{{ENVIRONMENTAL_PERFORMANCE}}

### Social
{{SOCIAL_PERFORMANCE}}

### Governance
{{GOVERNANCE_PERFORMANCE}}

## Future Goals
{{FUTURE_GOALS}}
"""
        else:
            content = f"# {file_name}\n\nTemplate ESG para {file_name}"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def create_standard_documentation(self, doc_path: Path):
        """Cria documentação padrão"""
        if 'README' in doc_path.name:
            content = """# Project Documentation

## Overview
This project is part of the ESG Token Ecosystem.

## Features
- ESG Token Integration
- Sustainability Metrics
- Blockchain Integration
- AI/ML Capabilities

## Getting Started
See the main README.md for installation instructions.

## Contributing
Please read CONTRIBUTING.md for details on our code of conduct.
"""
        elif 'CONTRIBUTING' in doc_path.name:
            content = """# Contributing to ESG Token Ecosystem

## Code of Conduct
We are committed to providing a welcoming and inspiring community for all.

## How to Contribute
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Development Guidelines
- Follow PEP 8 for Python code
- Write comprehensive tests
- Update documentation
- Ensure ESG compliance
"""
        else:
            content = f"# {doc_path.name}\n\nDocumentation for {doc_path.name}"
        
        with open(doc_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def update_docsync_config(self):
        """Atualiza configuração do docsync"""
        # Adicionar configurações adaptativas
        adaptive_config = {
            'adaptive_structure': {
                'enabled': True,
                'learning_rate': 0.1,
                'optimization_frequency': 'daily',
                'auto_apply_improvements': True
            },
            'structure_optimization': {
                'min_organization_score': 70,
                'auto_reorganize': True,
                'naming_conventions': 'standardized'
            }
        }
        
        # Atualizar configuração existente
        if 'adaptive_structure' not in self.config:
            self.config['adaptive_structure'] = adaptive_config['adaptive_structure']
        
        if 'structure_optimization' not in self.config:
            self.config['structure_optimization'] = adaptive_config['structure_optimization']
        
        # Salvar configuração atualizada
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
    
    def run_adaptive_optimization(self) -> Dict[str, Any]:
        """Executa otimização adaptativa completa"""
        logger.info("🧠 Iniciando otimização adaptativa...")
        
        # Análise da estrutura atual
        analysis = self.analyze_project_structure()
        
        # Geração de recomendações
        recommendations = self.generate_adaptive_recommendations(analysis)
        
        # Aplicação de melhorias
        improvements = self.apply_adaptive_improvements(recommendations)
        
        # Relatório final
        report = {
            'timestamp': datetime.now().isoformat(),
            'analysis': analysis,
            'recommendations': recommendations,
            'improvements_applied': improvements,
            'optimization_score': self.calculate_optimization_score(analysis, improvements)
        }
        
        # Salvar relatório
        with open('adaptive_optimization_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info("✅ Otimização adaptativa concluída!")
        return report
    
    def calculate_optimization_score(self, analysis: Dict[str, Any], improvements: Dict[str, Any]) -> float:
        """Calcula score de otimização"""
        base_score = analysis['structure_metrics']['average_organization_score']
        improvements_count = len(improvements['recommendations_applied'])
        files_modified = len(improvements['files_modified'])
        
        optimization_score = base_score + (improvements_count * 5) + (files_modified * 2)
        return min(optimization_score, 100.0)
    
    # Métodos auxiliares
    def is_esg_file(self, file_path: Path) -> bool:
        """Verifica se arquivo é relacionado a ESG"""
        esg_keywords = ['esg', 'sustainability', 'carbon', 'environment', 'social', 'governance']
        return any(keyword in file_path.name.lower() for keyword in esg_keywords)
    
    def is_documentation_file(self, file_path: Path) -> bool:
        """Verifica se arquivo é documentação"""
        doc_extensions = ['.md', '.rst', '.txt', '.doc', '.docx']
        return file_path.suffix.lower() in doc_extensions
    
    def is_code_file(self, file_path: Path) -> bool:
        """Verifica se arquivo é código"""
        code_extensions = ['.py', '.js', '.ts', '.rs', '.java', '.cpp', '.c']
        return file_path.suffix.lower() in code_extensions
    
    def is_config_file(self, file_path: Path) -> bool:
        """Verifica se arquivo é configuração"""
        config_extensions = ['.yaml', '.yml', '.json', '.toml', '.ini', '.cfg']
        return file_path.suffix.lower() in config_extensions
    
    def analyze_naming_pattern(self, name: str) -> str:
        """Analisa padrão de nomenclatura"""
        if '_' in name:
            return 'snake_case'
        elif '-' in name:
            return 'kebab-case'
        elif name.isupper():
            return 'UPPER_CASE'
        elif name.islower():
            return 'lower_case'
        else:
            return 'mixed_case'
    
    def extract_esg_keywords(self, content: str) -> List[str]:
        """Extrai palavras-chave ESG do conteúdo"""
        esg_keywords = [
            'sustainability', 'environmental', 'social', 'governance',
            'carbon', 'footprint', 'emissions', 'energy', 'waste',
            'diversity', 'inclusion', 'ethics', 'transparency',
            'esg', 'sustainable', 'green', 'eco', 'climate'
        ]
        
        found_keywords = []
        content_lower = content.lower()
        for keyword in esg_keywords:
            if keyword in content_lower:
                found_keywords.append(keyword)
        
        return found_keywords
    
    def extract_technical_terms(self, content: str) -> List[str]:
        """Extrai termos técnicos do conteúdo"""
        tech_terms = [
            'api', 'database', 'blockchain', 'token', 'smart contract',
            'algorithm', 'framework', 'architecture', 'integration',
            'deployment', 'testing', 'monitoring', 'analytics'
        ]
        
        found_terms = []
        content_lower = content.lower()
        for term in tech_terms:
            if term in content_lower:
                found_terms.append(term)
        
        return found_terms
    
    def analyze_documentation_quality(self, content: str, file_path: Path) -> float:
        """Analisa qualidade da documentação"""
        score = 0.0
        
        # Verificar se tem título
        if content.startswith('#'):
            score += 20
        
        # Verificar se tem seções
        sections = content.count('#')
        score += min(sections * 5, 30)
        
        # Verificar se tem código
        if '```' in content:
            score += 15
        
        # Verificar se tem links
        if '[' in content and ']' in content:
            score += 10
        
        # Verificar tamanho
        if len(content) > 500:
            score += 15
        elif len(content) > 200:
            score += 10
        
        # Verificar se tem estrutura
        if '##' in content:
            score += 10
        
        return min(score, 100.0)
    
    def check_pattern_violations(self, file_path: Path, section_name: str) -> List[str]:
        """Verifica violações de padrão"""
        violations = []
        
        # Verificar nomenclatura
        if '_' in file_path.name and '-' in file_path.name:
            violations.append(f"Mixed naming convention in {file_path.name}")
        
        # Verificar tamanho do nome
        if len(file_path.name) > 50:
            violations.append(f"File name too long: {file_path.name}")
        
        # Verificar caracteres especiais
        if re.search(r'[^a-zA-Z0-9._-]', file_path.name):
            violations.append(f"Special characters in file name: {file_path.name}")
        
        return violations
    
    def generate_file_optimization_suggestions(self, patterns: Dict[str, Any]) -> List[str]:
        """Gera sugestões de otimização de arquivos"""
        suggestions = []
        
        if len(patterns['pattern_violations']) > 5:
            suggestions.append("Standardize file naming conventions")
        
        if len(patterns['esg_files']) < len(patterns['code_files']) / 2:
            suggestions.append("Add more ESG-related documentation")
        
        if len(patterns['documentation_files']) < len(patterns['code_files']):
            suggestions.append("Improve documentation coverage")
        
        return suggestions
    
    def identify_consistency_issues(self, content_analysis: Dict[str, Any]) -> List[str]:
        """Identifica problemas de consistência"""
        issues = []
        
        # Verificar consistência de termos ESG
        esg_keywords = content_analysis['esg_keywords']
        if esg_keywords:
            most_common = esg_keywords.most_common(1)[0][0]
            for keyword, count in esg_keywords.items():
                if count < len(esg_keywords) * 0.1:  # Menos de 10% do uso
                    issues.append(f"Inconsistent use of ESG keyword: {keyword}")
        
        return issues
    
    def generate_content_improvement_suggestions(self, content_analysis: Dict[str, Any]) -> List[str]:
        """Gera sugestões de melhoria de conteúdo"""
        suggestions = []
        
        if not content_analysis['esg_keywords']:
            suggestions.append("Add ESG-related content to documentation")
        
        if content_analysis['documentation_quality']:
            avg_quality = sum(content_analysis['documentation_quality'].values()) / len(content_analysis['documentation_quality'])
            if avg_quality < 70:
                suggestions.append("Improve documentation quality and structure")
        
        return suggestions

def main():
    """Função principal"""
    print("🧠 ESG Token Ecosystem - Adaptive Structure System")
    print("=" * 60)
    
    # Inicializar gerenciador adaptativo
    manager = AdaptiveStructureManager()
    
    # Executar otimização adaptativa
    report = manager.run_adaptive_optimization()
    
    print("✅ Otimização adaptativa concluída!")
    print(f"📊 Score de otimização: {report['optimization_score']:.1f}")
    print(f"📁 Arquivos modificados: {len(report['improvements_applied']['files_modified'])}")
    print(f"📂 Diretórios criados: {len(report['improvements_applied']['directories_created'])}")
    print("📄 Relatório salvo em: adaptive_optimization_report.json")

if __name__ == "__main__":
    main()








