from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    res = [
    {
        "id": "bitcoin",
        "name": "Bitcoin",
        "symbol": "BTC",
        "rank": "1",
        "price_usd": "5295.5504633",
        "price_btc": "1.0",
        "24h_volume_usd": "12669322221.2",
        "market_cap_usd": "93569331745.0",
        "available_supply": "17669425.0",
        "total_supply": "17669425.0",
        "max_supply": "21000000.0",
        "percent_change_1h": "0.18",
        "percent_change_24h": "0.48",
        "percent_change_7d": "-0.44",
        "last_updated": "1556438011"
    }]
    return str(res)

if __name__ == '__main__':
    app.run()
