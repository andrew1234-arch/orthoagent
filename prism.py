import requests
import os

PRISM_BASE = "https://api.prismapi.ai"

class PrismClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"X-API-Key": os.getenv("PRISM_API_KEY")})

    def get_orthogonal_factors(self, symbol="BTC"):
        # Simplified for speed
        return {
            "symbol": symbol,
            "idiosyncratic_alpha": 0.45,   # placeholder
            "market_beta": 0.52,
            "recommendation": "BUY"
        }