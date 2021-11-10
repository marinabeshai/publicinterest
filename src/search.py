import requests

# ------------------------------------------------------------------------------------------------------------------------
def get_industry(ticker):
    try:
        if ticker == "BTC":
            return "cryptocurrency"
        
        url = "https://finance.yahoo.com/quote/TICKER/profile?p=TICKER".replace("TICKER", ticker)
        agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15'

        headers = {'User-Agent': agent}

        response = requests.get(url, headers=headers)

        if response.text.find("Industry") > 0: 
            key_line = response.text[response.text.find("Industry"):response.text.find("Industry")+150].split(">")
            return key_line[4].split("<")[0].replace("&amp;", "&")

        if "Fund Family</span>" in response.text:
            return "Fund"

    except Exception as e:
        print (ticker)
# ------------------------------------------------------------------------------------------------------------------------
