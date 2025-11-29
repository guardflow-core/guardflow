# -*- coding: utf-8 -*-
"""
🧾 GUARDFLOW NFE ESG CALCULATOR
Sistema de cálculo de scores ESG por item/nota fiscal
"""

import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime
import xml.etree.ElementTree as ET
import json
import re

from app.services.esg_engine import esg_engine, ESGScore, ESGCategory

logger = logging.getLogger(__name__)

@dataclass
class NFeItem:
    """Item de uma NFe com dados ESG"""
    codigo_produto: str
    descricao: str
    ncm: str
    cfop: str
    unidade_comercial: str
    quantidade_comercial: float
    valor_unitario: float
    valor_total: float
    esg_score: Optional[ESGScore] = None
    esg_factors: List[str] = None
    esg_insights: Dict[str, str] = None
    esg_recommendations: List[Dict[str, str]] = None

@dataclass
class NFeESGResult:
    """Resultado do cálculo ESG de uma NFe completa"""
    chave_acesso: str
    numero_nfe: str
    serie: str
    data_emissao: datetime
    emitente: Dict[str, Any]
    destinatario: Dict[str, Any]
    items: List[NFeItem]
    esg_score_geral: ESGScore
    esg_score_medio: float
    esg_score_ponderado: float
    total_esg_impact: float
    esg_breakdown: Dict[str, float]
    esg_insights: Dict[str, str]
    esg_recommendations: List[Dict[str, str]]
    calculation_timestamp: datetime
    version: str

