import requests
import matplotlib.pyplot as plt

def fetch_market_chart(coin_id, days=30, currency='usd'):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {'vs_currency': currency, 'days': days}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def fetch_global_data():
    url = "https://api.coingecko.com/api/v3/global"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['data']

def plot_price_comparison(btc_data, eth_data):
    days = list(range(len(btc_data['prices'])))

    btc_prices = [p[1] for p in btc_data['prices']]
    eth_prices = [p[1] for p in eth_data['prices']]

    plt.figure(figsize=(12,6))
    plt.plot(days, btc_prices, label='Bitcoin (BTC)', color='orange')
    plt.plot(days, eth_prices, label='Ethereum (ETH)', color='purple')
    plt.title('BTC vs ETH Price Trend (Last 30 Days)')
    plt.xlabel('Days Ago')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("price_comparison.png")
    plt.show()

def plot_volume_comparison(btc_data, eth_data):
    days = list(range(len(btc_data['total_volumes'])))

    btc_volumes = [v[1] for v in btc_data['total_volumes']]
    eth_volumes = [v[1] for v in eth_data['total_volumes']]

    width = 0.4
    plt.figure(figsize=(12,6))
    plt.bar([d - width/2 for d in days], btc_volumes, width=width, label='BTC Volume', color='skyblue')
    plt.bar([d + width/2 for d in days], eth_volumes, width=width, label='ETH Volume', color='lightgreen')
    plt.title('BTC vs ETH Daily Trading Volume (Last 30 Days)')
    plt.xlabel('Days Ago')
    plt.ylabel('Volume (USD)')
    plt.legend()
    plt.tight_layout()
    plt.savefig("volume_comparison.png")
    plt.show()

def plot_market_cap_pie(global_data):
    btc_cap = global_data['market_cap_percentage']['btc']
    eth_cap = global_data['market_cap_percentage']['eth']
    others = 100 - (btc_cap + eth_cap)

    labels = ['Bitcoin', 'Ethereum', 'Others']
    sizes = [btc_cap, eth_cap, others]
    colors = ['orange', 'purple', 'grey']

    plt.figure(figsize=(7,7))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
    plt.title('Crypto Market Cap Dominance')
    plt.tight_layout()
    plt.savefig("market_cap_pie.png")
    plt.show()

def main():
    print("Fetching data... Please wait.")
    btc_data = fetch_market_chart('bitcoin')
    eth_data = fetch_market_chart('ethereum')
    global_data = fetch_global_data()

    while True:
        print("\nChoose Visualization Option:")
        print("1. BTC vs ETH Price Trend")
        print("2. BTC vs ETH Trading Volume")
        print("3. Crypto Market Cap Pie Chart")
        print("4. Exit")
        choice = input("Enter choice (1-4): ")

        if choice == '1':
            plot_price_comparison(btc_data, eth_data)
        elif choice == '2':
            plot_volume_comparison(btc_data, eth_data)
        elif choice == '3':
            plot_market_cap_pie(global_data)
        elif choice == '4':
            print("Exiting. Thanks for using the dashboard!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == '__main__':
    main()
