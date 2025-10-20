from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict


router = APIRouter(prefix="/agility-tax", tags=["Agility Tax"])


class AgilityTaxRequest(BaseModel):
    transaction_amount: float = Field(gt=0)
    plan_tier: str = Field(pattern=r"^(starter|professional|enterprise)$")
    market_id: str
    product_count: int = Field(ge=1)


class AgilityTaxResponse(BaseModel):
    base_amount: float
    agility_tax: float
    net_amount: float
    time_saved_minutes: float
    conversion_boost_factor: float
    roi_estimate_percent: float


PLAN_RATES: Dict[str, float] = {
    "starter": 0.02,
    "professional": 0.035,
    "enterprise": 0.05,
}


def _volume_discount(monthly_tx: int) -> float:
    if monthly_tx > 50000:
        return 0.20
    if monthly_tx > 10000:
        return 0.10
    return 0.0


def _estimate_benefits(product_count: int, plan_tier: str) -> Dict[str, float]:
    base_minutes = 4.5
    tier_factor = {"starter": 0.7, "professional": 0.9, "enterprise": 0.95}[plan_tier]
    time_saved = base_minutes * tier_factor
    conversion_boost = {"starter": 5.0, "professional": 6.5, "enterprise": 7.0}[plan_tier]
    return {"time_saved": time_saved, "conversion_boost": conversion_boost}


@router.post("/calculate", response_model=AgilityTaxResponse)
async def calculate_agility_tax(payload: AgilityTaxRequest, monthly_transactions: Optional[int] = 0):
    if payload.plan_tier not in PLAN_RATES:
        raise HTTPException(status_code=400, detail="Plano inválido")

    rate = PLAN_RATES[payload.plan_tier]
    discount = _volume_discount(monthly_transactions or 0)
    base_tax = payload.transaction_amount * rate
    final_tax = base_tax * (1 - discount)

    benefits = _estimate_benefits(payload.product_count, payload.plan_tier)

    hourly_rate = 25.0
    time_value = (benefits["time_saved"] / 60.0) * hourly_rate
    conversion_value = payload.transaction_amount * (benefits["conversion_boost"] - 1)
    abandonment_value = payload.transaction_amount * 0.75
    total_benefit = time_value + conversion_value + abandonment_value
    roi_pct = ((total_benefit - final_tax) / final_tax) * 100 if final_tax > 0 else 0.0

    return AgilityTaxResponse(
        base_amount=payload.transaction_amount,
        agility_tax=round(final_tax, 2),
        net_amount=round(payload.transaction_amount - final_tax, 2),
        time_saved_minutes=round(benefits["time_saved"], 2),
        conversion_boost_factor=round(benefits["conversion_boost"], 2),
        roi_estimate_percent=round(roi_pct, 2),
    )


@router.post("/authorize")
async def authorize_agility_tax(payload: AgilityTaxRequest):
    return {
        "authorization_id": f"agt_{payload.market_id}",
        "status": "authorized",
        "plan_tier": payload.plan_tier,
    }


@router.get("/usage/{market_id}")
async def get_usage(market_id: str):
    return {
        "market_id": market_id,
        "monthly_transactions": 0,
        "agility_tax_collected": 0.0,
    }


@router.get("/roi/{market_id}")
async def get_roi(market_id: str):
    return {
        "market_id": market_id,
        "roi_estimate_percent": 0.0,
        "kpis": {
            "checkout_time_p50": 0,
            "conversion_rate": 0.0,
            "abandonment_rate": 0.0,
        },
    }


