import key
import json
import Symbols
import Analiz
import time
import math
import telegram
import datetime
import Settings

from binance.client import Client
client = Client(key.api_key, key.api_secret)

from color import colorize
#from color import uncolorize

from telegram import (Animation, Audio, Contact, Document, Chat, Location,
                      PhotoSize, Sticker, TelegramObject, User, Video, Voice,
                      Venue, MessageEntity, Game, Invoice, SuccessfulPayment,
                      VideoNote, PassportData)

bot = telegram.Bot(token=key.token)

def StrategyRSI():
  k=0
  a=1
  min = Settings.minRSI
  max = Settings.maxRSI
  budget_order = Settings.budget_orderRSI
  budget_total = Settings.budget_totalRSI

  print("\t Start strategy RSI with NuBot Python. Main factor RSI: \n\t\t Min: " + colorize(47, 0, 32, str(min)) + "\n\t\t Max: " + colorize(47, 0, 32, str(max)) + "\n\t\t One order[BTC]: \t" + colorize(47, 0, 32, str(budget_order)) + "\n\t\t Total order[BTC]: \t" + colorize(47, 0, 32, str(budget_total))+ "\n")
  print("------------------------------------------------------------------------------------------------------------------------------------")

  while k < 1:
    #------------------Balance BTC--------------------------------------------------------------------------------------------
    balanceBTC = client.get_asset_balance(asset='BTC')
    balanceBTCJSON = json.dumps(balanceBTC)
    balanceBTCRESP = json.loads(balanceBTCJSON)
    balanceBTCFREE = balanceBTCRESP['free']
    #------------------Balance ALT--------------------------------------------------------------------------------------------
    balanceALT = client.get_asset_balance(asset=str(Symbols.SymbolsMatrix[a][0]))
    balanceALTJSON = json.dumps(balanceALT)
    balanceALTRESP = json.loads(balanceALTJSON)
    balanceALTFREE = balanceALTRESP['free']
    #------------------RSI----------------------------------------------------------------------------------------------------
    rsi = Analiz.RSI14(market=str(Symbols.SymbolsMatrix[a][0])+"BTC", tick_interval=Settings.tick_intervalRSI)
    rsi = round(float(rsi),2)
    #------------------Jeżeli mamy daną walutę zostanie oznaczona kolorem-----------------------------------------------------
    if float(balanceALTFREE) > 0:
      print("------------------------------------------------------------------------------------------------------------------------------------")
      print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  + " RSI(14): " + colorize(47, 0, 32, str(Symbols.SymbolsMatrix[a][0])+"BTC ") + str(rsi) + " Free:" + str(balanceALTFREE)+"\t" +"Free budget: " + str(budget_total))
    else: 
      print("------------------------------------------------------------------------------------------------------------------------------------")
      print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  + " RSI(14): " + str(Symbols.SymbolsMatrix[a][0])+"BTC "  + str(rsi)+"\t" + "Free budget: " + str(budget_total))
    #------------------Jeżeli RSI jest mniejsze od założonego && Jeżeli mamy środki w BTC && Jeżeli Nie mamy danej waluty && Jeżeli nasz maksymalny budżet na tą strategię jest większy od budżetu na order -----------------------------------------------------
    if float(rsi) < min and float(balanceBTCFREE) >= float(budget_order) and float(balanceALTFREE) == 0 and float(budget_total) >= float(budget_order):
      budget_total = float(budget_total) - float(budget_order)
      budget_total = round(float(budget_total), 2)
      price = client.get_symbol_ticker(symbol=str(Symbols.SymbolsMatrix[a][0])+"BTC")
      priceJSON = json.dumps(price)
      priceRESP = json.loads(priceJSON)
      price = priceRESP['price']
      le = len(str(Symbols.SymbolsMatrix[a][2]))
      qua = float(budget_order) / float(price)
      if le==1:
        qua = math.floor(qua)
      else: 
        qua = str(qua)[0:le]
      print(colorize(42,1,30,"\tCreate new order [BUY]\n\t") + str(Symbols.SymbolsMatrix[a][0])+"BTC RSI =\t"  + str(rsi) + "\n\tFree budget =\t" + str(budget_total) + "\n\tPrice =\t" + str(price) + "\n\tQuantity =\t" + str(qua))
      bot.send_message(chat_id=key.chat_id, text="\t Create new order [BUY] " + str(Symbols.SymbolsMatrix[a][0])+"BTC "  + str(rsi) + "\t Free budget: " + str(budget_total) + "\n Price: \t" + str(price) + "\n Quantity: \t" + str(qua))
      #OrderBuy = client.create_order(symbol=str(Symbols.SymbolsMatrix[a][0]), side=client.SIDE_BUY, type=client.ORDER_TYPE_LIMIT, timeInForce=client.TIME_IN_FORCE_GTC, quantity=str(qua), price=str(price))
      #print(str(OrderBuy))
      print("------------------------------------------------------------------------------------------------------------------------------------")
    elif float(rsi) > max:
      balanceALT = client.get_asset_balance(asset=str(Symbols.SymbolsMatrix[a][0]))
      balanceALTJSON = json.dumps(balanceALT)
      balanceALTRESP = json.loads(balanceALTJSON)
      balanceALTFREE = balanceALTRESP['free']
      price = client.get_symbol_ticker(symbol=str(Symbols.SymbolsMatrix[a][0]) + 'BTC')
      priceJSON = json.dumps(price)
      priceRESP = json.loads(priceJSON)
      price = priceRESP['price']
      if float(balanceALTFREE)*float(price) > Symbols.SymbolsMatrix[a][4]:
        budget_total = float(budget_total) + float(budget_order)
        budget_total = round(float(budget_total), 2)
        le = len(str(Symbols.SymbolsMatrix[a][2]))
        qua = float(balanceALTFREE)
        if le==1:
          qua = math.floor(qua)
        else: 
          qua = str(qua)[0:le]
        print("\t Create new order [SELL] " + str(Symbols.SymbolsMatrix[a][0])+"BTC "  + str(rsi) + "Free budget: " + str(budget_total) + "\n Price: \t" + str(price) + "\n Quantity: \t" + str(qua))
        bot.send_message(chat_id=key.chat_id, text="\t Create new order [SELL] " + str(Symbols.SymbolsMatrix[a][0])+"BTC "  + str(rsi) + "Free budget: " + str(budget_total) + "\n\t Price: \t" + str(price) + "\n\t Quantity: \t" + str(qua))
        #OrderSell = client.create_order(symbol=str(Symbols.SymbolsMatrix[a][0]), side=client.SIDE_SELL, type=client.ORDER_TYPE_LIMIT, timeInForce=client.TIME_IN_FORCE_GTC, quantity=str(qua), price=str(price))
        #print(str(OrderSell))
        print("------------------------------------------------------------------------------------------------------------------------------------")
      else: 
        T = "%-.8f" % (float(balanceALTFREE)*float(price))
        #colorize(47, 0, 32, str(Symbols.SymbolsMatrix[a][0])+"BTC ")
        print(colorize(41,1,30,"\tYou don't have minimum balance.") + "\n\tFree: " + str(Symbols.SymbolsMatrix[a][0]) + " = "  + str(balanceALTFREE) + "\n\tPrice = " + str(price) + "\n\tTotal = " + str(T) + "\n\tMinimum to order = " + str(Symbols.SymbolsMatrix[a][4]))
        print("------------------------------------------------------------------------------------------------------------------------------------")
    if a == len(Symbols.SymbolsMatrix)-1:
      a = 1
    else:
      a = a + 1
      time.sleep(1)
      
