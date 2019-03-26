import Analiz
import Balance
import Strategy_RSI
import Strategy_PingPong
def menu():
  print("\n Welcome in NuBot_Phyton \n \n \t 1. Analiz and Signal \n \t 2. Strategy RSI \n \t 3. Strategy PingPong \n \t 4. Strategy BB \n \t 5. Balance")
  choice = input()

  if choice == "1":
    print("Start Analiz and Signal \n------------------------------------------------------------------------------------------------------------------------------------")
    Analiz.StartAnaliz()
  if choice == "2":
    print("Strategy RSI \n------------------------------------------------------------------------------------------------------------------------------------")
    Strategy_RSI.StrategyRSI()
  if choice == "3":
    print("Strategy PingPong \n------------------------------------------------------------------------------------------------------------------------------------")
    Strategy_PingPong.Strategy_PingPong()
  if choice == "4":
    print("Strategy BB \n------------------------------------------------------------------------------------------------------------------------------------")
  if choice == "5":
    print("Balance Account \n------------------------------------------------------------------------------------------------------------------------------------")
    Balance.MyBalance()
    