class NFeESGCalculator:
    """Calculadora ESG para NFe e itens"""
    
    def __init__(self):
        self.version = "1.0.0"
        self.namespaces = {
            'nfe': 'http://www.portalfiscal.inf.br/nfe'
        }
        logger.info(f"NFe ESG Calculator v{self.version} inicializado")
    
    def parse_nfe_xml(self, xml_content: str) -> Dict[str, Any]:
        """
        Faz o parsing do XML da NFe e extrai dados relevantes
        
        Args:
            xml_content: Conteúdo XML da NFe
        
        Returns:
            Dict com dados estruturados da NFe
        """
        try:
            root = ET.fromstring(xml_content)
            
            # Extrair dados básicos da NFe
            inf_nfe = root.find('.//nfe:infNFe', self.namespaces)
            if inf_nfe is None:
                raise ValueError("Estrutura XML da NFe inválida")
            
            # Chave de acesso
            chave_acesso = inf_nfe.get('Id', '').replace('NFe', '')
            
            # Dados do emitente
            emitente = self._extract_emitente(inf_nfe)
            
            # Dados do destinatário
            destinatario = self._extract_destinatario(inf_nfe)
            
            # Dados da NFe
            ide = inf_nfe.find('nfe:ide', self.namespaces)
            numero_nfe = ide.find('nfe:nNF', self.namespaces).text if ide.find('nfe:nNF', self.namespaces) is not None else ""
            serie = ide.find('nfe:serie', self.namespaces).text if ide.find('nfe:serie', self.namespaces) is not None else ""
            data_emissao = ide.find('nfe:dhEmi', self.namespaces).text if ide.find('nfe:dhEmi', self.namespaces) is not None else ""
            
            # Itens da NFe
            items = self._extract_items(inf_nfe)
            
            return {
                "chave_acesso": chave_acesso,
                "numero_nfe": numero_nfe,
                "serie": serie,
                "data_emissao": data_emissao,
                "emitente": emitente,
                "destinatario": destinatario,
                "items": items
            }
            
        except Exception as e:
            logger.error(f"Erro ao fazer parsing do XML da NFe: {e}")
            raise ValueError(f"Erro ao processar XML da NFe: {str(e)}")
    
    def _extract_emitente(self, inf_nfe) -> Dict[str, Any]:
        """Extrai dados do emitente"""
        emit = inf_nfe.find('nfe:emit', self.namespaces)
        if emit is None:
            return {}
        
        ender_emit = emit.find('nfe:enderEmit', self.namespaces)
        
        return {
            "cnpj": emit.find('nfe:CNPJ', self.namespaces).text if emit.find('nfe:CNPJ', self.namespaces) is not None else "",
            "nome": emit.find('nfe:xNome', self.namespaces).text if emit.find('nfe:xNome', self.namespaces) is not None else "",
            "endereco": {
                "logradouro": ender_emit.find('nfe:xLgr', self.namespaces).text if ender_emit and ender_emit.find('nfe:xLgr', self.namespaces) is not None else "",
                "numero": ender_emit.find('nfe:nro', self.namespaces).text if ender_emit and ender_emit.find('nfe:nro', self.namespaces) is not None else "",
                "bairro": ender_emit.find('nfe:xBairro', self.namespaces).text if ender_emit and ender_emit.find('nfe:xBairro', self.namespaces) is not None else "",
                "cidade": ender_emit.find('nfe:xMun', self.namespaces).text if ender_emit and ender_emit.find('nfe:xMun', self.namespaces) is not None else "",
                "uf": ender_emit.find('nfe:UF', self.namespaces).text if ender_emit and ender_emit.find('nfe:UF', self.namespaces) is not None else "",
                "cep": ender_emit.find('nfe:CEP', self.namespaces).text if ender_emit and ender_emit.find('nfe:CEP', self.namespaces) is not None else ""
            }
        }
    
    def _extract_destinatario(self, inf_nfe) -> Dict[str, Any]:
        """Extrai dados do destinatário"""
        dest = inf_nfe.find('nfe:dest', self.namespaces)
        if dest is None:
            return {}
        
        ender_dest = dest.find('nfe:enderDest', self.namespaces)
        
        return {
            "cpf_cnpj": dest.find('nfe:CPF', self.namespaces).text if dest.find('nfe:CPF', self.namespaces) is not None else dest.find('nfe:CNPJ', self.namespaces).text if dest.find('nfe:CNPJ', self.namespaces) is not None else "",
            "nome": dest.find('nfe:xNome', self.namespaces).text if dest.find('nfe:xNome', self.namespaces) is not None else "",
            "endereco": {
                "logradouro": ender_dest.find('nfe:xLgr', self.namespaces).text if ender_dest and ender_dest.find('nfe:xLgr', self.namespaces) is not None else "",
                "numero": ender_dest.find('nfe:nro', self.namespaces).text if ender_dest and ender_dest.find('nfe:nro', self.namespaces) is not None else "",
                "bairro": ender_dest.find('nfe:xBairro', self.namespaces).text if ender_dest and ender_dest.find('nfe:xBairro', self.namespaces) is not None else "",
                "cidade": ender_dest.find('nfe:xMun', self.namespaces).text if ender_dest and ender_dest.find('nfe:xMun', self.namespaces) is not None else "",
                "uf": ender_dest.find('nfe:UF', self.namespaces).text if ender_dest and ender_dest.find('nfe:UF', self.namespaces) is not None else "",
                "cep": ender_dest.find('nfe:CEP', self.namespaces).text if ender_dest and ender_dest.find('nfe:CEP', self.namespaces) is not None else ""
            }
        }
    
    def _extract_items(self, inf_nfe) -> List[Dict[str, Any]]:
        """Extrai itens da NFe"""
        items = []
        det_items = inf_nfe.findall('.//nfe:det', self.namespaces)
        
        for det in det_items:
            prod = det.find('nfe:prod', self.namespaces)
            if prod is None:
                continue
            
            # Dados básicos do produto
            codigo_produto = prod.find('nfe:cProd', self.namespaces).text if prod.find('nfe:cProd', self.namespaces) is not None else ""
            descricao = prod.find('nfe:xProd', self.namespaces).text if prod.find('nfe:xProd', self.namespaces) is not None else ""
            ncm = prod.find('nfe:NCM', self.namespaces).text if prod.find('nfe:NCM', self.namespaces) is not None else ""
            cfop = prod.find('nfe:CFOP', self.namespaces).text if prod.find('nfe:CFOP', self.namespaces) is not None else ""
            unidade_comercial = prod.find('nfe:uCom', self.namespaces).text if prod.find('nfe:uCom', self.namespaces) is not None else ""
            
            # Quantidade e valores
            quantidade_comercial = float(prod.find('nfe:qCom', self.namespaces).text) if prod.find('nfe:qCom', self.namespaces) is not None else 0.0
            valor_unitario = float(prod.find('nfe:vUnCom', self.namespaces).text) if prod.find('nfe:vUnCom', self.namespaces) is not None else 0.0
            valor_total = float(prod.find('nfe:vProd', self.namespaces).text) if prod.find('nfe:vProd', self.namespaces) is not None else 0.0
            
            items.append({
                "codigo_produto": codigo_produto,
                "descricao": descricao,
                "ncm": ncm,
                "cfop": cfop,
                "unidade_comercial": unidade_comercial,
                "quantidade_comercial": quantidade_comercial,
                "valor_unitario": valor_unitario,
                "valor_total": valor_total
            })
        
        return items
    
    def calculate_nfe_esg_score(self, xml_content: str) -> NFeESGResult:
        """
        Calcula score ESG para uma NFe completa
        
        Args:
            xml_content: Conteúdo XML da NFe
        
        Returns:
            NFeESGResult: Resultado completo do cálculo ESG
        """
        try:
            # Fazer parsing da NFe
            nfe_data = self.parse_nfe_xml(xml_content)
            
            # Calcular ESG para cada item
            items_with_esg = []
            esg_scores = []
            esg_breakdown = {"environmental": [], "social": [], "governance": []}
            
            for item_data in nfe_data["items"]:
                # Criar objeto NFeItem
                nfe_item = NFeItem(
                    codigo_produto=item_data["codigo_produto"],
                    descricao=item_data["descricao"],
                    ncm=item_data["ncm"],
                    cfop=item_data["cfop"],
                    unidade_comercial=item_data["unidade_comercial"],
                    quantidade_comercial=item_data["quantidade_comercial"],
                    valor_unitario=item_data["valor_unitario"],
                    valor_total=item_data["valor_total"]
                )
                
                # Calcular score ESG para o item
                if nfe_item.ncm:
                    esg_score = esg_engine.calculate_esg_score(nfe_item.ncm)
                    nfe_item.esg_score = esg_score
                    nfe_item.esg_factors = esg_score.factors_applied
                    nfe_item.esg_insights = esg_engine.get_esg_insights(esg_score)
                    nfe_item.esg_recommendations = esg_engine.get_esg_recommendations(esg_score)
                    
                    esg_scores.append(esg_score)
                    esg_breakdown["environmental"].append(esg_score.environmental)
                    esg_breakdown["social"].append(esg_score.social)
                    esg_breakdown["governance"].append(esg_score.governance)
                
                items_with_esg.append(nfe_item)
            
            # Calcular score geral da NFe
            if esg_scores:
                esg_score_geral = self._calculate_overall_nfe_score(esg_scores, nfe_data["items"])
                esg_score_medio = sum(s.overall for s in esg_scores) / len(esg_scores)
                esg_score_ponderado = self._calculate_weighted_score(esg_scores, nfe_data["items"])
                total_esg_impact = sum(item.valor_total for item in items_with_esg if item.esg_score)
            else:
                esg_score_geral = esg_engine._create_default_score()
                esg_score_medio = 50.0
                esg_score_ponderado = 50.0
                total_esg_impact = 0.0
            
            # Calcular breakdown médio
            esg_breakdown_avg = {
                "environmental": sum(esg_breakdown["environmental"]) / len(esg_breakdown["environmental"]) if esg_breakdown["environmental"] else 0,
                "social": sum(esg_breakdown["social"]) / len(esg_breakdown["social"]) if esg_breakdown["social"] else 0,
                "governance": sum(esg_breakdown["governance"]) / len(esg_breakdown["governance"]) if esg_breakdown["governance"] else 0
            }
            
            # Gerar insights e recomendações gerais
            esg_insights = esg_engine.get_esg_insights(esg_score_geral)
            esg_recommendations = esg_engine.get_esg_recommendations(esg_score_geral)
            
            return NFeESGResult(
                chave_acesso=nfe_data["chave_acesso"],
                numero_nfe=nfe_data["numero_nfe"],
                serie=nfe_data["serie"],
                data_emissao=datetime.fromisoformat(nfe_data["data_emissao"].replace('Z', '+00:00')) if nfe_data["data_emissao"] else datetime.utcnow(),
                emitente=nfe_data["emitente"],
                destinatario=nfe_data["destinatario"],
                items=items_with_esg,
                esg_score_geral=esg_score_geral,
                esg_score_medio=esg_score_medio,
                esg_score_ponderado=esg_score_ponderado,
                total_esg_impact=total_esg_impact,
                esg_breakdown=esg_breakdown_avg,
                esg_insights=esg_insights,
                esg_recommendations=esg_recommendations,
                calculation_timestamp=datetime.utcnow(),
                version=self.version
            )
            
        except Exception as e:
            logger.error(f"Erro ao calcular score ESG da NFe: {e}")
            raise ValueError(f"Erro no cálculo ESG da NFe: {str(e)}")
    
    def _calculate_overall_nfe_score(self, esg_scores: List[ESGScore], items: List[Dict]) -> ESGScore:
        """Calcula score ESG geral da NFe"""
        if not esg_scores:
            return esg_engine._create_default_score()
        
        # Média ponderada pelos valores dos itens
        total_value = sum(item["valor_total"] for item in items)
        if total_value == 0:
            # Se não há valores, usar média simples
            avg_environmental = sum(s.environmental for s in esg_scores) / len(esg_scores)
            avg_social = sum(s.social for s in esg_scores) / len(esg_scores)
            avg_governance = sum(s.governance for s in esg_scores) / len(esg_scores)
            avg_overall = sum(s.overall for s in esg_scores) / len(esg_scores)
        else:
            # Média ponderada por valor
            weighted_env = sum(s.environmental * item["valor_total"] for s, item in zip(esg_scores, items)) / total_value
            weighted_soc = sum(s.social * item["valor_total"] for s, item in zip(esg_scores, items)) / total_value
            weighted_gov = sum(s.governance * item["valor_total"] for s, item in zip(esg_scores, items)) / total_value
            weighted_overall = sum(s.overall * item["valor_total"] for s, item in zip(esg_scores, items)) / total_value
            
            avg_environmental = weighted_env
            avg_social = weighted_soc
            avg_governance = weighted_gov
            avg_overall = weighted_overall
        
        # Coletar todos os fatores aplicados
        all_factors = []
        for score in esg_scores:
            all_factors.extend(score.factors_applied)
        
        return ESGScore(
            environmental=round(avg_environmental, 2),
            social=round(avg_social, 2),
            governance=round(avg_governance, 2),
            overall=round(avg_overall, 2),
            factors_applied=list(set(all_factors)),
            calculation_timestamp=datetime.utcnow(),
            version=self.version
        )
    
    def _calculate_weighted_score(self, esg_scores: List[ESGScore], items: List[Dict]) -> float:
        """Calcula score ESG ponderado por valor dos itens"""
        if not esg_scores or not items:
            return 50.0
        
        total_value = sum(item["valor_total"] for item in items)
        if total_value == 0:
            return sum(s.overall for s in esg_scores) / len(esg_scores)
        
        weighted_score = sum(s.overall * item["valor_total"] for s, item in zip(esg_scores, items)) / total_value
        return round(weighted_score, 2)
    
    def calculate_item_esg_score(self, ncm: str, product_data: Dict = None) -> ESGScore:
        """
        Calcula score ESG para um item específico
        
        Args:
            ncm: Código NCM do produto
            product_data: Dados adicionais do produto
        
        Returns:
            ESGScore: Score ESG do item
        """
        return esg_engine.calculate_esg_score(ncm, product_data)
    
    def batch_calculate_items_esg(self, items_data: List[Dict]) -> List[NFeItem]:
        """
        Calcula scores ESG para múltiplos itens
        
        Args:
            items_data: Lista de dados dos itens
        
        Returns:
            List[NFeItem]: Lista de itens com scores ESG
        """
        items_with_esg = []
        
        for item_data in items_data:
            nfe_item = NFeItem(
                codigo_produto=item_data.get("codigo_produto", ""),
                descricao=item_data.get("descricao", ""),
                ncm=item_data.get("ncm", ""),
                cfop=item_data.get("cfop", ""),
                unidade_comercial=item_data.get("unidade_comercial", ""),
                quantidade_comercial=item_data.get("quantidade_comercial", 0.0),
                valor_unitario=item_data.get("valor_unitario", 0.0),
                valor_total=item_data.get("valor_total", 0.0)
            )
            
            if nfe_item.ncm:
                esg_score = esg_engine.calculate_esg_score(nfe_item.ncm, item_data.get("product_data"))
                nfe_item.esg_score = esg_score
                nfe_item.esg_factors = esg_score.factors_applied
                nfe_item.esg_insights = esg_engine.get_esg_insights(esg_score)
                nfe_item.esg_recommendations = esg_engine.get_esg_recommendations(esg_score)
            
            items_with_esg.append(nfe_item)
        
        return items_with_esg
    
    def export_nfe_esg_report(self, result: NFeESGResult, format: str = "json") -> str:
        """
        Exporta relatório ESG da NFe
        
        Args:
            result: Resultado do cálculo ESG da NFe
            format: Formato do relatório (json, csv, xml)
        
        Returns:
            str: Relatório formatado
        """
        report_data = {
            "nfe_info": {
                "chave_acesso": result.chave_acesso,
                "numero_nfe": result.numero_nfe,
                "serie": result.serie,
                "data_emissao": result.data_emissao.isoformat(),
                "emitente": result.emitente,
                "destinatario": result.destinatario
            },
            "esg_summary": {
                "score_geral": {
                    "environmental": result.esg_score_geral.environmental,
                    "social": result.esg_score_geral.social,
                    "governance": result.esg_score_geral.governance,
                    "overall": result.esg_score_geral.overall
                },
                "score_medio": result.esg_score_medio,
                "score_ponderado": result.esg_score_ponderado,
                "total_esg_impact": result.total_esg_impact,
                "breakdown": result.esg_breakdown
            },
            "items": [
                {
                    "codigo_produto": item.codigo_produto,
                    "descricao": item.descricao,
                    "ncm": item.ncm,
                    "valor_total": item.valor_total,
                    "esg_score": {
                        "environmental": item.esg_score.environmental if item.esg_score else 0,
                        "social": item.esg_score.social if item.esg_score else 0,
                        "governance": item.esg_score.governance if item.esg_score else 0,
                        "overall": item.esg_score.overall if item.esg_score else 0
                    } if item.esg_score else None,
                    "esg_factors": item.esg_factors,
                    "esg_insights": item.esg_insights,
                    "esg_recommendations": item.esg_recommendations
                }
                for item in result.items
            ],
            "insights": result.esg_insights,
            "recommendations": result.esg_recommendations,
            "calculation_info": {
                "timestamp": result.calculation_timestamp.isoformat(),
                "version": result.version
            }
        }
        
        if format.lower() == "json":
            return json.dumps(report_data, indent=2, ensure_ascii=False)
        elif format.lower() == "csv":
            # Implementar exportação CSV
            csv_lines = ["NCM,Descricao,Valor_Total,ESG_Score,Environmental,Social,Governance"]
            for item in result.items:
                if item.esg_score:
                    csv_lines.append(f"{item.ncm},{item.descricao},{item.valor_total},{item.esg_score.overall},{item.esg_score.environmental},{item.esg_score.social},{item.esg_score.governance}")
            return "\n".join(csv_lines)
        elif format.lower() == "xml":
            # Implementar exportação XML
            return f"""<?xml version="1.0" encoding="UTF-8"?>
<nfe_esg_report>
    <nfe_info>
        <chave_acesso>{result.chave_acesso}</chave_acesso>
        <numero_nfe>{result.numero_nfe}</numero_nfe>
        <esg_score_geral>{result.esg_score_geral.overall}</esg_score_geral>
    </nfe_info>
    <items count="{len(result.items)}">
        <!-- Items details would go here -->
    </items>
</nfe_esg_report>"""
        else:
            return json.dumps(report_data, indent=2, ensure_ascii=False)

# Instância global do NFe ESG Calculator
nfe_esg_calculator = NFeESGCalculator()
