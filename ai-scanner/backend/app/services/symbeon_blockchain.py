"""
GuardFlow SYMBEON Blockchain Engine
Motor blockchain para tokens ESG, rastreabilidade e governança descentralizada
"""

import asyncio
import json
import logging
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
from collections import defaultdict, deque
import time

logger = logging.getLogger(__name__)

class TransactionType(Enum):
    ESG_TOKEN_MINT = "esg_token_mint"
    ESG_TOKEN_TRANSFER = "esg_token_transfer"
    ESG_TOKEN_BURN = "esg_token_burn"
    PRODUCT_REGISTRATION = "product_registration"
    SUPPLY_CHAIN_EVENT = "supply_chain_event"
    ESG_CERTIFICATION = "esg_certification"
    GOVERNANCE_VOTE = "governance_vote"
    CARBON_OFFSET = "carbon_offset"

class TokenType(Enum):
    ESG_SCORE_TOKEN = "ESG"  # Token baseado em score ESG
    CARBON_CREDIT = "CCR"    # Crédito de carbono
    GOVERNANCE_TOKEN = "GOV" # Token de governança
    UTILITY_TOKEN = "UTL"    # Token utilitário

@dataclass
class BlockchainTransaction:
    tx_id: str
    tx_type: TransactionType
    from_address: Optional[str]
    to_address: Optional[str]
    amount: float
    token_type: TokenType
    data: Dict[str, Any]
    timestamp: datetime
    signature: Optional[str] = None
    gas_fee: float = 0.0
    status: str = "pending"  # pending, confirmed, failed
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            **asdict(self),
            'tx_type': self.tx_type.value,
            'token_type': self.token_type.value,
            'timestamp': self.timestamp.isoformat()
        }

@dataclass
class Block:
    block_number: int
    previous_hash: str
    merkle_root: str
    timestamp: datetime
    transactions: List[BlockchainTransaction]
    nonce: int = 0
    hash: Optional[str] = None
    validator: Optional[str] = None
    
    def calculate_hash(self) -> str:
        """Calcular hash do bloco"""
        block_string = f"{self.block_number}{self.previous_hash}{self.merkle_root}{self.timestamp.isoformat()}{self.nonce}"
        for tx in self.transactions:
            block_string += tx.tx_id
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'block_number': self.block_number,
            'previous_hash': self.previous_hash,
            'merkle_root': self.merkle_root,
            'timestamp': self.timestamp.isoformat(),
            'transactions': [tx.to_dict() for tx in self.transactions],
            'nonce': self.nonce,
            'hash': self.hash,
            'validator': self.validator
        }

@dataclass
class ESGToken:
    token_id: str
    token_type: TokenType
    owner_address: str
    amount: float
    esg_score: float
    metadata: Dict[str, Any]
    created_at: datetime
    last_updated: datetime
    locked_until: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            **asdict(self),
            'token_type': self.token_type.value,
            'created_at': self.created_at.isoformat(),
            'last_updated': self.last_updated.isoformat(),
            'locked_until': self.locked_until.isoformat() if self.locked_until else None
        }

@dataclass
class WalletAddress:
    address: str
    public_key: str
    private_key_hash: str
    owner_id: str
    created_at: datetime
    balances: Dict[str, float]  # token_type -> amount
    transaction_history: List[str]  # tx_ids
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'address': self.address,
            'public_key': self.public_key,
            'owner_id': self.owner_id,
            'created_at': self.created_at.isoformat(),
            'balances': self.balances,
            'transaction_count': len(self.transaction_history)
        }

