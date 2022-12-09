''' 
Util functions for ichimoku strategy
'''
from datetime import datetime
from config import symbol, demoSymbol
from utils import makeApiCall

# extract closing price with high and low
def extractPriceListWithMetrics(data):
    priceList = []
    for d in data:
        priceList.append({'close':float(d[4]), 'high': float(d[2]), 'low': float(d[3])})   # extract closing price from candles api response 
    return priceList

def calculate_metrics(data):
    baseLine, laggingLine = calculate_and_makeList(data, 26)    # 26 period  
    conversionLine, _ = calculate_and_makeList(data)  # 9 period
    lineA, lineB = calculateCloud(data, baseLine, conversionLine)
    return baseLine, conversionLine, laggingLine, lineA, lineB

def calculateCloud(data, baseLine, conversionLine):
    line_spanA = []   # 26 period aheead current avg
    line_spanB = []   # 26 period ahead 52 period behing avg (high, low)
    len_ = len(data)
    periodA = 26
    periodB = 52
    for i in range(len_ - periodA+1):
        line_spanA.append((baseLine[i+periodA] + conversionLine[i+periodA]) / 2)   # line_spanA[i-26]
    for i in range(len_ - periodA+1):
        highest_high, lowest_low = 0, data[-1]['low']    
        for j in range(i+periodA-periodB, i+periodA):
            lowest_low = min(lowest_low, data[j]['low'])
            highest_high = max(highest_high, data[j]['high'])
        spanBVal = (lowest_low + highest_high) / 2
        line_spanB.append(spanBVal)   # line_spanB[i-26]    
    return line_spanA, line_spanB

# util to calculate baseline and conversionline
def calculate_and_makeList(data, lrange=9):
    default_val = 0
    llist = [default_val for i in range(lrange)]
    laggingList = []
    len_ = len(data)
    i = lrange - 1
    while i < len_:
        lowlest_low, highest_high = data[i]['low'], 0
        for j in range(i-lrange-1,i+1):
            lowlest_low = min(lowlest_low, data[j]['low'])
            highest_high = max(highest_high, data[j]['high'])
        calculated_val = (highest_high + lowlest_low) / 2
        llist.append(calculated_val)
        laggingList.append(data[i-lrange-1]['close'])   # creating chikou sen (only for 26 period)
        i += 1
    return llist, laggingList

def getLatestPrice():
    params = dict()
    params["symbol"] = demoSymbol
    response = makeApiCall("/index", params=params)
    return float(response["data"]["index"])