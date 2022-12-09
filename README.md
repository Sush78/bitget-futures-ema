# bitget-futures-ema
a simple EMA trading bot for bitget futures using two strategies
- EMA crossover (short v long)
- Ichimoku 
- RSI

Includes a config file. Feel free to play around!

## Trading Details:
The model uses bitget APIs (candles and indexPrice) to fetch latest candle details and index price. It looks for the symbols specified in config file. If you want to change it please use correct symbols from bitget API docs. The process of fetching data, making calculations and predicting BUY/SELL positions, post the trade to the exchange is repeated in intervals of the value specifric for "interval" in config file.
Feel free to change configs. There might be errors for some specifc config values as the code is not extesibly tested yet.

Following are the trading strategies used. All of them are very basic with no risk-managment. It will be added in later dev stages

- EMA Cross-over: (Exponential Moving Average) The model uses bitget API to fetch data continuously and looks for following signals
    - short_ema crossing above the long_ema for a BUY signal
    - short_ema crossing below the long_ema for a SELL signal

- Ichimoku: The model uses bitget API to fetch data continuously and looks for following signals
    - Go long (Buy): Whenever the Tenkan-sen crosses the Kijun-sen from the below to the above while the market price is above the  Ichimoku cloud. And finally, the Chikou span’s last value must be higher than the corresponding market price in the same point in time.
    - Go short (Sell): Whenever the Tenkan-sen crosses the Kijun-sen from the above to the below while the market price is below the Ichimoku cloud. And finally, the Chikou span’s last value must be lower than the corresponding market price in the same point in time.

- RSI Threshold cross-over: The model works similar to others. The thresholds can be changed from config files
    - Sell when RSI line crosses above the oversold threshold
    - Buy when RSI line crosses below the overbought threshold

Currenly the code opens a long positon for BUY signal and closes it for SELL. you can modify it to use short signals using the functins, openShortPosition(), closeShortPosition() in app.py file. The amount being traded (margin coin) can be changed from config file, "quantity" which is currently set to 0.1. 

### NOTE: 
All trades are made in demo/simulations environement, change the "productType" or the "symbol" property in comfig file for real environment