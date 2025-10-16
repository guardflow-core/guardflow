"""
GuardFlow Database Configuration
Configuração do banco PostgreSQL com SQLAlchemy
"""
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from databases import Database
import logging
from typing import AsyncGenerator

from app.config import settings, get_database_url

# Logger
logger = logging.getLogger("guardflow.database")

# Metadata para convenções de naming
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

# Base para modelos
Base = declarative_base(metadata=metadata)

# Database URL
DATABASE_URL = get_database_url()

# Engine síncrono (para migrations)
if DATABASE_URL.startswith("sqlite"):
    sync_engine = create_engine(
        DATABASE_URL.replace("+aiosqlite", ""),
        echo=settings.DEBUG,
        connect_args={"check_same_thread": False},
    )
else:
    sync_engine = create_engine(
        DATABASE_URL.replace("+asyncpg", ""),
        echo=settings.DEBUG,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        pool_recycle=300,
    )

# Engine assíncrono (para aplicação)
async_engine = create_async_engine(
    DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)

# Session makers
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_engine
)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Database instance para queries diretas
database = Database(DATABASE_URL)

# Dependency para FastAPI
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency que fornece sessão de banco de dados para FastAPI
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"❌ Erro na sessão de banco: {str(e)}")
            raise
        finally:
            await session.close()

# Dependency síncrona (para casos específicos)
def get_sync_db() -> Session:
    """
    Dependency síncrona para casos específicos
    """
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

# Inicialização do banco
async def init_db():
    """
    Inicializar conexão com banco de dados
    """
    try:
        # Conectar ao banco
        await database.connect()
        logger.info("✅ Conectado ao PostgreSQL - Banco agilizado!")
        
        # Testar conexão
        test_query = "SELECT 1" if not DATABASE_URL.startswith("sqlite") else "SELECT 1"
        await database.execute(test_query)
        logger.info("✅ Teste de conexão bem-sucedido!")
        
        # Criar tabelas se não existirem (apenas em desenvolvimento)
        if settings.DEBUG:
            async with async_engine.begin() as conn:
                # Importar modelos para criar tabelas
                from app.models import user, product, store, cart, transaction
                await conn.run_sync(Base.metadata.create_all)
                logger.info("✅ Tabelas criadas/verificadas!")
                
    except Exception as e:
        logger.error(f"❌ Erro ao conectar ao banco: {str(e)}")
        raise

async def close_db():
    """
    Fechar conexões com banco de dados
    """
    try:
        await database.disconnect()
        await async_engine.dispose()
        logger.info("✅ Conexões de banco fechadas!")
    except Exception as e:
        logger.error(f"❌ Erro ao fechar conexões: {str(e)}")

# Utilitários de banco
class DatabaseUtils:
    """Utilitários para operações de banco"""
    
    @staticmethod
    async def health_check() -> dict:
        """
        Verificar saúde do banco de dados
        """
        try:
            # Teste de conexão
            result = await database.fetch_one("SELECT 1 as health_check")
            
            # Informações do banco
            version_result = await database.fetch_one("SELECT version()")
            
            return {
                "status": "healthy",
                "message": "Banco agilizando perfeitamente! ✅",
                "connection": "active",
                "version": version_result[0] if version_result else "unknown",
                "pool_size": async_engine.pool.size(),
                "checked_out": async_engine.pool.checkedout(),
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"Banco não agilizou: {str(e)} ❌",
                "error": str(e)
            }
    
    @staticmethod
    async def get_table_counts() -> dict:
        """
        Obter contagem de registros das principais tabelas
        """
        try:
            counts = {}
            
            tables = [
                "users",
                "stores", 
                "products",
                "carts",
                "cart_items",
                "transactions",
                "scan_events"
            ]
            
            for table in tables:
                try:
                    result = await database.fetch_one(f"SELECT COUNT(*) as count FROM {table}")
                    counts[table] = result[0] if result else 0
                except:
                    counts[table] = "N/A"
            
            return {
                "status": "success",
                "message": "Contagens agilizadas! 📊",
                "counts": counts
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Erro ao contar registros: {str(e)}",
                "error": str(e)
            }
    
    @staticmethod
    async def cleanup_expired_carts():
        """
        Limpar carrinhos expirados (background task)
        """
        try:
            query = """
                UPDATE carts 
                SET status = 'abandoned'
                WHERE status = 'active' 
                AND created_at < NOW() - INTERVAL '%s hours'
            """ % settings.CART_EXPIRY_HOURS
            
            result = await database.execute(query)
            
            logger.info(f"✅ {result} carrinhos expirados marcados como abandonados")
            
            return {
                "status": "success",
                "message": f"Agilizou! {result} carrinhos expirados limpos",
                "affected_rows": result
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao limpar carrinhos: {str(e)}")
            return {
                "status": "error",
                "message": f"Erro na limpeza: {str(e)}",
                "error": str(e)
            }

# Context manager para transações
class DatabaseTransaction:
    """Context manager para transações de banco"""
    
    def __init__(self):
        self.session = None
    
    async def __aenter__(self) -> AsyncSession:
        self.session = AsyncSessionLocal()
        return self.session
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.session.rollback()
            logger.error(f"❌ Transação revertida: {exc_val}")
        else:
            await self.session.commit()
            logger.debug("✅ Transação confirmada")
        
        await self.session.close()

# Funções de conveniência
async def execute_query(query: str, values: dict = None):
    """Executar query direta no banco"""
    try:
        if values:
            return await database.execute(query, values)
        else:
            return await database.execute(query)
    except Exception as e:
        logger.error(f"❌ Erro ao executar query: {str(e)}")
        raise

async def fetch_one(query: str, values: dict = None):
    """Buscar um registro"""
    try:
        if values:
            return await database.fetch_one(query, values)
        else:
            return await database.fetch_one(query)
    except Exception as e:
        logger.error(f"❌ Erro ao buscar registro: {str(e)}")
        raise

async def fetch_all(query: str, values: dict = None):
    """Buscar múltiplos registros"""
    try:
        if values:
            return await database.fetch_all(query, values)
        else:
            return await database.fetch_all(query)
    except Exception as e:
        logger.error(f"❌ Erro ao buscar registros: {str(e)}")
        raise

# Exportar dependências principais
__all__ = [
    "Base",
    "get_db",
    "get_sync_db", 
    "init_db",
    "close_db",
    "database",
    "async_engine",
    "sync_engine",
    "DatabaseUtils",
    "DatabaseTransaction",
    "execute_query",
    "fetch_one",
    "fetch_all"
]



