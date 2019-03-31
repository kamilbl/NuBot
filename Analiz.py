import requests
import json
import math
import datetime
import key
import telegram
import sys

from binance.client import Client
client = Client(key.api_key, key.api_secret)

from telegram import (Animation, Audio, Contact, Document, Chat, Location,
                      PhotoSize, Sticker, TelegramObject, User, Video, Voice,
                      Venue, MessageEntity, Game, Invoice, SuccessfulPayment,
                      VideoNote, PassportData)

bot = telegram.Bot(token=key.token)
bot.send_message(chat_id=key.chat_id, text="Start NuBot")

def RSI14(market, tick_interval):
  try:
    licznik = 1
    avaGain = 0
    avaLoss = 0
    #parms
    #market = 'GTOBTC'
    #tick_interval = '1h'
    url = 'https://api.binance.com/api/v1/klines?symbol=' + market + '&interval=' + tick_interval + '&limit=17'
    data = requests.get(url).json()
    json1 = json.dumps(data)
    resp_price = json.loads(json1)
    
    tab = [[0 for close in range(18)] for market in range(1)]
    tab[0][0] = market
    tab[0][1] = resp_price[0][4]
    tab[0][2] = resp_price[1][4]  #1
    tab[0][3] = resp_price[2][4]  #2
    tab[0][4] = resp_price[3][4]  #3
    tab[0][5] = resp_price[4][4]  #4
    tab[0][6] = resp_price[5][4]  #5
    tab[0][7] = resp_price[6][4]  #6
    tab[0][8] = resp_price[7][4]  #7
    tab[0][9] = resp_price[8][4]  #8
    tab[0][10] = resp_price[9][4]  #9
    tab[0][11] = resp_price[10][4]  #10
    tab[0][12] = resp_price[11][4]  #11
    tab[0][13] = resp_price[12][4]  #12
    tab[0][14] = resp_price[13][4]  #13
    tab[0][15] = resp_price[14][4]  #14
    tab[0][16] = resp_price[15][4]

    while True:
        a = float(tab[0][licznik + 1]) - float(tab[0][licznik])
        if a >= 0:
            avaGain = float(avaGain) + float(a)
            #print('gain ' + str(avaGain))
            licznik = licznik + 1
        elif a < 0:
            avaLoss = float(avaLoss) + float(a) * (-1)
            #print('loss ' + str(avaLoss))
            licznik = licznik + 1
        #elif a == 0:
        #licznik = licznik + 1

        if licznik == 15:
            #print('suma ' + str(avaGain))
            #print('suma ' + str(avaLoss))
            if float(avaGain) > 0 and float(avaLoss) > 0:
                avaGain = float(avaGain) / 14
                avaLoss = float(avaLoss) / 14
                #print('średniaGain ' + str(avaGain))
                #print('średniaLoss ' + str(avaLoss))
                RS = float(avaGain) / float(avaLoss)
                #print('RS ' + str(RS))
                RSI14 = 100 - (100 / (1 + float(RS)))
                return RSI14
                break
            else:
                RSI14 = 0
                return RSI14
  except: 
    errorC = resp_price['code']
    errorM = resp_price['msg']
    if float(errorC) < 0:
        print(str(errorC) + " " + str(errorM))
        sys.exit()

