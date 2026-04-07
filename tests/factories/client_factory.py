from decimal import Decimal
from tests.factories.account_factory import AccountFactory
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

        return Client(client_id, firstname, lastname)
    
    
    @staticmethod
    def create_client_with_accounts():
        """Génère un client avec 2 comptes pré-remplis pour les tests"""
        client = ClientFactory.create_client()
        client.accounts.append(AccountFactory.create_account(
            account_name="Compte courant", 
            account_number="12345", 
            balance=Decimal("100.00"), 
            max_balance=Decimal("22950")
        ))
        client.accounts.append(AccountFactory.create_account(
            account_name="Livret A", 
            account_number="3333", 
            balance=Decimal("500.00"), 
            max_balance=Decimal("22950")
        ))
        
        return client