from bank.bank import Bank
from tests.factories.client_factory import ClientFactory

class BankFactory:

    @staticmethod
    def create_bank(bank_id = 1, name = "Banque Route"):
        
        return Bank(bank_id, name)
    

    @staticmethod
    def create_bank_with_clients():
        """Génère une banque avec 2 clients pour les tests"""
        bank = BankFactory.create_bank()

        client1 = ClientFactory.create_client()
        client2 = ClientFactory.create_client(client_id=2, firstname="Jane", lastname="Smith")
        bank.clients.append(client1)
        bank.clients.append(client2)

        return bank


    @staticmethod
    def create_bank_with_clients_and_accounts():
        """Génère une banque avec 2 clients, chacun ayant 2 comptes pré-remplis pour les tests"""
        bank = BankFactory.create_bank()

        client1 = ClientFactory.create_client_with_accounts()
        client2 = ClientFactory.create_client_with_accounts()
        bank.clients.append(client1)
        bank.clients.append(client2)

        for client in bank.clients:
            for account in client.accounts:
                bank.accounts.append(account)
        
        return bank
