import time 
from datetime import datetime
import sys
import math
from config import symbol, granularity, short_ema, long_ema, startDate
from utils import convertDateToTimestamp, makeApiCall

def getCandleData():
    params = dict()
    params["symbol"] = symbol
    params["granularity"] = granularity
    params["startTime"] = convertDateToTimestamp(startDate)    # 1659688421000
    params["endTime"] = convertDateToTimestamp(datetime.now()) # 1669763688000
    return makeApiCall("/candles", params=params)

def extractPriceList(data):
    priceList = []
    for d in data:
        priceList.append(float(d[4]))   # extract closing price from candles api response 
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
def main():
   print("Looking for new Trades....")
   print("Watching: ",symbol)
   last_ema50 = None
   last_ema200 = None
   buy = False
   sell = False
   i=0
   while True:
        candleData = getCandleData()
        print("totalrecords: ",len(candleData))
        priceList = extractPriceList(candleData)
        #print(price)
        ema50 = ema(priceList, short_ema)[-1]
        ema200 = ema(priceList, long_ema)[-1]
        print("ema1: {}, ema2: {}".format(ema50, ema200))
        print("lastema1: {}, lastema2: {}".format(last_ema50, last_ema200))
        print("-------------------------")

        if(ema50 > ema200 and last_ema50 and not buy):  # looking for crossOver
            print("trying up cross")
            if(last_ema50 < last_ema200):
                print("buy it")
                buy = True
                sell = False
                break
                

        if(ema200  > ema50 and last_ema50 and not sell):
            print("trying down cross")
            if(last_ema200 < last_ema50):
                print("Sell it")
                sell = True
                buy = False
                break


        last_ema50 = ema50 
        last_ema200 = ema200
        i+=1
        time.sleep(10)


if __name__ == "__main__":
    main()
