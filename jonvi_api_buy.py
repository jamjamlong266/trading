import hmac
import hashlib
import urllib
import json
import httplib
import time
import requests

class JonviClient_Buy(object):
    __headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
    }

    def __init__(self, access_id, secret_key):

        self.api_key = access_id   
        self.secret_key = secret_key
        self.url = 'api.jonvi.com'
        self.headers = self.__headers
        

    
    def get_access_token(self): 
        
        params = {'appKey': self.api_key,'appSecret': self.secret_key}
        
        response = requests.post("https://api.jonvi.com/ak/getAccessToken",params)
        resp = json.loads(response.text)
        self.xtoken=resp["data"]
        self.headers['accessToken']=self.xtoken
        
        return resp
        
        
    def sell_orderbook(self,pair, size): 
        
        response = requests.get("https://api.jonvi.com/order/get_asks_price_volume?txPair="+pair+"&size="+str(size))
        resp = json.loads(response.text)
        
        self.ask1 = 0
        self.ask1vol = 0

        if resp['data'] != []:
            self.ask1 = resp['data'][0]['price']
            self.ask1vol = resp['data'][0]['volume']
        
        return resp
    
    def buy_orderbook(self,pair, size): 
        
        response = requests.get("https://api.jonvi.com/order/get_bids_price_volume?txPair="+pair+"&size="+str(size))
        resp = json.loads(response.text)

        self.bid1 = 0
        self.bid1vol = 0

        if resp['data'] !=[]:
            self.bid1=resp['data'][0]['price']
            self.bid1vol=resp['data'][0]['volume']
        
        return resp
        
        
    def balance(self): 
        
        response = requests.get("https://api.jonvi.com/user/get_user_coins",headers=self.headers)
        resp = json.loads(response.text)
        for item in resp['data']:
            if item['symbol']=='BTC':
                self.btc=item['useBalance']
                self.btc_pending=item['freezeBalance']
            elif item['symbol']=='USDT':
                self.usd=item['useBalance']
                self.usd_pending=item['freezeBalance']
            elif item['symbol']=='BCH':
                self.bch=item['useBalance']
                self.bch_pending=item['freezeBalance']
            elif item['symbol']=='ETH':
                self.eth=item['useBalance']
                self.eth_pending=item['freezeBalance']
            elif item['symbol']=='JE':
                self.je=item['useBalance']
                self.je_pending=item['freezeBalance']
            elif item['symbol']=='LTC':
                self.ltc=item['useBalance']
                self.ltc_pending=item['freezeBalance']
            elif item['symbol']=='eMYR':
                self.myr=item['useBalance']
                self.myr_pending=item['freezeBalance']
        return resp
        
    
    def place_order(self,pair, amount, price, side): 
        
        params = {'accessToken':self.xtoken, 'txPair': pair, 'volume': amount, 'price': price, 'side': side}
        # print self.headers
        response = requests.post("https://api.jonvi.com/order/create",headers=self.headers,params=params)
        resp = json.loads(response.text)
        # print "order placed"
        
        return resp
    
    
    def cancel_order(self, order_id): 
        
        params = {'accessToken': self.xtoken, 'orderId': order_id}
        
        response = requests.post("https://api.jonvi.com/order/cancel",headers=self.headers,params=params)
        resp = json.loads(response.text)

        return resp

    def current_order(self, pair):
        params = {'accessToken':self.xtoken, 'txPair': pair}
        response = requests.get("https://api.jonvi.com/order/get_current_order",headers=self.headers,params=params)

        if response.status_code == 200:
            resp = json.loads(response.text)
    
            self.askID = 0
            self.askPrice = 0
            self.askVol = 0
    
            self.bidID = 0
            self.bidPrice = 0
            self.bidVol = 0
        
            if resp['data'] != []:
                for orderId in resp['data']:
                    if orderId['side'] == 2:
                        self.askID = orderId['id']
                        self.askPrice = orderId['price']
                        self.askVol = orderId['volume']
                    elif orderId['side'] == 1:
                        self.bidID = orderId['id']
                        self.bidPrice = orderId['price']
                        self.bidVol = orderId['volume']
        else:
            self.current_order(pair)
        return resp
        

        
