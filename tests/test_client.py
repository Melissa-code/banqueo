import unittest
from bank.client import Client
from bank.account import Account 

class TestClient(unittest.TestCase): 

    def setUp(self) -> None:
        self.client = Client(1, "Magali", "Framont")
        self.account = Account("Livret B", "12354", 1432.88, 22950)
        self.client.accounts.append(self.account)

    
    def test_get_account(self) -> None: 
        result = self.client.get_account("12354")
        self.assertIsNotNone(result)
        self.assertEqual(result.account_name, "Livret B")
        self.assertEqual(result.account_number, "12354")
        self.assertEqual(result.balance, 1432.88)
        self.assertEqual(result.max_balance, 22950)


    def test_get_account_not_found(self) -> None:
        result = self.client.get_account("444444")
        self.assertIsNone(result)
    
  