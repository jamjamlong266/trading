from jonvi_api import JonviClient
from jonvi_api_buy import JonviClient_Buy
from binanceapi import BinanceClient
import time
# import request
# import random
import json

pair = "btcusdt"
trading_pair = {"btcusdt"}

binance_api_key="8ovOuiaMx7NwodKm34xTH4Dq62zWZgB8Whnkojgx9ZfZLEhhPIlPAqFuOqzP6cIg" 
binance_secret_key="WXDjj0Ws6jLrTEyozR9mXbOCYIcFigojokRIB1q5uNkytDFU1ccYci4EIzIEUdA7"
binance=BinanceClient(binance_api_key,binance_secret_key)

api_key='MDRjNTJmNzktOWNjZi00ODUyLWI5Y2QtMjQyOTBjYmU5ZWI4' # robot 2
api_secret='MjUxMWZlNTItNzNjZS00NjViLWFiY2ItMTgxZmUzNWE4YTNj' # robot 2
jonviBot = JonviClient(api_key, api_secret)

resp = jonviBot.get_access_token()

isPlaceAskOrder = 0
isPlaceBidOrder = 0

margin = 0.005
marketGap = 0.007

botAskPrice = 0
botBidPrice = 0

askGap = False
askLoss = False
bidGap = False
bidLoss = False


marginAskPrice = 0
marginAskLoss = 0
marginBidPrice = 0
marginBidLoss = 0

askId = 0
bidId = 0

currentBotAskPrice = 0
currentBotAskVol = 0

currentBotBidPrice = 0
currentBotBidVol = 0



for i in range(1, 10000):

    # ..Get binance order book
    binanceOrderBook = binance.get_order_book(symbol=pair.upper(), limit=5)
    binanceAskPrice = float(binanceOrderBook["asks"][0][0])
    binanceBidPrice = float(binanceOrderBook["bids"][0][0])

    # ..Keep check jonvi ask order book
    jonviBot.sell_orderbook(pair, 5)

    # ..Keep check jonvi bid order book
    jonviBot.buy_orderbook(pair, 5)

    # ..Keep check bot current order   
    jonviBot.current_order(pair)
    

    # ..Bot place Ask order
    if (isPlaceAskOrder == 0) and (jonviBot.askID == 0):
        
        botAskPrice = binanceAskPrice * (1 + margin)
        currentBotAskPrice = botAskPrice
        resp = jonviBot.place_order(pair, 0.001, currentBotAskPrice, 2) # 1 bid 2 ask
        isPlaceAskOrder = 1
    
    # ..Bot place Bid order
    if (isPlaceBidOrder == 0) and (jonviBot.bidID == 0):

        botBidPrice = binanceBidPrice * (1 - margin)
        currentBotBidPrice = botBidPrice
        resp = jonviBot.place_order(pair, 0.001, currentBotBidPrice, 1) # 1 bid 2 ask
        isPlaceBidOrder = 1

    # ..Robot auto take ask order
    if isPlaceAskOrder == 1 or (jonviBot.askID != 0):
        
        marginAskPrice = currentBotAskPrice * (1 + marketGap) # !! for testing
        marginAskLoss = currentBotAskPrice * (1 - marketGap) # !! for testing
        askGap = binanceAskPrice > currentBotAskPrice * (1 + marketGap)
        askLoss = binanceAskPrice < currentBotAskPrice * (1 - marketGap)

        jonviBot.current_order(pair)
        currentBotAskPrice = jonviBot.askPrice
        currentBotAskVol = jonviBot.askVol

        if askGap:
            if jonviBot.ask1 == currentBotAskPrice and jonviBot.ask1vol == currentBotAskVol:
                print("ROBOT PLACE BUY ORDER")
                api_key1 = 'MTc0YTkwNTAtOGE0NC00ZmI5LWIyZDktMmM1ZWRlM2VkYzdk'  # robot 3
                api_secret1 = 'YjJmMTVmYjUtZmIyMy00YTg5LWEyODYtM2I1YWI3MDYzMGZk' # robot 3
                jonviBuyBot = JonviClient_Buy(api_key1, api_secret1)
                resp1 = jonviBuyBot.get_access_token()
                print("ROBOT PLACE BUY ORDER @ " + str(jonviBot.askPrice))
                resp1 = jonviBuyBot.place_order(pair, jonviBot.askVol, jonviBot.askPrice, 1)
                
                isPlaceAskOrder = 0
            else:
                jonviBot.current_order(pair)
                askID = jonviBot.askID
                resp = jonviBot.cancel_order(askID)
                isPlaceAskOrder = 0

        if askLoss:
            print("CANCEL ASK ORDER PLACE NEW ONE")
            jonviBot.current_order(pair)
            askID = jonviBot.askID
            print(askID)
            resp = jonviBot.cancel_order(askID)
            isPlaceAskOrder = 0
    
    # ..Robot auto take bid order
    if isPlaceBidOrder ==1 or (jonviBot.bidID != 0):
        
        marginBidPrice = currentBotBidPrice * (1 - marketGap) # !! for testing
        marginBidLoss = currentBotBidPrice * (1 + marketGap) # !! for testing
        bidGap = binanceBidPrice < currentBotBidPrice * (1 - marketGap)
        bidLoss = binanceBidPrice > currentBotBidPrice * (1 + marketGap)

        jonviBot.current_order(pair)
        currentBotBidPrice = jonviBot.bidPrice
        currentBotBidVol = jonviBot.bidVol

        if bidGap:
            if jonviBot.bid1 == currentBotBidPrice and jonviBot.bid1vol == currentBotBidVol:
                
                api_key1 = 'MTc0YTkwNTAtOGE0NC00ZmI5LWIyZDktMmM1ZWRlM2VkYzdk' #robot 3
                api_secret1 = 'YjJmMTVmYjUtZmIyMy00YTg5LWEyODYtM2I1YWI3MDYzMGZk' #robot 3
                jonviBuyBot = JonviClient_Buy(api_key1, api_secret1)
                resp1 = jonviBuyBot.get_access_token()
                print ("ROBOT PLACE SELL ORDER @ " + str(jonviBot.bidPrice))
                resp1 = jonviBuyBot.place_order(pair, jonviBot.bidVol, jonviBot.bidPrice, 2)
                isPlaceBidOrder = 0
            else:
                jonviBot.current_order(pair)
                bidID = jonviBot.bidID
                resp = jonviBot.cancel_order(bidID)
                isPlaceBidOrder = 0
        if bidLoss:
            print ("CANCEL BID ORDER PLACE NEW ONE")
            jonviBot.current_order(pair)
            bidID = jonviBot.bidID
            print (bidID)
            resp = jonviBot.cancel_order(bidID)
            isPlaceBidOrder = 0

    print (currentBotAskPrice, currentBotBidPrice)
    print (binanceAskPrice, askGap, marginAskPrice, marginAskLoss)
    print (binanceBidPrice, bidGap, marginBidPrice, marginBidLoss)
    print ("#################")
    

    time.sleep(1);

