from account import Account 

class Client: 

    def __init__(self, id: int, firstname: str, name: str): 
        self.id: int = id
        self.firstname: str = firstname
        self.name: str = name
        self.accounts: list[Account] = [] #objects list


    def get_account(self, account_number: str) -> Account | None:
        for account in self.accounts:
            if account.account_number == account_number:
                print("compte trouvé: ", account)
                return account
        print('aucun compte trouvé.')
        return None
    

    def __str__(self) -> str: 
        if self.accounts: 
            accounts_numbers = [account.account_number for account in self.accounts]
            accounts_str = ", ".join(accounts_numbers)
        else: 
            accounts_str = "Aucun compte."
        return f"ID: {self.id}, Prénom: {self.firstname}, Nom: {self.name}, Comptes: {accounts_str}"


    def __repr__(self) -> str:
        return self.__str__()