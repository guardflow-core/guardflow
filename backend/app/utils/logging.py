"""
GuardFlow Logging Utilities
Utilitários de logging com suporte a emojis e UTF-8
"""
import logging
import sys
from typing import Any, Dict, Optional
import re

class SafeConsoleHandler(logging.StreamHandler):
    """
    Handler de console que remove emojis para evitar problemas de encoding
    """
    
    # Regex para remover emojis
    EMOJI_PATTERN = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"  # dingbats
        "\U000024C2-\U0001F251"  # enclosed characters
        "]+", 
        flags=re.UNICODE
    )
    
    def __init__(self, stream=None):
        super().__init__(stream or sys.stdout)
        self.setLevel(logging.INFO)
    
    def emit(self, record: logging.LogRecord) -> None:
        """
        Emite o log removendo emojis para evitar problemas de encoding
        """
        try:
            # Remove emojis da mensagem
            if hasattr(record, 'msg') and isinstance(record.msg, str):
                record.msg = self.EMOJI_PATTERN.sub('', record.msg)
            
            # Remove emojis dos argumentos
            if hasattr(record, 'args') and record.args:
                new_args = []
                for arg in record.args:
                    if isinstance(arg, str):
                        new_args.append(self.EMOJI_PATTERN.sub('', arg))
                    else:
                        new_args.append(arg)
                record.args = tuple(new_args)
            
            super().emit(record)
        except Exception:
            # Se houver erro, tenta emitir sem modificações
            try:
                super().emit(record)
            except Exception:
                # Se ainda houver erro, ignora o log
                pass

class SafeFileHandler(logging.handlers.RotatingFileHandler):
    """
    Handler de arquivo com encoding UTF-8
    """
    
    def __init__(self, filename: str, **kwargs):
        # Força encoding UTF-8
        kwargs['encoding'] = 'utf-8'
        super().__init__(filename, **kwargs)

def get_safe_logging_config() -> Dict[str, Any]:
    """
    Retorna configuração de logging segura para Windows
    """
    return {
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
                "()": "app.utils.logging.SafeConsoleHandler",
                "formatter": "safe",
                "level": "INFO",
            },
            "file": {
                "()": "app.utils.logging.SafeFileHandler",
                "filename": "logs/guardflow.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "formatter": "json",
                "level": "INFO",
            }
        },
        "loggers": {
            "guardflow": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            }
        }
    }

def setup_logging():
    """
    Configura logging com handlers seguros
    """
    import logging.config
    config = get_safe_logging_config()
    logging.config.dictConfig(config)
    
    # Configura encoding UTF-8 para stdout/stderr
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')

# Função para criar mensagens seguras
def safe_message(message: str) -> str:
    """
    Remove emojis de uma mensagem para logging seguro
    """
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"  # dingbats
        "\U000024C2-\U0001F251"  # enclosed characters
        "]+", 
        flags=re.UNICODE
    )
    return emoji_pattern.sub('', message)

# Mensagens seguras para logging
class SafeMessages:
    """Mensagens sem emojis para logging seguro"""
    
    # Sucesso
    PRODUCT_SCANNED_SUCCESS = "Agilizou! Produto reconhecido com sucesso!"
    PRODUCT_ADDED_TO_CART = "Produto agilizado para o carrinho!"
    PAYMENT_CREATED = "PIX gerado! Agiliza ai o pagamento!"
    PAYMENT_CONFIRMED = "Pagamento agilizado! Compra confirmada!"
    CHECKOUT_COMPLETED = "Agilizou! Checkout finalizado com sucesso!"
    
    # Informações
    SCANNING_PRODUCT = "Agilizando reconhecimento do produto..."
    PROCESSING_PAYMENT = "Agilizando seu pagamento..."
    CART_UPDATED = "Carrinho agilizado!"
    
    # Erros amigáveis
    PRODUCT_NOT_RECOGNIZED = "Ops! Nao conseguimos agilizar esse produto. Tenta de novo?"
    PAYMENT_FAILED = "Pagamento nao agilizou. Vamos tentar novamente!"
    CART_EMPTY = "Carrinho vazio! Vamos agilizar algumas compras?"
    SERVER_ERROR = "Algo deu errado, mas vamos agilizar isso! Tenta de novo em instantes."
    
    # Autenticação
    LOGIN_SUCCESS = "Agilizou! Bem-vindo ao GuardFlow!"
    LOGIN_FAILED = "Credenciais nao agilizaram. Verifica ai!"
    TOKEN_EXPIRED = "Sessao expirou. Agiliza ai o login novamente!"
    
    # Validação
    INVALID_BARCODE = "Codigo de barras nao agilizou. Verifica se esta legivel!"
    INVALID_IMAGE = "Imagem nao agilizou. Tenta uma foto mais clara!"
    STORE_NOT_FOUND = "Supermercado nao encontrado. Agiliza ai a selecao!"
