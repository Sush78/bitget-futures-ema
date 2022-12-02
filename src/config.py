api_key = '' # api key example given
secret_key = '' # secret key for binance api 
symbol =  "BTCUSDT_UMCBL" # "BTCUSDT_UMCBL" # symbol to trade on 
interval = 5 #time interval to trade (in seconds): Hits API for new process in intervals
granularity = "3m"  #"6H" # granularity of candles 
quantity = 30 # amount of usd ( base coin) to trade with 
short_ema = 9 # short EMA
long_ema = 21  # Long EMA
startDate = "05.08.2022 08:33:41,76"   # candle data start date (DD.MM.YYYY hh:mm:ms,76)
endDate = "29.11.2022 11:14:48,76"      # candle data end date (DD.MM.YYYY hh:mm:ms,76)
# Don't use spot API without changing logic call stack: Diff resp struct with 1m delay in response
market_api_url = "https://api.bitget.com/api/mix/v1/market" #"https://api.bitget.com/api/spot/v1/market" 
strategy = "ichimoku"   # pick out of "ema", "ichimoku"

strategy_map = {"ema": 1, "ichimoku": 2}