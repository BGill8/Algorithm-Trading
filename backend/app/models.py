from pydantic import BaseModel
from typing import List, Dict

class ProjectionRequest(BaseModel):
    ticker: str
    revenue_growth_forecast: Dict[str, List[float]] # {"base": [0.1, 0.08], "bull": [...], "bear": [...]}

class FinancialData(BaseModel):
    years: List[str]
    revenues: List[float]
    revenue_growths: List[float]

class ProjectionResponse(BaseModel):
    base_case: float
    bull_case: float
    bear_case: float
