from jonvi_api import JonviClient
from jonvi_api_buy import JonviClient_Buy
from binanceapi import BinanceClient
import time
# import request
import random
import json

pair = "btcusdt"
trading_pair = {"btcusdt"}

binance_api_key="8ovOuiaMx7NwodKm34xTH4Dq62zWZgB8Whnkojgx9ZfZLEhhPIlPAqFuOqzP6cIg" 
binance_secret_key="WXDjj0Ws6jLrTEyozR9mXbOCYIcFigojokRIB1q5uNkytDFU1ccYci4EIzIEUdA7"
binance=BinanceClient(binance_api_key,binance_secret_key)

api_key='MDRjNTJmNzktOWNjZi00ODUyLWI5Y2QtMjQyOTBjYmU5ZWI4'
api_secret='MjUxMWZlNTItNzNjZS00NjViLWFiY2ItMTgxZmUzNWE4YTNj'
jonviBot = JonviClient(api_key, api_secret)

# api_key1 = 'MTc0YTkwNTAtOGE0NC00ZmI5LWIyZDktMmM1ZWRlM2VkYzdk'
# api_secret1 = 'YjJmMTVmYjUtZmIyMy00YTg5LWEyODYtM2I1YWI3MDYzMGZk'
# jonviBuyBot = JonviClient(api_key1, api_secret1)

resp = jonviBot.get_access_token()
# resp1 = jonviBuyBot.get_access_token()

isSellOrder = 0
isBuyOrder = 0

margin = 0.05
orderMargin = 0.0015

for i in range(1, 10000):
    binancePrice = binance.get_recent_trades(symbol='BTCUSDT', limit=5)
    currentBinancePrice = float(binancePrice[0]['price'])

    

    balance = jonviBot.balance()
    useBalance = balance['data'][0]['useBalance']

        

    if isSellOrder == 0:
        currentSellPrice = float(currentBinancePrice) + 1 * margin
        resp = jonviBot.place_order(pair, 0.002 , currentSellPrice, 2)
        isSellOrder = 1
        print currentSellPrice
        print "DONE PLACE SELL ORDER"
    
    if isBuyOrder == 0:
        currentBuyPrice = float(currentBinancePrice) - 1 * margin
        resp = jonviBot.place_order(pair, 0.002, currentBuyPrice, 1)
        isBuyOrder = 1;
        print currentBuyPrice
        print "DONE PLACE BUY ORDER"

    if isSellOrder == 1:
        marginSellPrice = currentBinancePrice > currentSellPrice * (1 + orderMargin)
        

        cSell = jonviBot.current_order(pair)
        cSellData = cSell['data']
        for sellD in cSellData:
            if sellD['side'] == 2:
                botSellOrder = {"price":sellD["price"],"volume":sellD["volume"]}
                jovinSellBook = jonviBot.sell_orderbook(pair, 5)
                jonviSellOrder = {"price":jovinSellBook["data"][0]["price"],"volume":jovinSellBook["data"][0]["volume"]}

                getSellPair = botSellOrder == jonviSellOrder
                
                if marginSellPrice and getSellPair:
                    api_key1 = 'MTc0YTkwNTAtOGE0NC00ZmI5LWIyZDktMmM1ZWRlM2VkYzdk'
                    api_secret1 = 'YjJmMTVmYjUtZmIyMy00YTg5LWEyODYtM2I1YWI3MDYzMGZk'
                    jonviBuyBot = JonviClient_Buy(api_key1, api_secret1)
                    resp1 = jonviBuyBot.get_access_token()
                    resp1 = jonviBuyBot.place_order(pair, 0.002, sellD["price"], 1)
                    isSellOrder = 0
                    print "place buy"
                elif marginSellPrice and not getSellPair:
                    isSellOrder = 0
                    print "cancel sell order"
            
    if isBuyOrder == 1:
        marginBuyPrice = currentBinancePrice < currentBuyPrice * (1 - orderMargin)
        
        cBuy = jonviBot.current_order(pair)
        cBuyData = cBuy['data']

        for buyD in cBuyData:
        
            if buyD['side'] == 1:
                botBuyOrder = {"price":buyD["price"],"volume":buyD["volume"]}
                jovinBuyBook = jonviBot.buy_orderbook(pair, 5)
                jonviBuyOrder = {"price":jovinBuyBook["data"][0]["price"],"volume":jovinBuyBook["data"][0]["volume"]}

                getBuyPair = botBuyOrder == jonviBuyOrder
                
                if marginBuyPrice and getBuyPair:
                    api_key1 = 'MTc0YTkwNTAtOGE0NC00ZmI5LWIyZDktMmM1ZWRlM2VkYzdk'
                    api_secret1 = 'YjJmMTVmYjUtZmIyMy00YTg5LWEyODYtM2I1YWI3MDYzMGZk'
                    jonviBuyBot = JonviClient_Buy(api_key1, api_secret1)
                    resp1 = jonviBuyBot.get_access_token()
                    resp1 = jonviBuyBot.place_order(pair, 0.002, buyD["price"], 2)
                    isBuyOrder = 0
                    print "place sell"
                elif marginBuyPrice and not getBuyPair:
                    isBuyOrder = 0
                    print "cancel buy order"

        

        # print botSellOrder, jonviSellOrder
        # print botSellOrder == jonviSellOrder

        print currentBinancePrice, marginSellPrice, currentSellPrice * (1 + orderMargin)
        print currentBinancePrice, marginBuyPrice, currentBuyPrice * (1 - orderMargin)
        print "#################"
        


    time.sleep(1);