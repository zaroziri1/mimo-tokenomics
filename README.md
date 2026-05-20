# 🔮 MiMo Tokenomics Simulator

**AI-powered token economics simulation platform built with MiMo v2.5 Pro**

![MiMo Tokenomics](https://img.shields.io/badge/Powered%20by-MiMo%20v2.5%20Pro-6c5ce7)
![License](https://img.shields.io/badge/License-MIT-green)
![Python](https://img.shields.io/badge/Python-3.10+-blue)

## 🎯 Overview

MiMo Tokenomics Simulator is an advanced platform that simulates token economics using Monte Carlo methods and provides AI-powered analysis through MiMo v2.5 Pro. It helps crypto projects, investors, and researchers model and predict token dynamics before launch.

## ✨ Key Features

### 🧮 Simulation Engine
- **Monte Carlo Simulation** - Run thousands of price scenarios
- **Vesting Schedule Modeling** - Team, investor, and community vesting
- **Supply Dynamics** - Inflation, burning, and staking rewards
- **Price Discovery** - Demand-driven price modeling with volatility

### 📊 Analytics Dashboard
- **Real-time Charts** - Price, market cap, supply, staking metrics
- **Risk Metrics** - Sharpe ratio, max drawdown, Value at Risk (VaR)
- **Distribution Visualization** - Token allocation breakdown
- **Historical Tracking** - Full simulation history

### 🤖 AI Analysis (Powered by MiMo)
- **Tokenomics Assessment** - Good/Neutral/Bad rating
- **Strengths & Weaknesses** - Key factors analysis
- **Risk Analysis** - Potential vulnerabilities
- **Optimization Recommendations** - Improvement suggestions
- **Market Outlook** - Predictive insights

### 🎨 Preset Models
- **DeFi Token** - High yield, moderate risk
- **Gaming Token** - High supply, fast circulation
- **Governance Token** - Low inflation, stable
- **Meme Token** - High volatility, community-driven

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# Clone repository
git clone https://github.com/zaroziri1/mimo-tokenomics.git
cd mimo-tokenomics

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### Access
Open your browser and navigate to:
```
http://localhost:8080
```

## 📖 API Documentation

### Endpoints

#### `POST /api/simulate`
Run tokenomics simulation with custom parameters.

**Request Body:**
```json
{
  "token_name": "MyToken",
  "total_supply": 1000000000,
  "initial_price": 0.01,
  "initial_circulating": 100000000,
  "team_pct": 15,
  "investors_pct": 20,
  "community_pct": 30,
  "treasury_pct": 15,
  "staking_pct": 10,
  "liquidity_pct": 10,
  "inflation_rate": 5,
  "burn_rate": 2,
  "staking_apy": 15,
  "initial_demand_growth": 10,
  "volatility": 30,
  "simulation_months": 36
}
```

**Response:**
```json
{
  "success": true,
  "simulation": {
    "months": [0, 1, 2, ...],
    "price_history": [0.01, 0.012, 0.015, ...],
    "market_cap_history": [...],
    "circulating_supply_history": [...],
    "final_price": 0.045,
    "final_market_cap": 45000000,
    "sharpe_ratio": 1.2,
    "max_drawdown": 0.35,
    ...
  },
  "analysis": "MiMo AI analysis text...",
  "timestamp": "2026-05-21T10:30:00"
}
```

#### `GET /api/presets`
Get preset tokenomics models.

#### `POST /api/compare`
Compare multiple scenarios side-by-side.

#### `GET /health`
Health check endpoint.

## 🏗️ Architecture

```
mimo-tokenomics/
├── app.py                 # FastAPI backend
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html         # Frontend UI
└── static/                # Static assets
```

### Tech Stack
- **Backend:** Python, FastAPI, NumPy
- **Frontend:** HTML, CSS, JavaScript, Chart.js
- **AI:** MiMo v2.5 Pro (via API)
- **Simulation:** Monte Carlo methods

## 📊 Simulation Model

### Token Dynamics
1. **Vesting Unlocks** - Gradual release of team/investor tokens
2. **Inflation** - New token minting (configurable rate)
3. **Burning** - Token destruction from transactions
4. **Staking** - Lock-up and reward distribution
5. **Price Discovery** - Demand-driven with volatility

### Risk Metrics
- **Sharpe Ratio** - Risk-adjusted returns
- **Max Drawdown** - Largest peak-to-trough decline
- **Value at Risk (95%)** - Worst-case loss at 95% confidence
- **Volatility** - Annualized price volatility

## 🎯 Use Cases

### For Projects
- Model tokenomics before launch
- Test different distribution strategies
- Optimize vesting schedules
- Predict long-term sustainability

### For Investors
- Evaluate token economics
- Assess risk/reward profile
- Compare different projects
- Make informed investment decisions

### For Researchers
- Study token dynamics
- Test economic models
- Analyze market behavior
- Publish findings

## 🔧 Configuration

### Environment Variables
```bash
MIMO_API_URL=http://43.153.206.68:20128/v1
MIMO_MODEL=xmtp/mimo-v2.5-pro
```

### Customization
- Modify `app.py` to adjust simulation parameters
- Update `templates/index.html` for UI changes
- Add new presets in the `/api/presets` endpoint

## 📈 Roadmap

- [ ] Multi-chain support (Ethereum, Solana, BSC, etc.)
- [ ] Historical data integration (CoinGecko, DeFiLlama)
- [ ] Advanced Monte Carlo (10,000+ simulations)
- [ ] Export reports (PDF, CSV)
- [ ] Team collaboration features
- [ ] API rate limiting and authentication

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **MiMo v2.5 Pro** - AI analysis powered by Xiaomi's MiMo
- **FastAPI** - High-performance web framework
- **Chart.js** - Beautiful charts
- **NumPy** - Scientific computing

## 📞 Support

- **Demo:** [Live Demo](https://diffs-pee-figures-prize.trycloudflare.com)
- **Issues:** [GitHub Issues](https://github.com/zaroziri1/mimo-tokenomics/issues)
- **Email:** zaroziri@users.noreply.github.com

---

**Built with ❤️ and MiMo v2.5 Pro**
