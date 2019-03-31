import key
import json
import Symbols
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

def Strategy_PingPong():
  OrderStatus = ''
  OrderID = ''
  OrderSide = ''
  symbol = Settings.symbolPP
  base_price = Settings.base_pricePP
  budget_BTC = Settings.budget_BTCPP
  start_operation = Settings.start_operationPP
  up_profit = Settings.up_profitPP
  down_profit = Settings.down_profitPP
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
    try:
      time.sleep(1)
      balanceALT = client.get_asset_balance(asset=str(symbol), recvWindow=1000000)
      balanceALTJSON = json.dumps(balanceALT)
      balanceALTRESP = json.loads(balanceALTJSON)
      balanceALTFREE = balanceALTRESP['free']

      balanceBTC = client.get_asset_balance(asset='BTC', recvWindow=1000000)
      balanceBTCJSON = json.dumps(balanceBTC)
      balanceBTCRESP = json.loads(balanceBTCJSON)
      balanceBTCFREE = balanceBTCRESP['free']
      budget_BTC = balanceBTCFREE

      price = client.get_symbol_ticker(symbol=str(symbol)+"BTC")
      priceJSON = json.dumps(price)
      priceRESP = json.loads(priceJSON)
      price = priceRESP['price']
      aprofit = float(price) / float(base_price) - 1
      aprofit = float(aprofit) * 100
      aprofit = round(aprofit,2)
      up_price = float(up_profit) * float(price)
      up_price = round(up_price,8)
      down_price = float(down_profit) * float(price)
      down_price = round(down_price,8)

      up_profit2 = (float(up_profit) - 1) * 100
      up_profit2 = round(up_profit2, 2)

      down_profit2 = (float(down_profit) - 1) * 100
      down_profit2 = round(down_profit2, 2)

      title = str("Market :" + str(symbol + "BTC ") + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
      table_price= [
            ['Prices', 'Value', 'Profits'],
            ['Up Price', str(up_price), str(up_profit2)+'%'],
            ['Actual Price', str(price), ''],
            ['Down Price', str(down_price), str(down_profit2)+'%'],
            ['\nBase Price', '\n' + str(base_price), '\n' + str(aprofit)+'%']
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
      y.justify_columns[2] = 'right'
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

      if start_operation == "SELL" and float(base_price)*float(up_profit) < float(price):
        qua = float(balanceALTFREE)
        if le==1:
          qua = math.floor(qua)
        else: 
          qua = str(qua)[0:le]
        OrderSell = client.create_order(symbol=str(symbol+"BTC"), side=client.SIDE_SELL, type=client.ORDER_TYPE_LIMIT, timeInForce=client.TIME_IN_FORCE_GTC, quantity=str(qua), price=str(price))
        com = "\t Sell Order. Balance: " + str(qua) + "\tPrice: " + str(price) + "\tNext operation: " + str(start_operation) + "\tBudget Total: " + str(budget_BTC)
        print(str(com))
        bot.send_message(chat_id=key.chat_id, text=str(com))
        start_operation = "BUY"
        Jorder = json.loads(json.dumps(OrderSell))
        OrderStatus = Jorder['status']
        OrderID = Jorder['orderId']
        OrderSide = Jorder['side']

      if start_operation == "BUY" and float(base_price)*float(down_profit) > float(price):
        qua = float(budget_BTC) / float(price)
        if le==1:
          qua = math.floor(qua)
        else: 
          qua = str(qua)[0:le]
        OrderBuy = client.create_order(symbol=str(symbol+"BTC"), side=client.SIDE_BUY, type=client.ORDER_TYPE_LIMIT, timeInForce=client.TIME_IN_FORCE_GTC, quantity=str(qua), price=str(price))
        com = "\t Buy Order. Balance: " + str(qua) + "\tPrice: " + str(price) + "\tNext operation: " + str(start_operation) + "\tBalance ALT: " + str(qua)
        print(str(com))
        bot.send_message(chat_id=key.chat_id, text=str(com))
        start_operation = "SELL" 
        Jorder = json.loads(json.dumps(OrderBuy))
        OrderStatus = Jorder['status']
        OrderID = Jorder['orderId']
        OrderSide = Jorder['side'] 
    except:
      print("EOFError")
      print("balanceAltResp " + balanceALTRESP['code'] + " " + balanceALTRESP['msg'])
      print("balanceBTCResp " + balanceBTCRESP['code'] + " " + balanceBTCRESP['msg'])
      print("priceRESP  " + priceRESP['code'] + " " + priceRESP['msg'])
      print("Jorder  " + Jorder['code'] + " " + Jorder['msg'])


