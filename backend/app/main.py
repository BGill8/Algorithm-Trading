from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from . import services, models

app = FastAPI()

# CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # The default Next.js dev port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/stock/{ticker}", response_model=models.FinancialData)
def get_stock_data(ticker: str):
    """Endpoint to get historical financial data."""
    try:
        data = services.get_financial_data(ticker)
        return data
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/api/calculate_projection", response_model=models.ProjectionResponse)
def calculate_projection(request: models.ProjectionRequest):
    """Endpoint to calculate stock price projection."""
    try:
        projection = services.calculate_projection(request.ticker, request.revenue_growth_forecast)
        return projection
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
