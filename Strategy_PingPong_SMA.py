import key
import json
import Symbols
import Analiz
import time
import math
import telegram
import datetime
import Settings
import decimal
from terminaltables import AsciiTable

from binance.client import Client
client = Client(key.api_key, key.api_secret)

from telegram import (Animation, Audio, Contact, Document, Chat, Location,
                      PhotoSize, Sticker, TelegramObject, User, Video, Voice,
                      Venue, MessageEntity, Game, Invoice, SuccessfulPayment,
                      VideoNote, PassportData)

bot = telegram.Bot(token=key.token)

def Strategy_PingPong_SMA():
  OrderStatus = ''
  OrderID = ''
  OrderSide = ''
  comSell = ''
  comBuy = ''
  #budget_BTC = Settings.budget_BTCPPSMA
  symbol = Settings.symbolPPSMA
  base_priceSMA = Analiz.SMA14(market=symbol+"BTC", tick_interval=Settings.tick_intervalPPSMA)
  base_priceSMA = round(float(base_priceSMA),8)

  balanceALT = client.get_asset_balance(asset=str(symbol), recvWindow=1000000)
  balanceALTJSON = json.dumps(balanceALT)
  balanceALTRESP = json.loads(balanceALTJSON)
  balanceALTFREE = balanceALTRESP['free']
  budget_ALT = balanceALTFREE
  balanceBTC = client.get_asset_balance(asset='BTC', recvWindow=1000000)
  balanceBTCJSON = json.dumps(balanceBTC)
  balanceBTCRESP = json.loads(balanceBTCJSON)
  balanceBTCFREE = balanceBTCRESP['free']
  budget_BTC = float(balanceBTCFREE) * float(Settings.use_budget_BTCPPSMA_procent)
  budget_BTC = round(budget_BTC,8)
  budget_BTC = decimal.Decimal(budget_BTC)
  budget_BTC = str(budget_BTC)[0:10]

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

  while True:
    try:
      base_priceSMA = Analiz.SMA14(market=symbol+"BTC", tick_interval=Settings.tick_intervalPPSMA)
      #base_priceSMA = round(float(base_priceSMA),8)
      base_priceSMA = decimal.Decimal(base_priceSMA)
      base_priceSMA = str(base_priceSMA)[0:10]
      time.sleep(2)
      balanceALT = client.get_asset_balance(asset=str(symbol), recvWindow=1000000)
      balanceALTJSON = json.dumps(balanceALT)
      balanceALTRESP = json.loads(balanceALTJSON)
      balanceALTFREE = balanceALTRESP['free']
      budget_ALT = balanceALTFREE
      balanceBTC = client.get_asset_balance(asset='BTC', recvWindow=1000000)
      balanceBTCJSON = json.dumps(balanceBTC)
      balanceBTCRESP = json.loads(balanceBTCJSON)
      balanceBTCFREE = balanceBTCRESP['free']
      budget_BTC = float(balanceBTCFREE) * float(Settings.use_budget_BTCPPSMA_procent)
      budget_BTC = round(budget_BTC,8)
      budget_BTC = decimal.Decimal(budget_BTC)
      budget_BTC = str(budget_BTC)[0:10]

      price = client.get_symbol_ticker(symbol=str(symbol)+"BTC")
      priceJSON = json.dumps(price)
      priceRESP = json.loads(priceJSON)
      price = priceRESP['price']
      aprofit = float(price) / float(base_priceSMA) - 1
      aprofit = float(aprofit) * 100
      aprofit = round(aprofit,2)

      up_price = float(up_profit) * float(price)
      up_price = decimal.Decimal(up_price)
      up_price = str(up_price)[0:10]
      down_price = float(down_profit) * float(price)
      down_price = decimal.Decimal(down_price)
      down_price = str(down_price)[0:10]

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
            ['\nBase Price', '\n' + str(base_priceSMA), '\n' + str(aprofit)+'%']
        ]

      table_balance= [
            ['Balance', 'Value'],
            [str(symbol), str(balanceALTFREE)],
            ['BTC', str(balanceBTCFREE)],
						['Budget BTC', str(budget_BTC)],
					  ['Budget ALT', str(budget_ALT)],
					  ['Next operation', str(start_operation)]
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
        if OrderStatus == "FILLED" and OrderSide == "SELL":
          start_operation = "BUY"
          bot.send_message(chat_id=key.chat_id, text=str(comSell))  #<--send msg Telegram
          time.sleep(5)
          budget_BTC = float(balanceBTCFREE) * float(Settings.use_budget_BTCPPSMA_procent)
          budget_BTC = round(budget_BTC,8)
          budget_BTC = decimal.Decimal(budget_BTC)
          budget_BTC = str(budget_BTC)[0:10]
          budget_ALT = float(balanceALTFREE)
          OrderID = ""
        elif  OrderStatus == "FILLED" and OrderSide == "BUY":
          start_operation = "SELL"
          bot.send_message(chat_id=key.chat_id, text=str(comBuy))  #<--send msg Telegram
          time.sleep(5)
          budget_BTC = float(balanceBTCFREE) * float(Settings.use_budget_BTCPPSMA_procent)
          budget_BTC = round(budget_BTC,8)
          budget_BTC = decimal.Decimal(budget_BTC)
          budget_BTC = str(budget_BTC)[0:10]
          budget_ALT = float(balanceALTFREE)
          OrderID = ""

      if start_operation == "SELL" and float(base_priceSMA)*float(up_profit) < float(price) and float(budget_BTC)>0 and str(OrderID) == "":
          qua = float(budget_ALT)
          start_operation == "BUY"
          if le==1:
            qua = math.floor(qua)
          else: 
            qua = str(qua)[0:le]
          OrderSell = client.create_order(symbol=str(symbol+"BTC"), side=client.SIDE_SELL, type=client.ORDER_TYPE_LIMIT, timeInForce=client.TIME_IN_FORCE_GTC, quantity=str(qua), price=str(price), recvWindow=1000000)
          comSell = "\tCreate Sell Order. Balance: " + str(qua) + "\tPrice: " + str(price)
          print(str(comSell))
          Jorder = json.loads(json.dumps(OrderSell))
          OrderStatus = Jorder['status']
          OrderID = Jorder['orderId']
          OrderSide = Jorder['side']

      if start_operation == "BUY" and float(base_priceSMA)*float(down_profit) > float(price) and float(budget_BTC)>0 and str(OrderID) == "":
          qua = float(budget_BTC) / float(price)
          start_operation == "SELL"
          if le==1:
            qua = math.floor(qua)
          else: 
            qua = str(qua)[0:le]
          OrderBuy = client.create_order(symbol=str(symbol+"BTC"), side=client.SIDE_BUY, type=client.ORDER_TYPE_LIMIT, timeInForce=client.TIME_IN_FORCE_GTC, quantity=str(qua), price=str(price), recvWindow=1000000)
          comBuy = "\tCreate Buy Order. Balance: " + str(qua) + "\tPrice: " + str(price)
          print(str(comBuy))
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
