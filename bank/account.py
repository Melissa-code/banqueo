from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class Account: 
    def __init__(self, account_name: str, account_number: str, balance: float = 0, max_balance: float = 10000): 
        self.account_name: str = account_name
        self.account_number: str = account_number
        self.balance: float = balance
        self.max_balance: float = max_balance
        self.history: list[dict] = [] 
    

    def date_now(self) -> str:
        """Retourne la date du jour heure et minute de l'opération pour précision"""
        return datetime.now().strftime("%d-%m-%Y (%H:%M)")


    def deposit(self, amount: float) -> dict:
        """
        Effectue un dépôt sur le compte.
        
        Returns: 
            dict avec 'success', 'balance', 'message'
        """
        new_balance = amount + self.balance

        if (new_balance >= self.max_balance): 
            logger.warning("Dépôt refusé : plafond dépassé.")
            return {
                'success': False,
                'balance': self.balance,
                'message': f"Dépôt refusé : le solde dépasserait le plafond de {self.max_balance} €"
            }

        self.balance = new_balance
        operation = {
            'type': 'deposit',
            'date': self.date_now(),
            'amount': amount,
            'balance': self.balance,
            'account_name': self.account_name
        }
        self.history.append(operation)
        logger.info(f"Dépôt de {amount} € sur {self.account_name}")

        return {
            'success': True,
            'balance': self.balance,
            'message': f"Dépôt de {amount} € effectué avec succès. Nouveau solde: {self.balance}"
        }


    def withdraw(self, amount: float) -> dict:
        """
        Effectue un retrait sur le compte.
        
        Returns: 
            dict avec 'success', 'balance', 'message'
        """
        new_balance = self.balance - amount
    
        if (new_balance < 0): 
            logger.warning(f"Retrait refusé sur {self.account_name}: fonds insuffisants")
            return {
                'success': False,
                'balance': self.balance,
                'message': f"Retrait refusé : fonds insuffisants (solde: {self.balance} €)"
            }
        
        self.balance = new_balance
        operation = {
            'type': 'withdraw',
            'date': self.date_now(),
            'amount': amount,
            'balance': self.balance,
            'account_name': self.account_name
        }
        self.history.append(operation)
        logger.info(f"Retrait de {amount} € sur {self.account_name}")

        return {
            'success': True,
            'balance': self.balance,
            'message': f"Dépôt de {amount} € effectué avec succès"
        }
    

    def get_history(self) -> list[dict]:
        """
        Retourne l'historique des opérations.
        
        Returns:
            Liste de dictionnaires contenant les opérations (copie pour éviter les modifications)
        """
        return self.history.copy() 

    
    def __str__(self) -> str: 
        return f"Nom: {self.account_name}, N°: {self.account_number}, Solde: {self.balance}, Plafond: {self.max_balance}"
    

    def __repr__(self) -> str:
        return f"Account('{self.account_name}', '{self.account_number}', {self.balance}, {self.max_balance})"