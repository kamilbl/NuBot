import Analiz
import Balance
import Strategy_RSI
import Strategy_PingPong
import Strategy_PingPong2
import Strategy_PingPong_SMA
import Strategy_BB
import Strategy_SD

def menu():
  print("\n Welcome in NuBot_Phyton \n \n \t 1. Analiz and Signal \n \t 2. Strategy RSI \n \t 3. Strategy PingPong \n \t 4. Strategy PingPong2  \n \t 5. Strategy PingPong with SMA \n \t 6. Strategy BB \n \t 7. Strategy Scalping Depth \n \t 8. Balance")
  choice = input()

  if choice == "1":
    print("Start Analiz and Signal \n------------------------------------------------------------------------------------------------------------------------------------")
    Analiz.StartAnaliz()
  if choice == "2":
    print("Strategy RSI \n------------------------------------------------------------------------------------------------------------------------------------")
    Strategy_RSI.Strategy_RSI()
  if choice == "3":
    print("Strategy PingPong \n------------------------------------------------------------------------------------------------------------------------------------")
    Strategy_PingPong.Strategy_PingPong()
  if choice == "4":
    print("Strategy PingPong \n------------------------------------------------------------------------------------------------------------------------------------")
    Strategy_PingPong2.Strategy_PingPong2()
  if choice == "5":
    print("Strategy PingPong with SMA \n------------------------------------------------------------------------------------------------------------------------------------")
    Strategy_PingPong_SMA.Strategy_PingPong_SMA()
  if choice == "6":
    print("Strategy BB \n------------------------------------------------------------------------------------------------------------------------------------")
    Strategy_BB.Strategy_BB()
  if choice == "7":
    print("Strategy Scalping Depth \n------------------------------------------------------------------------------------------------------------------------------------")
    Strategy_SD.Strategy_Scalping_Depth()
  if choice == "8":
    print("Balance Account \n------------------------------------------------------------------------------------------------------------------------------------")
    Balance.MyBalance()
  
