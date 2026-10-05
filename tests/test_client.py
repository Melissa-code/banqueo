import unittest
from decimal import Decimal

from bank.account import Account
from bank.client import Client


class TestClient(unittest.TestCase): 

    def setUp(self) -> None:
        """Initialise avant chaque test"""
        self.client = Client(1, "Magali", "Framont")
        self.account = Account(
            "Livret B", "12345", 
            Decimal("1432.88"), 
            Decimal("22950.00")
        )
        self.account2 = Account(
            "Compte courant", 
            "3333", Decimal("22000.88"), 
            Decimal("22950.00")
        )
        self.client.accounts.append(self.account)
        self.client.accounts.append(self.account2)

    def test_init(self) -> None: 
        """Teste la création d'un client"""
        new_client = Client(2, "Jean", "Dupont")
        self.assertEqual(new_client.firstname, "Jean")
        self.assertEqual(new_client.lastname, "Dupont")
        self.assertEqual(new_client.accounts, []) 
        self.assertIsInstance(new_client.accounts, list)

    def test_init_with_accounts(self) -> None:
        """Teste qu'un client peut avoir des comptes après initialisation"""
        # self.client a déjà 2 comptes ajoutés dans setUp
        self.assertEqual(len(self.client.accounts), 2)
        self.assertIn(self.account, self.client.accounts)
        self.assertIn(self.account2, self.client.accounts)

    # ===== Tests de get_account =====

    def test_get_account_found(self) -> None:
        result = self.client.get_account("12345")
        self.assertEqual(result, self.account)

    def test_get_account_found_second(self) -> None:
        result = self.client.get_account("3333")
        self.assertEqual(result, self.account2)
        self.assertEqual(result.account_name, "Compte courant")

    def test_get_account_not_found(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            self.client.get_account("444444")
        self.assertIn("444444", str(ctx.exception))

    def test_get_account_empty_client(self) -> None:
        empty_client = Client(4, "Marie", "Martin")
        with self.assertRaises(ValueError):
            empty_client.get_account("7890")
        
    # ===== Tests de get_all_accounts =====

    def test_get_all_accounts(self) -> None:
        """Teste la récupération de tous les comptes"""
        results = self.client.get_all_accounts()
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 2)
        self.assertIn(self.account, results)
        self.assertIn(self.account2, results)

    def test_get_all_accounts_empty(self) -> None:
        """Teste get_all_accounts sur un client sans compte"""
        empty_client = Client(3, "Marie", "Martin")
        results = empty_client.get_all_accounts()
        self.assertEqual(results, [])
        self.assertEqual(len(results), 0)
    
    def test_get_all_accounts_returns_copy(self) -> None:
        """Teste que get_all_accounts retourne une copie"""
        results = self.client.get_all_accounts()
        # Modifier la copie ne doit pas affecter l'original
        results.append(Account("Nouveau", "9999", 0, 1000))
        # L'original doit toujours avoir 2 comptes
        self.assertEqual(len(self.client.accounts), 2)
        self.assertEqual(len(self.client.get_all_accounts()), 2)

    # ===== Tests de get_total_balance =====

    def test_get_total_balance(self) -> None:
        result_sum = self.client.get_total_balance()
        self.assertEqual(result_sum, Decimal("23433.76"))
        self.assertIsInstance(result_sum, Decimal)

    def test_get_total_balance_empty(self) -> None:
        """Teste le solde total d'un client sans compte"""
        empty_client = Client(3, "Marie", "Martin")
        result_sum = empty_client.get_total_balance()
        self.assertEqual(result_sum, 0)

    def test_get_total_balance_after_operations(self) -> None:
        """Teste le solde total après des opérations sur les comptes"""
        self.account.deposit(Decimal("100.00"))      # 1432.88 + 100 = 1532.88
        self.account2.withdraw(Decimal("1000.00"))   # 22000.88 - 1000 = 21000.88
        result_sum = self.client.get_total_balance()
        # 1532.88 + 21000.88 = 22533.76
        self.assertAlmostEqual(result_sum, Decimal("22533.76"), places=2) #AssertionError: 22533.760000000002 != 22533.76

    def test_get_total_balance_single_account(self) -> None:
        """Teste le solde total avec un seul compte"""
        single_client = Client(4, "Paul", "Durand")
        single_account = Account("Livret A", "5555", Decimal("5000.00"), Decimal("22950.00"))
        single_client.accounts.append(single_account)
        result_sum = single_client.get_total_balance()
        self.assertEqual(result_sum, Decimal("5000.00"))

    # ===== Tests de __str__ et __repr__ =====

    def test_str(self) -> None:
        """Teste la représentation string"""
        result = str(self.client)  
        self.assertIn("Magali", result)
        self.assertIn("Framont", result)
        self.assertIn("12345", result) 
        self.assertIn("3333", result)  
    
    def test_str_without_accounts(self) -> None:
        """Teste __str__ pour un client sans compte"""
        empty_client = Client(3, "Marie", "Martin")
        result = str(empty_client)
        self.assertIn("Marie", result)
        self.assertIn("Martin", result)
        self.assertIn("Aucun compte", result)
    
    def test_repr(self) -> None:
        """Teste la représentation repr"""
        result = repr(self.client)
        self.assertIn("Client", result)
        self.assertIn("1", result)
        self.assertIn("Magali", result)
        self.assertIn("Framont", result)
        