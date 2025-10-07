"""
GuardPass Service (Simulado)
Integração simulada com GuardPass para o MVP
"""
from typing import Optional, Dict, Any
from datetime import datetime


class GuardPassService:
    """Serviço de integração com GuardPass (simulado)."""

    async def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Autenticar usuário via GuardPass (simulado para MVP).
        Retorna dados mínimos do usuário se credenciais parecerem válidas.
        """
        if not email or not password:
            return None

        # Simples validação mock: qualquer senha com 6+ caracteres é aceita
        if len(password) < 6:
            return None

        # Simular resposta do GuardPass
        guardpass_user = {
            "id": f"gp_{abs(hash(email)) % 10_000_000}",
            "guardpass_id": f"gp_{abs(hash(email)) % 10_000_000}",
            "email": email,
            "name": email.split("@")[0].replace(".", " ").title(),
            "esg": {"score": 65},
            "created_at": datetime.utcnow().isoformat(),
        }
        return guardpass_user

    async def get_user_esg_score(self, guardpass_id: str) -> Optional[Dict[str, Any]]:
        """Obter ESG score do usuário (simulado)."""
        if not guardpass_id:
            return None
        score = 50 + (abs(hash(guardpass_id)) % 51)  # 50-100
        return {"score": score, "source": "guardpass_mock"}


__all__ = ["GuardPassService"]


