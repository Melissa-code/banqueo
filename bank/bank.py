import logging
from decimal import Decimal

from bank.account import Account
from bank.client import Client

logger = logging.getLogger(__name__)


class Bank: 

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.clients: list[Client] = []  
        self.accounts: list[Account] = []  


    def get_client_by_id(self, client_id: int) -> Client:
        """Récupère un client par son ID ou lève une erreur si le client n'existe pas"""
        for client in self.clients:
            if client.id == client_id:
                return client
        
        logger.warning(f"[Bank ID:{self.id}] get_client_by_id(): client ID {client_id} introuvable dans {self.name}")
        raise ValueError(f"Client avec l'ID {client_id} n'existe pas dans la banque {self.name}")
    
    
    def add_client(self, client: Client) -> Client:
        """Ajoute un client à la banque (refuse les ID en double)"""
        if any(c.id == client.id for c in self.clients):
            logger.warning(f"[Bank ID:{self.id}] add_client(): client ID {client.id} existe déjà dans {self.name}")
            raise ValueError(f"Client avec l'ID {client.id} existe déjà dans la banque {self.name}")

        self.clients.append(client)
        logger.info(f"[Bank ID:{self.id}] add_client(): client {client.firstname} {client.lastname} (ID {client.id}) ajouté à la banque {self.name}")
        return client
        
        
    def get_all_clients(self) -> list[Client]:
        """Retourne tous les clients de la banque"""
        return self.clients.copy()
    
    
    def get_account_by_number(self, account_number: str) -> Account:
        """Récupère un compte par son numéro ou lève une erreur si le compte n'existe pas"""
        for account in self.accounts:
            if account.account_number == account_number:
                return account
        
        logger.warning(f"[Bank ID:{self.id}] get_account_by_number(): compte {account_number} introuvable")
        raise ValueError(f"Compte avec le numéro {account_number} n'existe pas dans la banque {self.name}")


    def get_all_accounts(self) -> list[Account]:
        """Retourne tous les comptes de la banque"""
        return self.accounts.copy()
    
    
    def open_account(self, client: Client, account_name: str, account_number: str, initial_balance: Decimal = Decimal("0.00"), max_balance: Decimal = Decimal("20000.00")) -> Account:
        """Ouvre un compte pour un client de la banque"""
        if client not in self.clients:
            logger.warning(f"[Bank ID:{self.id}] open_account(): client {client.firstname} {client.lastname} (ID {client.id}) n'appartient pas à la banque {self.name}")
            raise ValueError(f"Le client {client.firstname} n'appartient pas à la banque {self.name}")

        if any(a.account_number == account_number for a in self.accounts):
            logger.warning(f"[Bank ID:{self.id}] open_account(): compte {account_number} existe déjà")
            raise ValueError(f"Le numéro de compte {account_number} existe déjà dans la banque {self.name}")

        account = Account(account_name, account_number, initial_balance, max_balance)
        client.accounts.append(account)
        self.accounts.append(account)
        return account


    def delete_client_by_id(self, client_id: int) -> None:
        """Supprime un client et tous ses comptes"""
        client = self.get_client_by_id(client_id)
        
        # Supprime tous les comptes du client
        accounts_to_remove = client.accounts.copy()
        for account in accounts_to_remove:
            self.delete_account_by_number(account.account_number)
        
        # Supprimer le client
        self.clients.remove(client)
        logger.info(f"[Bank ID:{self.id}] delete_client_by_id(): client {client.firstname} {client.lastname} (ID {client_id}) supprimé")
        

    def delete_account_by_number(self, account_number: str) -> None:
        """Supprime un compte"""
        account = self.get_account_by_number(account_number)
        
        # Supprimer le compte de la liste globale de la banque
        self.accounts.remove(account)
        
        # Supprimer le compte de la liste du client
        for client in self.clients:
            if account in client.accounts:
                client.accounts.remove(account)
                logger.info(f"[Bank ID:{self.id}] delete_account_by_number(): compte { account.account_name } {account.account_number} supprimé du client {client.firstname} {client.lastname}")
                break
    

    def __str__(self) -> str:
        return f"Banque: {self.name} (ID: {self.id}), Clients: {len(self.clients)}, Comptes: {len(self.accounts)}"
    
    
    def __repr__(self) -> str:
        return f"Bank({self.id}, '{self.name}')"