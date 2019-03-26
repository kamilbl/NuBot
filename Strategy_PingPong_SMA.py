import key
import json
import Symbols
import Analiz
import time
import math
import telegram
import datetime
import Settings
#import matplotlib.pyplot as plt

from binance.client import Client
client = Client(key.api_key, key.api_secret)

from color import colorize
#from color import uncolorize

from telegram import (Animation, Audio, Contact, Document, Chat, Location,
                      PhotoSize, Sticker, TelegramObject, User, Video, Voice,
                      Venue, MessageEntity, Game, Invoice, SuccessfulPayment,
                      VideoNote, PassportData)

bot = telegram.Bot(token=key.token)

def Strategy_PingPong_SMA():
  #print("Please input symbol(TRX):")
  #symbol = input()          #TRX or GAS
  symbol = Settings.symbolPPSMA
  
  #print("Please input base price(0.00000600):")
  #base_price = input()
  base_priceSMA = Analiz.SMA14(market=symbol+"BTC", tick_interval=Settings.tick_intervalPPSMA)
  base_priceSMA = round(float(base_priceSMA),8)
  budget_BTC = Settings.budget_BTCPPSMA
  #print("Please input start operation(SELL/BUY):")
  #start_operation = input() #SELL or BUY
  start_operation = Settings.start_operationPPSMA
  up_profit = Settings.up_profitPPSMA
  down_profit = Settings.down_profitPPSMA
  k = 0
  a=1

  while k <1:
    if symbol == Symbols.SymbolsMatrix[a][0]:
      le = len(str(Symbols.SymbolsMatrix[a][2]))
      k = 1
    else:
      a = int(a) + 1
  
  #print(str(le))

  while True:
    base_priceSMA = Analiz.SMA14(market=symbol+"BTC", tick_interval=Settings.tick_intervalPPSMA)
    base_priceSMA = round(float(base_priceSMA),8)
    time.sleep(1)
    balanceALT = client.get_asset_balance(asset=str(symbol))
    balanceALTJSON = json.dumps(balanceALT)
    balanceALTRESP = json.loads(balanceALTJSON)
    balanceALTFREE = balanceALTRESP['free']
    balanceBTC = client.get_asset_balance(asset='BTC')
    balanceBTCJSON = json.dumps(balanceBTC)
    balanceBTCRESP = json.loads(balanceBTCJSON)
    balanceBTCFREE = balanceBTCRESP['free']

    price = client.get_symbol_ticker(symbol=str(symbol)+"BTC")
    priceJSON = json.dumps(price)
    priceRESP = json.loads(priceJSON)
    price = priceRESP['price']
    aprofit = float(price) / float(base_priceSMA) - 1
    aprofit = float(aprofit) * 100
    aprofit = round(aprofit,2)
    print("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("Symbol:\t" + str(symbol + "BTC") + "\n\tBase price: " + str(base_priceSMA) + "\n\tProfit UP: " + str(up_profit) + "\n\tProfit DOWN: " + str(down_profit))
    print("\tPrice: " + str(price) + "\tProfit: " + str(aprofit) + "%\tBalance: " + str(balanceALTFREE) + "\tBalance[BTC] : " + str(balanceBTCFREE))
    print("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

    if start_operation == "SELL" and float(base_priceSMA)*float(up_profit) < float(price):
        qua = float(balanceALTFREE)
        if le==1:
          qua = math.floor(qua)
        else: 
          qua = str(qua)[0:le]
        OrderSell = client.create_order(symbol=str(symbol+"BTC"), side=client.SIDE_SELL, type=client.ORDER_TYPE_LIMIT, timeInForce=client.TIME_IN_FORCE_GTC, quantity=str(qua), price=str(price))
        print(str(OrderSell))
        start_operation = "BUY"
        budget_BTC = float(qua)*float(base_priceSMA)
        budget_BTC = round(budget_BTC,8)
        com = "\t Sell Order. Balance: " + str(qua) + "\tPrice: " + str(price) + "\tNext operation: " + str(start_operation) + "\tBudget Total: " + str(budget_BTC)
        print(colorize(47, 0, 32, com))

    if start_operation == "BUY" and float(base_priceSMA)*float(down_profit) > float(price):
        qua = float(budget_BTC) / float(price)
        if le==1:
          qua = math.floor(qua)
        else: 
          qua = str(qua)[0:le]
        OrderBuy = client.create_order(symbol=str(symbol+"BTC"), side=client.SIDE_BUY, type=client.ORDER_TYPE_LIMIT, timeInForce=client.TIME_IN_FORCE_GTC, quantity=str(qua), price=str(price))
        print(str(OrderBuy))
        start_operation = "SELL"  
        com = "\t Buy Order. Balance: " + str(qua) + "\tPrice: " + str(price) + "\tNext operation: " + str(start_operation) + "\tBalance ALT: " + str(qua)
        print(colorize(47, 0, 32, com))


