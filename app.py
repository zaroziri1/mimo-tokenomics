"""
MiMo Tokenomics Simulator - Backend Engine
AI-powered token economics simulation platform
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import numpy as np
import json
from datetime import datetime
import httpx

app = FastAPI(title="MiMo Tokenomics Simulator", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# MiMo API configuration
MIMO_API_URL = "http://43.153.206.68:20128/v1"
MIMO_MODEL = "xmtp/mimo-v2.5-pro"


class TokenomicsInput(BaseModel):
    """Input model for tokenomics simulation"""
    token_name: str = "TOKEN"
    total_supply: float = 1_000_000_000
    initial_price: float = 0.01
    initial_circulating: float = 100_000_000
    
    # Distribution
    team_pct: float = 15.0
    investors_pct: float = 20.0
    community_pct: float = 30.0
    treasury_pct: float = 15.0
    staking_pct: float = 10.0
    liquidity_pct: float = 10.0
    
    # Vesting
    team_cliff_months: int = 12
    team_vesting_months: int = 36
    investors_cliff_months: int = 6
    investors_vesting_months: int = 24
    
    # Economics
    inflation_rate: float = 5.0  # % per year
    burn_rate: float = 2.0  # % of transactions
    staking_apy: float = 15.0  # %
    
    # Market
    initial_demand_growth: float = 10.0  # % per month
    volatility: float = 30.0  # %
    simulation_months: int = 36


class SimulationResult(BaseModel):
    """Output model for simulation results"""
    months: List[int]
    price_history: List[float]
    market_cap_history: List[float]
    circulating_supply_history: List[float]
    total_supply_history: List[float]
    staking_ratio_history: List[float]
    burned_tokens_history: List[float]
    
    # Statistics
    final_price: float
    final_market_cap: float
    max_price: float
    min_price: float
    price_volatility: float
    total_burned: float
    total_staked: float
    
    # Risk metrics
    sharpe_ratio: float
    max_drawdown: float
    var_95: float  # Value at Risk 95%


def run_simulation(params: TokenomicsInput) -> SimulationResult:
    """Run Monte Carlo simulation for tokenomics"""
    np.random.seed(42)  # For reproducibility
    
    months = list(range(params.simulation_months + 1))
    
    # Initialize arrays
    price_history = [params.initial_price]
    market_cap_history = [params.initial_price * params.initial_circulating]
    circulating_history = [params.initial_circulating]
    total_supply_history = [params.total_supply]
    staking_ratio_history = [0.0]
    burned_history = [0.0]
    
    current_supply = params.total_supply
    current_circulating = params.initial_circulating
    current_price = params.initial_price
    total_burned = 0
    total_staked = 0
    
    # Monthly simulation
    for month in range(1, params.simulation_months + 1):
        # 1. Calculate vesting unlocks
        team_unlock = 0
        investor_unlock = 0
        
        if month > params.team_cliff_months:
            months_vested = min(month - params.team_cliff_months, params.team_vesting_months)
            team_unlock = (params.total_supply * params.team_pct / 100) * (months_vested / params.team_vesting_months)
        
        if month > params.investors_cliff_months:
            months_vested = min(month - params.investors_cliff_months, params.investors_vesting_months)
            investor_unlock = (params.total_supply * params.investors_pct / 100) * (months_vested / params.investors_vesting_months)
        
        # New tokens entering circulation
        new_tokens = (team_unlock + investor_unlock) / params.team_vesting_months
        current_circulating = min(current_circulating + new_tokens, current_supply)
        
        # 2. Inflation
        monthly_inflation = params.inflation_rate / 12 / 100
        current_supply *= (1 + monthly_inflation)
        
        # 3. Burn mechanism
        monthly_burn = current_circulating * params.burn_rate / 100 / 12
        current_supply -= monthly_burn
        current_circulating -= monthly_burn
        total_burned += monthly_burn
        
        # 4. Staking
        staking_participants = current_circulating * 0.3  # 30% stake
        staking_rewards = staking_participants * params.staking_apy / 100 / 12
        current_supply += staking_rewards
        total_staked = staking_participants
        
        # 5. Price dynamics (demand-driven with volatility)
        demand_growth = params.initial_demand_growth / 100 / 12
        volatility_monthly = params.volatility / 100 / np.sqrt(12)
        
        # Price impact from supply changes
        supply_ratio = current_circulating / params.initial_circulating
        
        # Demand factor (grows over time with noise)
        demand_factor = (1 + demand_growth) ** month
        
        # Random walk component
        random_factor = np.exp(np.random.normal(0, volatility_monthly))
        
        # Calculate new price
        base_price = params.initial_price * demand_factor / np.sqrt(supply_ratio)
        current_price = base_price * random_factor
        
        # Ensure price doesn't go negative
        current_price = max(current_price, params.initial_price * 0.01)
        
        # Record history
        price_history.append(current_price)
        market_cap_history.append(current_price * current_circulating)
        circulating_history.append(current_circulating)
        total_supply_history.append(current_supply)
        staking_ratio_history.append(total_staked / current_circulating if current_circulating > 0 else 0)
        burned_history.append(total_burned)
    
    # Calculate statistics
    prices = np.array(price_history)
    returns = np.diff(prices) / prices[:-1]
    
    # Sharpe ratio (annualized)
    if len(returns) > 0 and np.std(returns) > 0:
        sharpe = np.mean(returns) / np.std(returns) * np.sqrt(12)
    else:
        sharpe = 0
    
    # Max drawdown
    peak = np.maximum.accumulate(prices)
    drawdown = (peak - prices) / peak
    max_drawdown = np.max(drawdown)
    
    # Value at Risk (95%)
    var_95 = np.percentile(returns, 5) if len(returns) > 0 else 0
    
    return SimulationResult(
        months=months,
        price_history=price_history,
        market_cap_history=market_cap_history,
        circulating_supply_history=circulating_history,
        total_supply_history=total_supply_history,
        staking_ratio_history=staking_ratio_history,
        burned_tokens_history=burned_history,
        final_price=price_history[-1],
        final_market_cap=market_cap_history[-1],
        max_price=max(price_history),
        min_price=min(price_history),
        price_volatility=float(np.std(returns) * np.sqrt(12)) if len(returns) > 0 else 0,
        total_burned=total_burned,
        total_staked=total_staked,
        sharpe_ratio=sharpe,
        max_drawdown=max_drawdown,
        var_95=var_95
    )


async def get_mimo_analysis(params: TokenomicsInput, result: SimulationResult) -> str:
    """Get AI analysis from MiMo"""
    prompt = f"""Analyze this tokenomics simulation for {params.token_name}:

