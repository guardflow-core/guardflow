"""
GuardFlow Vision Service
Serviço de Computer Vision com Google Cloud Vision API
"""

import os
import io
import logging
from typing import Optional, Dict, List, Tuple
from PIL import Image
import base64

try:
    from google.cloud import vision
    from google.cloud.vision_v1 import types
    GOOGLE_VISION_AVAILABLE = True
except ImportError:
    GOOGLE_VISION_AVAILABLE = False
    vision = None
    types = None

logger = logging.getLogger("guardflow.vision")

class VisionService:
    """Serviço de Computer Vision com Google Cloud Vision API"""
    
    def __init__(self):
        self.client = None
        self.is_available = False
        
        if GOOGLE_VISION_AVAILABLE:
            try:
                # Configurar credenciais do Google Cloud
                credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
                if credentials_path and os.path.exists(credentials_path):
                    self.client = vision.ImageAnnotatorClient()
                    self.is_available = True
                    logger.info("✅ Google Cloud Vision API configurada")
                else:
                    logger.warning("⚠️ Credenciais do Google Cloud não encontradas")
            except Exception as e:
                logger.error(f"❌ Erro ao configurar Google Cloud Vision: {e}")
        else:
            logger.warning("⚠️ Google Cloud Vision não disponível")
    
    async def detect_products(self, image_data: bytes) -> Dict:
        """
        Detectar produtos em uma imagem usando Google Cloud Vision
        """
        if not self.is_available:
            return await self._mock_detection(image_data)
        
        try:
            # Criar objeto de imagem
            image = types.Image(content=image_data)
            
            # Configurar features para detecção
            features = [
                types.Feature(type_=types.Feature.Type.LABEL_DETECTION, max_results=10),
                types.Feature(type_=types.Feature.Type.TEXT_DETECTION, max_results=10),
                types.Feature(type_=types.Feature.Type.OBJECT_LOCALIZATION, max_results=10),
            ]
            
            # Fazer requisição para a API
            response = self.client.annotate_image({
                'image': image,
                'features': features
            })
            
            # Processar resultados
            results = self._process_vision_results(response)
            
            logger.info(f"✅ Produtos detectados: {len(results.get('products', []))}")
            
            return {
                "success": True,
                "products": results.get('products', []),
                "confidence": results.get('confidence', 0.0),
                "method": "google_vision",
                "processing_time_ms": results.get('processing_time_ms', 0)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro na detecção de produtos: {e}")
            return await self._mock_detection(image_data)
    
    async def detect_barcodes(self, image_data: bytes) -> Dict:
        """
        Detectar códigos de barras em uma imagem
        """
        if not self.is_available:
            return await self._mock_barcode_detection(image_data)
        
        try:
            # Criar objeto de imagem
            image = types.Image(content=image_data)
            
            # Configurar feature para detecção de códigos de barras
            features = [types.Feature(type_=types.Feature.Type.TEXT_DETECTION, max_results=20)]
            
            # Fazer requisição para a API
            response = self.client.annotate_image({
                'image': image,
                'features': features
            })
            
            # Processar códigos de barras
            barcodes = self._extract_barcodes(response)
            
            logger.info(f"✅ Códigos de barras detectados: {len(barcodes)}")
            
            return {
                "success": True,
                "barcodes": barcodes,
                "method": "google_vision",
                "processing_time_ms": 500
            }
            
        except Exception as e:
            logger.error(f"❌ Erro na detecção de códigos de barras: {e}")
            return await self._mock_barcode_detection(image_data)
    
    def _process_vision_results(self, response) -> Dict:
        """Processar resultados da Google Cloud Vision API"""
        products = []
        confidence_scores = []
        
        # Processar labels (rótulos)
        for label in response.label_annotations:
            if label.score > 0.7:  # Apenas labels com alta confiança
                products.append({
                    "name": label.description,
                    "confidence": label.score,
                    "type": "label"
                })
                confidence_scores.append(label.score)
        
        # Processar objetos detectados
        for obj in response.localized_object_annotations:
            if obj.score > 0.7:
                products.append({
                    "name": obj.name,
                    "confidence": obj.score,
                    "type": "object",
                    "bounding_box": {
                        "x": obj.bounding_poly.normalized_vertices[0].x,
                        "y": obj.bounding_poly.normalized_vertices[0].y,
                        "width": obj.bounding_poly.normalized_vertices[2].x - obj.bounding_poly.normalized_vertices[0].x,
                        "height": obj.bounding_poly.normalized_vertices[2].y - obj.bounding_poly.normalized_vertices[0].y
                    }
                })
                confidence_scores.append(obj.score)
        
        # Calcular confiança média
        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
        
        return {
            "products": products,
            "confidence": avg_confidence,
            "processing_time_ms": 1000  # Simulado
        }
    
    def _extract_barcodes(self, response) -> List[Dict]:
        """Extrair códigos de barras dos resultados"""
        barcodes = []
        
        for text in response.text_annotations:
            # Verificar se é um código de barras (padrão numérico)
            if text.description.isdigit() and len(text.description) >= 8:
                barcodes.append({
                    "code": text.description,
                    "confidence": 0.9,
                    "type": "barcode"
                })
        
        return barcodes
    
    async def _mock_detection(self, image_data: bytes) -> Dict:
        """Mock de detecção para quando Google Vision não está disponível"""
        import random
        
        # Simular produtos baseados no tamanho da imagem
        mock_products = [
            {"name": "Coca-Cola 2L", "confidence": 0.85, "type": "label"},
            {"name": "Arroz Tio João 5kg", "confidence": 0.78, "type": "label"},
            {"name": "Feijão Carioca Camil 1kg", "confidence": 0.82, "type": "label"},
            {"name": "Leite Integral Parmalat 1L", "confidence": 0.88, "type": "label"},
            {"name": "Pão Integral Wickbold", "confidence": 0.75, "type": "label"},
        ]
        
        # Selecionar produto aleatório
        selected_product = random.choice(mock_products)
        
        return {
            "success": True,
            "products": [selected_product],
            "confidence": selected_product["confidence"],
            "method": "mock",
            "processing_time_ms": 1200
        }
    
    async def _mock_barcode_detection(self, image_data: bytes) -> Dict:
        """Mock de detecção de códigos de barras"""
        import random
        
        mock_barcodes = [
            "7891234567890",
            "7891234567891", 
            "7891234567892",
            "7891234567893",
            "7891234567894"
        ]
        
        return {
            "success": True,
            "barcodes": [{"code": random.choice(mock_barcodes), "confidence": 0.95, "type": "barcode"}],
            "method": "mock",
            "processing_time_ms": 800
        }
    
    def is_google_vision_available(self) -> bool:
        """Verificar se Google Vision está disponível"""
        return self.is_available

# Instância global do serviço
vision_service = VisionService()