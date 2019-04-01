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
import sys
from terminaltables import AsciiTable
#Cena kupna (bid), sprzedaży (ask) 
from binance.client import Client
client = Client(key.api_key, key.api_secret)

from telegram import (Animation, Audio, Contact, Document, Chat, Location,
                      PhotoSize, Sticker, TelegramObject, User, Video, Voice,
                      Venue, MessageEntity, Game, Invoice, SuccessfulPayment,
                      VideoNote, PassportData)

bot = telegram.Bot(token=key.token)

def Strategy_Scalping_Depth():
	k=0
	a=1
	print("Please chooes operation: " + "test" + ' or ' + 'symbol: MANA, TRX, XRP << only symbol' )
	chooes = input()
	if chooes == "test":
		while k<1:
			try:
				symbol = Symbols.SymbolsMatrix[a][0]
				depth = client.get_order_book(symbol = str(symbol) + 'BTC', limit=5)
				depthJSON = json.loads(json.dumps(depth))
				depthAskPrice = depthJSON['asks'][0][0]
				depthAskValue = depthJSON['asks'][0][1]
				depthBidPrice = depthJSON['bids'][0][0]
				depthBidValue = depthJSON['bids'][0][1]
				depth = (float(depthAskPrice) / float(depthBidPrice)) - 1
				depth = round((float(depth) * 100),2)
				#print(depth)
				if a == len(Symbols.SymbolsMatrix)- 1 :
						print("please choose your symbol:")
						symbol = input()
						Trading_with_SD(symbol=symbol)
				if float(depth) > Settings.minDepth:
					if a == len(Symbols.SymbolsMatrix)- 1 :
						print("please choose your symbol:")
						symbol = input()
						Trading_with_SD(symbol=symbol)
					else:
						le = len(str(Symbols.SymbolsMatrix[a][3]))
						#depthAskPrice = decimal.Decimal(depthAskPrice)
						#depthBidPrice = decimal.Decimal(depthBidPrice)
						depthAskPrice = str(depthAskPrice)[0:le]
						depthBidPrice = str(depthBidPrice)[0:le]
						depth = str(depth) + '%'
						table_depth = [
									['Symbol', 'Ask Price (SELL)', 'Ask Volumen', 'Bid Price (BUY)', 'Bid Volumen', 'Depth'],
									[str(symbol), str(depthAskPrice), str(depthAskValue), str(depthBidPrice), str(depthBidValue), str(depth)]
							]
						d = AsciiTable(table_depth)
						print(d.table)
				a=a+1
			except:
		         print(str(symbol) + ' ' +depthJSON['code'] + ' ' + depthJSON['msg'])
		         sys.exit()
	else:
		Trading_with_SD(symbol=chooes)

