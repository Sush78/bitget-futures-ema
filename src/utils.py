from datetime import datetime
import requests
from config import market_api_url, domain_url
import time
import hmac
import base64
import os


def convertDateToTimestamp(date):
    if(isinstance(date, str)) :
        dt_obj = datetime.strptime(date,
                            '%d.%m.%Y %H:%M:%S,%f')
    else: dt_obj = date
    epoch = datetime.utcfromtimestamp(0)
    return int((dt_obj - epoch).total_seconds() * 1000) # dt_obj.timestamp() * 1000

def makeApiCall(url, params):
    base_url = market_api_url + url
    #print("apirParams: ", params)
    response = requests.get(base_url, params=params)
    return response.json()

def sign(message, secret_key):
    print("To be signed: ", message)
    mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    d = mac.digest()
    return base64.b64encode(d)


def pre_hash(timestamp, method, request_path, queryString, body):
    if not body:
        return str(timestamp) + str.upper(method) + request_path + queryString
    return str(timestamp) + str.upper(method) + request_path + body

def makeVerifiedApiCall(method, request_path, queryString, body):
    timeMs = int(time.time()) *1000
    signature = sign(pre_hash(timeMs, method, request_path, queryString ,body), os.getenv("API_secret"))
    headers = {"ACCESS-KEY": os.getenv('API_key'), "ACCESS-SIGN": signature, "ACCESS-PASSPHRASE": os.getenv('PASS_PHRASE'), "ACCESS-TIMESTAMP": str(timeMs), "locale": "en-US","Content-Type": "application/json"}
    if method == "GET":
        try:
            url = domain_url+request_path+queryString
            response = requests.get(url, headers=headers)
            return response.json()
        except Exception as e:
            print("Exceptions: ", e)
            print("Connection refused, will retry")
    if method == "POST":
        url = domain_url+request_path
        response = requests.post(url, headers=headers, data=body)
        return response.json()