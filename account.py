from datetime import datetime

class Account: 

    def __init__(self, account_number: str, account_name: str, balance: float = 0, max_balance: float = 10000): 
        self.account_number: str = account_number
        self.account_name: str = account_name
        self.balance: float = balance
        self.max_balance: float = max_balance
        self.history: list[str] = [] 

    
    def date_now(self) -> str:
        return datetime.now().strftime("%d-%m-%Y (%H:%M)")


    def deposit(self, amount: float) -> float:
        new_balance = amount + self.balance
        if (new_balance < self.max_balance):
            self.balance = new_balance
            self.history.append(f"Dépôt le {self.date_now()} sur {self.account_name}: +{amount} €. Nouveau solde: {self.balance} €")
        else:
            print("Dépôt refusé : plafond dépassé.")

        return self.balance


    def withdraw(self, amount) -> float: 
        new_balance = self.balance - amount
        if (new_balance < 0): 
            print("Retrait refusé : fonds insuffisants.")
        else: 
            self.balance = new_balance
            self.history.append(f"Retrait le {self.date_now()} sur {self.account_name}: -{amount} €. Nouveau solde: {self.balance} €")

        return self.balance
    

    def show_history(self) -> None: 
        if (not self.history): 
            print("Auncune opération enregistrée.")
        else: 
            for operation in self.history:
                print(operation) 

    
    def __str__(self) -> str: 
        return f"Nom: {self.account_name}, N°: {self.account_number}, Montant: {self.balance}, Montant maximum: {self.max_balance}"
    

    def __repr__(self) -> str:
        return self.__str__()