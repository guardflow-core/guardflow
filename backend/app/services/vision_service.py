"""
Vision Service (Mock)
Abstração para reconhecimento de produtos no MVP
"""
from typing import Optional, Dict, Any


class VisionService:
    """Serviço de visão computacional (mock)."""

    async def analyze_image(self, image_bytes: bytes) -> Dict[str, Any]:
        # Retorna metadados básicos para debug
        size = len(image_bytes) if image_bytes else 0
        return {
            "size_bytes": size,
            "quality": "good" if size > 50_000 else "low",
            "confidence_hint": 0.9 if size > 50_000 else 0.7,
        }

    async def detect_barcode(self, image_bytes: bytes) -> Optional[str]:
        # Não implementado no MVP (retorna None)
        return None


__all__ = ["VisionService"]


