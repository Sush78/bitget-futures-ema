import time 
from datetime import datetime
from config import symbol, granularity, short_ema, long_ema, startDate, strategy, strategy_map, interval, rsi_overbought, rsi_oversold \
    ,rsi_tolerance, demoSymbol, quantity
from utils import convertDateToTimestamp, makeApiCall, makeVerifiedApiCall
from ichimoku import calculate_metrics, extractPriceListWithMetrics, getLatestPrice
from rsi import calculate_rsi
from ema import calculate_ema, pandas_ema
import hmac
import base64
from dotenv import load_dotenv
import os

def getCandleData():
    response = []
    params = dict()
    params["symbol"] = demoSymbol
    params["granularity"] = granularity
    params["startTime"] = convertDateToTimestamp(startDate)    # 1659688421000
    params["endTime"] = convertDateToTimestamp(datetime.now()) # 1669763688000
    ## following two lines are for spot API: comment above 3 to uncomment below 2
    #params["period"] = granularity
    #params["limit"] = 100
    response = makeApiCall("/candles", params=params)
    return response

def extractPriceList(data):
    priceList = []
    for d in data:
        priceList.append(float(d[4]))   # extract closing price from candles api response 
    return priceList

# This is for spot API
def extractPriceListOtherApi(data):
    priceList = []
    print(len(data["data"]), data["data"][0])
    for d in data["data"]:
        priceList.append(float(d["close"]))   # extract closing price from candles api response 
    return priceList

## Strategies ##

def main_ema():
   print("Using EMA to look for new trades at an interval of {} seconds".format(interval))
   print("Using short EMA: {}, long EMA: {}".format(short_ema, long_ema))
   print("Watching: ", demoSymbol)
   last_emaShort = None
   last_emaLong = None
   buy = False
   sell = True
   i=0
   while True:
        candleData = getCandleData()
        priceList = extractPriceList(candleData)
        emaShort = calculate_ema(priceList, short_ema)[-1] # pandas_ema(priceList, short_ema)[-1]
        emaLong = calculate_ema(priceList, long_ema)[-1] # pandas_ema(priceList, long_ema)[-1]
        print("ema1: {}, ema2: {}".format(emaShort, emaLong))
        print("lastema1: {}, lastema2: {}".format(last_emaShort, last_emaLong))
        print("current prices: ", priceList[-1])

        if(emaShort > emaLong and last_emaShort and not buy):  # looking for crossOver (short crosses long)
            print("trying up cross")
            if(last_emaShort <= last_emaLong):
                print("buy it")
                openLongPosition()
                buy = True
                sell = False
                
        if(emaLong  > emaShort and last_emaShort and not sell):  # looking for crossOver (long crosses short)
            print("trying down cross")
            if(last_emaLong <= last_emaShort):
                print("Sell it")
                closeLongPosition()
                sell = True
                buy = False

        last_emaShort = emaShort 
        last_emaLong = emaLong
        i+=1
        print("-------------------------")
        time.sleep(interval)

def main_ichimoku():
    print("Using Ichimoku to look for new trades at an interval of {} seconds".format(interval))
    print("Watching: ", demoSymbol)
    baseLine, conversionLine, laggingLine, line_spanA, line_spanB = [], [], [], [], []
    last_baseLine, last_conversionLine = None, None
    buy = False
    sell = False
    while True:
        candleData = getCandleData()
        currentPrice = getLatestPrice()
        priceList = extractPriceListWithMetrics(candleData)
        baseLine, conversionLine, laggingLine, line_spanA, line_spanB = calculate_metrics(priceList)
        current_baseLine = baseLine[-1]
        current_conversionLine = conversionLine[-1]

        print("current baseline: {}, current conversionLine: {}".format(current_baseLine, current_conversionLine))
        print("last baseline: {}, last conversionLine: {}".format(last_baseLine, last_conversionLine))
        print("current price: {}".format(currentPrice))

        if current_conversionLine > current_baseLine and last_conversionLine and not buy:
            if last_conversionLine <= last_baseLine:
                print("Crossover detected: UP")
                if (currentPrice > line_spanA[-26] 
                        and currentPrice > line_spanB[-26]) and laggingLine[-1] > priceList[-26]['close']:
                    print("Buy it now at {}!".format(currentPrice))
                    openLongPosition()
                    buy = True
                    sell = False

        if current_baseLine > current_conversionLine and last_conversionLine and not sell:
            if last_baseLine <= last_conversionLine:
                print("Crossover detected: DOWN")
                if (currentPrice < line_spanA[-26] 
                        and currentPrice < line_spanB[-26]) and laggingLine[-1] < priceList[-26]['close']:
                    print("Sell it now at {}!".format(currentPrice))
                    closeLongPosition()
                    buy = False
                    sell = True

        last_baseLine = current_baseLine
        last_conversionLine = current_conversionLine
        print("-----------------------------------")
        time.sleep(interval)