def SMA14(market, tick_interval):
  try:
    #parms
    #market = 'GTOBTC'
    #tick_interval = '1h'
    licznik = 1
    SMA14 = 0
    url = 'https://api.binance.com/api/v1/klines?symbol=' + market + '&interval=' + tick_interval + '&limit=14'
    data = requests.get(url).json()
    json1 = json.dumps(data)
    resp_price = json.loads(json1)

    tab = [[0 for close in range(16)] for market in range(1)]
    tab[0][0] = market
    tab[0][1] = resp_price[0][4]
    tab[0][2] = resp_price[1][4]
    tab[0][3] = resp_price[2][4]
    tab[0][4] = resp_price[3][4]
    tab[0][5] = resp_price[4][4]
    tab[0][6] = resp_price[5][4]
    tab[0][7] = resp_price[6][4]
    tab[0][8] = resp_price[7][4]
    tab[0][9] = resp_price[8][4]
    tab[0][10] = resp_price[9][4]
    tab[0][11] = resp_price[10][4]
    tab[0][12] = resp_price[11][4]
    tab[0][13] = resp_price[12][4]
    tab[0][14] = resp_price[13][4]

    while True:
        SMA14 = float(SMA14) + float(tab[0][licznik])
        licznik = licznik + 1
        if licznik == 15:
            SMA14 = float(SMA14) / 14
            return str(SMA14)
            break
  except:
    errorC = resp_price['code']
    errorM = resp_price['msg']
    if float(errorC) < 0:
        print(str(errorC) + " " + str(errorM))
        sys.exit()

def BB14(market, tick_interval):
  try:
    Q = 0
    BB14up = 0
    BB14down = 0
    SMA14 = 0
    licznik = 1
    url = 'https://api.binance.com/api/v1/klines?symbol=' + market + '&interval=' + tick_interval + '&limit=14'
    data = requests.get(url).json()
    json1 = json.dumps(data)
    resp_price = json.loads(json1)

    tab = [[0 for close in range(16)] for market in range(1)]
    tab[0][0] = market
    tab[0][1] = resp_price[0][4]
    tab[0][2] = resp_price[1][4]
    tab[0][3] = resp_price[2][4]
    tab[0][4] = resp_price[3][4]
    tab[0][5] = resp_price[4][4]
    tab[0][6] = resp_price[5][4]
    tab[0][7] = resp_price[6][4]
    tab[0][8] = resp_price[7][4]
    tab[0][9] = resp_price[8][4]
    tab[0][10] = resp_price[9][4]
    tab[0][11] = resp_price[10][4]
    tab[0][12] = resp_price[11][4]
    tab[0][13] = resp_price[12][4]
    tab[0][14] = resp_price[13][4]

    while True:
        SMA14 = float(SMA14) + float(tab[0][licznik])
        licznik = licznik + 1
        if licznik == 15:
            SMA14 = float(SMA14) / 14
            licznik = 1
            break

    while True:
        Q = float(Q) + (float(tab[0][licznik]) - float(SMA14))**2
        licznik = licznik + 1
        if licznik == 15:
            Q = float(Q) / 14
            Q = math.sqrt(float(Q))
            BB14up = float(SMA14) + float(Q) * 2
            BB14down = float(SMA14) - float(Q) * 2
            #print "%-.24f"%(r)
            return [
                "%-.8f" % (SMA14),
                "%-.8f" % (BB14up),
                "%-.8f" % (BB14down)
            ]
            break
  except:
    errorC = resp_price['code']
    errorM = resp_price['msg']
    if float(errorC) < 0:
        print(str(errorC) + " " + str(errorM))
        sys.exit()

def Symbol(a):
  try:
    if a == 0:
        a = 0
    else:
        a = a
    url = 'https://api.binance.com/api/v3/ticker/price'
    data = requests.get(url).json()
    json1 = json.dumps(data)
    resp_price = json.loads(json1)
    symbol = resp_price[a]['symbol']
    return symbol
  except:
    errorC = resp_price['code']
    errorM = resp_price['msg']
    if float(errorC) < 0:
        print(str(errorC) + " " + str(errorM))
        sys.exit()

