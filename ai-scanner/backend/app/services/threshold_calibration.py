"""
Sistema de calibração de thresholds para QR Checkout
Analisa dados de piloto para otimizar decisões de allow/sample/block
"""

import json
import os
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import statistics
import logging

logger = logging.getLogger(__name__)

class ThresholdCalibrator:
    def __init__(self):
        self.data_file = "threshold_calibration_data.json"
        self.pilot_data = self._load_pilot_data()
        
        # Configurações de calibração
        self.target_false_positive_rate = 0.05  # 5% máximo
        self.target_false_negative_rate = 0.02  # 2% máximo
        self.min_samples_per_context = 50  # Mínimo de amostras para calibrar
    
    def _load_pilot_data(self) -> List[Dict]:
        """Carrega dados do piloto ou cria dados simulados"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Gerar dados simulados de piloto
        return self._generate_pilot_data()
    
    def _generate_pilot_data(self) -> List[Dict]:
        """Gera dados simulados baseados em cenários reais de piloto"""
        import random
        
        pilot_data = []
        
        # Cenários por contexto
        contexts = [
            {"sector": "retail", "store_type": "supermercado", "samples": 200},
            {"sector": "security", "store_type": "farmacia", "samples": 150},
            {"sector": "retail", "store_type": "eletronicos", "samples": 100},
            {"sector": "retail", "store_type": "conveniencia", "samples": 80}
        ]
        
        for context in contexts:
            for i in range(context["samples"]):
                # Simular transação
                expected_weight = random.uniform(0.5, 10.0)
                
                # Simular diferentes tipos de anomalias
                anomaly_type = random.choices(
                    ["normal", "weight_variance", "fraud_attempt", "measurement_error"],
                    weights=[0.85, 0.10, 0.03, 0.02]
                )[0]
                
                if anomaly_type == "normal":
                    measured_weight = expected_weight * random.uniform(0.95, 1.05)
                    actual_fraud = False
                elif anomaly_type == "weight_variance":
                    measured_weight = expected_weight * random.uniform(0.85, 1.15)
                    actual_fraud = False
                elif anomaly_type == "fraud_attempt":
                    measured_weight = expected_weight * random.uniform(0.6, 0.85)
                    actual_fraud = True
                else:  # measurement_error
                    measured_weight = expected_weight * random.uniform(1.15, 1.4)
                    actual_fraud = False
                
                # Outros fatores
                has_sensitive_items = random.random() < 0.3
                scan_duration = random.randint(15, 120)
                guardpass_tier = random.choices(
                    ["basic", "premium", "enterprise"],
                    weights=[0.6, 0.3, 0.1]
                )[0]
                time_of_day = random.randint(6, 23)
                
                # Calcular score com algoritmo atual
                score = self._calculate_score_for_calibration(
                    expected_weight, measured_weight, has_sensitive_items,
                    scan_duration, guardpass_tier, context["sector"], context["store_type"]
                )
                
                pilot_data.append({
                    "transaction_id": f"pilot_{context['sector']}_{i:04d}",
                    "timestamp": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat(),
                    "context": context,
                    "expected_weight_kg": expected_weight,
                    "measured_weight_kg": measured_weight,
                    "has_sensitive_items": has_sensitive_items,
                    "scan_duration_sec": scan_duration,
                    "guardpass_tier": guardpass_tier,
                    "time_of_day": time_of_day,
                    "calculated_score": score,
                    "actual_fraud": actual_fraud,
                    "anomaly_type": anomaly_type
                })
        
        # Salvar dados simulados
        with open(self.data_file, 'w') as f:
            json.dump(pilot_data, f, indent=2)
        
        return pilot_data
    
    def _calculate_score_for_calibration(self, expected_weight: float, measured_weight: float,
                                       has_sensitive: bool, scan_duration: int, guardpass_tier: str,
                                       sector: str, store_type: str) -> float:
        """Calcula score usando algoritmo atual para calibração"""
        # Pesos base
        w_weight = 0.5
        w_sensitive = 0.2
        w_time = 0.15
        w_user = 0.15
        
        # Delta peso
        delta_ratio = abs(measured_weight - expected_weight) / max(expected_weight, 0.001)
        
        # Fatores
        sensitive_factor = 1.0 if has_sensitive else 0.0
        time_factor = 1.0 if scan_duration < 20 else 0.3
        
        # User factor baseado no tier
        user_factors = {"basic": 0.5, "premium": 0.3, "enterprise": 0.2}
        user_factor = user_factors.get(guardpass_tier, 0.5)
        
        # Score final
        score = (
            w_weight * min(delta_ratio, 1.0) +
            w_sensitive * sensitive_factor +
            w_time * time_factor +
            w_user * user_factor
        )
        
        return score
    
    def calibrate_thresholds(self, context_filter: Optional[Dict] = None) -> Dict:
        """Calibra thresholds baseado nos dados do piloto"""
        # Filtrar dados por contexto se especificado
        if context_filter:
            filtered_data = [
                d for d in self.pilot_data
                if all(d["context"].get(k) == v for k, v in context_filter.items())
            ]
        else:
            filtered_data = self.pilot_data
        
        if len(filtered_data) < self.min_samples_per_context:
            return {
                "error": f"Dados insuficientes para calibração. Mínimo: {self.min_samples_per_context}, atual: {len(filtered_data)}"
            }
        
        # Separar dados por resultado real
        fraud_cases = [d for d in filtered_data if d["actual_fraud"]]
        normal_cases = [d for d in filtered_data if not d["actual_fraud"]]
        
        # Calcular estatísticas
        fraud_scores = [d["calculated_score"] for d in fraud_cases]
        normal_scores = [d["calculated_score"] for d in normal_cases]
        
        # Encontrar thresholds ótimos
        optimal_thresholds = self._find_optimal_thresholds(fraud_scores, normal_scores)
        
        # Validar thresholds
        validation = self._validate_thresholds(filtered_data, optimal_thresholds)
        
        return {
            "context_filter": context_filter,
            "data_samples": len(filtered_data),
            "fraud_cases": len(fraud_cases),
            "normal_cases": len(normal_cases),
            "current_thresholds": {"allow": 0.35, "sample": 0.6},
            "optimal_thresholds": optimal_thresholds,
            "validation": validation,
            "recommendation": self._generate_recommendation(validation),
            "calibrated_at": datetime.now().isoformat()
        }
    
    def _find_optimal_thresholds(self, fraud_scores: List[float], normal_scores: List[float]) -> Dict[str, float]:
        """Encontra thresholds ótimos usando análise ROC"""
        if not fraud_scores or not normal_scores:
            return {"allow": 0.35, "sample": 0.6}
        
        # Testar diferentes thresholds
        test_thresholds = [i * 0.05 for i in range(1, 20)]  # 0.05 a 0.95
        best_allow = 0.35
        best_sample = 0.6
        best_score = 0
        
        for allow_thresh in test_thresholds:
            for sample_thresh in test_thresholds:
                if sample_thresh <= allow_thresh:
                    continue
                
                # Calcular métricas
                fp_rate = sum(1 for score in normal_scores if score >= allow_thresh) / len(normal_scores)
                fn_rate = sum(1 for score in fraud_scores if score < sample_thresh) / len(fraud_scores)
                
                # Função objetivo: minimizar falsos positivos e negativos
                if fp_rate <= self.target_false_positive_rate and fn_rate <= self.target_false_negative_rate:
                    # Score baseado na separação entre classes
                    separation_score = sample_thresh - allow_thresh
                    if separation_score > best_score:
                        best_score = separation_score
                        best_allow = allow_thresh
                        best_sample = sample_thresh
        
        return {"allow": best_allow, "sample": best_sample}
    
    def _validate_thresholds(self, data: List[Dict], thresholds: Dict[str, float]) -> Dict:
        """Valida thresholds calculando métricas de performance"""
        allow_thresh = thresholds["allow"]
        sample_thresh = thresholds["sample"]
        
        # Classificar todas as transações
        results = {
            "true_positives": 0,    # Fraude detectada corretamente (sample/block)
            "true_negatives": 0,    # Normal liberado corretamente (allow)
            "false_positives": 0,   # Normal bloqueado incorretamente (sample/block)
            "false_negatives": 0,   # Fraude liberada incorretamente (allow)
            "total_fraud": 0,
            "total_normal": 0
        }
        
        for transaction in data:
            score = transaction["calculated_score"]
            is_fraud = transaction["actual_fraud"]
            
            if is_fraud:
                results["total_fraud"] += 1
                if score >= allow_thresh:  # Detectado (sample ou block)
                    results["true_positives"] += 1
                else:  # Não detectado
                    results["false_negatives"] += 1
            else:
                results["total_normal"] += 1
                if score < allow_thresh:  # Liberado corretamente
                    results["true_negatives"] += 1
                else:  # Bloqueado incorretamente
                    results["false_positives"] += 1
        
        # Calcular métricas
        precision = results["true_positives"] / max(results["true_positives"] + results["false_positives"], 1)
        recall = results["true_positives"] / max(results["true_positives"] + results["false_negatives"], 1)
        f1_score = 2 * (precision * recall) / max(precision + recall, 0.001)
        
        false_positive_rate = results["false_positives"] / max(results["total_normal"], 1)
        false_negative_rate = results["false_negatives"] / max(results["total_fraud"], 1)
        
        return {
            **results,
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1_score, 4),
            "false_positive_rate": round(false_positive_rate, 4),
            "false_negative_rate": round(false_negative_rate, 4),
            "accuracy": round((results["true_positives"] + results["true_negatives"]) / len(data), 4)
        }
    
    def _generate_recommendation(self, validation: Dict) -> Dict:
        """Gera recomendação baseada na validação"""
        fp_rate = validation["false_positive_rate"]
        fn_rate = validation["false_negative_rate"]
        f1_score = validation["f1_score"]
        
        if fp_rate <= self.target_false_positive_rate and fn_rate <= self.target_false_negative_rate:
            recommendation = "APPROVE"
            reason = "Thresholds atendem aos critérios de qualidade"
        elif fp_rate > self.target_false_positive_rate:
            recommendation = "ADJUST_UP"
            reason = f"Taxa de falsos positivos muito alta: {fp_rate:.1%} > {self.target_false_positive_rate:.1%}"
        elif fn_rate > self.target_false_negative_rate:
            recommendation = "ADJUST_DOWN"
            reason = f"Taxa de falsos negativos muito alta: {fn_rate:.1%} > {self.target_false_negative_rate:.1%}"
        else:
            recommendation = "REVIEW"
            reason = "Métricas borderline, revisar manualmente"
        
        return {
            "action": recommendation,
            "reason": reason,
            "confidence": f1_score,
            "priority": "HIGH" if fn_rate > 0.05 else "MEDIUM" if fp_rate > 0.1 else "LOW"
        }
    
    def get_calibration_by_context(self) -> Dict:
        """Obtém calibração para todos os contextos"""
        contexts = [
            {"sector": "retail", "store_type": "supermercado"},
            {"sector": "security", "store_type": "farmacia"},
            {"sector": "retail", "store_type": "eletronicos"},
            {"sector": "retail", "store_type": "conveniencia"}
        ]
        
        results = {}
        for context in contexts:
            context_key = f"{context['sector']}_{context['store_type']}"
            results[context_key] = self.calibrate_thresholds(context)
        
        return results
    
    def export_calibrated_thresholds(self) -> Dict:
        """Exporta thresholds calibrados para uso em produção"""
        calibrations = self.get_calibration_by_context()
        
        production_thresholds = {}
        for context_key, calibration in calibrations.items():
            if "optimal_thresholds" in calibration:
                production_thresholds[context_key] = calibration["optimal_thresholds"]
        
        # Salvar configuração de produção
        config_file = "production_thresholds.json"
        with open(config_file, 'w') as f:
            json.dump({
                "thresholds": production_thresholds,
                "calibrated_at": datetime.now().isoformat(),
                "version": "1.0"
            }, f, indent=2)
        
        return {
            "config_file": config_file,
            "contexts_calibrated": len(production_thresholds),
            "thresholds": production_thresholds
        }

# Instância global do calibrador
threshold_calibrator = ThresholdCalibrator()
