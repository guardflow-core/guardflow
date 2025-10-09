"""
Monetization API Endpoints
API para linhas de monetização do GuardFlow
- Conversão de notas fiscais em dinheiro
- Conversão em ativos ESG
- Sistema de comissões e taxas
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from slowapi import Limiter
from slowapi.util import get_remote_address
import logging
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import uuid
from decimal import Decimal

from app.database import get_db
from app.config import settings, AppMessages
from app.models.user import User
from app.models.transaction import Transaction
from app.models.monetization import InvoiceConversion, ESGAsset, MonetizationTransaction
from app.utils.security import get_current_user

# Logger
logger = logging.getLogger("guardflow.monetization")

# Router
router = APIRouter()

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

@router.post("/invoice/convert-to-cash")
@limiter.limit("5/minute")
async def convert_invoice_to_cash(
    request: Request,
    transaction_id: str,
    conversion_amount: Optional[float] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Converter nota fiscal em dinheiro
    Linha de monetização principal do GuardFlow
    """
    try:
        logger.info(f"💰 Convertendo nota fiscal: {transaction_id}")

        # Buscar transação
        from sqlalchemy import select
        result = await db.execute(
            select(Transaction).where(
                Transaction.id == transaction_id,
                Transaction.user_id == current_user.id,
                Transaction.status == "completed"
            )
        )
        transaction = result.scalar_one_or_none()

        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transação não encontrada ou não paga! 🔍"
            )

        if not transaction.invoice_number:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Transação não possui nota fiscal válida! 📄"
            )

        # Verificar se já foi convertida
        existing_conversion = await db.execute(
            select(InvoiceConversion).where(
                InvoiceConversion.transaction_id == transaction_id,
                InvoiceConversion.status.in_(["pending", "completed"])
            )
        )
        if existing_conversion.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nota fiscal já foi convertida! ✅"
            )

        # Calcular valor de conversão (padrão: 95% do valor da nota)
        if not conversion_amount:
            conversion_amount = float(transaction.final_amount) * 0.95

        # Calcular taxa do GuardFlow (5% do valor)
        guardflow_fee = conversion_amount * 0.05
        user_amount = conversion_amount - guardflow_fee

        # Criar conversão
        conversion = InvoiceConversion(
            transaction_id=transaction.id,
            user_id=current_user.id,
            invoice_number=transaction.invoice_number,
            original_amount=float(transaction.final_amount),
            conversion_amount=conversion_amount,
            guardflow_fee=guardflow_fee,
            user_amount=user_amount,
            status="pending",
            conversion_type="cash"
        )

        db.add(conversion)

        # Criar transação de monetização
        monetization = MonetizationTransaction(
            user_id=current_user.id,
            transaction_id=transaction.id,
            amount=guardflow_fee,
            transaction_type="invoice_conversion_fee",
            description=f"Taxa de conversão - Nota {transaction.invoice_number}",
            status="pending"
        )

        db.add(monetization)

        await db.commit()

        logger.info(f"✅ Conversão criada: {conversion.id}")

        return {
            "success": True,
            "message": "Conversão de nota fiscal iniciada! 💰",
            "data": {
                "conversion_id": str(conversion.id),
                "invoice_number": transaction.invoice_number,
                "original_amount": float(transaction.final_amount),
                "conversion_amount": conversion_amount,
                "guardflow_fee": guardflow_fee,
                "user_amount": user_amount,
                "status": conversion.status,
                "estimated_completion": (datetime.utcnow() + timedelta(hours=24)).isoformat()
            },
            "timestamp": datetime.utcnow().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao converter nota fiscal: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao converter nota fiscal"
        )