Token Parameters:
- Total Supply: {params.total_supply:,.0f}
- Initial Price: ${params.initial_price}
- Initial Circulating: {params.initial_circulating:,.0f}
- Inflation Rate: {params.inflation_rate}% per year
- Burn Rate: {params.burn_rate}% of transactions
- Staking APY: {params.staking_apy}%

Distribution:
- Team: {params.team_pct}%
- Investors: {params.investors_pct}%
- Community: {params.community_pct}%
- Treasury: {params.treasury_pct}%
- Staking: {params.staking_pct}%
- Liquidity: {params.liquidity_pct}%

Simulation Results ({params.simulation_months} months):
- Final Price: ${result.final_price:.4f}
- Final Market Cap: ${result.final_market_cap:,.0f}
- Max Price: ${result.max_price:.4f}
- Min Price: ${result.min_price:.4f}
- Price Volatility: {result.price_volatility:.2%}
- Sharpe Ratio: {result.sharpe_ratio:.2f}
- Max Drawdown: {result.max_drawdown:.2%}
- Total Burned: {result.total_burned:,.0f} tokens
- Total Staked: {result.total_staked:,.0f} tokens

Provide:
1. Overall assessment (Good/Neutral/Bad)
2. Key strengths and weaknesses
3. Risk analysis
4. Optimization recommendations
5. Market outlook

Be concise but thorough."""

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{MIMO_API_URL}/chat/completions",
                json={
                    "model": MIMO_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 1000,
                    "temperature": 0.7
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                return "AI analysis unavailable at the moment."
    except Exception as e:
        return f"AI analysis error: {str(e)}"


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main page"""
    with open("templates/index.html", "r") as f:
        return f.read()


@app.post("/api/simulate")
async def simulate(params: TokenomicsInput):
    """Run tokenomics simulation"""
    try:
        result = run_simulation(params)
        
        # Get AI analysis
        analysis = await get_mimo_analysis(params, result)
        
        return {
            "success": True,
            "simulation": result.dict(),
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/compare")
async def compare_scenarios(params: List[TokenomicsInput]):
    """Compare multiple tokenomics scenarios"""
    try:
        results = []
        for p in params:
            result = run_simulation(p)
            results.append({
                "name": p.token_name,
                "simulation": result.dict()
            })
        
        return {
            "success": True,
            "scenarios": results,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/presets")
async def get_presets():
    """Get preset tokenomics models"""
    presets = {
        "defi": {
            "name": "DeFi Token",
            "params": TokenomicsInput(
                token_name="DeFi Token",
                total_supply=1_000_000_000,
                initial_price=0.05,
                initial_circulating=100_000_000,
                team_pct=15,
                investors_pct=20,
                community_pct=30,
                treasury_pct=15,
                staking_pct=10,
                liquidity_pct=10,
                inflation_rate=8,
                burn_rate=3,
                staking_apy=20,
                initial_demand_growth=15,
                volatility=40
            )
        },
        "gaming": {
            "name": "Gaming Token",
            "params": TokenomicsInput(
                token_name="Gaming Token",
                total_supply=10_000_000_000,
                initial_price=0.001,
                initial_circulating=1_000_000_000,
                team_pct=10,
                investors_pct=15,
                community_pct=40,
                treasury_pct=10,
                staking_pct=15,
                liquidity_pct=10,
                inflation_rate=12,
                burn_rate=5,
                staking_apy=10,
                initial_demand_growth=25,
                volatility=50
            )
        },
        "governance": {
            "name": "Governance Token",
            "params": TokenomicsInput(
                token_name="Governance Token",
                total_supply=100_000_000,
                initial_price=1.0,
                initial_circulating=20_000_000,
                team_pct=20,
                investors_pct=25,
                community_pct=25,
                treasury_pct=20,
                staking_pct=5,
                liquidity_pct=5,
                inflation_rate=3,
                burn_rate=1,
                staking_apy=8,
                initial_demand_growth=8,
                volatility=25
            )
        },
        "meme": {
            "name": "Meme Token",
            "params": TokenomicsInput(
                token_name="Meme Token",
                total_supply=1_000_000_000_000,
                initial_price=0.000001,
                initial_circulating=500_000_000_000,
                team_pct=5,
                investors_pct=10,
                community_pct=60,
                treasury_pct=5,
                staking_pct=10,
                liquidity_pct=10,
                inflation_rate=0,
                burn_rate=2,
                staking_apy=5,
                initial_demand_growth=100,
                volatility=80
            )
        }
    }
    
    return {
        "success": True,
        "presets": presets
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)
