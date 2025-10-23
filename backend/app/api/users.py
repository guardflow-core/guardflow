"""
Users API Endpoints
API de gerenciamento de usuários com CRUD completo
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from slowapi import Limiter
from slowapi.util import get_remote_address
import logging
from datetime import datetime
from typing import Optional, List
from uuid import UUID

from app.database import get_db
from app.config import settings, AppMessages
from app.models.user import User
from app.schemas.auth import UserResponse, UserCreate, UserUpdate, UserListResponse
from app.services.auth_service import AuthService
from app.utils.security import get_current_user, require_permissions

# Logger
logger = logging.getLogger("guardflow.users")

# Router
router = APIRouter()

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

# Security
security = HTTPBearer()

# Services
auth_service = AuthService()

@router.get("/", response_model=UserListResponse)
@limiter.limit("30/minute")
async def list_users(
    request: Request,
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    search: Optional[str] = Query(None, description="Termo de busca"),
    role: Optional[str] = Query(None, description="Filtrar por role"),
    is_active: Optional[bool] = Query(None, description="Filtrar por status ativo"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Listar usuários com filtros e paginação
    """
    try:
        # Verificar permissões
        await require_permissions(current_user, ["admin", "manager"])
        
        logger.info(f"📋 Listando usuários - {current_user.email}")
        
        # Buscar usuários
        users, total = await auth_service.list_users(
            db=db,
            skip=skip,
            limit=limit,
            search=search,
            role=role,
            is_active=is_active
        )
        
        return UserListResponse(
            users=[UserResponse.from_orm(user) for user in users],
            total=total,
            skip=skip,
            limit=limit,
            has_more=skip + limit < total
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao listar usuários: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=AppMessages.SERVER_ERROR
        )

@router.get("/{user_id}", response_model=UserResponse)
@limiter.limit("60/minute")
async def get_user(
    request: Request,
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Obter usuário por ID
    """
    try:
        # Verificar se pode acessar (próprio usuário ou admin/manager)
        if str(user_id) != str(current_user.id) and not current_user.has_role(["admin", "manager"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso negado"
            )
        
        logger.info(f"👤 Buscando usuário: {user_id}")
        
        # Buscar usuário
        user = await auth_service.get_user_by_id(db=db, user_id=user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        return UserResponse.from_orm(user)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao obter usuário: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=AppMessages.SERVER_ERROR
        )

@router.post("/", response_model=UserResponse)
@limiter.limit("10/minute")
async def create_user(
    request: Request,
    user_data: UserCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Criar novo usuário
    """
    try:
        # Verificar permissões
        await require_permissions(current_user, ["admin"])
        
        logger.info(f"➕ Criando usuário: {user_data.email}")
        
        # Verificar se email já existe
        existing_user = await auth_service.get_user_by_email(db=db, email=user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado"
            )
        
        # Criar usuário
        user = await auth_service.create_user(
            db=db,
            user_data=user_data,
            created_by=current_user.id
        )
        
        logger.info(f"✅ Usuário criado: {user.email}")
        
        return UserResponse.from_orm(user)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao criar usuário: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=AppMessages.SERVER_ERROR
        )

