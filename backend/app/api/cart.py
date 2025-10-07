"""
Cart API Endpoints
API para gerenciamento de carrinho de compras
DIA 1 MVP - Carrinho inteligente funcional
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from slowapi import Limiter
from slowapi.util import get_remote_address
import logging
from datetime import datetime
from typing import Optional

from app.database import get_db
from app.config import settings, AppMessages
from app.models.user import User
from app.models.cart import Cart, CartItem
from app.models.product import Product
from app.models.store import Store
from app.utils.security import get_current_user

# Logger
logger = logging.getLogger("guardflow.cart")

# Router
router = APIRouter()

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

@router.get("/")
async def get_current_cart(
    store_id: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Obter carrinho atual do usuário
    """
    try:
        from sqlalchemy import select, and_
        
        # Buscar carrinho ativo
        query = select(Cart).where(
            and_(
                Cart.user_id == current_user.id,
                Cart.status == "active"
            )
        )
        
        if store_id:
            query = query.where(Cart.store_id == store_id)
        
        result = await db.execute(query)
        cart = result.scalar_one_or_none()
        
        if not cart:
            # Criar carrinho se não existir
            if not store_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="store_id é obrigatório para criar novo carrinho! 🏪"
                )
            
            cart = Cart(
                user_id=current_user.id,
                store_id=store_id,
                status="active"
            )
            
            db.add(cart)
            await db.commit()
            
            logger.info(f"🛒 Novo carrinho criado: usuário {current_user.email}")
        
        cart_data = cart.to_dict(include_items=True)
        
        return {
            "success": True,
            "message": f"Carrinho agilizado! {cart.total_items} itens 🛒",
            "data": cart_data,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao obter carrinho: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=AppMessages.SERVER_ERROR
        )

