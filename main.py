from account import Account 
from client import Client

def main(): 
    acc = Account("12345", balance=1000, max_balance=2000)
    client = Client("1", "Melissa", "Gilbert")

    print(client)

if __name__ == "__main__":
    main()