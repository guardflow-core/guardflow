"""
Auth Service
Gerencia criação e sincronização de usuários com GuardPass
"""
from typing import Optional, Dict, Any
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User


class AuthService:
    """Serviços de autenticação e gerenciamento de usuário."""

    async def get_or_create_user(
        self,
        db: AsyncSession,
        guardpass_data: Dict[str, Any],
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> User:
        """
        Buscar usuário por guardpass_id ou email. Se não existir, criar.
        """
        guardpass_id = guardpass_data.get("guardpass_id") or guardpass_data.get("id")
        email = guardpass_data.get("email")
        name = guardpass_data.get("name") or email.split("@")[0]

        # Tentar por guardpass_id
        user = None
        if guardpass_id:
            result = await db.execute(select(User).where(User.guardpass_id == guardpass_id))
            user = result.scalar_one_or_none()

        # Fallback: procurar por email
        if not user and email:
            result = await db.execute(select(User).where(User.email == email))
            user = result.scalar_one_or_none()

        if user:
            # Atualizar dados básicos
            user.name = user.name or name
            user.guardpass_id = user.guardpass_id or guardpass_id
        else:
            # Criar novo usuário
            user = User(
                guardpass_id=guardpass_id or f"gp_{email}",
                email=email,
                name=name,
                is_active=True,
                is_verified=True,
            )
            db.add(user)

        # Atualizar metadados de acesso
        user.update_login_info(ip_address=ip_address, user_agent=user_agent)

        await db.flush()
        return user


__all__ = ["AuthService"]


