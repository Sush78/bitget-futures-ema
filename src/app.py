import time 
from datetime import datetime
import sys
import math
from config import symbol, granularity, short_ema, long_ema, startDate, strategy, strategy_map, interval
from utils import convertDateToTimestamp, makeApiCall
from ichimoku import calculate_metrics, extractPriceListWithMetrics, getLatestPrice

def getCandleData():
    response = []
    params = dict()
    params["symbol"] = symbol
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

def ema(s, n):
    """
    returns an n period exponential moving average for
    the time series s
    s is a list ordered from oldest (index 0) to most
    recent (index -1)
    n is an integer
    returns a numeric array of the exponential
    moving average
    """
    #s = array(s)
    ema = []
    j = 1

    #get n sma first and calculate the next n period ema
    sma = sum(s[:n]) / n
    multiplier = 2 / float(1 + n)
    ema.append(sma)

    #EMA(current) = ( (Price(current) - EMA(prev) ) x Multiplier) + EMA(prev)
    ema.append(( (s[n] - sma) * multiplier) + sma)

    #now calculate the rest of the values
    for i in s[n+1:]:
        tmp = ( (i - ema[j]) * multiplier) + ema[j]
        j = j + 1
        ema.append(tmp)

    return ema

# main function #
def main_ema():
   print("Using EMA to look for new trades at an interval of {} seconds".format(interval))
   print("Watching: ",symbol)
   last_emaShort = None
   last_emaLong = None
   buy = True
   sell = False
   i=0
   while True:
        candleData = getCandleData()
        priceList = extractPriceList(candleData)
        #print(price)
        emaShort = ema(priceList, short_ema)[-1]
        emaLong = ema(priceList, long_ema)[-1]
        print("ema1: {}, ema2: {}".format(emaShort, emaLong))
        print("lastema1: {}, lastema2: {}".format(last_emaShort, last_emaLong))

        if(emaShort > emaLong and last_emaShort and not buy):  # looking for crossOver (short crosses long)
            print("trying up cross")
            if(last_emaShort < last_emaLong):
                print("buy it")
                buy = True
                sell = False
                break
                

        if(emaLong  > emaShort and last_emaShort and not sell):  # looking for crossOver (long crosses short)
            print("trying down cross")
            if(last_emaLong < last_emaShort):
                print("Sell it")
                sell = True
                buy = False
                break


        last_emaShort = emaShort 
        last_emaLong = emaShort
        i+=1
        print("-------------------------")
        time.sleep(interval)

def main_ichimoku():
    print("Using Ichimoku to look for new trades at an interval of {} seconds".format(interval))
    print("Watching: ", symbol)
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
            if last_conversionLine < last_baseLine:
                print("Crossover detected: UP")
                if (currentPrice > line_spanA[-26] 
                        and currentPrice > line_spanB[-26]) and laggingLine[-1] > priceList[-26]['close']:
                    print("Buy it now at {}!".format(currentPrice))
                    buy = True
                    sell = False
                    break

        if current_baseLine > current_conversionLine and last_conversionLine and not sell:
            if last_baseLine < last_conversionLine:
                print("Crossover detected: DOWN")
                if (currentPrice < line_spanA[-26] 
                        and currentPrice < line_spanB[-26]) and laggingLine[-1] < priceList[-26]['close']:
                    print("Sell it now at {}!".format(currentPrice))
                    buy = False
                    sell = True
                    break

        last_baseLine = current_baseLine
        last_conversionLine = current_conversionLine
        print("-----------------------------------")
        time.sleep(interval)

## MAIN ##    
if __name__ == "__main__":
    if(short_ema > 100 or long_ema > 100):
        print("Only 100 recrods are returned by the API, please use short and long ema values below that")
        exit() 
    strategy_id = strategy_map[strategy]
    if(not strategy_id or strategy_id == 1):
        main_ema()
    elif strategy_id == 2:
        main_ichimoku()
    else:
        print("Please enter a valid strategy. Check config file")