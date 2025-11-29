"""
Notification Service (Mock)
Envio de notificações (email/push) no MVP
"""
from typing import Dict, Any
import logging


logger = logging.getLogger("guardflow.notify")


class NotificationService:
    async def send_email(self, to: str, subject: str, body: str) -> Dict[str, Any]:
        logger.info(f"📧 Email simulado para {to}: {subject}")
        return {"success": True}

    async def send_push(self, user_id: str, title: str, message: str) -> Dict[str, Any]:
        logger.info(f"📲 Push simulado para {user_id}: {title}")
        return {"success": True}


__all__ = ["NotificationService"]


