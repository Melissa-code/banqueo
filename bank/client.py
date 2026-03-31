from bank.account import Account 
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


class Client: 

    def __init__(self, id: int, firstname: str, lastname: str): 
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.accounts: list[Account] = [] #objects list


    def get_account(self, account_number: str) -> Account:
        """Récupère un compte par son numéro ou lève une erreur si le compte n'existe pas"""
        for account in self.accounts:
            if account.account_number == account_number:
                return account
    
        logger.warning(f"[Client ID:{self.id}] get_account(): compte {account_number} introuvable.")
        raise ValueError(f"Le compte n°{account_number} n'existe pas.")


    def get_all_accounts(self) -> list[Account]:
        """Retourne tous les comptes du client ou liste vide[] (copy pour éviter modification externe: encapsulation des données)"""
        return self.accounts.copy()
    

    def get_total_balance(self) -> Decimal:
        """Calcule le solde total de tous les comptes du client - Decimal('0.00') point de départ"""
        return sum(account.balance for account in self.accounts), Decimal('0.00')
        
    
    def __str__(self) -> str: 
        if self.accounts: 
            accounts_numbers = [account.account_number for account in self.accounts]
            accounts_str = ", ".join(accounts_numbers)
        else: 
            accounts_str = "Aucun compte."
            
        return f"ID: {self.id}, Prénom: {self.firstname}, Nom: {self.lastname}, Comptes: {accounts_str}"
    

    def __repr__(self) -> str:
        return f"Client({self.id}, {self.firstname}, {self.lastname})"