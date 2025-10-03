from account import Account 
from client import Client
from bank import Bank

def main(): 
    account = Account("Livret A", "12345", balance=1000, max_balance=20000)
    client = Client("1", "Melissa", "Gilbert")
    client2 = Client("2", "Ben", "Laforge")
    bank = Bank(1, "Banqueo")

    bank.add_client(client)
    bank.add_client(client2)
    bank.open_account(client, account.account_name, account.account_number, 1200.50, 22950)

    bank.delete_account_by_id(account.account_number)
    bank.delete_client_by_id(client.id)


if __name__ == "__main__":
    main()