import key
import json
import Symbols
import Menu

from binance.client import Client
client = Client(key.api_key, key.api_secret)

from color import colorize
from color import uncolorize


def MyBalance():
  k = 0
  a = 0
  while k < 1:
    if a <= len(Symbols.SymbolsMatrix)-1:
      balance = client.get_asset_balance(asset=str(Symbols.SymbolsMatrix[a][0]))
      balanceJSON = json.dumps(balance)
      balanceRESP = json.loads(balanceJSON)
      balanceFREE = balanceRESP['free']
      balanceFREE = "%-.8f" % (float(balanceFREE))
      balanceLOCKED = balanceRESP['locked']
      balanceLOCKED = "%-.8f" % (float(balanceLOCKED))
      balanceTOTAL = float(balanceFREE) + float(balanceLOCKED)
      balanceTOTAL = "%-.8f" % (float(balanceTOTAL))
      if float(balanceFREE) > 0 or float(balanceLOCKED) > 0:
        print("\t" + str(Symbols.SymbolsMatrix[a][0]) + "\t\t Free: " + str(balanceFREE) + "\t\t In Order: " + str(balanceLOCKED) + "\t\t TOTAL: " + str(balanceTOTAL))
        if str(Symbols.SymbolsMatrix[a][0]) == 'BTC':
          TotalBTC = float(balanceTOTAL)
        else:
          price = client.get_symbol_ticker(symbol=str(Symbols.SymbolsMatrix[a][0]) + 'BTC')
          priceJSON = json.dumps(price)
          priceRESP = json.loads(priceJSON)
          price = priceRESP['price']
          TotalBTC = float(TotalBTC) + float(balanceTOTAL) * float(price)
          #print(str(Symbols.SymbolsMatrix[a][0]) + "\t" + str(price))
      a = a + 1
    else:
      TotalBTC = "%-.8f" % (float(TotalBTC))
      print("---------------------------------------------------------------------------------------------")
      print("\t TOTAL [BTC]: " + colorize(47, 0, 32, str(TotalBTC)))
      print("---------------------------------------------------------------------------------------------")
      return(str(TotalBTC))
      k=1