def Trading_with_SD(symbol):
  budgetBTCSD = Settings.budgetBTCSD
  OrderStatus = ''
  OrderID = ''
  OrderSide = ''
  k = 0
  a = getA(symbol = symbol)
  while k < 1:
    try:
      print("Let's start ...")
      time.sleep(2)
      depth = client.get_order_book(symbol = symbol + 'BTC', limit=5)
      depthJSON = json.loads(json.dumps(depth))
      depthAskPrice = depthJSON['asks'][0][0]
      depthAskValue = depthJSON['asks'][0][1]
      depthBidPrice = depthJSON['bids'][0][0]
      depthBidValue = depthJSON['bids'][0][1]
      NewdepthAskPrice = float(depthAskPrice) - float(Symbols.SymbolsMatrix[a][3])
      NewdepthBidPrice = float(depthBidPrice) + float(Symbols.SymbolsMatrix[a][3])
      depth = (float(depthAskPrice) / float(depthBidPrice)) - 1
      depth = round((float(depth) * 100),2)
      Newdepth = (float(NewdepthAskPrice) / float(NewdepthBidPrice)) - 1
      Newdepth = round((float(Newdepth) * 100),2)
      le = len(str(Symbols.SymbolsMatrix[a][2]))
      lep = len(str(Symbols.SymbolsMatrix[a][3]))
      depthAskPrice = str(depthAskPrice)[0:lep]
      depthBidPrice = str(depthBidPrice)[0:lep]
      NewdepthAskPrice = decimal.Decimal(NewdepthAskPrice)
      NewdepthAskPrice = str(NewdepthAskPrice)[0:lep]
      NewdepthBidPrice = decimal.Decimal(NewdepthBidPrice)
      NewdepthBidPrice = str(NewdepthBidPrice)[0:lep]
      qua = float(Settings.budgetBTCSD)/float(NewdepthAskPrice)
      if le==1:
        qua = math.floor(qua)
      else: 
        qua = str(qua)[0:le]
      print(qua)
      table_depth = [
					['Symbol', 'Ask Price (SELL)', 'Ask Volumen', 'Bid Price (BUY)', 'Bid Volumen', 'Depth'],
					[str(symbol), str(depthAskPrice), str(depthAskValue), str(depthBidPrice), str(depthBidValue), str(depth)+'%'],
					[str(symbol), str(NewdepthAskPrice), str(qua), str(NewdepthBidPrice), str(qua), str(Newdepth)+'%'],
					["Status Order", str(OrderStatus), "Id Order", str(OrderID), "Side Order", str(OrderSide)]
					]
      d = AsciiTable(table_depth)
      
      print(d.table)
      if float(Newdepth) > float(Settings.minDepth):
        startoperation = Settings.start_operationSD
        if startoperation == "SELL" and float(budgetBTCSD) > 0:
          qua = float(Settings.budgetBTCSD)/float(NewdepthAskPrice)
          if le==1:
            qua = math.floor(qua)
          else: 
            qua = str(qua)[0:le]
          budgetBTCSD = 0
          OrderSell = client.create_order(symbol=str(symbol+"BTC"), side=client.SIDE_SELL, type=client.ORDER_TYPE_LIMIT, timeInForce=client.TIME_IN_FORCE_GTC, quantity=str(qua), price=str(NewdepthAskPrice))
          Jorder = json.loads(json.dumps(OrderSell))
          OrderStatus = Jorder['status']
          OrderID = Jorder['orderId']
          OrderSide = Jorder['side']
          print("Create SELL order: " + "Price: " + str(NewdepthAskPrice) + "Quantity: " + str(qua) + "Status: " + str(OrderStatus))
        if startoperation == "BUY" and float(budgetBTCSD) > 0:
          qua = float(Settings.budgetBTCSD)/float(NewdepthAskPrice)
          if le==1:
            qua = math.floor(qua)
          else: 
            qua = str(qua)[0:le]
          OrderBuy = client.create_order(symbol=str(symbol+"BTC"), side=client.SIDE_BUY, type=client.ORDER_TYPE_LIMIT, timeInForce=client.TIME_IN_FORCE_GTC, quantity=str(qua), price=str(NewdepthAskPrice))
          Jorder = json.loads(json.dumps(OrderBuy))
          OrderStatus = Jorder['status']
          OrderID = Jorder['orderId']
          OrderSide = Jorder['side']
          print("Create BUY order: " + "Price: " + str(NewdepthAskPrice) + "Quantity: " + str(qua) + "Status: " + str(OrderStatus))
        while True:
            print("Check status order and control prices")
            if str(OrderID) != "":
              price = client.get_symbol_ticker(symbol=str(symbol)+"BTC")
              check = client.get_order(symbol=str(symbol+"BTC"), orderId=OrderID, recvWindow=1000000)
              Jorder = json.loads(json.dumps(check))
              OrderStatus = Jorder['status']
              print("Check status Order: " + str(OrderStatus))
              if OrderStatus == "FILLED" and OrderSide == "SELL":
                startoperation = "BUY"
                budgetBTCSD = Settings.budgetBTCSD
                print("Bot sold your coins. Market: " + str(symbol+"BTC") + "Quantity: " + str(qua))
                break
              elif OrderStatus == "FILLED" and OrderSide == "BUY":
                startoperation = "BUY"
                budgetBTCSD = Settings.budgetBTCSD
                print("Bot bought your coins. Market: " + str(symbol+"BTC") + "Quantity: " + str(qua))
                break
              elif OrderSide == "SELL" and float(price) < float(NewdepthAskPrice):
                result = client.cancel_order(symbol=str(symbol+"BTC"),orderId=str(OrderID))
                print("Bot cancel last order, because price goes down...")
                break
              elif OrderSide == "BUY" and float(price) > float(NewdepthBidPrice):
                result = client.cancel_order(symbol=str(symbol+"BTC"),orderId=str(OrderID))
                print("Bot cancel last order, because price goes up...")
                break		
              else:
                print("Please wait...")	
    except:
      print("ERROR")
      print(check)
      print(OrderStatus + OrderID + OrderSide)
      print(result)

def getA(symbol):
   a=1
   while True:
    if symbol == Symbols.SymbolsMatrix[a][0]:
      return a
      break
    else:
     a = a + 1