import os
import requests
from dotenv import load_dotenv
from typing import Dict, List, Tuple

load_dotenv()

ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
BASE_URL = "https://www.alphavantage.co/query"

def get_financial_data(ticker: str) -> Dict:
    """Fetches income statement data from Alpha Vantage."""
    params = {
        "function": "INCOME_STATEMENT",
        "symbol": ticker,
        "apikey": ALPHAVANTAGE_API_KEY,
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    data = response.json()

    if "annualReports" not in data:
        raise ValueError("Could not retrieve financial data. The ticker may be invalid or the API limit reached.")

    annual_reports = data["annualReports"]
    
    years = [report["fiscalDateEnding"][:4] for report in annual_reports]
    revenues = [float(report["totalRevenue"]) for report in annual_reports]

    # Reverse data to be in chronological order
    years.reverse()
    revenues.reverse()

    revenue_growths = [0.0] # No growth for the first year
    for i in range(1, len(revenues)):
        growth = (revenues[i] - revenues[i-1]) / revenues[i-1]
        revenue_growths.append(round(growth, 4))

    return {
        "years": years,
        "revenues": revenues,
        "revenue_growths": revenue_growths,
    }


def calculate_projection(ticker: str, forecast: Dict[str, List[float]]) -> Dict[str, float]:
    """
    Calculates a simplified stock price projection based on revenue growth.
    
    This is a highly simplified model for MVP purposes.
    A real model would be much more complex (e.g., a full DCF).
    """
    # Assumptions for our simplified model
    ASSUMED_PROFIT_MARGIN = 0.15  # 15%
    ASSUMED_PE_RATIO = 20
    
    # Fetch current stock data for shares outstanding
    params = {
        "function": "OVERVIEW",
        "symbol": ticker,
        "apikey": ALPHAVANTAGE_API_KEY,
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    overview_data = response.json()
    if "SharesOutstanding" not in overview_data:
        raise ValueError("Could not retrieve shares outstanding.")
    
    shares_outstanding = float(overview_data["SharesOutstanding"])
    
    # Get the latest revenue
    financials = get_financial_data(ticker)
    latest_revenue = financials["revenues"][-1]

    results = {}
    for case in ["base", "bull", "bear"]:
        projected_revenue = latest_revenue
        for growth_rate in forecast[case]:
            projected_revenue *= (1 + growth_rate)
        
        projected_net_income = projected_revenue * ASSUMED_PROFIT_MARGIN
        future_market_cap = projected_net_income * ASSUMED_PE_RATIO
        projected_stock_price = future_market_cap / shares_outstanding
        results[f"{case}_case"] = round(projected_stock_price, 2)

    return results
