from bank.client import Client
from bank.account import Account
import logging

logger = logging.getLogger(__name__)


class Bank: 
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.clients: list[Client] = []  
        self.accounts: list[Account] = []  


    def get_client_by_id(self, client_id: int) -> dict:
        """
        Récupère un client par son ID.
        
        Returns:
            dict avec 'success', 'client', 'message'
        """
        for client in self.clients:
            if client.id == client_id:
                return {
                    'success': True,
                    'client': client,
                    'message': f"Client {client.firstname} {client.lastname} trouvé"
                }
        
        logger.warning(f"Client ID {client_id} introuvable dans {self.name}")
        return {
            'success': False,
            'client': None,
            'message': f"Client avec l'ID {client_id} introuvable"
        }
    
    
    def add_client(self, client:Client) -> dict:
        """Ajoute un client à la banque 
        
        Returns: 
            dict avec 'success', 'client', 'message' 
        """
        # Vérifier si le client existe déjà
        if self.get_client_by_id(client.id)['success']:
            logger.warning(f"Client ID {client.id} existe déjà chez {self.name}")
            return {
                'success': False,
                'client': None,
                'message': f"Client avec l'ID {client.id} existe déjà"
            }
        self.clients.append(client)
        
        return {
            'success': True,
            'client': client,
            'message': f"Client {client.firstname} {client.lastname} ajouté avec succès"
        }
    

    def get_all_clients(self) -> list[Client]:
        """
        Retourne tous les clients de la banque.
        
        Returns:
            Liste des clients
        """
        return self.clients.copy()
    
    
    def get_account_by_number(self, account_number: str) -> dict:
        """
        Récupère un compte par son numéro.
        
        Returns:
            dict avec 'success', 'account', 'message'
        """
        for account in self.accounts:
            if account.account_number == account_number:
                return {
                    'success': True,
                    'account': account,
                    'message': f"Compte {account.account_name} trouvé"
                }
        
        logger.warning(f"Compte {account_number} introuvable")
        return {
            'success': False,
            'account': None,
            'message': f"Compte {account_number} introuvable"
        }
    

    def get_all_accounts(self) -> list[Account]:
        """
        Retourne tous les comptes de la banque.
        
        Returns:
            Liste des comptes
        """
        return self.accounts.copy()
    
    
    def open_account(self, client: Client, account_name: str, account_number: str, 
                     initial_balance: float = 0, max_balance: float = 20000) -> Account:
        """
        Ouvre un nouveau compte pour un client.
        
        Returns:
            dict avec 'success', 'account', 'message'
        """
        # Vérifier que le client existe dans la banque
        if client not in self.clients:
            logger.warning(f"Tentative d'ouverture de compte pour un client non enregistré")
            return {
                'success': False,
                'account': None,
                'message': "Le client n'est pas enregistré dans cette banque"
            }
    
        # Vérifier que le numéro de compte n'existe pas déjà
        if self.get_account_by_number(account_number)['success']:
            logger.warning(f"Compte {account_number} existe déjà")
            return {
                'success': False,
                'account': None,
                'message': f"Le numéro de compte {account_number} existe déjà"
            }
        
        # Créer le compte
        account = Account(account_name, account_number, initial_balance, max_balance)
        client.accounts.append(account)
        self.accounts.append(account)
        
        return {
            'success': True,
            'account': account,
            'message': f"Compte {account_name} ouvert avec succès"
        }


    def delete_client_by_id(self, client_id: int) -> dict:
        """
        Supprime un client et tous ses comptes.
        
        Returns:
            dict avec 'success', 'message'
        """
        result = self.get_client_by_id(client_id)
        
        if not result['success']:
            return {
                'success': False,
                'message': f"Impossible de supprimer : client {client_id} introuvable"
            }
        
        client = result['client']
        
        # Supprimer tous les comptes du client
        accounts_to_remove = client.accounts.copy()
        for account in accounts_to_remove:
            self.delete_account_by_number(account.account_number)
        
        # Supprimer le client
        self.clients.remove(client)
        logger.info(f"Client {client.firstname} {client.lastname} (ID {client_id}) supprimé")
        
        return {
            'success': True,
            'message': f"Client {client.firstname} {client.lastname} supprimé avec succès"
        }
    

    def delete_account_by_number(self, account_number: str) -> dict:
        """
        Supprime un compte.
        
        Returns:
            dict avec 'success', 'message'
        """
        result = self.get_account_by_number(account_number)
        
        if not result['success']:
            return {
                'success': False,
                'message': f"Impossible de supprimer : compte {account_number} introuvable"
            }
        
        account = result['account']
        
        # Supprimer le compte de la liste globale de la banque
        self.accounts.remove(account)
        
        # Supprimer le compte de la liste du client
        for client in self.clients:
            if account in client.accounts:
                client.accounts.remove(account)
                logger.info(f"Compte {account_number} supprimé du client {client.firstname} {client.lastname}")
                break
        
        return {
            'success': True,
            'message': f"Compte {account_number} supprimé avec succès"
        }
    

    def __str__(self) -> str:
        return f"Banque: {self.name} (ID: {self.id}), Clients: {len(self.clients)}, Comptes: {len(self.accounts)}"
    
    
    def __repr__(self) -> str:
        return f"Bank({self.id}, '{self.name}')"