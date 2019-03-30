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

def Strategy_Scalping_Depth():
	k=0
	a=1
	while k<1:
		symbol = Symbols.SymbolsMatrix[a][0]
		depth = client.get_order_book(symbol = str(symbol) + 'BTC', limit=5)
		depthJSON = json.loads(json.dumps(depth))

		depthAskPrice = depthJSON['asks'][0][1]
		print(depthAskPrice)
		k=1