@router.post("/add")
@limiter.limit("30/minute")
async def add_item_to_cart(
    request: Request,
    product_id: str,
    quantity: int = 1,
    store_id: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Adicionar item ao carrinho
    """
    try:
        if quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantidade deve ser maior que zero! 📊"
            )
        
        if quantity > 50:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantidade máxima é 50 unidades por item! 📦"
            )
        
        # Buscar produto
        from sqlalchemy import select
        product_result = await db.execute(
            select(Product).where(
                Product.id == product_id,
                Product.is_active == True,
                Product.is_available == True
            )
        )
        product = product_result.scalar_one_or_none()
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto não encontrado ou indisponível! 🔍"
            )
        
        # Buscar ou criar carrinho
        cart_result = await db.execute(
            select(Cart).where(
                Cart.user_id == current_user.id,
                Cart.status == "active"
            )
        )
        cart = cart_result.scalar_one_or_none()
        
        if not cart:
            if not store_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="store_id é obrigatório para criar carrinho! 🏪"
                )
            
            cart = Cart(
                user_id=current_user.id,
                store_id=store_id,
                status="active"
            )
            db.add(cart)
            await db.flush()  # Para obter o ID
        
        # Verificar limite de itens
        if cart.total_items >= settings.MAX_CART_ITEMS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Carrinho cheio! Máximo {settings.MAX_CART_ITEMS} itens 🛒"
            )
        
        # Adicionar item
        cart.add_item(
            product_id=product_id,
            quantity=quantity,
            unit_price=product.get_price_float()
        )
        
        await db.commit()
        
        logger.info(f"✅ Item adicionado: {product.name} x{quantity} ao carrinho de {current_user.email}")
        
        return {
            "success": True,
            "message": AppMessages.PRODUCT_ADDED_TO_CART,
            "data": {
                "cart": cart.to_dict(include_items=True),
                "added_item": {
                    "product": product.to_dict(),
                    "quantity": quantity,
                    "unit_price": product.price,
                    "total_price": str(quantity * product.get_price_float())
                }
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao adicionar item: {str(e)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=AppMessages.SERVER_ERROR
        )

@router.put("/update/{item_id}")
async def update_cart_item(
    item_id: str,
    quantity: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Atualizar quantidade de item no carrinho
    """
    try:
        if quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantidade deve ser maior que zero! Use DELETE para remover 📊"
            )
        
        if quantity > 50:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantidade máxima é 50 unidades! 📦"
            )
        
        # Buscar item do carrinho
        from sqlalchemy import select, and_
        result = await db.execute(
            select(CartItem).join(Cart).where(
                and_(
                    CartItem.id == item_id,
                    Cart.user_id == current_user.id,
                    Cart.status == "active"
                )
            )
        )
        cart_item = result.scalar_one_or_none()
        
        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item não encontrado no carrinho! 🔍"
            )
        
        # Atualizar quantidade
        old_quantity = cart_item.quantity
        cart_item.update_quantity(quantity)
        
        # Recalcular totais do carrinho
        cart_item.cart.recalculate_totals()
        
        await db.commit()
        
        logger.info(f"✅ Item atualizado: {cart_item.product.name if cart_item.product else 'Produto'} de {old_quantity} para {quantity}")
        
        return {
            "success": True,
            "message": AppMessages.CART_UPDATED,
            "data": {
                "cart": cart_item.cart.to_dict(include_items=True),
                "updated_item": cart_item.to_dict()
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao atualizar item: {str(e)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=AppMessages.SERVER_ERROR
        )

@router.delete("/remove/{item_id}")
async def remove_cart_item(
    item_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Remover item do carrinho
    """
    try:
        # Buscar item do carrinho
        from sqlalchemy import select, and_
        result = await db.execute(
            select(CartItem).join(Cart).where(
                and_(
                    CartItem.id == item_id,
                    Cart.user_id == current_user.id,
                    Cart.status == "active"
                )
            )
        )
        cart_item = result.scalar_one_or_none()
        
        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item não encontrado no carrinho! 🔍"
            )
        
        cart = cart_item.cart
        product_name = cart_item.product.name if cart_item.product else "Produto"
        
        # Remover item
        await db.delete(cart_item)
        
        # Recalcular totais
        cart.recalculate_totals()
        
        await db.commit()
        
        logger.info(f"🗑️ Item removido: {product_name} do carrinho de {current_user.email}")
        
        return {
            "success": True,
            "message": f"Item removido do carrinho! {product_name} 🗑️",
            "data": {
                "cart": cart.to_dict(include_items=True),
                "removed_item": product_name
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao remover item: {str(e)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=AppMessages.SERVER_ERROR
        )

@router.delete("/clear")
async def clear_cart(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Limpar carrinho completamente
    """
    try:
        # Buscar carrinho ativo
        from sqlalchemy import select
        result = await db.execute(
            select(Cart).where(
                Cart.user_id == current_user.id,
                Cart.status == "active"
            )
        )
        cart = result.scalar_one_or_none()
        
        if not cart:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Carrinho não encontrado! 🛒"
            )
        
        if cart.is_empty:
            return {
                "success": True,
                "message": "Carrinho já estava vazio! 🛒",
                "data": cart.to_dict(),
                "timestamp": datetime.utcnow().isoformat()
            }
        
        items_count = cart.total_items
        
        # Limpar carrinho
        cart.clear()
        
        await db.commit()
        
        logger.info(f"🧹 Carrinho limpo: {items_count} itens removidos de {current_user.email}")
        
        return {
            "success": True,
            "message": f"Carrinho limpo! {items_count} itens removidos 🧹",
            "data": {
                "cart": cart.to_dict(),
                "removed_items_count": items_count
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao limpar carrinho: {str(e)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=AppMessages.SERVER_ERROR
        )

@router.post("/checkout")
async def start_checkout(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Iniciar processo de checkout
    """
    try:
        # Buscar carrinho ativo
        from sqlalchemy import select
        result = await db.execute(
            select(Cart).where(
                Cart.user_id == current_user.id,
                Cart.status == "active"
            )
        )
        cart = result.scalar_one_or_none()
        
        if not cart:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Carrinho não encontrado! 🛒"
            )
        
        if not cart.can_checkout:
            if cart.is_empty:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=AppMessages.CART_EMPTY
                )
            elif cart.is_expired():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Carrinho expirado! Crie um novo 🕐"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Carrinho não pode ser finalizado no momento ⚠️"
                )
        
        # Iniciar checkout
        cart.start_checkout()
        
        await db.commit()
        
        logger.info(f"🛒 Checkout iniciado: {cart.total_items} itens, R$ {cart.final_amount}")
        
        return {
            "success": True,
            "message": AppMessages.CHECKOUT_COMPLETED.replace("finalizado", "iniciado"),
            "data": {
                "cart": cart.to_dict(include_items=True),
                "checkout_info": {
                    "total_items": cart.total_items,
                    "total_amount": cart.total_amount,
                    "final_amount": cart.final_amount,
                    "expires_at": cart.expires_at.isoformat() if cart.expires_at else None,
                    "esg_score": cart.esg_score,
                    "esg_level": cart.esg_level
                }
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro no checkout: {str(e)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=AppMessages.SERVER_ERROR
        )

@router.get("/summary")
async def get_cart_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Resumo do carrinho com métricas ESG
    """
    try:
        # Buscar carrinho ativo
        from sqlalchemy import select
        result = await db.execute(
            select(Cart).where(
                Cart.user_id == current_user.id,
                Cart.status == "active"
            )
        )
        cart = result.scalar_one_or_none()
        
        if not cart:
            return {
                "success": True,
                "message": "Nenhum carrinho ativo encontrado 🛒",
                "data": {
                    "has_cart": False,
                    "summary": None
                },
                "timestamp": datetime.utcnow().isoformat()
            }
        
        # Calcular métricas ESG
        organic_items = sum(1 for item in cart.items if item.product and item.product.is_organic)
        local_items = sum(1 for item in cart.items if item.product and item.product.is_local_product)
        recyclable_items = sum(1 for item in cart.items if item.product and item.product.is_recyclable)
        
        # Calcular economia potencial
        total_savings = sum(item.calculate_savings() for item in cart.items)
        
        summary = {
            "has_cart": True,
            "cart_id": str(cart.id),
            "totals": {
                "items": cart.total_items,
                "amount": cart.total_amount,
                "discount": cart.discount_amount,
                "final_amount": cart.final_amount,
                "savings": str(round(total_savings, 2))
            },
            "sustainability": {
                "esg_score": cart.esg_score,
                "esg_level": cart.esg_level,
                "carbon_footprint_kg": cart.carbon_footprint_kg,
                "organic_items": organic_items,
                "local_items": local_items,
                "recyclable_items": recyclable_items
            },
            "status": {
                "can_checkout": cart.can_checkout,
                "is_expired": cart.is_expired(),
                "expires_at": cart.expires_at.isoformat() if cart.expires_at else None
            }
        }
        
        return {
            "success": True,
            "message": f"Resumo agilizado! {cart.total_items} itens, ESG {cart.esg_score} 📊",
            "data": summary,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter resumo: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter resumo do carrinho"
        )
