import Analiz
import Balance
import Strategy_RSI
import Strategy_PingPong
import Strategy_PingPong_SMA
import Strategy_BB

def menu():
  print("\n Welcome in NuBot_Phyton \n \n \t 1. Analiz and Signal \n \t 2. Strategy RSI \n \t 3. Strategy PingPong \n \t 4. Strategy PingPong with SMA \n \t 5. Strategy BB \n \t 6. Balance")
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
    print("Strategy PingPong with SMA \n------------------------------------------------------------------------------------------------------------------------------------")
    Strategy_PingPong_SMA.Strategy_PingPong_SMA()
  if choice == "5":
    print("Strategy BB \n------------------------------------------------------------------------------------------------------------------------------------")
    Strategy_BB.Strategy_BB()
  if choice == "6":
    print("Balance Account \n------------------------------------------------------------------------------------------------------------------------------------")
    Balance.MyBalance()
  
