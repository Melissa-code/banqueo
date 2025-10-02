from account import Account 

def main(): 
    acc = Account("12345", balance=1000, max_balance=2000)

    print(" Dépôt de 500")
    acc.deposit(500)
    acc.show_history()

    print("\n Retrait de 200")
    acc.withdraw(200)
    acc.show_history()

    print("\n Dépôt qui dépasse le plafond")
    acc.deposit(2000)  
    acc.show_history()

    print("\n Retrait qui rend le solde négatif")
    acc.withdraw(2000)  
    acc.show_history()

    print("\n Historique complet")
    acc.show_history()
  

if __name__ == "__main__":
    main()