def TestValue(market, tick_interval):
  try:
    #parms
    #market = 'GTOBTC'
    #tick_interval = '1h'
    #limit = 5
    url = 'https://api.binance.com/api/v1/klines?symbol=' + market + '&interval=' + tick_interval + '&limit=5'
    data = requests.get(url).json()
    json1 = json.dumps(data)
    resp_price = json.loads(json1)

    tab = [[0 for close in range(16)] for market in range(1)]
    tab[0][0] = market
    tab[0][1] = resp_price[0][5]
    tab[0][2] = resp_price[1][5]
    tab[0][3] = resp_price[2][5]
    tab[0][4] = resp_price[3][5]
    tab[0][5] = resp_price[4][5]

    if float(tab[0][1]) > 0 and float(tab[0][2]) > 0 and float(
            tab[0][3]) > 0 and float(tab[0][4]) > 0:
        procent_diff1 = float(tab[0][2]) / float(tab[0][1]) - 1
        procent_diff1 = float(procent_diff1) * 100
        procent_diff1 = round(procent_diff1, 2)
        TestValue1 = str(procent_diff1)

        procent_diff2 = float(tab[0][3]) / float(tab[0][2]) - 1
        procent_diff2 = float(procent_diff2) * 100
        procent_diff2 = round(procent_diff2, 2)
        TestValue2 = str(procent_diff2)

        procent_diff3 = float(tab[0][4]) / float(tab[0][3]) - 1
        procent_diff3 = float(procent_diff3) * 100
        procent_diff3 = round(procent_diff3, 2)
        TestValue3 = str(procent_diff3)

        procent_diff4 = float(tab[0][5]) / float(tab[0][4]) - 1
        procent_diff4 = float(procent_diff4) * 100
        procent_diff4 = round(procent_diff4, 2)
        TestValue4 = str(procent_diff4)
    else:
        TestValue1 = 0
        TestValue2 = 0
        TestValue3 = 0
        TestValue4 = 0

    return [TestValue1, TestValue2, TestValue3, TestValue4]
  except:
    errorC = resp_price['code']
    errorM = resp_price['msg']
    if float(errorC) < 0:
        print(str(errorC) + " " + str(errorM))
        sys.exit()

def TestPrice(market, tick_interval):
  try:
    #parms
    #market = 'GTOBTC'
    #tick_interval = '1h'
    #limit = 5
    url = 'https://api.binance.com/api/v1/klines?symbol=' + market + '&interval=' + tick_interval + '&limit=5'
    data = requests.get(url).json()
    json1 = json.dumps(data)
    resp_price = json.loads(json1)

    TestPrice0 = resp_price[0][4]
    TestPrice1 = resp_price[1][4]
    TestPrice2 = resp_price[2][4]
    TestPrice3 = resp_price[3][4]
    TestPrice4 = resp_price[4][4]

    return [TestPrice0, TestPrice1, TestPrice2, TestPrice3, TestPrice4]
  except:
    errorC = resp_price['code']
    errorM = resp_price['msg']
    if float(errorC) < 0:
        print(str(errorC) + " " + str(errorM))
        sys.exit()

