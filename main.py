from config.dictConfig import logger
from bank.account import Account
from bank.client import Client
from bank.bank import Bank

def main():
    logger.debug("Message DEBUG dans le fichier")
    logger.info("Message INFO dans le fichier")
    logger.info("=== Démarrage du programme ===")

    account = Account("Livret A", "12345", balance=1000, max_balance=20000)
    client = Client("1", "Melissa", "Gilbert")
    client2 = Client("2", "Ben", "Laforge")
    bank = Bank(1, "Banqueo")

    bank.add_client(client)
    bank.add_client(client2)
    bank.open_account(client, "Livret A", "12345", 1200.50, 22950)

    client.get_account(account.account_number)
    bank.delete_account_by_id(account.account_number)
    bank.delete_client_by_id(client.id)

    logger.info("=== Fin du programme ===")


if __name__ == "__main__":
    main()
