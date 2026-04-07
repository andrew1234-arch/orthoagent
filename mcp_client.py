import requests
import time

class KrakenCLIClient:
    """Fast public ticker via direct API + CLI fallback for orders"""
    def __init__(self):
        print("📄 OrthoAgent using fast public Kraken API for data + CLI for trading")
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "OrthoAgent-Hackathon"})

    def get_ticker(self, pair="XBTUSD"):
        """Fast public ticker (no CLI timeout)"""
        try:
            url = f"https://api.kraken.com/0/public/Ticker?pair={pair}"
            r = self.session.get(url, timeout=8)
            data = r.json()
            if data.get("error"):
                return {"error": data["error"]}
            result = data.get("result", {})
            # Kraken returns XBTUSD key
            ticker_data = list(result.values())[0] if result else {}
            return {
                "last": ticker_data.get("c", [None])[0],
                "pair": pair,
                "raw": ticker_data
            }
        except Exception as e:
            return {"error": str(e)}

    def get_paper_balance(self):
        """CLI for paper (private)"""
        try:
            result = subprocess.run(["kraken", "paper", "balance", "-o", "json"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return json.loads(result.stdout) if result.stdout.strip() else {"status": "ok"}
            return {"error": result.stderr.strip()}
        except:
            return {"error": "Paper balance CLI failed"}

if __name__ == "__main__":
    client = KrakenCLIClient()
    print("Ticker test:", client.get_ticker())
