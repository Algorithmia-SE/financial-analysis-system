import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

from src.core.financial_analysis import FinancialAnalysisSystem
from src.utils.logger import logger

class AnalysisRequest(BaseModel):
    ticker: str
    start_date: str
    end_date: Optional[str] = None

class AnalysisResponse(BaseModel):
    ticker: str
    market_insights: str
    prediction_results: dict
    visualization_paths: List[str]

app = FastAPI(
    title="Financial Analysis API",
    description="AI-powered financial analysis and prediction system",
    version="0.1.0"
)

@app.post("/analyze", response_model=AnalysisResponse)
async def perform_financial_analysis(request: AnalysisRequest):
    try:
        # Log the incoming request
        logger.info(f"Received analysis request for {request.ticker}")
        
        # Use current date if end_date is not provided
        end_date = request.end_date or datetime.now().strftime('%Y-%m-%d')
        
        # Initialize analysis system
        system = FinancialAnalysisSystem()
        
        # Run analysis
        result = system.run_analysis(
            ticker=request.ticker,
            start_date=request.start_date,
            end_date=end_date
        )
        
        # Log successful analysis
        logger.info(f"Completed analysis for {request.ticker}")
        
        return AnalysisResponse(
            ticker=request.ticker,
            market_insights=result.get('market_insights', ''),
            prediction_results=result.get('prediction_results', {}),
            visualization_paths=result.get('visualization_paths', [])
        )
    
    except Exception as e:
        # Log the error
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Additional endpoints can be added here
@app.get("/")
async def root():
    return {"message": "Financial Analysis API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)