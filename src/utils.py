from datetime import datetime
import requests
from config import market_api_url

def convertDateToTimestamp(date):
    if(isinstance(date, str)) :
        dt_obj = datetime.strptime(date,
                            '%d.%m.%Y %H:%M:%S,%f')
    else: dt_obj = date
    epoch = datetime.utcfromtimestamp(0)
    return int((dt_obj - epoch).total_seconds() * 1000) # dt_obj.timestamp() * 1000

def makeApiCall(url, params, method="get"):
    base_url = market_api_url + url
    #print("apirParams: ", params)
    response = requests.get(base_url, params=params)
    return response.json()