class SymbeonBlockchainEngine:
    def __init__(self):
        self.blockchain: List[Block] = []
        self.pending_transactions: deque = deque()
        self.wallets: Dict[str, WalletAddress] = {}
        self.tokens: Dict[str, ESGToken] = {}
        self.validators: List[str] = []
        self.consensus_threshold = 0.67  # 67% dos validadores
        self.block_time = 10  # segundos
        self.max_transactions_per_block = 100
        self.gas_price = 0.001  # Taxa base
        
        # Métricas
        self.total_supply = defaultdict(float)
        self.circulating_supply = defaultdict(float)
        self.burned_tokens = defaultdict(float)
        
        # Inicializar blockchain
        self._create_genesis_block()
        
        # Iniciar mineração
        asyncio.create_task(self._start_mining_loop())
    
    def _create_genesis_block(self):
        """Criar bloco gênesis"""
        genesis_block = Block(
            block_number=0,
            previous_hash="0" * 64,
            merkle_root="0" * 64,
            timestamp=datetime.now(),
            transactions=[],
            validator="genesis"
        )
        genesis_block.hash = genesis_block.calculate_hash()
        self.blockchain.append(genesis_block)
        logger.info("Bloco gênesis criado")
    
    async def create_wallet(self, owner_id: str) -> WalletAddress:
        """Criar nova carteira"""
        try:
            # Gerar endereço único
            address = self._generate_address()
            public_key = self._generate_public_key()
            private_key_hash = self._generate_private_key_hash()
            
            wallet = WalletAddress(
                address=address,
                public_key=public_key,
                private_key_hash=private_key_hash,
                owner_id=owner_id,
                created_at=datetime.now(),
                balances={token_type.value: 0.0 for token_type in TokenType},
                transaction_history=[]
            )
            
            self.wallets[address] = wallet
            logger.info(f"Carteira criada: {address} para {owner_id}")
            return wallet
            
        except Exception as e:
            logger.error(f"Erro ao criar carteira: {e}")
            raise
    
    async def mint_esg_tokens(self, to_address: str, amount: float, esg_score: float, metadata: Dict[str, Any]) -> str:
        """Mintar tokens ESG"""
        try:
            # Validar endereço
            if to_address not in self.wallets:
                raise ValueError(f"Endereço não encontrado: {to_address}")
            
            # Criar transação de mint
            tx = BlockchainTransaction(
                tx_id=self._generate_tx_id(),
                tx_type=TransactionType.ESG_TOKEN_MINT,
                from_address=None,  # Mint não tem origem
                to_address=to_address,
                amount=amount,
                token_type=TokenType.ESG_SCORE_TOKEN,
                data={
                    'esg_score': esg_score,
                    'metadata': metadata,
                    'mint_reason': metadata.get('reason', 'esg_achievement')
                },
                timestamp=datetime.now(),
                gas_fee=self._calculate_gas_fee(TransactionType.ESG_TOKEN_MINT)
            )
            
            # Adicionar à fila de transações pendentes
            self.pending_transactions.append(tx)
            
            logger.info(f"Token ESG mintado: {amount} para {to_address}")
            return tx.tx_id
            
        except Exception as e:
            logger.error(f"Erro ao mintar tokens ESG: {e}")
            raise
    
    async def transfer_tokens(self, from_address: str, to_address: str, amount: float, token_type: TokenType) -> str:
        """Transferir tokens entre endereços"""
        try:
            # Validar endereços
            if from_address not in self.wallets:
                raise ValueError(f"Endereço de origem não encontrado: {from_address}")
            if to_address not in self.wallets:
                raise ValueError(f"Endereço de destino não encontrado: {to_address}")
            
            # Verificar saldo
            from_wallet = self.wallets[from_address]
            if from_wallet.balances.get(token_type.value, 0) < amount:
                raise ValueError("Saldo insuficiente")
            
            # Criar transação
            tx = BlockchainTransaction(
                tx_id=self._generate_tx_id(),
                tx_type=TransactionType.ESG_TOKEN_TRANSFER,
                from_address=from_address,
                to_address=to_address,
                amount=amount,
                token_type=token_type,
                data={'transfer_type': 'standard'},
                timestamp=datetime.now(),
                gas_fee=self._calculate_gas_fee(TransactionType.ESG_TOKEN_TRANSFER)
            )
            
            self.pending_transactions.append(tx)
            
            logger.info(f"Transferência criada: {amount} {token_type.value} de {from_address} para {to_address}")
            return tx.tx_id
            
        except Exception as e:
            logger.error(f"Erro na transferência: {e}")
            raise
    
    async def register_product(self, product_data: Dict[str, Any], registrar_address: str) -> str:
        """Registrar produto na blockchain"""
        try:
            tx = BlockchainTransaction(
                tx_id=self._generate_tx_id(),
                tx_type=TransactionType.PRODUCT_REGISTRATION,
                from_address=registrar_address,
                to_address=None,
                amount=0.0,
                token_type=TokenType.UTILITY_TOKEN,
                data={
                    'product_id': product_data.get('id'),
                    'name': product_data.get('name'),
                    'barcode': product_data.get('barcode'),
                    'esg_score': product_data.get('esg_score'),
                    'supply_chain': product_data.get('supply_chain', []),
                    'certifications': product_data.get('certifications', []),
                    'carbon_footprint': product_data.get('carbon_footprint'),
                    'registration_timestamp': datetime.now().isoformat()
                },
                timestamp=datetime.now(),
                gas_fee=self._calculate_gas_fee(TransactionType.PRODUCT_REGISTRATION)
            )
            
            self.pending_transactions.append(tx)
            
            logger.info(f"Produto registrado: {product_data.get('name')} por {registrar_address}")
            return tx.tx_id
            
        except Exception as e:
            logger.error(f"Erro ao registrar produto: {e}")
            raise
    
    async def add_supply_chain_event(self, product_id: str, event_data: Dict[str, Any], recorder_address: str) -> str:
        """Adicionar evento da cadeia de suprimentos"""
        try:
            tx = BlockchainTransaction(
                tx_id=self._generate_tx_id(),
                tx_type=TransactionType.SUPPLY_CHAIN_EVENT,
                from_address=recorder_address,
                to_address=None,
                amount=0.0,
                token_type=TokenType.UTILITY_TOKEN,
                data={
                    'product_id': product_id,
                    'event_type': event_data.get('type'),
                    'location': event_data.get('location'),
                    'timestamp': event_data.get('timestamp', datetime.now().isoformat()),
                    'actor': event_data.get('actor'),
                    'details': event_data.get('details', {}),
                    'verification': event_data.get('verification', {})
                },
                timestamp=datetime.now(),
                gas_fee=self._calculate_gas_fee(TransactionType.SUPPLY_CHAIN_EVENT)
            )
            
            self.pending_transactions.append(tx)
            
            logger.info(f"Evento de supply chain adicionado para produto {product_id}")
            return tx.tx_id
            
        except Exception as e:
            logger.error(f"Erro ao adicionar evento de supply chain: {e}")
            raise
    
    async def issue_esg_certification(self, entity_id: str, certification_data: Dict[str, Any], issuer_address: str) -> str:
        """Emitir certificação ESG"""
        try:
            tx = BlockchainTransaction(
                tx_id=self._generate_tx_id(),
                tx_type=TransactionType.ESG_CERTIFICATION,
                from_address=issuer_address,
                to_address=None,
                amount=0.0,
                token_type=TokenType.GOVERNANCE_TOKEN,
                data={
                    'entity_id': entity_id,
                    'certification_type': certification_data.get('type'),
                    'score': certification_data.get('score'),
                    'criteria': certification_data.get('criteria', {}),
                    'valid_until': certification_data.get('valid_until'),
                    'issuer': certification_data.get('issuer'),
                    'audit_trail': certification_data.get('audit_trail', [])
                },
                timestamp=datetime.now(),
                gas_fee=self._calculate_gas_fee(TransactionType.ESG_CERTIFICATION)
            )
            
            self.pending_transactions.append(tx)
            
            logger.info(f"Certificação ESG emitida para {entity_id}")
            return tx.tx_id
            
        except Exception as e:
            logger.error(f"Erro ao emitir certificação ESG: {e}")
            raise
    
    async def get_wallet_balance(self, address: str) -> Dict[str, float]:
        """Obter saldo da carteira"""
        if address not in self.wallets:
            raise ValueError(f"Endereço não encontrado: {address}")
        
        return self.wallets[address].balances.copy()
    
    async def get_transaction_history(self, address: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Obter histórico de transações"""
        if address not in self.wallets:
            raise ValueError(f"Endereço não encontrado: {address}")
        
        wallet = self.wallets[address]
        tx_ids = wallet.transaction_history[-limit:]
        
        transactions = []
        for block in self.blockchain:
            for tx in block.transactions:
                if tx.tx_id in tx_ids:
                    transactions.append(tx.to_dict())
        
        return sorted(transactions, key=lambda x: x['timestamp'], reverse=True)
    
    async def get_product_history(self, product_id: str) -> List[Dict[str, Any]]:
        """Obter histórico completo de um produto"""
        history = []
        
        for block in self.blockchain:
            for tx in block.transactions:
                if (tx.tx_type in [TransactionType.PRODUCT_REGISTRATION, TransactionType.SUPPLY_CHAIN_EVENT] and
                    tx.data.get('product_id') == product_id):
                    history.append({
                        'block_number': block.block_number,
                        'transaction': tx.to_dict(),
                        'block_timestamp': block.timestamp.isoformat()
                    })
        
        return sorted(history, key=lambda x: x['block_timestamp'])
    
    async def get_blockchain_stats(self) -> Dict[str, Any]:
        """Obter estatísticas da blockchain"""
        total_transactions = sum(len(block.transactions) for block in self.blockchain)
        
        return {
            'total_blocks': len(self.blockchain),
            'total_transactions': total_transactions,
            'total_wallets': len(self.wallets),
            'pending_transactions': len(self.pending_transactions),
            'total_supply': dict(self.total_supply),
            'circulating_supply': dict(self.circulating_supply),
            'burned_tokens': dict(self.burned_tokens),
            'last_block_time': self.blockchain[-1].timestamp.isoformat() if self.blockchain else None,
            'network_hash_rate': self._calculate_network_hash_rate(),
            'average_block_time': self._calculate_average_block_time()
        }
    
    async def _start_mining_loop(self):
        """Loop principal de mineração"""
        while True:
            try:
                await self._mine_block()
                await asyncio.sleep(self.block_time)
            except Exception as e:
                logger.error(f"Erro na mineração: {e}")
                await asyncio.sleep(1)
    
    async def _mine_block(self):
        """Minerar novo bloco"""
        if not self.pending_transactions:
            return
        
        # Coletar transações pendentes
        transactions = []
        while len(transactions) < self.max_transactions_per_block and self.pending_transactions:
            tx = self.pending_transactions.popleft()
            
            # Processar transação
            if await self._process_transaction(tx):
                tx.status = "confirmed"
                transactions.append(tx)
            else:
                tx.status = "failed"
                logger.warning(f"Transação falhou: {tx.tx_id}")
        
        if not transactions:
            return
        
        # Criar novo bloco
        previous_block = self.blockchain[-1]
        new_block = Block(
            block_number=len(self.blockchain),
            previous_hash=previous_block.hash,
            merkle_root=self._calculate_merkle_root(transactions),
            timestamp=datetime.now(),
            transactions=transactions,
            validator="system"  # Em uma implementação real, seria selecionado
        )
        
        # Calcular hash do bloco
        new_block.hash = new_block.calculate_hash()
        
        # Adicionar à blockchain
        self.blockchain.append(new_block)
        
        logger.info(f"Bloco #{new_block.block_number} minerado com {len(transactions)} transações")
    
    async def _process_transaction(self, tx: BlockchainTransaction) -> bool:
        """Processar transação individual"""
        try:
            if tx.tx_type == TransactionType.ESG_TOKEN_MINT:
                return await self._process_mint_transaction(tx)
            elif tx.tx_type == TransactionType.ESG_TOKEN_TRANSFER:
                return await self._process_transfer_transaction(tx)
            elif tx.tx_type in [TransactionType.PRODUCT_REGISTRATION, 
                               TransactionType.SUPPLY_CHAIN_EVENT,
                               TransactionType.ESG_CERTIFICATION]:
                return await self._process_data_transaction(tx)
            
            return False
            
        except Exception as e:
            logger.error(f"Erro ao processar transação {tx.tx_id}: {e}")
            return False
    
    async def _process_mint_transaction(self, tx: BlockchainTransaction) -> bool:
        """Processar transação de mint"""
        if tx.to_address not in self.wallets:
            return False
        
        # Atualizar saldo
        wallet = self.wallets[tx.to_address]
        wallet.balances[tx.token_type.value] += tx.amount
        wallet.transaction_history.append(tx.tx_id)
        
        # Atualizar supply
        self.total_supply[tx.token_type.value] += tx.amount
        self.circulating_supply[tx.token_type.value] += tx.amount
        
        return True
    
    async def _process_transfer_transaction(self, tx: BlockchainTransaction) -> bool:
        """Processar transação de transferência"""
        if (tx.from_address not in self.wallets or 
            tx.to_address not in self.wallets):
            return False
        
        from_wallet = self.wallets[tx.from_address]
        to_wallet = self.wallets[tx.to_address]
        
        # Verificar saldo
        if from_wallet.balances.get(tx.token_type.value, 0) < tx.amount:
            return False
        
        # Executar transferência
        from_wallet.balances[tx.token_type.value] -= tx.amount
        to_wallet.balances[tx.token_type.value] += tx.amount
        
        # Atualizar histórico
        from_wallet.transaction_history.append(tx.tx_id)
        to_wallet.transaction_history.append(tx.tx_id)
        
        return True
    
    async def _process_data_transaction(self, tx: BlockchainTransaction) -> bool:
        """Processar transação de dados"""
        # Para transações de dados, apenas validar estrutura
        return bool(tx.data and isinstance(tx.data, dict))
    
    def _calculate_merkle_root(self, transactions: List[BlockchainTransaction]) -> str:
        """Calcular raiz de Merkle das transações"""
        if not transactions:
            return "0" * 64
        
        tx_hashes = [hashlib.sha256(tx.tx_id.encode()).hexdigest() for tx in transactions]
        
        while len(tx_hashes) > 1:
            if len(tx_hashes) % 2 == 1:
                tx_hashes.append(tx_hashes[-1])
            
            new_hashes = []
            for i in range(0, len(tx_hashes), 2):
                combined = tx_hashes[i] + tx_hashes[i + 1]
                new_hashes.append(hashlib.sha256(combined.encode()).hexdigest())
            
            tx_hashes = new_hashes
        
        return tx_hashes[0]
    
    def _calculate_gas_fee(self, tx_type: TransactionType) -> float:
        """Calcular taxa de gas"""
        base_fees = {
            TransactionType.ESG_TOKEN_MINT: 0.001,
            TransactionType.ESG_TOKEN_TRANSFER: 0.0005,
            TransactionType.PRODUCT_REGISTRATION: 0.002,
            TransactionType.SUPPLY_CHAIN_EVENT: 0.001,
            TransactionType.ESG_CERTIFICATION: 0.003,
        }
        return base_fees.get(tx_type, 0.001)
    
    def _calculate_network_hash_rate(self) -> float:
        """Calcular hash rate da rede (simulado)"""
        return len(self.blockchain) * 1000.0  # Simulação
    
    def _calculate_average_block_time(self) -> float:
        """Calcular tempo médio entre blocos"""
        if len(self.blockchain) < 2:
            return 0.0
        
        total_time = 0.0
        for i in range(1, len(self.blockchain)):
            time_diff = (self.blockchain[i].timestamp - self.blockchain[i-1].timestamp).total_seconds()
            total_time += time_diff
        
        return total_time / (len(self.blockchain) - 1)
    
    def _generate_address(self) -> str:
        """Gerar endereço único"""
        return f"0x{hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()[:40]}"
    
    def _generate_public_key(self) -> str:
        """Gerar chave pública (simulada)"""
        return hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()
    
    def _generate_private_key_hash(self) -> str:
        """Gerar hash da chave privada"""
        return hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()
    
    def _generate_tx_id(self) -> str:
        """Gerar ID único para transação"""
        return f"0x{hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()}"

# Instância global
symbeon_blockchain = SymbeonBlockchainEngine()
