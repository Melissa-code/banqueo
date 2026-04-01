from datetime import datetime
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


class Account: 
    
    def __init__(self, account_name: str, account_number: str, balance: Decimal = 0, max_balance: Decimal = 10000, history: list = None) -> None: 
        self.account_name = account_name
        self.account_number = account_number
        self.balance = balance
        self.max_balance = max_balance
        self.history: list[dict] = history if history is not None else [] 
    

    def date_now(self) -> str:
        """Retourne la date du jour heure et minute de l'opération pour précision"""
        return datetime.now().strftime("%d-%m-%Y (%H:%M)")


    def deposit(self, amount: Decimal) -> Decimal:
        # sourcery skip: class-extract-method
        """Effectue un dépôt sur le compte oulève une exception si le dépôt dépasse le plafond"""
        new_balance = amount + self.balance

        if (new_balance >= self.max_balance): 
            logger.warning(f"[Account {self.account_number} deposit()]: Dépôt de {amount} € refusé: plafond dépassé")
            raise ValueError(f"Dépôt refusé : le solde dépasserait le plafond de {self.max_balance} € autorisé.")

        self.balance = new_balance
        self._add_to_history('dépôt', amount)
        logger.info(f"[Account {self.account_number} deposit()]: dépôt de {amount} € effectué. Nouveau solde: {self.balance}")
        return self.balance


    def withdraw(self, amount: Decimal) -> Decimal:
        """Effectue un retrait sur le compte"""
        new_balance = self.balance - amount
    
        if (new_balance < 0): 
            logger.warning(f"[Account {self.account_number} withdraw()]: retrait refusé sur {self.account_name}: fonds insuffisants")
            raise ValueError(f"Retrait refusé : fonds insuffisants (solde: {self.balance} €)")
        
        self.balance = new_balance
        self._add_to_history('retrait', amount)
        logger.info(f"[Account {self.account_number} withdraw()]: retrait de {amount} € effectué. Nouveau solde: {self.balance}")
        return self.balance
    

    def get_history(self) -> list[dict]:
        """Retourne l'historique des opérations"""
        return self.history.copy() 

    
    def __str__(self) -> str: 
        return f"Nom: {self.account_name}, N°: {self.account_number}, Solde: {self.balance}, Plafond: {self.max_balance}"
    

    def __repr__(self) -> str:
        return f"Account('{self.account_name}', '{self.account_number}', {self.balance}, {self.max_balance})"
    

    #----------------------------- Méthodes privées --------------------------------#

    def _add_to_history(self, operation_type: str, amount: Decimal) -> None:
        """Ajoute une opération à l'historique du compte"""
        operation = {
            'type': operation_type,
            'date': self.date_now(),
            'amount': amount,
            'balance': self.balance,
            'account_name': self.account_name
        }
        self.history.append(operation)