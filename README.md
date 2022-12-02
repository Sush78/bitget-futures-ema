# bitget-futures-ema
a simple EMA trading bot for bitget futures using two strategies
- EMA crossover (short v long)
- Ichimoku 

Includes a config file. Feel free to play around!

## Trading Details:
The model uses bitget APIs (candles and indexPrice) to fetch latest candle details and index price. It looks for the symbols specified in config file. If you want to change it please use correct symbols from bitget API docs. The process of fetching data, making calculations and predicting BUY/SELL positions is repeated in intervals of the value specifric for "interval" in config file.
Feel free to change configs. There might be errors for some specifc config values as the code is not extesibly tested yet.

Following are the trading strategies used. Both of them are very basic with no risk-managment. Will be added in later dev stages

- 1. EMA Cross-over
The model uses bitget API to fetch data continuously and looks for following signals
    - short_ema crossing above the long_ema for a BUY signal
    - short_ema crossing below the long_ema for a SELL signal

- 2. Ichimoku
The model uses bitget API to fetch data continuously and looks for following signals
    - Go long (Buy): Whenever the Tenkan-sen crosses the Kijun-sen from the below to the above while the market price is above the Ichimoku cloud. And finally, the Chikou span’s last value must be higher than the corresponding market price in the same point in time.
    - Go short (Sell): Whenever the Tenkan-sen crosses the Kijun-sen from the above to the below while the market price is below the Ichimoku cloud. And finally, the Chikou span’s last value must be lower than the corresponding market price in the same point in time.