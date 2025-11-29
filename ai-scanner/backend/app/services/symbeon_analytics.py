"""
GuardFlow SYMBEON Analytics Engine
Motor de analytics avançado com IA para análise de comportamento e predições
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import numpy as np
from collections import defaultdict, deque
import hashlib

logger = logging.getLogger(__name__)

class AnalyticsEventType(Enum):
    USER_ACTION = "user_action"
    TRANSACTION = "transaction"
    ESG_INTERACTION = "esg_interaction"
    SYSTEM_EVENT = "system_event"
    PERFORMANCE_METRIC = "performance_metric"
    SECURITY_EVENT = "security_event"

class PredictionType(Enum):
    USER_BEHAVIOR = "user_behavior"
    PURCHASE_INTENT = "purchase_intent"
    ESG_SCORE_TREND = "esg_score_trend"
    CHURN_RISK = "churn_risk"
    FRAUD_DETECTION = "fraud_detection"
    DEMAND_FORECAST = "demand_forecast"

@dataclass
class AnalyticsEvent:
    event_id: str
    event_type: AnalyticsEventType
    timestamp: datetime
    user_id: Optional[str]
    session_id: Optional[str]
    data: Dict[str, Any]
    metadata: Dict[str, Any]
    processed: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            **asdict(self),
            'timestamp': self.timestamp.isoformat(),
            'event_type': self.event_type.value
        }

@dataclass
class AnalyticsInsight:
    insight_id: str
    type: str
    title: str
    description: str
    confidence: float
    impact_score: float
    data: Dict[str, Any]
    recommendations: List[str]
    created_at: datetime
    expires_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            **asdict(self),
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat() if self.expires_at else None
        }

@dataclass
class PredictionResult:
    prediction_id: str
    prediction_type: PredictionType
    target: str
    confidence: float
    predicted_value: Any
    probability_distribution: Optional[Dict[str, float]]
    features_importance: Dict[str, float]
    created_at: datetime
    valid_until: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            **asdict(self),
            'prediction_type': self.prediction_type.value,
            'created_at': self.created_at.isoformat(),
            'valid_until': self.valid_until.isoformat()
        }

class SymbeonAnalyticsEngine:
    def __init__(self):
        self.events_buffer = deque(maxlen=10000)
        self.processed_events = deque(maxlen=50000)
        self.insights_cache = {}
        self.predictions_cache = {}
        self.user_profiles = {}
        self.system_metrics = defaultdict(list)
        self.ml_models = {}
        self.processing_queue = asyncio.Queue()
        self.is_processing = False
        
        # Configurações
        self.batch_size = 100
        self.processing_interval = 5  # segundos
        self.insight_retention_days = 30
        self.prediction_retention_hours = 24
        
        # Inicializar processamento
        asyncio.create_task(self._start_processing_loop())
    
    async def track_event(self, event: AnalyticsEvent) -> bool:
        """Registrar evento para análise"""
        try:
            # Validar evento
            if not self._validate_event(event):
                logger.warning(f"Evento inválido: {event.event_id}")
                return False
            
            # Adicionar ao buffer
            self.events_buffer.append(event)
            
            # Adicionar à fila de processamento
            await self.processing_queue.put(event)
            
            logger.debug(f"Evento registrado: {event.event_id}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao registrar evento: {e}")
            return False
    
    async def track_user_action(self, user_id: str, action: str, data: Dict[str, Any]) -> bool:
        """Registrar ação do usuário"""
        event = AnalyticsEvent(
            event_id=self._generate_event_id(),
            event_type=AnalyticsEventType.USER_ACTION,
            timestamp=datetime.now(),
            user_id=user_id,
            session_id=data.get('session_id'),
            data={'action': action, **data},
            metadata={'source': 'user_tracking'}
        )
        return await self.track_event(event)
    
    async def track_transaction(self, user_id: str, transaction_data: Dict[str, Any]) -> bool:
        """Registrar transação"""
        event = AnalyticsEvent(
            event_id=self._generate_event_id(),
            event_type=AnalyticsEventType.TRANSACTION,
            timestamp=datetime.now(),
            user_id=user_id,
            session_id=transaction_data.get('session_id'),
            data=transaction_data,
            metadata={'source': 'transaction_system'}
        )
        return await self.track_event(event)
    
    async def track_esg_interaction(self, user_id: str, esg_data: Dict[str, Any]) -> bool:
        """Registrar interação ESG"""
        event = AnalyticsEvent(
            event_id=self._generate_event_id(),
            event_type=AnalyticsEventType.ESG_INTERACTION,
            timestamp=datetime.now(),
            user_id=user_id,
            session_id=esg_data.get('session_id'),
            data=esg_data,
            metadata={'source': 'esg_engine'}
        )
        return await self.track_event(event)
    
    async def get_user_insights(self, user_id: str) -> List[AnalyticsInsight]:
        """Obter insights do usuário"""
        try:
            # Verificar cache
            cache_key = f"user_insights_{user_id}"
            if cache_key in self.insights_cache:
                cached_insights = self.insights_cache[cache_key]
                if cached_insights['expires_at'] > datetime.now():
                    return cached_insights['insights']
            
            # Gerar insights
            insights = await self._generate_user_insights(user_id)
            
            # Cachear resultados
            self.insights_cache[cache_key] = {
                'insights': insights,
                'expires_at': datetime.now() + timedelta(hours=1)
            }
            
            return insights
            
        except Exception as e:
            logger.error(f"Erro ao obter insights do usuário {user_id}: {e}")
            return []
    
    async def get_system_insights(self) -> List[AnalyticsInsight]:
        """Obter insights do sistema"""
        try:
            cache_key = "system_insights"
            if cache_key in self.insights_cache:
                cached_insights = self.insights_cache[cache_key]
                if cached_insights['expires_at'] > datetime.now():
                    return cached_insights['insights']
            
            insights = await self._generate_system_insights()
            
            self.insights_cache[cache_key] = {
                'insights': insights,
                'expires_at': datetime.now() + timedelta(minutes=30)
            }
            
            return insights
            
        except Exception as e:
            logger.error(f"Erro ao obter insights do sistema: {e}")
            return []
    
    async def predict_user_behavior(self, user_id: str, prediction_type: PredictionType) -> Optional[PredictionResult]:
        """Fazer predição sobre comportamento do usuário"""
        try:
            cache_key = f"prediction_{user_id}_{prediction_type.value}"
            if cache_key in self.predictions_cache:
                cached_prediction = self.predictions_cache[cache_key]
                if cached_prediction.valid_until > datetime.now():
                    return cached_prediction
            
            prediction = await self._generate_prediction(user_id, prediction_type)
            
            if prediction:
                self.predictions_cache[cache_key] = prediction
            
            return prediction
            
        except Exception as e:
            logger.error(f"Erro ao fazer predição para usuário {user_id}: {e}")
            return None
    
    async def get_analytics_dashboard_data(self) -> Dict[str, Any]:
        """Obter dados para dashboard de analytics"""
        try:
            now = datetime.now()
            last_24h = now - timedelta(hours=24)
            last_7d = now - timedelta(days=7)
            
            # Métricas básicas
            events_24h = [e for e in self.processed_events if e.timestamp >= last_24h]
            events_7d = [e for e in self.processed_events if e.timestamp >= last_7d]
            
            # Usuários ativos
            active_users_24h = len(set(e.user_id for e in events_24h if e.user_id))
            active_users_7d = len(set(e.user_id for e in events_7d if e.user_id))
            
            # Transações
            transactions_24h = [e for e in events_24h if e.event_type == AnalyticsEventType.TRANSACTION]
            transactions_7d = [e for e in events_7d if e.event_type == AnalyticsEventType.TRANSACTION]
            
            # ESG interactions
            esg_interactions_24h = [e for e in events_24h if e.event_type == AnalyticsEventType.ESG_INTERACTION]
            
            # Top ações
            actions_count = defaultdict(int)
            for event in events_24h:
                if event.event_type == AnalyticsEventType.USER_ACTION:
                    action = event.data.get('action', 'unknown')
                    actions_count[action] += 1
            
            top_actions = sorted(actions_count.items(), key=lambda x: x[1], reverse=True)[:10]
            
            # Tendências horárias
            hourly_events = defaultdict(int)
            for event in events_24h:
                hour = event.timestamp.hour
                hourly_events[hour] += 1
            
            hourly_trend = [hourly_events[h] for h in range(24)]
            
            return {
                'summary': {
                    'total_events_24h': len(events_24h),
                    'total_events_7d': len(events_7d),
                    'active_users_24h': active_users_24h,
                    'active_users_7d': active_users_7d,
                    'transactions_24h': len(transactions_24h),
                    'transactions_7d': len(transactions_7d),
                    'esg_interactions_24h': len(esg_interactions_24h),
                },
                'trends': {
                    'hourly_events': hourly_trend,
                    'top_actions': top_actions,
                },
                'insights': await self.get_system_insights(),
                'generated_at': now.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Erro ao gerar dados do dashboard: {e}")
            return {}
    
    async def _start_processing_loop(self):
        """Loop principal de processamento"""
        self.is_processing = True
        
        while self.is_processing:
            try:
                await self._process_events_batch()
                await asyncio.sleep(self.processing_interval)
            except Exception as e:
                logger.error(f"Erro no loop de processamento: {e}")
                await asyncio.sleep(1)
    
    async def _process_events_batch(self):
        """Processar lote de eventos"""
        batch = []
        
        # Coletar eventos do buffer
        while len(batch) < self.batch_size and self.events_buffer:
            batch.append(self.events_buffer.popleft())
        
        if not batch:
            return
        
        # Processar cada evento
        for event in batch:
            try:
                await self._process_single_event(event)
                event.processed = True
                self.processed_events.append(event)
            except Exception as e:
                logger.error(f"Erro ao processar evento {event.event_id}: {e}")
        
        logger.debug(f"Processados {len(batch)} eventos")
    
    async def _process_single_event(self, event: AnalyticsEvent):
        """Processar evento individual"""
        # Atualizar perfil do usuário
        if event.user_id:
            await self._update_user_profile(event)
        
        # Detectar padrões
        await self._detect_patterns(event)
        
        # Atualizar métricas do sistema
        await self._update_system_metrics(event)
        
        # Verificar anomalias
        await self._check_anomalies(event)
    
    async def _update_user_profile(self, event: AnalyticsEvent):
        """Atualizar perfil do usuário"""
        user_id = event.user_id
        
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {
                'user_id': user_id,
                'first_seen': event.timestamp,
                'last_seen': event.timestamp,
                'total_events': 0,
                'actions': defaultdict(int),
                'transactions': [],
                'esg_interactions': [],
                'behavior_patterns': {},
                'preferences': {},
                'risk_scores': {},
            }
        
        profile = self.user_profiles[user_id]
        profile['last_seen'] = event.timestamp
        profile['total_events'] += 1
        
        # Atualizar baseado no tipo de evento
        if event.event_type == AnalyticsEventType.USER_ACTION:
            action = event.data.get('action', 'unknown')
            profile['actions'][action] += 1
        
        elif event.event_type == AnalyticsEventType.TRANSACTION:
            profile['transactions'].append({
                'timestamp': event.timestamp,
                'amount': event.data.get('amount', 0),
                'items': event.data.get('items', []),
                'esg_score': event.data.get('esg_score', 0)
            })
        
        elif event.event_type == AnalyticsEventType.ESG_INTERACTION:
            profile['esg_interactions'].append({
                'timestamp': event.timestamp,
                'interaction_type': event.data.get('type'),
                'score': event.data.get('score', 0)
            })
    
    async def _detect_patterns(self, event: AnalyticsEvent):
        """Detectar padrões nos eventos"""
        # Implementar detecção de padrões
        # Por exemplo: sequências de ações, horários preferenciais, etc.
        pass
    
    async def _update_system_metrics(self, event: AnalyticsEvent):
        """Atualizar métricas do sistema"""
        timestamp = event.timestamp
        hour_key = timestamp.replace(minute=0, second=0, microsecond=0)
        
        self.system_metrics['events_per_hour'].append((hour_key, 1))
        self.system_metrics['events_by_type'].append((timestamp, event.event_type.value))
        
        if event.user_id:
            self.system_metrics['active_users'].append((hour_key, event.user_id))
    
    async def _check_anomalies(self, event: AnalyticsEvent):
        """Verificar anomalias nos eventos"""
        # Implementar detecção de anomalias
        # Por exemplo: picos de atividade, comportamentos suspeitos, etc.
        pass
    
    async def _generate_user_insights(self, user_id: str) -> List[AnalyticsInsight]:
        """Gerar insights do usuário"""
        insights = []
        
        if user_id not in self.user_profiles:
            return insights
        
        profile = self.user_profiles[user_id]
        
        # Insight sobre atividade
        if profile['total_events'] > 100:
            insights.append(AnalyticsInsight(
                insight_id=self._generate_insight_id(),
                type="user_activity",
                title="Usuário Altamente Ativo",
                description=f"Este usuário tem {profile['total_events']} eventos registrados, indicando alto engajamento.",
                confidence=0.9,
                impact_score=0.8,
                data={'total_events': profile['total_events']},
                recommendations=["Oferecer programa de fidelidade", "Personalizar experiência"],
                created_at=datetime.now()
            ))
        
        # Insight sobre ESG
        if len(profile['esg_interactions']) > 10:
            avg_esg = np.mean([i['score'] for i in profile['esg_interactions']])
            insights.append(AnalyticsInsight(
                insight_id=self._generate_insight_id(),
                type="esg_engagement",
                title="Alto Engajamento ESG",
                description=f"Usuário demonstra interesse em sustentabilidade com score médio de {avg_esg:.1f}.",
                confidence=0.85,
                impact_score=0.7,
                data={'avg_esg_score': avg_esg, 'interactions': len(profile['esg_interactions'])},
                recommendations=["Destacar produtos sustentáveis", "Oferecer conteúdo educativo ESG"],
                created_at=datetime.now()
            ))
        
        return insights
    
    async def _generate_system_insights(self) -> List[AnalyticsInsight]:
        """Gerar insights do sistema"""
        insights = []
        
        # Insight sobre usuários ativos
        now = datetime.now()
        last_24h = now - timedelta(hours=24)
        recent_events = [e for e in self.processed_events if e.timestamp >= last_24h]
        active_users = len(set(e.user_id for e in recent_events if e.user_id))
        
        if active_users > 50:
            insights.append(AnalyticsInsight(
                insight_id=self._generate_insight_id(),
                type="system_activity",
                title="Alta Atividade do Sistema",
                description=f"{active_users} usuários ativos nas últimas 24 horas.",
                confidence=1.0,
                impact_score=0.9,
                data={'active_users_24h': active_users},
                recommendations=["Monitorar performance", "Preparar para escala"],
                created_at=datetime.now()
            ))
        
        # Insight sobre transações ESG
        esg_transactions = [e for e in recent_events 
                          if e.event_type == AnalyticsEventType.TRANSACTION 
                          and e.data.get('esg_score', 0) > 7]
        
        if len(esg_transactions) > 10:
            insights.append(AnalyticsInsight(
                insight_id=self._generate_insight_id(),
                type="esg_trend",
                title="Crescimento em Compras Sustentáveis",
                description=f"{len(esg_transactions)} transações com alto score ESG nas últimas 24h.",
                confidence=0.8,
                impact_score=0.85,
                data={'esg_transactions_24h': len(esg_transactions)},
                recommendations=["Expandir catálogo sustentável", "Criar campanhas ESG"],
                created_at=datetime.now()
            ))
        
        return insights
    
    async def _generate_prediction(self, user_id: str, prediction_type: PredictionType) -> Optional[PredictionResult]:
        """Gerar predição"""
        if user_id not in self.user_profiles:
            return None
        
        profile = self.user_profiles[user_id]
        
        # Predição simples baseada em padrões históricos
        if prediction_type == PredictionType.PURCHASE_INTENT:
            # Calcular intenção de compra baseada em atividade recente
            recent_actions = sum(1 for action, count in profile['actions'].items() 
                               if 'view' in action.lower() or 'cart' in action.lower())
            
            confidence = min(recent_actions / 10.0, 1.0)
            predicted_value = confidence > 0.6
            
            return PredictionResult(
                prediction_id=self._generate_prediction_id(),
                prediction_type=prediction_type,
                target=user_id,
                confidence=confidence,
                predicted_value=predicted_value,
                probability_distribution={'will_purchase': confidence, 'will_not_purchase': 1 - confidence},
                features_importance={'recent_views': 0.4, 'cart_actions': 0.6},
                created_at=datetime.now(),
                valid_until=datetime.now() + timedelta(hours=6)
            )
        
        elif prediction_type == PredictionType.CHURN_RISK:
            # Calcular risco de churn baseado em inatividade
            days_since_last_activity = (datetime.now() - profile['last_seen']).days
            churn_risk = min(days_since_last_activity / 30.0, 1.0)
            
            return PredictionResult(
                prediction_id=self._generate_prediction_id(),
                prediction_type=prediction_type,
                target=user_id,
                confidence=0.7,
                predicted_value=churn_risk,
                probability_distribution={'high_risk': churn_risk, 'low_risk': 1 - churn_risk},
                features_importance={'days_inactive': 0.8, 'total_events': 0.2},
                created_at=datetime.now(),
                valid_until=datetime.now() + timedelta(hours=24)
            )
        
        return None
    
    def _validate_event(self, event: AnalyticsEvent) -> bool:
        """Validar evento"""
        return (
            event.event_id and
            event.event_type and
            event.timestamp and
            isinstance(event.data, dict)
        )
    
    def _generate_event_id(self) -> str:
        """Gerar ID único para evento"""
        return f"evt_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(datetime.now()) % 10000:04d}"
    
    def _generate_insight_id(self) -> str:
        """Gerar ID único para insight"""
        return f"ins_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(datetime.now()) % 10000:04d}"
    
    def _generate_prediction_id(self) -> str:
        """Gerar ID único para predição"""
        return f"pred_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(datetime.now()) % 10000:04d}"
    
    async def cleanup_old_data(self):
        """Limpar dados antigos"""
        now = datetime.now()
        
        # Limpar insights expirados
        expired_insights = []
        for key, cached_insight in self.insights_cache.items():
            if cached_insight['expires_at'] <= now:
                expired_insights.append(key)
        
        for key in expired_insights:
            del self.insights_cache[key]
        
        # Limpar predições expiradas
        expired_predictions = []
        for key, prediction in self.predictions_cache.items():
            if prediction.valid_until <= now:
                expired_predictions.append(key)
        
        for key in expired_predictions:
            del self.predictions_cache[key]
        
        logger.debug(f"Limpeza concluída: {len(expired_insights)} insights e {len(expired_predictions)} predições removidas")

# Instância global
symbeon_analytics = SymbeonAnalyticsEngine()
