"""
Scanner API Endpoints
API para reconhecimento de produtos via Computer Vision
DIA 1 MVP - Versão funcional com mock inteligente
"""
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Request
from sqlalchemy.ext.asyncio import AsyncSession
from slowapi import Limiter
from slowapi.util import get_remote_address
import logging
from datetime import datetime
from typing import Optional
import base64
import io
from PIL import Image

from app.database import get_db
from app.config import settings, AppMessages
from app.models.user import User
from app.models.product import Product
from app.models.store import Store
from app.models.transaction import ScanEvent
from app.utils.security import get_current_user

# Logger
logger = logging.getLogger("guardflow.scanner")

# Router
router = APIRouter()

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

@router.post("/scan")
@limiter.limit("30/minute")
async def scan_product(
    request: Request,
    image: UploadFile = File(...),
    store_id: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Escanear produto via imagem
    MVP: Mock inteligente que simula Computer Vision
    """
    try:
        logger.info(f"🔍 Escaneamento iniciado: usuário {current_user.email}")
        
        # Validar arquivo de imagem
        if not image.content_type.startswith("image/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Arquivo deve ser uma imagem! 📸"
            )
        
        # Ler imagem
        image_data = await image.read()
        
        # Mock Computer Vision - Simular reconhecimento
        scan_result = await _mock_vision_recognition(image_data, store_id, db)
        
        # Registrar evento de escaneamento
        scan_event = ScanEvent.create_scan_event(
            barcode=scan_result.get("barcode"),
            user_id=str(current_user.id),
            store_id=store_id,
            product_id=scan_result.get("product_id"),
            confidence=scan_result.get("confidence", 0.85),
            duration_ms=scan_result.get("duration_ms", 1500),
            successful=scan_result.get("success", True),
            recognition_method="computer_vision_mock",
            action_taken="scanned"
        )
        
        db.add(scan_event)
        await db.commit()
        
        # Incrementar contador de scan no produto
        if scan_result.get("product"):
            product = scan_result["product"]
            product.increment_scan_count()
            await db.commit()
        
        logger.info(f"✅ Produto escaneado: {scan_result.get('product_name', 'Desconhecido')}")
        
        return {
            "success": True,
            "message": AppMessages.PRODUCT_SCANNED_SUCCESS,
            "data": {
                "product": scan_result.get("product_data"),
                "confidence": scan_result.get("confidence"),
                "scan_time_ms": scan_result.get("duration_ms"),
                "barcode": scan_result.get("barcode"),
                "recognized": scan_result.get("success"),
                "scan_id": str(scan_event.id)
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro no escaneamento: {str(e)}")
        
        # Registrar evento de erro
        error_event = ScanEvent.create_scan_event(
            user_id=str(current_user.id),
            store_id=store_id,
            successful=False,
            error_message=str(e),
            recognition_method="computer_vision_mock"
        )
        db.add(error_event)
        await db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=AppMessages.PRODUCT_NOT_RECOGNIZED
        )

@router.post("/scan-barcode")
@limiter.limit("60/minute")
async def scan_barcode(
    request: Request,
    barcode: str,
    store_id: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Escanear produto via código de barras
    """
    try:
        logger.info(f"📱 Escaneamento barcode: {barcode}")
        
        # Buscar produto por código de barras
        from sqlalchemy import select
        result = await db.execute(
            select(Product).where(Product.barcode == barcode)
        )
        product = result.scalar_one_or_none()
        
        if not product:
            # Criar produto mock se não existir
            product = await _create_mock_product(barcode, db)
        
        # Registrar evento
        scan_event = ScanEvent.create_scan_event(
            barcode=barcode,
            user_id=str(current_user.id),
            store_id=store_id,
            product_id=str(product.id) if product else None,
            confidence=0.95,
            duration_ms=800,
            successful=True,
            recognition_method="barcode",
            action_taken="scanned"
        )
        
        db.add(scan_event)
        
        # Incrementar contador
        if product:
            product.increment_scan_count()
        
        await db.commit()
        
        logger.info(f"✅ Barcode escaneado: {product.name if product else 'Produto não encontrado'}")
        
        return {
            "success": True,
            "message": AppMessages.PRODUCT_SCANNED_SUCCESS,
            "data": {
                "product": product.to_dict() if product else None,
                "confidence": 0.95,
                "scan_time_ms": 800,
                "barcode": barcode,
                "recognized": product is not None,
                "scan_id": str(scan_event.id)
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Erro no escaneamento barcode: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=AppMessages.PRODUCT_NOT_RECOGNIZED
        )

@router.get("/history")
async def get_scan_history(
    limit: int = 20,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Histórico de escaneamentos do usuário
    """
    try:
        from sqlalchemy import select, desc
        
        query = select(ScanEvent).where(
            ScanEvent.user_id == current_user.id
        ).order_by(desc(ScanEvent.created_at)).limit(limit).offset(offset)
        
        result = await db.execute(query)
        scan_events = result.scalars().all()
        
        history = [event.to_dict() for event in scan_events]
        
        return {
            "success": True,
            "message": f"Histórico agilizado! {len(history)} escaneamentos encontrados 📊",
            "data": {
                "scans": history,
                "total": len(history),
                "limit": limit,
                "offset": offset
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao buscar histórico: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar histórico de escaneamentos"
        )

@router.get("/stats")
async def get_scan_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Estatísticas de escaneamento do usuário
    """
    try:
        from sqlalchemy import select, func
        
        # Total de scans
        total_query = select(func.count(ScanEvent.id)).where(
            ScanEvent.user_id == current_user.id
        )
        total_result = await db.execute(total_query)
        total_scans = total_result.scalar() or 0
        
        # Scans bem-sucedidos
        success_query = select(func.count(ScanEvent.id)).where(
            ScanEvent.user_id == current_user.id,
            ScanEvent.successful == True
        )
        success_result = await db.execute(success_query)
        successful_scans = success_result.scalar() or 0
        
        # Taxa de sucesso
        success_rate = (successful_scans / total_scans * 100) if total_scans > 0 else 0
        
        # Tempo médio
        avg_time_query = select(func.avg(ScanEvent.scan_duration_ms)).where(
            ScanEvent.user_id == current_user.id,
            ScanEvent.successful == True
        )
        avg_time_result = await db.execute(avg_time_query)
        avg_scan_time = avg_time_result.scalar() or 0
        
        return {
            "success": True,
            "message": "Estatísticas agilizadas! 📈",
            "data": {
                "total_scans": total_scans,
                "successful_scans": successful_scans,
                "success_rate": round(success_rate, 1),
                "avg_scan_time_ms": round(avg_scan_time, 0) if avg_scan_time else 0,
                "avg_scan_time_seconds": round(avg_scan_time / 1000, 1) if avg_scan_time else 0
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao buscar estatísticas: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao calcular estatísticas"
        )

# Funções auxiliares para MVP

async def _mock_vision_recognition(image_data: bytes, store_id: str, db: AsyncSession) -> dict:
    """
    Mock da Computer Vision para MVP
    Simula reconhecimento inteligente baseado em produtos existentes
    """
    try:
        # Simular processamento de imagem
        image = Image.open(io.BytesIO(image_data))
        
        # Mock: Selecionar produto aleatório baseado na loja
        from sqlalchemy import select, func
        
        if store_id:
            # Buscar produtos da loja específica (mock)
            query = select(Product).where(Product.is_active == True).order_by(func.random()).limit(1)
        else:
            # Produto aleatório
            query = select(Product).where(Product.is_active == True).order_by(func.random()).limit(1)
        
        result = await db.execute(query)
        product = result.scalar_one_or_none()
        
        if not product:
            # Criar produto mock se não houver nenhum
            product = await _create_mock_product("7891234567890", db)
        
        # Simular confiança baseada na "qualidade" da imagem
        confidence = 0.85 + (hash(str(len(image_data))) % 15) / 100  # 0.85-0.99
        
        # Simular tempo de processamento
        duration_ms = 1200 + (hash(str(len(image_data))) % 800)  # 1.2-2.0s
        
        return {
            "success": True,
            "product": product,
            "product_id": str(product.id),
            "product_name": product.name,
            "product_data": product.to_dict(),
            "barcode": product.barcode,
            "confidence": round(confidence, 2),
            "duration_ms": duration_ms
        }
        
    except Exception as e:
        logger.error(f"❌ Erro no mock vision: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "confidence": 0.0,
            "duration_ms": 2000
        }

async def _create_mock_product(barcode: str, db: AsyncSession) -> Product:
    """
    Criar produto mock para demonstração
    """
    import random
    
    # Dados mock realistas
    mock_products = [
        {"name": "Coca-Cola 2L", "brand": "Coca-Cola", "category": "Bebidas", "price": "8.99"},
        {"name": "Arroz Tio João 5kg", "brand": "Tio João", "category": "Alimentício", "price": "24.90"},
        {"name": "Feijão Carioca Camil 1kg", "brand": "Camil", "category": "Alimentício", "price": "7.50"},
        {"name": "Leite Integral Parmalat 1L", "brand": "Parmalat", "category": "Laticínios", "price": "4.89"},
        {"name": "Pão de Açúcar Integral", "brand": "Wickbold", "category": "Padaria", "price": "5.99"},
        {"name": "Detergente Ypê 500ml", "brand": "Ypê", "category": "Limpeza", "price": "2.99"},
        {"name": "Shampoo Seda 325ml", "brand": "Seda", "category": "Higiene", "price": "12.90"},
        {"name": "Banana Prata kg", "brand": "Natural", "category": "Hortifruti", "price": "6.90"}
    ]
    
    mock_data = random.choice(mock_products)
    
    product = Product(
        barcode=barcode,
        name=mock_data["name"],
        brand=mock_data["brand"],
        category=mock_data["category"],
        price=mock_data["price"],
        is_active=True,
        is_available=True,
        esg_score=random.randint(40, 90),
        stock_quantity=random.randint(10, 100),
        image_url=f"https://guardflow.app/products/{barcode}.jpg"
    )
    
    # Calcular ESG score
    product.calculate_esg_score()
    
    db.add(product)
    await db.commit()
    
    logger.info(f"✅ Produto mock criado: {product.name}")
    
    return product

# Endpoint de desenvolvimento para popular produtos
if settings.DEBUG:
    @router.post("/populate-products")
    async def populate_mock_products(db: AsyncSession = Depends(get_db)):
        """
        Popular banco com produtos mock para demonstração
        """
        try:
            mock_products = [
                {"barcode": "7891234567890", "name": "Coca-Cola 2L", "brand": "Coca-Cola", "category": "Bebidas", "price": "8.99"},
                {"barcode": "7891234567891", "name": "Arroz Tio João 5kg", "brand": "Tio João", "category": "Alimentício", "price": "24.90"},
                {"barcode": "7891234567892", "name": "Feijão Carioca Camil 1kg", "brand": "Camil", "category": "Alimentício", "price": "7.50"},
                {"barcode": "7891234567893", "name": "Leite Integral Parmalat 1L", "brand": "Parmalat", "category": "Laticínios", "price": "4.89"},
                {"barcode": "7891234567894", "name": "Pão Integral Wickbold", "brand": "Wickbold", "category": "Padaria", "price": "5.99"},
                {"barcode": "7891234567895", "name": "Detergente Ypê 500ml", "brand": "Ypê", "category": "Limpeza", "price": "2.99"},
                {"barcode": "7891234567896", "name": "Shampoo Seda 325ml", "brand": "Seda", "category": "Higiene", "price": "12.90"},
                {"barcode": "7891234567897", "name": "Banana Prata kg", "brand": "Natural", "category": "Hortifruti", "price": "6.90"},
                {"barcode": "7891234567898", "name": "Açúcar Cristal União 1kg", "brand": "União", "category": "Alimentício", "price": "4.50"},
                {"barcode": "7891234567899", "name": "Café Pilão 500g", "brand": "Pilão", "category": "Alimentício", "price": "15.90"}
            ]
            
            created_count = 0
            for mock_data in mock_products:
                # Verificar se já existe
                from sqlalchemy import select
                result = await db.execute(
                    select(Product).where(Product.barcode == mock_data["barcode"])
                )
                existing = result.scalar_one_or_none()
                
                if not existing:
                    product = Product(
                        barcode=mock_data["barcode"],
                        name=mock_data["name"],
                        brand=mock_data["brand"],
                        category=mock_data["category"],
                        price=mock_data["price"],
                        is_active=True,
                        is_available=True,
                        esg_score=hash(mock_data["barcode"]) % 50 + 40,  # 40-90
                        stock_quantity=100,
                        image_url=f"https://guardflow.app/products/{mock_data['barcode']}.jpg"
                    )
                    
                    product.calculate_esg_score()
                    db.add(product)
                    created_count += 1
            
            await db.commit()
            
            return {
                "success": True,
                "message": f"Agilizou! {created_count} produtos criados para demonstração! 🛒",
                "data": {
                    "created_products": created_count,
                    "total_products": len(mock_products)
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao popular produtos: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao criar produtos mock"
            )