def main_rsi_and_ema():
    print("Using RSI with EMA to look for new trades at an interval of {} seconds".format(interval))
    print("over: ", rsi_overbought)
    print("Watching: ", demoSymbol)
    last_rsi = None
    buy = False
    sell = False
    while True:
        candleData = getCandleData()
        priceList = extractPriceList(candleData)
        rsi_line = calculate_rsi(priceList)
        current_rsi = rsi_line[-1] + rsi_tolerance
        print("current RSI: {}, last RSI: {}, closing price: {}".format(current_rsi, last_rsi, priceList[-1]))
        if current_rsi > rsi_oversold and last_rsi and not buy:
            if last_rsi <= rsi_oversold:   # detecting crossover of rsi above oversold threshold
                print("Buy It!")
                openLongPosition()
                buy = True
                sell = False
                
        if current_rsi < rsi_overbought and last_rsi and not sell:
            if last_rsi >= rsi_overbought:   # detecting crossover of rsi below overbought threshold
                print("Sell It!")
                closeLongPosition()
                buy = False
                sell = True

        last_rsi = current_rsi
        print("-----------------------")
        time.sleep(interval)

def openLongPosition():
    print("-----------Opening long position------------")
    body = '{"symbol":' + '\"' + demoSymbol + '",' + '\"marginCoin":"SUSDT","side":"open_long","orderType":"market","size":' + '\"' + str(quantity) + '\"}'
    response = makeVerifiedApiCall('POST', '/api/mix/v1/order/placeOrder', None, body)
    print(response)
    print("-----------Done-----------")
    return


def closeLongPosition():
    print("-----------Closing long position------------")
    body = '{"symbol":' + '\"' + demoSymbol + '",' + '\"marginCoin":"SUSDT","side":"close_long","orderType":"market","size":' + '\"' + str(quantity) + '\"}'
    #body2 = '{"symbol":"SBTCSUSDT_SUMCBL","marginCoin":"SUSDT","side":"close_long","orderType":"market","size":"0.1"}'
    response = makeVerifiedApiCall('POST', '/api/mix/v1/order/placeOrder', None, body)
    print(response)
    print("-----------Done-----------")
    return

def openShortPosition():
    print("-----------Opening short position------------")
    body = '{"symbol":' + '\"' + demoSymbol + '",' + '\"marginCoin":"SUSDT","side":"open_short","orderType":"market","size":' + '\"' + str(quantity) + '\"}'
    response = makeVerifiedApiCall('POST', '/api/mix/v1/order/placeOrder', None, body)
    print(response)
    print("-----------Done-----------")
    return

def closeShortPosition():
    print("-----------Closing long position------------")
    body = '{"symbol":' + '\"' + demoSymbol + '",' + '\"marginCoin":"SUSDT","side":"close_short","orderType":"market","size":' + '\"' + str(quantity) + '\"}'
    response = makeVerifiedApiCall('POST', '/api/mix/v1/order/placeOrder', None, body)
    print(response)
    print("-----------Done-----------")
    return


## MAIN ##    
if __name__ == "__main__":
    load_dotenv()
    if(short_ema >= 100 or long_ema >= 100):
        print("Only 100 recrods are returned by the API, please use short and long ema values below that")
        exit() 
    strategy_id = strategy_map[strategy]
    if(not strategy_id or strategy_id == 1):
        main_ema()
    elif strategy_id == 2:
        main_ichimoku()
    elif strategy_id == 3:
        main_rsi_and_ema()
    else:
        print("Please enter a valid strategy. Check config file")
        exit()
    