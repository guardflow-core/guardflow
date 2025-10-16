"""
GuardFlow Backend Configuration
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
import os

class Settings(BaseSettings):
    """Configurações da aplicação GuardFlow"""
    
    # App Info
    APP_NAME: str = "GuardFlow API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "GuardFlow - Agiliza aí suas compras! API Backend"
    
    # Environment
    ENVIRONMENT: str = Field(default="development")
    DEBUG: bool = Field(default=True)
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    API_BASE_URL: str = Field(default="http://localhost:8000")
    
    # Database
    DATABASE_URL: str = Field(default="sqlite+aiosqlite:///./guardflow_dev.db")
    
    # Redis Cache
    REDIS_URL: str = Field(default="redis://localhost:6379/0")
    
    # Security
    SECRET_KEY: str = Field(default="guardflow-super-secret-key-agiliza-ai-2024")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60*24*7)  # 7 days
    ALGORITHM: str = "HS256"
    
    # CORS
    ALLOWED_HOSTS: list[str] = ["*"]
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:19006",  # Expo
        "exp://localhost:19000",   # Expo
        "https://guardflow.app",
        "https://*.guardflow.app"
    ]
    
    # Google Vision API
    GOOGLE_CLOUD_PROJECT: str = Field(default="guardflow-vision", env="GOOGLE_CLOUD_PROJECT")
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = Field(default=None, env="GOOGLE_APPLICATION_CREDENTIALS")
    
    # Mercado Pago
    MERCADO_PAGO_ACCESS_TOKEN: str = Field(default="", env="MERCADO_PAGO_ACCESS_TOKEN")
    MERCADO_PAGO_PUBLIC_KEY: str = Field(default="", env="MERCADO_PAGO_PUBLIC_KEY")
    MERCADO_PAGO_WEBHOOK_SECRET: str = Field(default="", env="MERCADO_PAGO_WEBHOOK_SECRET")
    
    # GuardPass Integration (Simulado para MVP)
    GUARDPASS_API_URL: str = Field(default="https://api.guardpass.com/v1", env="GUARDPASS_API_URL")
    GUARDPASS_API_KEY: str = Field(default="guardpass-api-key-simulator", env="GUARDPASS_API_KEY")
    GUARDPASS_CLIENT_ID: str = Field(default="guardflow-client", env="GUARDPASS_CLIENT_ID")
    
    # File Upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: str = "uploads"
    ALLOWED_IMAGE_TYPES: list[str] = ["image/jpeg", "image/png", "image/webp"]
    
    # Scanner Settings
    VISION_CONFIDENCE_THRESHOLD: float = 0.7
    BARCODE_DETECTION_ENABLED: bool = True
    PRODUCT_RECOGNITION_ENABLED: bool = True
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_BURST: int = 10
    
    # Monitoring
    SENTRY_DSN: Optional[str] = Field(default=None, env="SENTRY_DSN")
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Email (para notificações)
    SMTP_SERVER: str = Field(default="smtp.gmail.com", env="SMTP_SERVER")
    SMTP_PORT: int = Field(default=587, env="SMTP_PORT")
    SMTP_USERNAME: str = Field(default="", env="SMTP_USERNAME")
    SMTP_PASSWORD: str = Field(default="", env="SMTP_PASSWORD")
    
    # Celery (background tasks)
    CELERY_BROKER_URL: str = Field(default="redis://localhost:6379/1", env="CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: str = Field(default="redis://localhost:6379/2", env="CELERY_RESULT_BACKEND")
    
    # Business Logic
    DEFAULT_STORE_RADIUS_KM: float = 50.0
    MAX_CART_ITEMS: int = 100
    CART_EXPIRY_HOURS: int = 24
    
    # ESG Settings (para integração GuardPass)
    ESG_CALCULATION_ENABLED: bool = True
    ESG_DEFAULT_SCORE: int = 50
    
    # Feature Flags
    ENABLE_PRODUCT_RECOMMENDATIONS: bool = True
    ENABLE_LOYALTY_PROGRAM: bool = True
    ENABLE_ESG_TRACKING: bool = True
    ENABLE_ANALYTICS: bool = True
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# Instância global das configurações
settings = Settings()

# Configurações específicas por ambiente
def get_database_url() -> str:
    """Retorna URL do banco baseada no ambiente"""
    # Em produção, respeitar variável de ambiente obrigatoriamente
    if settings.ENVIRONMENT == "production":
        return settings.DATABASE_URL
    
    # Em desenvolvimento/teste, permitir fallback para SQLite local
    db_url = os.getenv("DATABASE_URL", settings.DATABASE_URL)
    if settings.ENVIRONMENT == "testing":
        if db_url.startswith("sqlite"):
            return db_url.replace("guardflow_dev.db", "guardflow_test.db")
        return db_url.replace("guardflow_db", "guardflow_test_db")
    return db_url

def get_cors_origins() -> list[str]:
    """Retorna origens CORS baseadas no ambiente"""
    if settings.ENVIRONMENT == "production":
        return [
            "https://guardflow.app",
            "https://www.guardflow.app",
            "https://admin.guardflow.app"
        ]
    else:
        return settings.CORS_ORIGINS

def is_development() -> bool:
    """Verifica se está em ambiente de desenvolvimento"""
    return settings.ENVIRONMENT == "development"

def is_production() -> bool:
    """Verifica se está em ambiente de produção"""
    return settings.ENVIRONMENT == "production"

# Configurações de logging
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[{asctime}] {levelname} in {name}: {message}",
            "style": "{",
        },
        "json": {
            "format": '{{"timestamp": "{asctime}", "level": "{levelname}", "logger": "{name}", "message": "{message}"}}',
            "style": "{",
        },
        "safe": {
            "format": "[{asctime}] {levelname} in {name}: {message}",
            "style": "{",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "safe" if is_development() else "json",
            "level": settings.LOG_LEVEL,
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/guardflow.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "formatter": "json",
            "level": "INFO",
            "encoding": "utf-8",
        }
    },
    "loggers": {
        "guardflow": {
            "handlers": ["console", "file"],
            "level": settings.LOG_LEVEL,
            "propagate": False,
        },
        "uvicorn": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        }
    }
}

# Mensagens da aplicação (tema "Agiliza aí")
class AppMessages:
    # Sucesso
    PRODUCT_SCANNED_SUCCESS = "Agilizou! Produto reconhecido com sucesso! 🚀"
    PRODUCT_ADDED_TO_CART = "Produto agilizado para o carrinho! ⚡"
    PAYMENT_CREATED = "PIX gerado! Agiliza aí o pagamento! 💳"
    PAYMENT_CONFIRMED = "Pagamento agilizado! Compra confirmada! ✅"
    CHECKOUT_COMPLETED = "Agilizou! Checkout finalizado com sucesso! 🎉"
    
    # Informações
    SCANNING_PRODUCT = "Agilizando reconhecimento do produto... 🔍"
    PROCESSING_PAYMENT = "Agilizando seu pagamento... ⏱️"
    CART_UPDATED = "Carrinho agilizado! 🛒"
    
    # Erros amigáveis
    PRODUCT_NOT_RECOGNIZED = "Ops! Não conseguimos agilizar esse produto. Tenta de novo? 😅"
    PAYMENT_FAILED = "Pagamento não agilizou. Vamos tentar novamente! 🔄"
    CART_EMPTY = "Carrinho vazio! Vamos agilizar algumas compras? 🛍️"
    SERVER_ERROR = "Algo deu errado, mas vamos agilizar isso! Tenta de novo em instantes. ⚡"
    
    # Autenticação
    LOGIN_SUCCESS = "Agilizou! Bem-vindo ao GuardFlow! 🎯"
    LOGIN_FAILED = "Credenciais não agilizaram. Verifica aí! 🔐"
    TOKEN_EXPIRED = "Sessão expirou. Agiliza aí o login novamente! ⏰"
    
    # Validação
    INVALID_BARCODE = "Código de barras não agilizou. Verifica se está legível! 📱"
    INVALID_IMAGE = "Imagem não agilizou. Tenta uma foto mais clara! 📸"
    STORE_NOT_FOUND = "Supermercado não encontrado. Agiliza aí a seleção! 🏪"

# Constantes da aplicação
class AppConstants:
    # Códigos de status personalizados
    STATUS_SCANNING = "scanning"
    STATUS_RECOGNIZED = "recognized"
    STATUS_ADDED_TO_CART = "added_to_cart"
    STATUS_PAYMENT_PENDING = "payment_pending"
    STATUS_PAYMENT_CONFIRMED = "payment_confirmed"
    STATUS_COMPLETED = "completed"
    
    # Tipos de produtos
    PRODUCT_CATEGORIES = [
        "Alimentício",
        "Bebidas",
        "Limpeza",
        "Higiene",
        "Padaria",
        "Açougue",
        "Hortifruti",
        "Outros"
    ]
    
    # Métodos de pagamento
    PAYMENT_METHODS = [
        "pix",
        "credit_card",
        "debit_card",
        "guardpass_tokens"
    ]
    
    # Estados do carrinho
    CART_STATUS_ACTIVE = "active"
    CART_STATUS_CHECKOUT = "checkout"
    CART_STATUS_COMPLETED = "completed"
    CART_STATUS_ABANDONED = "abandoned"

# Exportar configurações
__all__ = [
    "settings",
    "get_database_url",
    "get_cors_origins",
    "is_development",
    "is_production",
    "LOGGING_CONFIG",
    "AppMessages",
    "AppConstants"
]