def StartAnaliz():
    k = 0
    a = 0
    interval = '15m'
    base = 'BTC'
    while k < 1:
        if Symbol(a)[-3:] == str(base) and Symbol(a)[0:3] != 'HSR' and Symbol(
                a)[0:3] != 'SUB' and Symbol(a)[0:3] != 'MOD' and Symbol(
                    a)[0:5] != 'CLOAK' and Symbol(
                        a)[0:5] != 'WINGS' and Symbol(a)[0:4] != 'SALT':
            if a <= 161:
                balanceBTC = client.get_asset_balance(asset='BTC', recvWindow=1000000)
                balanceBTCJSON = json.dumps(balanceBTC)
                balanceBTCRESP = json.loads(balanceBTCJSON)
                balanceBTCFREE = balanceBTCRESP['free']
                balanceBTCLOCKED = balanceBTCRESP['locked']
                symbol = Symbol(a)
                Diff1 = TestValue(market=symbol, tick_interval=interval)[0]
                Diff2 = TestValue(market=symbol, tick_interval=interval)[1]
                Diff3 = TestValue(market=symbol, tick_interval=interval)[2]
                Diff4 = TestValue(market=symbol, tick_interval=interval)[3]
                Price1 = TestPrice(market=symbol, tick_interval=interval)[1]
                Price2 = TestPrice(market=symbol, tick_interval=interval)[2]
                Price3 = TestPrice(market=symbol, tick_interval=interval)[3]
                Price4 = TestPrice(market=symbol, tick_interval=interval)[4]
                print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +
                      ' >> ' + str(symbol) + ' NONE!' + '\t' + '\t' +
                      ' Your balance in BTC: FREE:' +
                      str(balanceBTCFREE) + '\t' +
                      ' LOCKED:' +
                      str(balanceBTCLOCKED))
                print(
                    '***********************************************************************************************************************'
                )
                if float(Diff1) < float(Diff2) < float(Diff3) < float(Diff4):
                    rsi = RSI14(market=symbol, tick_interval='1h')
                    bbsma = BB14(market=symbol, tick_interval='1h')[0]
                    bbup = BB14(market=symbol, tick_interval='1h')[1]
                    bbdown = BB14(market=symbol, tick_interval='1h')[2]
                    pbbsma = (
                        float(Price4) - float(bbsma)) / float(bbsma) * 100
                    pbbsma = round(pbbsma, 2)
                    if pbbsma < 0:
                        pbbsma = "%-.2f" % (pbbsma) + '%'
                    else:
                        pbbsma = " " "%-.2f" % (pbbsma) + '%'
                    pbbup = (float(Price4) - float(bbup)) / float(bbup) * 100
                    pbbup = round(pbbup, 2)
                    if pbbup < 0:
                        pbbup = "%-.2f" % (pbbup) + '%'
                    else:
                        pbbup = " " "%-.2f" % (pbbup) + '%'
                    pbbdown = (
                        float(Price4) - float(bbdown)) / float(bbdown) * 100
                    pbbdown = round(pbbdown, 2)
                    if pbbdown < 0:
                        pbbdown = "%-.2f" % (pbbdown) + '%'
                    else:
                        pbbdown = " " "%-.2f" % (pbbdown) + '%'
                    Diff1 = Diff1 + '%'
                    Diff2 = Diff2 + '%'
                    Diff3 = Diff3 + '%'
                    Diff4 = Diff4 + '%'
                    Price = (float(Price4) / float(Price1) - 1) * 100
                    Price = round(Price, 2)
                    Price = str(Price) + '%'
                    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                          + ' >> ' + str(symbol) + ' << ' + str(Diff2) +
                          ' << ' + str(Diff3) + ' << ' + str(Diff4))
                    print("\t" + "\t" + "\t" + "\t" + "\t" + "\t" +
                          "|--- c1: " + str(Price1) + '  |' + "\n" + "\t" +
                          "\t" + "\t" + "\t" + "\t" + "\t" + "|--- c2: " +
                          str(Price2) + '  |' + "\n" + "\t" + "\t" + "\t" +
                          "\t" + "\t" + "\t" + "|--- c3: " + str(Price3) +
                          '  |' + "\n" + "\t" + "\t" + "\t" + "\t" + "\t" +
                          "\t" + "|--- c4: " + str(Price4) +
                          '  ---> change price: ' + str(Price))
                    print("Analiz:" + '\n' + "\t" + 'RSI(14):' + "\t" +
                          str(rsi)[0:4] + '\n' + "\t" + 'SMA(14):' + "\t" +
                          str(bbsma) + "\t" + '-->' + "\t" + str(pbbsma) +
                          "\n" + "\t" + 'BBup(14):' + "\t" + str(bbup) + "\t" +
                          '-->' + "\t" + str(pbbup) + "\n" + "\t" +
                          'BBdown(14):' + "\t" + str(bbdown) + "\t" + '-->' +
                          "\t" + str(pbbdown))
                    print(
                        '***********************************************************************************************************************'
                    )
                a = a + 1
            else:
                a = 0
        else:
            a = a + 1

