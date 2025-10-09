from bank.account import Account 
import logging

logger = logging.getLogger(__name__)

class Client: 
    def __init__(self, id: int, firstname: str, lastname: str): 
        self.id: int = id
        self.firstname: str = firstname
        self.lastname: str = lastname
        self.accounts: list[Account] = [] #objects list


    def get_account(self, account_number: str) -> Account | None:
        """
        Récupère un compte par son numéro
        
        Returns:
            dict avec 'success', 'account', 'message'
        """
        for account in self.accounts:
            if account.account_number == account_number:
                return {
                'success': True,
                'account': account,
                'message': f"Compte trouvé: {account.account_name} N° {account.account_number} (solde {account.balance} €)" 
                }
    
        logger.warning(f"Aucun compte trouvé pour le numéro : {account_number}")
        return {
                'success': False,
                'account': None,
                'message': f"Aucun compte trouvé pour le numéro : {account_number}."
            }


    def get_all_accounts(self) -> list[Account]:
        """
        Retourne tous les comptes du client
        
        Returns:
            Liste des comptes
        """
        return self.accounts.copy()
    

    def get_total_balance(self) -> float: 
        """
        Calcule le solde total de tous les comptes du client.
        
        Returns:
            Solde total
        """
        return sum(account.balance for account in self.accounts)
        
    
    def __str__(self) -> str: 
        if self.accounts: 
            accounts_numbers = [account.account_number for account in self.accounts]
            accounts_str = ", ".join(accounts_numbers)
        else: 
            accounts_str = "Aucun compte."
            
        return f"ID: {self.id}, Prénom: {self.firstname}, Nom: {self.lastname}, Comptes: {accounts_str}"
    

    def __repr__(self) -> str:
        return f"Client({self.id}, {self.firstname}, {self.lastname}, {self.accounts})"