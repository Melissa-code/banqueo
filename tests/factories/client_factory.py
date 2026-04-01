from factories.account_factory import AccountFactory
from bank.client import Client

class ClientFactory:

    @staticmethod
    def create_client(
        client_id = 1, 
        firstname = "John", 
        lastname = "Doe",
        client_accounts = None
        ) -> Client:

        if client_accounts is None:
            client_accounts = []

        return Client(client_id, firstname, lastname, client_accounts)
    
    
    @staticmethod
    def create_client_with_accounts():
        """Génère un client avec 2 comptes pré-remplis pour les tests"""
        client = ClientFactory.create_client()
        client.accounts.append(AccountFactory.create_account(account_name="Compte courant", balance="100"))
        client.accounts.append(AccountFactory.create_account(account_name="Livret A", balance="500"))
        
        return client