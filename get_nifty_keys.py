import pandas as pd
import requests
import gzip
import json
import io

def get_nifty50_instruments():
    # 1. Official Upstox NSE Instrument JSON URL
    url = "https://assets.upstox.com/market-quote/instruments/exchange/NSE.json.gz"
    
    print("Downloading Upstox NSE instrument master...")
    response = requests.get(url)
    
    if response.status_code == 200:
        # 2. Decompress and parse JSON
        with gzip.GzipFile(fileobj=io.BytesIO(response.content)) as f:
            data = json.load(f)
            
        df = pd.DataFrame(data)
        
        # 3. List of current Nifty 50 symbols (Update this as Nifty rebalances)
        nifty50_symbols = [
            'RELIANCE', 'TCS', 'HDFCBANK', 'ICICIBANK', 'INFY', 'BHARTIARTL',
            'ITC', 'SBIN', 'LICI', 'LT', 'KOTAKBANK', 'AXISBANK', 'HCLTECH',
            'M&M', 'SUNPHARMA', 'ADANIENT', 'MARUTI', 'ULTRACEMCO', 'TITAN',
            'NTPC', 'TATASTEEL', 'POWERGRID', 'ASIANPAINT', 'BAJFINANCE',
            'TATAMOTORS', 'JSWSTEEL', 'ADANIPORTS', 'NESTLEIND', 'BAJAJFINSV',
            'COALINDIA', 'HINDUNILVR', 'ONGC', 'GRASIM', 'HINDALCO', 'SBILIFE',
            'TECHM', 'WIPRO', 'EICHERMOT', 'DIVISLAB', 'CIPLA', 'LTIM',
            'BRITANNIA', 'BAJAJ-AUTO', 'HEROMOTOCO', 'DRREDDY', 'APOLLOHOSP',
            'TRENT', 'BEL', 'SHRIRAMFIN', 'BPCL'
        ]

        # 4. Filter for Nifty 50 Stocks (NSE_EQ) and the Nifty Index
        # The Index itself has the key: NSE_INDEX|Nifty 50
        nifty_stocks = df[df['trading_symbol'].isin(nifty50_symbols) & (df['segment'] == 'NSE_EQ')]
        
        # Add the Index manually to ensure it's included
        index_key = df[df['instrument_key'] == 'NSE_INDEX|Nifty 50']
        final_list = pd.concat([index_key, nifty_stocks])

        print(f"Successfully filtered {len(final_list)} instruments.")
        return final_list[['trading_symbol', 'instrument_key', 'isin']]
    else:
        print("Failed to download file.")
        return None

# Execute and save to CSV for your dashboard
nifty_data = get_nifty50_instruments()
if nifty_data is not None:
    nifty_data.to_csv("nifty50_upstox_keys.csv", index=False)
    print("Keys saved to nifty50_upstox_keys.csv")
