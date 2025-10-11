#!/usr/bin/env python3
"""
🤖 ESG Token Ecosystem - Auto Organization System
Sistema de Auto-Organização Inteligente
"""

import os
import json
import yaml
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Tuple
import logging
from collections import defaultdict, Counter
import re

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('auto_organization.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AutoOrganizationSystem:
    """Sistema de Auto-Organização ESG Token Ecosystem"""
    
    def __init__(self, config_path: str = "esg-token-docsync.yaml"):
        self.config_path = config_path
        self.config = self.load_config()
        self.organization_rules = self.load_organization_rules()
        self.auto_actions = []
        
    def load_config(self) -> Dict[str, Any]:
        """Carrega configuração"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
                logger.info(f"✅ Configuração carregada: {self.config_path}")
                return config
        except Exception as e:
            logger.error(f"❌ Erro ao carregar configuração: {e}")
            return {}
    
    def load_organization_rules(self) -> Dict[str, Any]:
        """Carrega regras de organização"""
        rules_file = Path("organization_rules.json")
        if rules_file.exists():
            try:
                with open(rules_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"⚠️ Erro ao carregar regras de organização: {e}")
        
        # Regras padrão
        return {
            'file_organization': {
                'naming_conventions': {
                    'python_files': 'snake_case',
                    'markdown_files': 'kebab-case',
                    'config_files': 'snake_case',
                    'documentation': 'UPPER_CASE'
                },
                'directory_structure': {
                    'docs': ['README.md', 'CONTRIBUTING.md', 'CHANGELOG.md'],
                    'src': ['main.py', 'utils.py', 'config.py'],
                    'tests': ['test_*.py'],
                    'templates': ['project/', 'integration/', 'service/']
                }
            },
            'esg_standards': {
                'required_files': [
                    'ESG_METRICS.md',
                    'SUSTAINABILITY_REPORT.md',
                    'CARBON_FOOTPRINT.md'
                ],
                'content_requirements': {
                    'esg_keywords': ['sustainability', 'environmental', 'social', 'governance'],
                    'documentation_quality': 70,
                    'consistency_check': True
                }
            },
            'auto_actions': {
                'create_missing_files': True,
                'standardize_naming': True,
                'organize_directories': True,
                'validate_esg_content': True,
                'update_documentation': True
            }
        }
    
    def analyze_current_organization(self) -> Dict[str, Any]:
        """Analisa organização atual"""
        logger.info("🔍 Analisando organização atual...")
        
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'organization_score': 0.0,
            'issues_found': [],
            'improvements_needed': [],
            'auto_actions_available': []
        }
        
        directories = self.config.get('directories', {})
        
        for dir_name, dir_config in directories.items():
            if not dir_config.get('sync_enabled', False):
                continue
                
            path = Path(dir_config['path'])
            if not path.exists():
                continue
            
            logger.info(f"📁 Analisando: {dir_name}")
            
            # Análise de organização
            dir_analysis = self.analyze_directory_organization(path, dir_name)
            analysis['issues_found'].extend(dir_analysis['issues'])
            analysis['improvements_needed'].extend(dir_analysis['improvements'])
            analysis['auto_actions_available'].extend(dir_analysis['auto_actions'])
        
        # Calcular score de organização
        analysis['organization_score'] = self.calculate_organization_score(analysis)
        
        return analysis
    
    def analyze_directory_organization(self, path: Path, dir_name: str) -> Dict[str, Any]:
        """Analisa organização de diretório"""
        analysis = {
            'issues': [],
            'improvements': [],
            'auto_actions': []
        }
        
        # Verificar estrutura de diretórios
        structure_issues = self.check_directory_structure(path, dir_name)
        analysis['issues'].extend(structure_issues)
        
        # Verificar nomenclatura de arquivos
        naming_issues = self.check_file_naming(path, dir_name)
        analysis['issues'].extend(naming_issues)
        
        # Verificar arquivos ESG obrigatórios
        esg_issues = self.check_esg_requirements(path, dir_name)
        analysis['issues'].extend(esg_issues)
        
        # Verificar qualidade da documentação
        doc_issues = self.check_documentation_quality(path, dir_name)
        analysis['issues'].extend(doc_issues)
        
        # Gerar ações automáticas
        analysis['auto_actions'] = self.generate_auto_actions(analysis['issues'], path, dir_name)
        
        return analysis
    
    def check_directory_structure(self, path: Path, dir_name: str) -> List[Dict[str, Any]]:
        """Verifica estrutura de diretórios"""
        issues = []
        
        # Verificar diretórios padrão
        standard_dirs = self.organization_rules['file_organization']['directory_structure']
        
        for std_dir, files in standard_dirs.items():
            dir_path = path / std_dir
            if not dir_path.exists():
                issues.append({
                    'type': 'missing_directory',
                    'path': str(dir_path),
                    'severity': 'medium',
                    'description': f"Diretório padrão ausente: {std_dir}",
                    'auto_fix': True
                })
            else:
                # Verificar arquivos obrigatórios
                for file_name in files:
                    if not file_name.endswith('/'):  # Não é diretório
                        file_path = dir_path / file_name
                        if not file_path.exists():
                            issues.append({
                                'type': 'missing_file',
                                'path': str(file_path),
                                'severity': 'low',
                                'description': f"Arquivo padrão ausente: {file_name}",
                                'auto_fix': True
                            })
        
        return issues
    
    def check_file_naming(self, path: Path, dir_name: str) -> List[Dict[str, Any]]:
        """Verifica nomenclatura de arquivos"""
        issues = []
        
        naming_conventions = self.organization_rules['file_organization']['naming_conventions']
        
        for file_path in path.rglob('*'):
            if file_path.is_file():
                file_name = file_path.name
                file_ext = file_path.suffix.lower()
                
                # Determinar convenção esperada
                expected_convention = None
                if file_ext == '.py':
                    expected_convention = naming_conventions['python_files']
                elif file_ext in ['.md', '.rst']:
                    expected_convention = naming_conventions['markdown_files']
                elif file_ext in ['.yaml', '.yml', '.json']:
                    expected_convention = naming_conventions['config_files']
                
                if expected_convention:
                    # Verificar se segue a convenção
                    if not self.follows_naming_convention(file_name, expected_convention):
                        issues.append({
                            'type': 'naming_convention',
                            'path': str(file_path),
                            'severity': 'low',
                            'description': f"Arquivo não segue convenção {expected_convention}: {file_name}",
                            'auto_fix': True,
                            'expected_convention': expected_convention
                        })
        
        return issues
    
    def check_esg_requirements(self, path: Path, dir_name: str) -> List[Dict[str, Any]]:
        """Verifica requisitos ESG"""
        issues = []
        
        required_files = self.organization_rules['esg_standards']['required_files']
        
        for required_file in required_files:
            file_path = path / required_file
            if not file_path.exists():
                issues.append({
                    'type': 'missing_esg_file',
                    'path': str(file_path),
                    'severity': 'high',
                    'description': f"Arquivo ESG obrigatório ausente: {required_file}",
                    'auto_fix': True
                })
        
        # Verificar conteúdo ESG em arquivos existentes
        esg_content_issues = self.check_esg_content(path)
        issues.extend(esg_content_issues)
        
        return issues
    
    def check_esg_content(self, path: Path) -> List[Dict[str, Any]]:
        """Verifica conteúdo ESG"""
        issues = []
        
        esg_keywords = self.organization_rules['esg_standards']['content_requirements']['esg_keywords']
        
        # Verificar arquivos de documentação
        doc_files = list(path.rglob('*.md')) + list(path.rglob('*.rst'))
        
        for doc_file in doc_files:
            try:
                with open(doc_file, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                
                # Verificar se contém palavras-chave ESG
                esg_found = any(keyword in content for keyword in esg_keywords)
                if not esg_found:
                    issues.append({
                        'type': 'missing_esg_content',
                        'path': str(doc_file),
                        'severity': 'medium',
                        'description': f"Arquivo de documentação sem conteúdo ESG: {doc_file.name}",
                        'auto_fix': True
                    })
                    
            except Exception as e:
                logger.warning(f"⚠️ Erro ao verificar conteúdo ESG em {doc_file}: {e}")
        
        return issues
    
    def check_documentation_quality(self, path: Path, dir_name: str) -> List[Dict[str, Any]]:
        """Verifica qualidade da documentação"""
        issues = []
        
        min_quality = self.organization_rules['esg_standards']['content_requirements']['documentation_quality']
        
        doc_files = list(path.rglob('*.md')) + list(path.rglob('*.rst'))
        
        for doc_file in doc_files:
            try:
                with open(doc_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                quality_score = self.calculate_documentation_quality(content)
                
                if quality_score < min_quality:
                    issues.append({
                        'type': 'low_documentation_quality',
                        'path': str(doc_file),
                        'severity': 'medium',
                        'description': f"Qualidade da documentação baixa ({quality_score}/100): {doc_file.name}",
                        'auto_fix': True,
                        'current_quality': quality_score,
                        'target_quality': min_quality
                    })
                    
            except Exception as e:
                logger.warning(f"⚠️ Erro ao verificar qualidade da documentação em {doc_file}: {e}")
        
        return issues
    
    def generate_auto_actions(self, issues: List[Dict[str, Any]], path: Path, dir_name: str) -> List[Dict[str, Any]]:
        """Gera ações automáticas"""
        actions = []
        
        for issue in issues:
            if issue.get('auto_fix', False):
                action = self.create_auto_action(issue, path, dir_name)
                if action:
                    actions.append(action)
        
        return actions
    
    def create_auto_action(self, issue: Dict[str, Any], path: Path, dir_name: str) -> Dict[str, Any]:
        """Cria ação automática para um problema"""
        action = {
            'type': issue['type'],
            'path': issue['path'],
            'description': issue['description'],
            'severity': issue['severity'],
            'auto_fixable': True,
            'fix_action': None,
            'fix_content': None
        }
        
        if issue['type'] == 'missing_directory':
            action['fix_action'] = 'create_directory'
            action['fix_content'] = {
                'directory_path': issue['path'],
                'create_standard_files': True
            }
        
        elif issue['type'] == 'missing_file':
            action['fix_action'] = 'create_file'
            action['fix_content'] = {
                'file_path': issue['path'],
                'template': self.get_file_template(Path(issue['path']).name)
            }
        
        elif issue['type'] == 'naming_convention':
            action['fix_action'] = 'rename_file'
            action['fix_content'] = {
                'current_path': issue['path'],
                'new_name': self.generate_correct_name(Path(issue['path']), issue['expected_convention'])
            }
        
        elif issue['type'] == 'missing_esg_file':
            action['fix_action'] = 'create_esg_file'
            action['fix_content'] = {
                'file_path': issue['path'],
                'esg_template': self.get_esg_template(Path(issue['path']).name)
            }
        
        elif issue['type'] == 'missing_esg_content':
            action['fix_action'] = 'add_esg_content'
            action['fix_content'] = {
                'file_path': issue['path'],
                'esg_content': self.generate_esg_content()
            }
        
        elif issue['type'] == 'low_documentation_quality':
            action['fix_action'] = 'improve_documentation'
            action['fix_content'] = {
                'file_path': issue['path'],
                'improvements': self.generate_documentation_improvements(issue['current_quality'], issue['target_quality'])
            }
        
        return action
    
    def execute_auto_organization(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Executa auto-organização"""
        logger.info("🤖 Executando auto-organização...")
        
        execution_report = {
            'timestamp': datetime.now().isoformat(),
            'actions_executed': [],
            'actions_failed': [],
            'files_created': [],
            'files_modified': [],
            'directories_created': [],
            'improvements_applied': []
        }
        
        # Executar ações automáticas
        for dir_name, dir_config in self.config.get('directories', {}).items():
            if not dir_config.get('sync_enabled', False):
                continue
                
            path = Path(dir_config['path'])
            if not path.exists():
                continue
            
            logger.info(f"🔧 Aplicando auto-organização em: {dir_name}")
            
            # Analisar e executar ações
            dir_analysis = self.analyze_directory_organization(path, dir_name)
            
            for action in dir_analysis['auto_actions']:
                try:
                    result = self.execute_auto_action(action, path)
                    if result['success']:
                        execution_report['actions_executed'].append(action)
                        execution_report['files_created'].extend(result.get('files_created', []))
                        execution_report['files_modified'].extend(result.get('files_modified', []))
                        execution_report['directories_created'].extend(result.get('directories_created', []))
                    else:
                        execution_report['actions_failed'].append({
                            'action': action,
                            'error': result.get('error', 'Unknown error')
                        })
                        
                except Exception as e:
                    logger.error(f"❌ Erro ao executar ação {action['type']}: {e}")
                    execution_report['actions_failed'].append({
                        'action': action,
                        'error': str(e)
                    })
        
        # Calcular melhorias aplicadas
        execution_report['improvements_applied'] = self.calculate_improvements_applied(execution_report)
        
        # Salvar relatório
        with open('auto_organization_report.json', 'w', encoding='utf-8') as f:
            json.dump(execution_report, f, indent=2, ensure_ascii=False)
        
        logger.info("✅ Auto-organização concluída!")
        return execution_report
    
    def execute_auto_action(self, action: Dict[str, Any], base_path: Path) -> Dict[str, Any]:
        """Executa uma ação automática"""
        result = {
            'success': False,
            'files_created': [],
            'files_modified': [],
            'directories_created': []
        }
        
        try:
            if action['fix_action'] == 'create_directory':
                dir_path = Path(action['fix_content']['directory_path'])
                dir_path.mkdir(parents=True, exist_ok=True)
                result['directories_created'].append(str(dir_path))
                
                # Criar arquivos padrão se necessário
                if action['fix_content'].get('create_standard_files', False):
                    self.create_standard_directory_files(dir_path)
                
                result['success'] = True
            
            elif action['fix_action'] == 'create_file':
                file_path = Path(action['fix_content']['file_path'])
                template = action['fix_content']['template']
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(template)
                
                result['files_created'].append(str(file_path))
                result['success'] = True
            
            elif action['fix_action'] == 'rename_file':
                current_path = Path(action['fix_content']['current_path'])
                new_name = action['fix_content']['new_name']
                new_path = current_path.parent / new_name
                
                current_path.rename(new_path)
                result['files_modified'].append(str(new_path))
                result['success'] = True
            
            elif action['fix_action'] == 'create_esg_file':
                file_path = Path(action['fix_content']['file_path'])
                esg_template = action['fix_content']['esg_template']
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(esg_template)
                
                result['files_created'].append(str(file_path))
                result['success'] = True
            
            elif action['fix_action'] == 'add_esg_content':
                file_path = Path(action['fix_content']['file_path'])
                esg_content = action['fix_content']['esg_content']
                
                # Adicionar conteúdo ESG ao arquivo existente
                with open(file_path, 'a', encoding='utf-8') as f:
                    f.write(f"\n\n{esg_content}")
                
                result['files_modified'].append(str(file_path))
                result['success'] = True
            
            elif action['fix_action'] == 'improve_documentation':
                file_path = Path(action['fix_content']['file_path'])
                improvements = action['fix_content']['improvements']
                
                # Aplicar melhorias na documentação
                self.apply_documentation_improvements(file_path, improvements)
                result['files_modified'].append(str(file_path))
                result['success'] = True
            
        except Exception as e:
            result['error'] = str(e)
            logger.error(f"❌ Erro ao executar ação {action['fix_action']}: {e}")
        
        return result
    
    def create_standard_directory_files(self, dir_path: Path):
        """Cria arquivos padrão em diretório"""
        standard_files = {
            'README.md': """# {dir_name}

## Visão Geral
Descrição do diretório.

## Estrutura
- Arquivos principais
- Documentação
- Configurações

## Uso
Instruções de uso específicas do diretório.
""".format(dir_name=dir_path.name),
            'CONTRIBUTING.md': """# Contribuindo para {dir_name}

## Diretrizes
- Seguir padrões de código
- Documentar mudanças
- Testar alterações

## Processo
1. Fork do repositório
2. Criar branch de feature
3. Fazer mudanças
4. Testar
5. Pull request
""".format(dir_name=dir_path.name)
        }
        
        for file_name, content in standard_files.items():
            file_path = dir_path / file_name
            if not file_path.exists():
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
    
    def apply_documentation_improvements(self, file_path: Path, improvements: List[str]):
        """Aplica melhorias na documentação"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Aplicar melhorias
            improved_content = content
            
            for improvement in improvements:
                if improvement == 'add_structure':
                    if not content.startswith('#'):
                        improved_content = f"# {file_path.stem}\n\n{improved_content}"
                
                elif improvement == 'add_sections':
                    if '##' not in improved_content:
                        improved_content += "\n\n## Estrutura\n\n## Uso\n\n## Contribuição"
                
                elif improvement == 'add_esg_content':
                    if 'sustainability' not in improved_content.lower():
                        improved_content += "\n\n## Sustentabilidade\n\nEste projeto segue padrões ESG (Environmental, Social, Governance)."
            
            # Salvar conteúdo melhorado
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(improved_content)
                
        except Exception as e:
            logger.error(f"❌ Erro ao aplicar melhorias em {file_path}: {e}")
    
    def calculate_organization_score(self, analysis: Dict[str, Any]) -> float:
        """Calcula score de organização"""
        total_issues = len(analysis['issues_found'])
        high_severity = len([issue for issue in analysis['issues_found'] if issue.get('severity') == 'high'])
        medium_severity = len([issue for issue in analysis['issues_found'] if issue.get('severity') == 'medium'])
        low_severity = len([issue for issue in analysis['issues_found'] if issue.get('severity') == 'low'])
        
        # Calcular score baseado na severidade dos problemas
        score = 100.0
        score -= high_severity * 20  # Problemas de alta severidade
        score -= medium_severity * 10  # Problemas de média severidade
        score -= low_severity * 5  # Problemas de baixa severidade
        
        return max(score, 0.0)
    
    def calculate_improvements_applied(self, execution_report: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula melhorias aplicadas"""
        return {
            'total_actions': len(execution_report['actions_executed']),
            'successful_actions': len(execution_report['actions_executed']),
            'failed_actions': len(execution_report['actions_failed']),
            'files_created': len(execution_report['files_created']),
            'files_modified': len(execution_report['files_modified']),
            'directories_created': len(execution_report['directories_created']),
            'success_rate': len(execution_report['actions_executed']) / (len(execution_report['actions_executed']) + len(execution_report['actions_failed'])) if (len(execution_report['actions_executed']) + len(execution_report['actions_failed'])) > 0 else 0
        }
    
    # Métodos auxiliares
    def follows_naming_convention(self, file_name: str, convention: str) -> bool:
        """Verifica se arquivo segue convenção de nomenclatura"""
        if convention == 'snake_case':
            return '_' in file_name and not '-' in file_name and not file_name.isupper()
        elif convention == 'kebab-case':
            return '-' in file_name and not '_' in file_name and not file_name.isupper()
        elif convention == 'UPPER_CASE':
            return file_name.isupper()
        elif convention == 'lower_case':
            return file_name.islower()
        return True
    
    def generate_correct_name(self, file_path: Path, convention: str) -> str:
        """Gera nome correto baseado na convenção"""
        name = file_path.stem
        ext = file_path.suffix
        
        if convention == 'snake_case':
            return re.sub(r'[^a-zA-Z0-9]', '_', name).lower() + ext
        elif convention == 'kebab-case':
            return re.sub(r'[^a-zA-Z0-9]', '-', name).lower() + ext
        elif convention == 'UPPER_CASE':
            return name.upper() + ext
        elif convention == 'lower_case':
            return name.lower() + ext
        
        return name + ext
    
    def get_file_template(self, file_name: str) -> str:
        """Obtém template para arquivo"""
        if file_name == 'README.md':
            return """# {name}

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
""".format(name=file_name.replace('.md', ''))
        
        elif file_name == 'CONTRIBUTING.md':
            return """# Contribuindo

## Diretrizes
- Seguir padrões de código
- Documentar mudanças
- Testar alterações

## Processo
1. Fork do repositório
2. Criar branch de feature
3. Fazer mudanças
4. Testar
5. Pull request
"""
        
        else:
            return f"# {file_name}\n\nConteúdo padrão para {file_name}"
    
    def get_esg_template(self, file_name: str) -> str:
        """Obtém template ESG"""
        if 'ESG_METRICS' in file_name:
            return """# ESG Metrics

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
        
        elif 'SUSTAINABILITY_REPORT' in file_name:
            return """# Sustainability Report

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
            return f"# {file_name}\n\nTemplate ESG para {file_name}"
    
    def generate_esg_content(self) -> str:
        """Gera conteúdo ESG"""
        return """
## 🌱 Sustentabilidade ESG

Este projeto segue os princípios ESG (Environmental, Social, Governance):

### 🌍 Environmental (Ambiental)
- Redução de pegada de carbono
- Uso eficiente de recursos
- Práticas sustentáveis

### 👥 Social
- Inclusão e diversidade
- Impacto social positivo
- Bem-estar da comunidade

### ⚖️ Governance (Governança)
- Transparência
- Ética
- Conformidade regulatória
"""
    
    def generate_documentation_improvements(self, current_quality: float, target_quality: float) -> List[str]:
        """Gera melhorias de documentação"""
        improvements = []
        
        if current_quality < target_quality:
            if current_quality < 50:
                improvements.extend(['add_structure', 'add_sections', 'add_esg_content'])
            elif current_quality < 70:
                improvements.extend(['add_sections', 'add_esg_content'])
            else:
                improvements.append('add_esg_content')
        
        return improvements
    
    def calculate_documentation_quality(self, content: str) -> float:
        """Calcula qualidade da documentação"""
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
    
    def run_auto_organization(self) -> Dict[str, Any]:
        """Executa auto-organização completa"""
        logger.info("🤖 Iniciando auto-organização...")
        
        # Analisar organização atual
        analysis = self.analyze_current_organization()
        
        # Executar auto-organização
        execution_report = self.execute_auto_organization(analysis)
        
        # Relatório final
        report = {
            'timestamp': datetime.now().isoformat(),
            'initial_analysis': analysis,
            'execution_report': execution_report,
            'organization_improvement': {
                'initial_score': analysis['organization_score'],
                'final_score': self.calculate_organization_score(analysis),
                'improvement': self.calculate_organization_score(analysis) - analysis['organization_score']
            }
        }
        
        # Salvar relatório
        with open('auto_organization_final_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info("✅ Auto-organização concluída!")
        return report

def main():
    """Função principal"""
    print("🤖 ESG Token Ecosystem - Auto Organization System")
    print("=" * 60)
    
    # Inicializar sistema de auto-organização
    auto_org = AutoOrganizationSystem()
    
    # Executar auto-organização
    report = auto_org.run_auto_organization()
    
    print("✅ Auto-organização concluída!")
    print(f"📊 Score inicial: {report['initial_analysis']['organization_score']:.1f}")
    print(f"📈 Melhoria: {report['organization_improvement']['improvement']:.1f} pontos")
    print(f"📁 Arquivos criados: {report['execution_report']['files_created']}")
    print(f"📝 Arquivos modificados: {report['execution_report']['files_modified']}")
    print("📄 Relatório salvo em: auto_organization_final_report.json")

if __name__ == "__main__":
    main()