@router.post("/invoice/convert-to-esg")
@limiter.limit("5/minute")
async def convert_invoice_to_esg(
    request: Request,
    transaction_id: str,
    esg_category: str = "sustainability",
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Converter nota fiscal em ativos ESG
    Linha de monetização sustentável do GuardFlow
    """
    try:
        logger.info(f"🌱 Convertendo nota fiscal em ESG: {transaction_id}")

        # Buscar transação
        from sqlalchemy import select
        result = await db.execute(
            select(Transaction).where(
                Transaction.id == transaction_id,
                Transaction.user_id == current_user.id,
                Transaction.status == "completed"
            )
        )
        transaction = result.scalar_one_or_none()

        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transação não encontrada ou não paga! 🔍"
            )

        # Calcular valor ESG otimizado com bônus de sustentabilidade
        base_esg_score = transaction.esg_score / 100.0  # 0.4 a 0.9
        
        # Bônus de sustentabilidade baseado nos produtos
        sustainability_bonus = await _calculate_sustainability_bonus(transaction)
        
        # Bônus de carbono baseado no impacto ambiental
        carbon_bonus = await _calculate_carbon_bonus(transaction)
        
        # Multiplicador ESG otimizado (máximo 1.0)
        esg_multiplier = min(base_esg_score + sustainability_bonus + carbon_bonus, 1.0)
        esg_value = float(transaction.final_amount) * esg_multiplier

        # Criar ativo ESG
        esg_asset = ESGAsset(
            transaction_id=transaction.id,
            user_id=current_user.id,
            invoice_number=transaction.invoice_number,
            original_amount=float(transaction.final_amount),
            esg_value=esg_value,
            esg_score=transaction.esg_score,
            category=esg_category,
            status="active",
            carbon_offset_kg=transaction.carbon_footprint_kg or 0.0
        )

        db.add(esg_asset)

        # Criar conversão
        conversion = InvoiceConversion(
            transaction_id=transaction.id,
            user_id=current_user.id,
            invoice_number=transaction.invoice_number,
            original_amount=float(transaction.final_amount),
            conversion_amount=esg_value,
            guardflow_fee=0.0,  # Sem taxa para ESG
            user_amount=esg_value,
            status="completed",
            conversion_type="esg"
        )

        db.add(conversion)

        # Atualizar tokens ESG do usuário
        current_user.add_esg_tokens(int(esg_value))

        await db.commit()

        logger.info(f"✅ Ativo ESG criado: {esg_asset.id}")

        return {
            "success": True,
            "message": "Nota fiscal convertida em ativo ESG! 🌱",
            "data": {
                "esg_asset_id": str(esg_asset.id),
                "invoice_number": transaction.invoice_number,
                "original_amount": float(transaction.final_amount),
                "esg_value": esg_value,
                "esg_score": transaction.esg_score,
                "carbon_offset_kg": esg_asset.carbon_offset_kg,
                "category": esg_category,
                "status": esg_asset.status
            },
            "timestamp": datetime.utcnow().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao converter em ESG: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao converter em ativo ESG"
        )

@router.get("/conversions/history")
async def get_conversion_history(
    limit: int = 20,
    offset: int = 0,
    conversion_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Histórico de conversões do usuário
    """
    try:
        from sqlalchemy import select, desc

        query = select(InvoiceConversion).where(
            InvoiceConversion.user_id == current_user.id
        )

        if conversion_type:
            query = query.where(InvoiceConversion.conversion_type == conversion_type)

        query = query.order_by(desc(InvoiceConversion.created_at)).limit(limit).offset(offset)

        result = await db.execute(query)
        conversions = result.scalars().all()

        history = []
        for conversion in conversions:
            history.append({
                "id": str(conversion.id),
                "invoice_number": conversion.invoice_number,
                "conversion_type": conversion.conversion_type,
                "original_amount": conversion.original_amount,
                "conversion_amount": conversion.conversion_amount,
                "guardflow_fee": conversion.guardflow_fee,
                "user_amount": conversion.user_amount,
                "status": conversion.status,
                "created_at": conversion.created_at.isoformat() if conversion.created_at else None,
                "completed_at": conversion.completed_at.isoformat() if conversion.completed_at else None
            })

        return {
            "success": True,
            "message": f"Histórico agilizado! {len(history)} conversões encontradas 💰",
            "data": {
                "conversions": history,
                "total": len(history),
                "limit": limit,
                "offset": offset,
                "conversion_type": conversion_type
            },
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        logger.error(f"❌ Erro ao buscar histórico: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar histórico de conversões"
        )

@router.get("/esg-assets")
async def get_esg_assets(
    limit: int = 20,
    offset: int = 0,
    category: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Listar ativos ESG do usuário
    """
    try:
        from sqlalchemy import select, desc

        query = select(ESGAsset).where(
            ESGAsset.user_id == current_user.id,
            ESGAsset.status == "active"
        )

        if category:
            query = query.where(ESGAsset.category == category)

        query = query.order_by(desc(ESGAsset.created_at)).limit(limit).offset(offset)

        result = await db.execute(query)
        assets = result.scalars().all()

        assets_list = []
        for asset in assets:
            assets_list.append({
                "id": str(asset.id),
                "invoice_number": asset.invoice_number,
                "esg_value": asset.esg_value,
                "esg_score": asset.esg_score,
                "category": asset.category,
                "carbon_offset_kg": asset.carbon_offset_kg,
                "status": asset.status,
                "created_at": asset.created_at.isoformat() if asset.created_at else None
            })

        return {
            "success": True,
            "message": f"Ativos ESG agilizados! {len(assets_list)} ativos encontrados 🌱",
            "data": {
                "assets": assets_list,
                "total": len(assets_list),
                "limit": limit,
                "offset": offset,
                "category": category
            },
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        logger.error(f"❌ Erro ao buscar ativos ESG: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar ativos ESG"
        )

@router.post("/esg-assets/{asset_id}/sell")
@limiter.limit("3/minute")
async def sell_esg_asset(
    request: Request,
    asset_id: str,
    sell_price: float,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Vender ativo ESG no marketplace
    """
    try:
        logger.info(f"💱 Vendendo ativo ESG: {asset_id}")

        # Buscar ativo
        from sqlalchemy import select
        result = await db.execute(
            select(ESGAsset).where(
                ESGAsset.id == asset_id,
                ESGAsset.user_id == current_user.id,
                ESGAsset.status == "active"
            )
        )
        asset = result.scalar_one_or_none()

        if not asset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ativo ESG não encontrado! 🔍"
            )

        # Calcular taxa de venda (2% do valor)
        guardflow_fee = sell_price * 0.02
        user_amount = sell_price - guardflow_fee

        # Marcar ativo como vendido
        asset.status = "sold"
        asset.sold_price = sell_price
        asset.sold_at = datetime.utcnow()

        # Criar transação de monetização
        monetization = MonetizationTransaction(
            user_id=current_user.id,
            transaction_id=asset.transaction_id,
            amount=guardflow_fee,
            transaction_type="esg_sale_fee",
            description=f"Taxa de venda - Ativo ESG {asset.invoice_number}",
            status="completed"
        )

        db.add(monetization)

        # Atualizar saldo do usuário
        current_user.add_cash_balance(user_amount)

        await db.commit()

        logger.info(f"✅ Ativo ESG vendido: {asset.id}")

        return {
            "success": True,
            "message": "Ativo ESG vendido com sucesso! 💱",
            "data": {
                "asset_id": str(asset.id),
                "sell_price": sell_price,
                "guardflow_fee": guardflow_fee,
                "user_amount": user_amount,
                "sold_at": asset.sold_at.isoformat() if asset.sold_at else None
            },
            "timestamp": datetime.utcnow().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao vender ativo ESG: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao vender ativo ESG"
        )

@router.get("/monetization/stats")
async def get_monetization_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Estatísticas de monetização do usuário
    """
    try:
        from sqlalchemy import select, func

        # Total de conversões
        total_conversions = await db.execute(
            select(func.count(InvoiceConversion.id)).where(
                InvoiceConversion.user_id == current_user.id
            )
        )
        total_conversions = total_conversions.scalar() or 0

        # Total convertido em dinheiro
        cash_conversions = await db.execute(
            select(func.sum(InvoiceConversion.user_amount)).where(
                InvoiceConversion.user_id == current_user.id,
                InvoiceConversion.conversion_type == "cash",
                InvoiceConversion.status == "completed"
            )
        )
        total_cash = float(cash_conversions.scalar() or 0)

        # Total em ativos ESG
        esg_assets = await db.execute(
            select(func.sum(ESGAsset.esg_value)).where(
                ESGAsset.user_id == current_user.id,
                ESGAsset.status == "active"
            )
        )
        total_esg_value = float(esg_assets.scalar() or 0)

        # Total de taxas pagas ao GuardFlow
        fees_paid = await db.execute(
            select(func.sum(MonetizationTransaction.amount)).where(
                MonetizationTransaction.user_id == current_user.id,
                MonetizationTransaction.status == "completed"
            )
        )
        total_fees = float(fees_paid.scalar() or 0)

        return {
            "success": True,
            "message": "Estatísticas de monetização agilizadas! 📊",
            "data": {
                "total_conversions": total_conversions,
                "total_cash_converted": total_cash,
                "total_esg_value": total_esg_value,
                "total_fees_paid": total_fees,
                "esg_tokens": current_user.esg_tokens,
                "cash_balance": getattr(current_user, 'cash_balance', 0.0)
            },
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        logger.error(f"❌ Erro ao buscar estatísticas: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar estatísticas de monetização"
        )


# Funções auxiliares para cálculo ESG otimizado
async def _calculate_sustainability_bonus(transaction: Transaction) -> float:
    """
    Calcular bônus de sustentabilidade baseado nos produtos
    """
    try:
        # Produtos sustentáveis com bônus
        sustainable_products = [
            "orgânico", "sustentável", "eco", "verde", "natural",
            "reciclado", "biodegradável", "energia solar", "eletrônico verde"
        ]
        
        bonus = 0.0
        if hasattr(transaction, 'products') and transaction.products:
            for product in transaction.products:
                product_name = product.get('name', '').lower()
                for sustainable_keyword in sustainable_products:
                    if sustainable_keyword in product_name:
                        bonus += 0.05  # 5% de bônus por produto sustentável
                        break
        
        return min(bonus, 0.20)  # Máximo 20% de bônus
        
    except Exception as e:
        logger.error(f"❌ Erro ao calcular bônus sustentabilidade: {str(e)}")
        return 0.0


async def _calculate_carbon_bonus(transaction: Transaction) -> float:
    """
    Calcular bônus de carbono baseado no impacto ambiental
    """
    try:
        # Bônus baseado na pegada de carbono
        carbon_footprint = getattr(transaction, 'carbon_footprint_kg', 0.0)
        
        if carbon_footprint <= 0:
            return 0.0
        
        # Bônus inversamente proporcional à pegada de carbono
        # Menos carbono = mais bônus
        if carbon_footprint <= 1.0:  # Muito baixo
            return 0.15
        elif carbon_footprint <= 2.0:  # Baixo
            return 0.10
        elif carbon_footprint <= 3.0:  # Médio
            return 0.05
        else:  # Alto
            return 0.0
            
    except Exception as e:
        logger.error(f"❌ Erro ao calcular bônus carbono: {str(e)}")
        return 0.0
