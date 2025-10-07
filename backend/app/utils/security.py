"""
Security Utilities
JWT auth helpers e dependências para FastAPI
"""
from typing import Optional, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config import settings, AppMessages
from app.models.user import User
from app.database import get_db


security_scheme = HTTPBearer(auto_error=False)


def create_access_token(data: dict, expires_minutes: Optional[int] = None) -> str:
    """Criar token JWT de acesso."""
    to_encode = data.copy()
    from datetime import datetime, timedelta

    expire_delta = timedelta(
        minutes=expires_minutes if expires_minutes is not None else settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    expire = datetime.utcnow() + expire_delta
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


def decode_token(token: str) -> dict:
    """Decodificar token JWT."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=AppMessages.TOKEN_EXPIRED
        ) from exc


async def _get_user_by_id(user_id: str, db: AsyncSession) -> Optional[User]:
    from uuid import UUID

    try:
        # Garantir UUID válido
        _ = UUID(str(user_id))
    except Exception:
        return None

    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_current_user(
    credentials_or_token: Union[HTTPAuthorizationCredentials, str, None] = Depends(security_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Dependência para obter o usuário atual.
    - Pode ser usada como Depends(get_current_user) (com HTTP Bearer)
    - Ou chamada diretamente passando uma string de token
    """
    token: Optional[str]

    if isinstance(credentials_or_token, HTTPAuthorizationCredentials):
        token = credentials_or_token.credentials
    elif isinstance(credentials_or_token, str):
        token = credentials_or_token
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais ausentes"
        )

    payload = decode_token(token)
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

    user = await _get_user_by_id(user_id, db)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário inválido ou inativo"
        )

    return user


__all__ = [
    "create_access_token",
    "decode_token",
    "get_current_user",
]


