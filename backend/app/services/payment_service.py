"""
Payment Service (Mock)
Abstrai criação e verificação de pagamentos para o MVP
"""
from typing import Dict, Any
from datetime import datetime, timedelta
import uuid
import base64
import io
import qrcode


class PaymentService:
    """Serviço de pagamentos (mock Mercado Pago PIX)."""

    async def create_pix(self, amount: float) -> Dict[str, Any]:
        payment_id = f"MP{uuid.uuid4().hex[:12].upper()}"
        pix_code = f"00020126{len(payment_id):02d}{payment_id}5204000053039865802BR5925GUARDFLOW PAGAMENTOS LTDA6009SAO PAULO6304"

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(pix_code)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()

        expiration = datetime.utcnow() + timedelta(minutes=30)

        return {
            "payment_id": payment_id,
            "pix_code": pix_code,
            "qr_code": f"data:image/png;base64,{qr_code_base64}",
            "expiration": expiration,
            "raw_data": {
                "id": payment_id,
                "status": "pending",
                "transaction_amount": amount,
                "currency_id": "BRL",
                "payment_method_id": "pix",
                "date_created": datetime.utcnow().isoformat(),
                "date_of_expiration": expiration.isoformat(),
            },
        }

    async def get_status(self, payment_id: str) -> Dict[str, Any]:
        return {"id": payment_id, "status": "pending"}

    async def confirm(self, payment_id: str) -> Dict[str, Any]:
        return {"id": payment_id, "status": "approved", "confirmed_at": datetime.utcnow().isoformat()}


__all__ = ["PaymentService"]


