"""
Payment API Endpoints  
API para pagamentos PIX e processamento de transações
DIA 1 MVP - Versão funcional com Mercado Pago simulado
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from slowapi import Limiter
from slowapi.util import get_remote_address
import logging
from datetime import datetime, timedelta
from typing import Optional
import uuid
import qrcode
import io
import base64

from app.database import get_db
from app.config import settings, AppMessages
from app.models.user import User
from app.models.cart import Cart
from app.models.transaction import Transaction
from app.utils.security import get_current_user

# Logger
logger = logging.getLogger("guardflow.payment")

# Router
router = APIRouter()

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

@router.post("/create-pix")
@limiter.limit("10/minute")
async def create_pix_payment(
    request: Request,
    cart_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Criar pagamento PIX
    MVP: Simulação realista do Mercado Pago
    """
    try:
        logger.info(f"💳 Criando PIX: usuário {current_user.email}, carrinho {cart_id}")
        
        # Buscar carrinho
        from sqlalchemy import select
        result = await db.execute(
            select(Cart).where(
                Cart.id == cart_id,
                Cart.user_id == current_user.id,
                Cart.status == "active"
            )
        )
        cart = result.scalar_one_or_none()
        
        if not cart:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Carrinho não encontrado ou não ativo! 🛒"
            )
        
        if cart.is_empty:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=AppMessages.CART_EMPTY
            )
        
        # Criar transação
        transaction = Transaction(
            cart_id=cart.id,
            user_id=current_user.id,
            store_id=cart.store_id,
            amount=cart.total_amount,
            final_amount=cart.final_amount,
            payment_method="pix",
            payment_gateway="mercado_pago_mock",
            status="pending"
        )
        
        # Gerar PIX mock
        pix_data = await _generate_mock_pix(transaction, db)
        
        transaction.payment_id = pix_data["payment_id"]
        transaction.pix_qr_code = pix_data["qr_code"]
        transaction.pix_code = pix_data["pix_code"]
        transaction.pix_expiration = pix_data["expiration"]
        transaction.transaction_data = pix_data["raw_data"]
        
        # Gerar número da nota fiscal
        transaction.generate_invoice_number()
        
        # Calcular impacto ESG
        transaction.calculate_esg_impact()
        
        db.add(transaction)
        
        # Atualizar carrinho para checkout
        cart.start_checkout()
        
        await db.commit()
        
        logger.info(f"✅ PIX criado: {transaction.payment_id}")
        
        return {
            "success": True,
            "message": AppMessages.PAYMENT_CREATED,
            "data": {
                "transaction_id": str(transaction.id),
                "payment_id": transaction.payment_id,
                "pix_code": transaction.pix_code,
                "qr_code": transaction.pix_qr_code,
                "amount": transaction.final_amount,
                "expires_at": transaction.pix_expiration.isoformat() if transaction.pix_expiration else None,
                "invoice_number": transaction.invoice_number,
                "status": transaction.status
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao criar PIX: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=AppMessages.SERVER_ERROR
        )

@router.get("/status/{transaction_id}")
async def get_payment_status(
    transaction_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Verificar status do pagamento
    """
    try:
        from sqlalchemy import select
        
        result = await db.execute(
            select(Transaction).where(
                Transaction.id == transaction_id,
                Transaction.user_id == current_user.id
            )
        )
        transaction = result.scalar_one_or_none()
        
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transação não encontrada! 🔍"
            )
        
        # Simular mudança de status baseada no tempo (para demo)
        if transaction.status == "pending":
            await _simulate_payment_status_change(transaction, db)
        
        logger.info(f"📊 Status consultado: {transaction.status}")
        
        return {
            "success": True,
            "message": f"Status agilizado! Pagamento {transaction.status} ⚡",
            "data": {
                "transaction_id": str(transaction.id),
                "payment_id": transaction.payment_id,
                "status": transaction.status,
                "amount": transaction.final_amount,
                "payment_method": transaction.payment_method_display,
                "created_at": transaction.created_at.isoformat() if transaction.created_at else None,
                "paid_at": transaction.paid_at.isoformat() if transaction.paid_at else None,
                "invoice_number": transaction.invoice_number
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao consultar status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao consultar status do pagamento"
        )

@router.post("/confirm/{transaction_id}")
async def confirm_payment(
    transaction_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Confirmar pagamento manualmente (para demo)
    Em produção seria via webhook
    """
    try:
        from sqlalchemy import select
        
        result = await db.execute(
            select(Transaction).where(
                Transaction.id == transaction_id,
                Transaction.user_id == current_user.id
            )
        )
        transaction = result.scalar_one_or_none()
        
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transação não encontrada! 🔍"
            )
        
        if transaction.status != "pending":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Pagamento já está {transaction.status}! ✅"
            )
        
        # Confirmar pagamento
        transaction.mark_as_paid({
            "confirmed_at": datetime.utcnow().isoformat(),
            "confirmation_method": "manual_demo",
            "pix_txid": f"PIX{uuid.uuid4().hex[:8].upper()}"
        })
        
        # Completar carrinho
        if transaction.cart:
            transaction.cart.complete_checkout()
        
        # Atualizar estatísticas do usuário
        current_user.increment_purchases(transaction.get_final_amount_float())
        current_user.add_loyalty_points(transaction.gst_tokens_earned)
        
        # Atualizar estatísticas da loja
        if transaction.store:
            transaction.store.add_transaction(transaction.get_final_amount_float())
        
        await db.commit()
        
        logger.info(f"✅ Pagamento confirmado: {transaction.payment_id}")
        
        return {
            "success": True,
            "message": AppMessages.PAYMENT_CONFIRMED,
            "data": {
                "transaction_id": str(transaction.id),
                "status": transaction.status,
                "amount": transaction.final_amount,
                "gst_tokens_earned": transaction.gst_tokens_earned,
                "esg_score": transaction.esg_score,
                "invoice_number": transaction.invoice_number,
                "paid_at": transaction.paid_at.isoformat() if transaction.paid_at else None
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao confirmar pagamento: {str(e)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao confirmar pagamento"
        )

@router.get("/history")
async def get_payment_history(
    limit: int = 20,
    offset: int = 0,
    status_filter: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Histórico de pagamentos do usuário
    """
    try:
        from sqlalchemy import select, desc
        
        query = select(Transaction).where(
            Transaction.user_id == current_user.id
        )
        
        if status_filter:
            query = query.where(Transaction.status == status_filter)
        
        query = query.order_by(desc(Transaction.created_at)).limit(limit).offset(offset)
        
        result = await db.execute(query)
        transactions = result.scalars().all()
        
        history = [transaction.to_dict() for transaction in transactions]
        
        return {
            "success": True,
            "message": f"Histórico agilizado! {len(history)} transações encontradas 💳",
            "data": {
                "transactions": history,
                "total": len(history),
                "limit": limit,
                "offset": offset,
                "status_filter": status_filter
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao buscar histórico: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar histórico de pagamentos"
        )

@router.post("/webhook")
async def payment_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Webhook para receber notificações do Mercado Pago
    MVP: Simulação básica
    """
    try:
        # Em produção, validar assinatura do webhook
        webhook_data = await request.json()
        
        logger.info(f"📨 Webhook recebido: {webhook_data.get('type', 'unknown')}")
        
        # Processar notificação
        if webhook_data.get("type") == "payment":
            payment_id = webhook_data.get("data", {}).get("id")
            
            if payment_id:
                # Buscar transação pelo payment_id
                from sqlalchemy import select
                result = await db.execute(
                    select(Transaction).where(Transaction.payment_id == payment_id)
                )
                transaction = result.scalar_one_or_none()
                
                if transaction and transaction.status == "pending":
                    # Atualizar status baseado no webhook
                    webhook_status = webhook_data.get("data", {}).get("status", "pending")
                    
                    if webhook_status == "approved":
                        transaction.mark_as_paid(webhook_data)
                        if transaction.cart:
                            transaction.cart.complete_checkout()
                        await db.commit()
                        
                        logger.info(f"✅ Pagamento aprovado via webhook: {payment_id}")
                    elif webhook_status in ["cancelled", "rejected"]:
                        transaction.mark_as_failed(f"Webhook status: {webhook_status}")
                        await db.commit()
                        
                        logger.info(f"❌ Pagamento rejeitado via webhook: {payment_id}")
        
        return {"success": True, "message": "Webhook processado com sucesso"}
        
    except Exception as e:
        logger.error(f"❌ Erro no webhook: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao processar webhook"
        )

# Funções auxiliares

async def _generate_mock_pix(transaction: Transaction, db: AsyncSession) -> dict:
    """
    Gerar dados PIX mock para demonstração
    """
    try:
        # Gerar IDs únicos
        payment_id = f"MP{uuid.uuid4().hex[:12].upper()}"
        pix_code = f"00020126{len(payment_id):02d}{payment_id}5204000053039865802BR5925GUARDFLOW PAGAMENTOS LTDA6009SAO PAULO62{len(str(transaction.id)):02d}{str(transaction.id)[:10]}6304"
        
        # Gerar QR Code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(pix_code)
        qr.make(fit=True)
        
        # Converter QR Code para base64
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        # Expiração em 30 minutos
        expiration = datetime.utcnow() + timedelta(minutes=30)
        
        return {
            "payment_id": payment_id,
            "pix_code": pix_code,
            "qr_code": f"data:image/png;base64,{qr_code_base64}",
            "expiration": expiration,
            "raw_data": {
                "id": payment_id,
                "status": "pending",
                "transaction_amount": float(transaction.final_amount),
                "currency_id": "BRL",
                "description": f"GuardFlow - Compra {transaction.invoice_number}",
                "payment_method_id": "pix",
                "date_created": datetime.utcnow().isoformat(),
                "date_of_expiration": expiration.isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao gerar PIX mock: {str(e)}")
        raise

async def _simulate_payment_status_change(transaction: Transaction, db: AsyncSession):
    """
    Simular mudança de status para demo
    Baseado no tempo desde criação
    """
    try:
        if not transaction.created_at:
            return
        
        # Simular aprovação automática após 2 minutos (para demo)
        time_elapsed = datetime.utcnow() - transaction.created_at
        
        if time_elapsed.total_seconds() > 120:  # 2 minutos
            # 80% chance de aprovação automática
            import random
            if random.random() < 0.8:
                transaction.mark_as_paid({
                    "auto_approved_at": datetime.utcnow().isoformat(),
                    "simulation": True,
                    "pix_txid": f"PIX{uuid.uuid4().hex[:8].upper()}"
                })
                
                if transaction.cart:
                    transaction.cart.complete_checkout()
                
                await db.commit()
                
                logger.info(f"✅ Pagamento aprovado automaticamente (demo): {transaction.payment_id}")
        
    except Exception as e:
        logger.error(f"❌ Erro na simulação de status: {str(e)}")

# Endpoints de desenvolvimento
if settings.DEBUG:
    @router.post("/simulate-approval/{transaction_id}")
    async def simulate_payment_approval(
        transaction_id: str,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
    ):
        """
        Simular aprovação de pagamento (apenas desenvolvimento)
        """
        try:
            from sqlalchemy import select
            
            result = await db.execute(
                select(Transaction).where(
                    Transaction.id == transaction_id,
                    Transaction.user_id == current_user.id
                )
            )
            transaction = result.scalar_one_or_none()
            
            if not transaction:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Transação não encontrada"
                )
            
            if transaction.status != "pending":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Transação já está {transaction.status}"
                )
            
            # Simular aprovação
            transaction.mark_as_paid({
                "simulated_at": datetime.utcnow().isoformat(),
                "simulation": True,
                "method": "development_simulation"
            })
            
            if transaction.cart:
                transaction.cart.complete_checkout()
            
            await db.commit()
            
            return {
                "success": True,
                "message": "Pagamento simulado com sucesso! 🎭",
                "data": {
                    "transaction_id": str(transaction.id),
                    "status": transaction.status,
                    "simulated": True
                }
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ Erro na simulação: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao simular pagamento"
            )

