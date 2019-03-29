# NuBot

Nubot is simply bot on Binance market. I'm testing now. I' begginer in Python. I want learning :D 

Now this bot has:
  1) Analiz and Signal = Analiz RSI and BB only par BTC. We can send on Telegram.
  2) Strategy RSI = In Setting.py we can change params. 
  3) Strategy PingPong = In Setting.py we can change parms.
  4) Strategy PingPong SMA = In setting.py we can change parms.
  5) Strategy BB = In setting.py we can change parms.
  6) Balance = Your balance account on Binance Market.


Strategy RSI - This strategy is very simply. We need add MIN and MAX. Of course we have possibility add budget_order and budget_total.
  https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:relative_strength_index_rsi
  
Strategy PingPong - In this strategy we set base price, profit up, profit down. This strategy buy/sell coins when profit will be done. We have possibility set start operation "SELL" or "BUY".

Strategy PingPong SMA - In this strategy we set profit up, profit down. Base price is line SMA. This strategy buy/sell coins when profit will be done. We have possibility set start operation "SELL" or "BUY".

Strategy BB - In this strategy we use BB. Bot checks actual price and levels BB line (base, up and down). When actual bot cross line BB will be order (Sell or Buy). We can change tick_interval in Setting file.
  https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:bollinger_bands
    ![ScreenShot](https://github.com/kamilbl/NuBot/blob/master/Screen/Screen_Strategy_BB.PNG)

In file key.py we need add Api Binance and Telegram.
