api_key = '' # api key for api
secret_key = '' # secret key for  api 

symbol = "BTCUSDT_UMCBL" # symbol to trade on || examples: BTCUSDT_UMCBL, ETHUSDT_UMCBL, XRPUSDT_UMCBL, LTCUSDT_UMCBL

interval = 5 # time interval to trade (in seconds): Hits API for new process in intervals

granularity = "1m" # granularity of candles , link: https://bitgetlimited.github.io/apidoc/en/mix/#producttype

quantity = 30 # amount of usd ( base coin) to trade with 

short_ema = 9 # short EMA
long_ema = 21 # Long EMA || API is returning only 100 records so long_ema is constrained to 100

rsi_period = 14  # period used for Relative Strength Index calculation
rsi_overbought = 49 # overbought threshold for RSI (in percentage | RSI value)
rsi_oversold = 30 # oversold threshold for RSI (in percentage | RSI value)
rsi_tolerance = 0 # RSI calculatins result in floating errors, this value is added to the result to match it with exchange value

startDate = "05.08.2022 08:33:41,76"   # candle data start date (DD.MM.YYYY hh:mm:ms,76)
endDate = "29.11.2022 11:14:48,76"      # candle data end date (DD.MM.YYYY hh:mm:ms,76)
# Don't use spot API without changing logic call stack: Diff resp struct with 1m delay in response
market_api_url = "https://api.bitget.com/api/mix/v1/market" #"https://api.bitget.com/api/spot/v1/market" 
strategy = "rsi"   # pick out of "ema", "ichimoku", "rsi"

strategy_map = {"ema": 1, "ichimoku": 2, "rsi": 3}