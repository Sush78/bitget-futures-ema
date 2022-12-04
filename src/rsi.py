'''
This file is used to calculate RSI
'''
from ema import calculate_ema
from config import rsi_period
import pandas as pd

def calculate_rsi(priceList):
    ## pandas method
    df = pd.DataFrame(priceList, columns=['price'])
    delta = df['price'].diff()
    up = delta.clip(lower=0)
    down = abs(delta.clip(upper=0))
    ema_up = up.ewm(com=14, adjust=False).mean()
    ema_down = down.ewm(com=14, adjust=False).mean()
    rs = ema_up/ema_down
    df['RSI'] = 100 - (100/(1 + rs))
    return list(df['RSI'])


## Vanilla method ##
# upTrend, downTrend = [0], [0]
# rsi=[]
# len_ = len(priceList)
# for i in range(1, len_):
#     val = priceList[i] - priceList[i-1]
#     if val > 0:
#         upTrend.append(val) 
#         downTrend.append(0) 
#     else:
#         downTrend.append(-1*val)   # store positive value
#         upTrend.append(0)
# emaUp = calculate_ema(upTrend, rsi_period)
# emaDown = calculate_ema(downTrend, rsi_period)
# len_up = len(emaUp)
# if(len_up != len(emaDown)):
#     print("Error in calculation of EMA up/down")
#     exit()
# rsi = []  # relative strength index
# for i in range(len_up):
#     rs = emaUp[i] / emaDown[i]  # relative strength 
#     rsi.append(100 - (100/(1+rs)))