@router.put("/{user_id}", response_model=UserResponse)
@limiter.limit("30/minute")
async def update_user(
    request: Request,
    user_id: UUID,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Atualizar usuário
    """
    try:
        # Verificar se pode editar (próprio usuário ou admin)
        if str(user_id) != str(current_user.id) and not current_user.has_role(["admin"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso negado"
            )
        
        logger.info(f"✏️ Atualizando usuário: {user_id}")
        
        # Buscar usuário
        user = await auth_service.get_user_by_id(db=db, user_id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        # Atualizar usuário
        updated_user = await auth_service.update_user(
            db=db,
            user=user,
            user_data=user_data,
            updated_by=current_user.id
        )
        
        logger.info(f"✅ Usuário atualizado: {updated_user.email}")
        
        return UserResponse.from_orm(updated_user)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao atualizar usuário: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=AppMessages.SERVER_ERROR
        )

@router.delete("/{user_id}")
@limiter.limit("10/minute")
async def delete_user(
    request: Request,
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Desativar usuário (soft delete)
    """
    try:
        # Verificar permissões
        await require_permissions(current_user, ["admin"])
        
        # Não permitir auto-exclusão
        if str(user_id) == str(current_user.id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não é possível desativar sua própria conta"
            )
        
        logger.info(f"🗑️ Desativando usuário: {user_id}")
        
        # Buscar usuário
        user = await auth_service.get_user_by_id(db=db, user_id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        # Desativar usuário
        await auth_service.deactivate_user(
            db=db,
            user=user,
            deactivated_by=current_user.id
        )
        
        logger.info(f"✅ Usuário desativado: {user.email}")
        
        return {
            "success": True,
            "message": "Usuário desativado com sucesso",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao desativar usuário: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=AppMessages.SERVER_ERROR
        )

@router.post("/{user_id}/activate")
@limiter.limit("10/minute")
async def activate_user(
    request: Request,
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Ativar usuário
    """
    try:
        # Verificar permissões
        await require_permissions(current_user, ["admin"])
        
        logger.info(f"✅ Ativando usuário: {user_id}")
        
        # Buscar usuário
        user = await auth_service.get_user_by_id(db=db, user_id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        # Ativar usuário
        await auth_service.activate_user(
            db=db,
            user=user,
            activated_by=current_user.id
        )
        
        logger.info(f"✅ Usuário ativado: {user.email}")
        
        return {
            "success": True,
            "message": "Usuário ativado com sucesso",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao ativar usuário: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=AppMessages.SERVER_ERROR
        )

@router.get("/{user_id}/stats")
@limiter.limit("60/minute")
async def get_user_stats(
    request: Request,
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Obter estatísticas do usuário
    """
    try:
        # Verificar se pode acessar (próprio usuário ou admin/manager)
        if str(user_id) != str(current_user.id) and not current_user.has_role(["admin", "manager"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso negado"
            )
        
        logger.info(f"📊 Estatísticas do usuário: {user_id}")
        
        # Buscar usuário
        user = await auth_service.get_user_by_id(db=db, user_id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        # Obter estatísticas
        stats = await auth_service.get_user_stats(db=db, user=user)
        
        return {
            "success": True,
            "message": "Estatísticas agilizadas! 📊",
            "data": stats
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao obter estatísticas: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=AppMessages.SERVER_ERROR
        )

@router.post("/{user_id}/change-role")
@limiter.limit("5/minute")
async def change_user_role(
    request: Request,
    user_id: UUID,
    new_role: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Alterar role do usuário
    """
    try:
        # Verificar permissões
        await require_permissions(current_user, ["admin"])
        
        # Validar role
        valid_roles = ["admin", "manager", "user", "guest"]
        if new_role not in valid_roles:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Role inválida. Roles válidas: {', '.join(valid_roles)}"
            )
        
        logger.info(f"🔄 Alterando role do usuário: {user_id} -> {new_role}")
        
        # Buscar usuário
        user = await auth_service.get_user_by_id(db=db, user_id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        # Alterar role
        await auth_service.change_user_role(
            db=db,
            user=user,
            new_role=new_role,
            changed_by=current_user.id
        )
        
        logger.info(f"✅ Role alterada: {user.email} -> {new_role}")
        
        return {
            "success": True,
            "message": f"Role alterada para {new_role}",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao alterar role: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=AppMessages.SERVER_ERROR
        )

# Endpoint de desenvolvimento (apenas debug)
if settings.DEBUG:
    @router.get("/debug/user-info")
    async def debug_user_info(
        current_user: User = Depends(get_current_user)
    ):
        """
        Debug: Informações do usuário atual (apenas desenvolvimento)
        """
        try:
            return {
                "success": True,
                "message": "Informações do usuário! 🔍",
                "data": {
                    "id": str(current_user.id),
                    "email": current_user.email,
                    "name": current_user.name,
                    "role": current_user.role,
                    "is_active": current_user.is_active,
                    "created_at": current_user.created_at.isoformat() if current_user.created_at else None,
                    "last_login": current_user.last_login.isoformat() if current_user.last_login else None
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro ao obter informações: {str(e)}",
                "error": str(e)
            }
