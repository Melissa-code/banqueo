from decimal import Decimal
from bank.account import Account

class AccountFactory:

    @staticmethod
    def create_account(
        account_name = "Compte courant", 
        account_number = "12345", 
        balance = '0.00',
        max_balance = '10000.00',
        history = None
        ) -> Account:

        # pour que chaque test ait sa liste indépendante d'historique != tous les comptes créés partagent la même liste d'historique
        if history is None:
            history = []
        
        return Account(account_name, account_number, Decimal(str(balance)), Decimal(str(max_balance)), history)