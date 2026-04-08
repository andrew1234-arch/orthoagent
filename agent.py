from mcp_client import KrakenCLIClient
from prism import PrismClient
import time
from dotenv import load_dotenv

load_dotenv(".env")
load_dotenv(".env.local", override=True)

def main():
    print("🚀 OrthoAgent starting...")
    client = KrakenCLIClient()
    prism = PrismClient()

    for i in range(4):
        print(f"\n=== Cycle {i+1} ===")
        
        factors = prism.get_orthogonal_factors()
        print("🧠 Orthogonal Factors:", factors)

        ticker = client.get_ticker("XBTUSD")
        print("📈 Kraken Ticker:", ticker)

        if factors.get("recommendation") == "BUY":
            print("✅ Orthogonal signal strong → Paper trade ready")

        time.sleep(5)

    print("\n✅ Test completed. Now we add real PRISM + ERC-8004.")

if __name__ == "__main__":
    main()
