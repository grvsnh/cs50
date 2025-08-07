import sys
import requests

def main():
    if len(sys.argv) != 2:
        sys.exit("Missing command-line argument")

    try:
        bitcoins = float(sys.argv[1])
    except ValueError:
        sys.exit("Command-line argument is not a number")

    API_KEY = "a9f18a15f6930ae513f645006b3c666789653f5ce40d260551c6a0d8b13ea8d6"
    url = "https://rest.coincap.io/v3/assets/bitcoin"

    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        price = float(data["data"]["priceUsd"])
    except requests.RequestException:
        sys.exit("Request error while accessing CoinCap API")
    except (KeyError, ValueError):
        sys.exit("Error processing API response")

    total_cost = bitcoins * price

    print(f"${total_cost:,.4f}")

if __name__ == "__main__":
    main()
