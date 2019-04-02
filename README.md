# NuBot

Nubot is simply bot on Binance market. I'm testing now. I'm begginer in Python.

**Now this bot has:**
  1) Analiz and Signal = Analiz RSI and BB only par BTC. We can send on Telegram.
  2) Strategy RSI
  3) Strategy PingPong
  4) Strategy PingPong2
  5) Strategy PingPong SMA
  6) Strategy BB
  7) Strategy SD
  8) Balance


**Strategy RSI** [Link](https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:relative_strength_index_rsi) - This strategy is very simply. We need add level RSI MIN and MAX.
  
**Strategy PingPong** - In this strategy we set base price, profit up, profit down. This strategy buy/sell coins when profit will be done. We have possibility set start operation "SELL" or "BUY".

**Strategy PingPong2** - In this strategy we set base price, profit up, profit down. This strategy buy/sell coins when profit will be done. We have possibility set start operation "SELL" or "BUY". Main diffrent between Strategy PingPong is in Strategy PingPong2 orders is create in the begining. "Orders wait for grows or downhill".

**Strategy PingPong SMA** - In this strategy we set profit up, profit down. Base price is line SMA. This strategy buy/sell coins when profit will be done. We have possibility set start operation "SELL" or "BUY".

**Strategy BB** [Link](https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:bollinger_bands) - In this strategy we use BB. Bot checks actual price and levels BB line (base, up and down). When actual bot cross line BB will be order (Sell or Buy). We can change tick_interval in Settings file. 
    ![ScreenShot](https://github.com/kamilbl/NuBot/blob/master/Screen/Screen_Strategy_BB.PNG)

In file key.py we need add Api Binance and Telegram.
