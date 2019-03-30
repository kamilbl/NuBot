import key
import json
import Symbols
import Analiz
import time
import math
import telegram
import datetime
import Settings
from terminaltables import AsciiTable

from binance.client import Client
client = Client(key.api_key, key.api_secret)

from telegram import (Animation, Audio, Contact, Document, Chat, Location,
                      PhotoSize, Sticker, TelegramObject, User, Video, Voice,
                      Venue, MessageEntity, Game, Invoice, SuccessfulPayment,
                      VideoNote, PassportData)

bot = telegram.Bot(token=key.token)

def Strategy_RSI():
  OrderStatus = ''
  OrderID = ''
  OrderSide = ''
  start_operation = Settings.start_operationRSI
  symbol = Settings.symbolRSI
  RSI = Analiz.RSI14(market=symbol+"BTC", tick_interval=Settings.tick_intervalRSI)
 
  balanceBTC = client.get_asset_balance(asset='BTC')
  balanceBTCJSON = json.dumps(balanceBTC)
  balanceBTCRESP = json.loads(balanceBTCJSON)
  balanceBTCFREE = balanceBTCRESP['free']
  budget_BTC = balanceBTCFREE
  #budget_BTC = Settings.budget_orderRSI
  
  k = 0
  a = 1
  while k <1:
    if symbol == Symbols.SymbolsMatrix[a][0]:
      le = len(str(Symbols.SymbolsMatrix[a][2]))
      k = 1
    else:
      a = int(a) + 1

  while True:
    try:
      RSI = Analiz.RSI14(market=symbol+"BTC", tick_interval=Settings.tick_intervalRSI)
      RSI = round(RSI,2)
      time.sleep(2)
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

      title = str("Market :" + str(symbol + "BTC ") + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
      table_price= [
            ['Prices', 'Value',],
            ['RSI', str(RSI),],
            ['\nActual Price', '\n'+str(price),]
        ]
      table_balance= [
            ['Balance', 'Value'],
            [str(symbol), str(balanceALTFREE)],
            ['BTC', str(balanceBTCFREE)]
        ]
      table_order= [
            ['OrderID', 'Status', 'Side'],
            [str(OrderStatus),str(OrderID),str(OrderSide)]
        ]
      o = AsciiTable(table_order)
      y = AsciiTable(table_price)
      y.justify_columns[1] = 'right'
      x = AsciiTable(table_balance)
      x.justify_columns[1] = 'right'
      print(title)
      print(y.table)
      print(x.table)
      print(o.table)
      print("\n********************************************************************\n")

      if str(OrderID) != "":
        check = client.get_order(symbol=str(symbol+"BTC"), orderId=OrderID, recvWindow=1000000)
        Jorder = json.loads(json.dumps(check))
        OrderStatus = Jorder['status']

      if start_operation == "SELL" and float(RSI) > float(Settings.maxRSI):
          qua = float(budget_BTC) / float(price)
          if le==1:
            qua = math.floor(qua)
          else: 
            qua = str(qua)[0:le]
          OrderSell = client.create_order(symbol=str(symbol+"BTC"), side=client.SIDE_SELL, type=client.ORDER_TYPE_LIMIT, timeInForce=client.TIME_IN_FORCE_GTC, quantity=str(qua), price=str(price))
          #print(str(OrderSell))
          start_operation = "BUY"
          budget_BTC = float(qua)*float(price)
          budget_BTC = round(budget_BTC,8)
          com = "\t Sell Order. Balance: " + str(qua) + "\tPrice: " + str(price) + "\tNext operation: " + str(start_operation) + "\tBudget Total: " + str(budget_BTC)
          print(str(com))
          bot.send_message(chat_id=key.chat_id, text=str(com))
          Jorder = json.loads(json.dumps(OrderSell))
          OrderStatus = Jorder['status']
          OrderID = Jorder['orderId']
          OrderSide = Jorder['side']

      if start_operation == "BUY" and float(RSI) < float(Settings.minRSI):
          qua = float(balanceALTFREE)
          if le==1:
            qua = math.floor(qua)
          else: 
            qua = str(qua)[0:le]
          OrderBuy = client.create_order(symbol=str(symbol+"BTC"), side=client.SIDE_BUY, type=client.ORDER_TYPE_LIMIT, timeInForce=client.TIME_IN_FORCE_GTC, quantity=str(qua), price=str(price))
          #print(str(OrderBuy))
          start_operation = "SELL"  
          com = "\t Buy Order. Balance: " + str(qua) + "\tPrice: " + str(price) + "\tNext operation: " + str(start_operation) + "\tBalance ALT: " + str(qua)
          print(str(com))
          bot.send_message(chat_id=key.chat_id, text=str(com))
          Jorder = json.loads(json.dumps(OrderBuy))
          OrderStatus = Jorder['status']
          OrderID = Jorder['orderId']
          OrderSide = Jorder['side']
    except:
      print("EOFError")
