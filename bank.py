from client import Client
from account import Account

class Bank: 

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.clients: list[Client] = []  
        self.accounts: list[Account] = []  

    
    def add_client(self, client:Client) -> None:
        self.clients.append(client)
        print("Clients: ", self.clients)

    
    def open_account(self, client: Client, account_name: str, account_number: str, initial_balance: float = 0, max_balance: float = 10000) -> Account:
        account = Account(account_name, account_number, initial_balance, max_balance)
        client.accounts.append(account)
        self.accounts.append(account)
        print("Compte nouvellement ouvert: ", account)

        return account


    def delete_client_by_id(self, client_id: int) -> None:
        """
        Création d"une nouvelle liste de clients: copie de ceux qui n'ont pas le même id que le client
        """
        self.clients = [clientBank for clientBank in self.clients if clientBank.id != client_id]
        print("Clients: ", self.clients)


    def delete_account_by_id(self, account_number: int) -> None: 
        self.accounts = [accountBank for accountBank in self.accounts if accountBank.account_number != account_number]
        print("Comptes: ", self.accounts)