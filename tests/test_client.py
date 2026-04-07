from decimal import Decimal
import unittest
from tests.factories.account_factory import AccountFactory 
from tests.factories.client_factory import ClientFactory 


class TestClient(unittest.TestCase): 

    def setUp(self) -> None: 
        """Initialise un clientavant chaque test"""
        self.client = ClientFactory.create_client_with_accounts()
        self.client2 = ClientFactory.create_client(2, "Jean", "Dupont")

        # Pour tests spécifiques, comptes créés séparément
        # self.account = AccountFactory.create_account("Livret B", "98765", Decimal("1600.80"), Decimal("22950"))
        # self.account2 = AccountFactory.create_account("Compte courant", "4444", Decimal("22000.88"), Decimal("22950"))


    # ==================== Tests init_with_accounts ======================

    def test_init_with_accounts(self) -> None:
        """Vérifie que les comptes sont bien rattachés au client"""
        self.assertEqual(len(self.client.accounts), 2)
        self.assertEqual(self.client.accounts[0].account_number, "12345")
        self.assertEqual(self.client.accounts[0].balance, Decimal("100.00"))
        self.assertEqual(self.client.accounts[1].account_number, "3333")
        self.assertEqual(self.client.accounts[1].balance, Decimal("500.00"))


    # ======================= Tests de get_account =======================

    def test_get_account_found(self) -> None: 
        """Teste la récupération d'un compte existant (1er compte)"""
        result = self.client.get_account("12345")
        self.assertEqual(result.account_name, "Compte courant")
        self.assertEqual(result.balance, Decimal("100.00"))
        self.assertEqual(result.max_balance, Decimal("22950"))
        self.assertEqual(result.account_number, "12345")

    def test_get_account_found_second(self) -> None:
        """Teste la récupération du deuxième compte"""
        result = self.client.get_account("3333")
        self.assertEqual(result.account_name, "Livret A")
        self.assertEqual(result.account_number, "3333")
        self.assertEqual(result.balance, Decimal("500.00")) 
        self.assertEqual(result.max_balance, Decimal("22950"))

    def test_get_account_not_found(self) -> None:
        """Teste la récupération d'un compte inexistant"""
        with self.assertRaises(ValueError) as cm:
            self.client.get_account("444444")
        self.assertIn("n'existe pas", str(cm.exception))
    
    def test_get_account_empty_client(self) -> None:
        """Teste get_account sur un client sans compte"""
        with self.assertRaises(ValueError) as cm:
            empty_client = ClientFactory.create_client(4, "Marie", "Martin")
            empty_client.get_account("12345")
        self.assertIn("n'existe pas", str(cm.exception))


    # ================ Tests de get_all_accounts ======================

    def test_get_all_accounts(self) -> None:
        """Teste la récupération de tous les comptes"""
        results = self.client.get_all_accounts()
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].account_number, "12345")
        self.assertEqual(results[1].account_number, "3333")
        
    def test_get_all_accounts_empty(self) -> None:
        """Teste get_all_accounts sur un client sans compte"""
        empty_client = ClientFactory.create_client(4, "Julie", "Dubois")
        with self.assertRaises(ValueError) as cm:
            empty_client.get_all_accounts() 
            empty_client.get_account("12345")
        self.assertIn("n'existe pas", str(cm.exception))
        self.assertEqual(empty_client.get_all_accounts(), []) 

    def test_get_all_accounts_returns_copy(self) -> None:
        """Teste que get_all_accounts retourne une copie"""

        results = self.client.get_all_accounts()
        # Modifier la copie ne doit pas affecter l'original
        results.append(AccountFactory.create_account("Nouveau", "9999", 0, 1000))
        # L'original doit toujours avoir 2 comptes
        self.client.get_all_accounts()
        self.assertEqual(len(self.client.accounts), 2)


    # ======================== Tests de get_total_balance =========================

    def test_get_total_balance(self) -> None:
        """Teste le calcul du solde total (2 chiffres ap virgule: 23433.760000000002. Pas exactement 23433.76 avec Decimal)"""
        result_sum = self.client.get_total_balance()
        expected = Decimal("600.00") # Somme de deux comptes 1600.80 + 22000.88
        self.assertIsInstance(result_sum, Decimal)
        self.assertEqual(result_sum, expected)

    def test_get_total_balance_empty(self) -> None:
        """Teste le solde total d'un client sans compte"""
        empty_client = ClientFactory.create_client(4, "Julie", "Dubois")
        result_sum = empty_client.get_total_balance()
        self.assertIsInstance(result_sum, Decimal)  
        self.assertEqual(result_sum, Decimal("0.00"))   

    def test_get_total_balance_after_operations(self) -> None:
        """Teste le solde total après des opérations sur les comptes"""
        self.client.get_account("12345").deposit(Decimal("1432.88"))  # 100 + 1432.88 = 1532.88
        self.client.get_account("3333").deposit(Decimal("21500.88"))  # 500 + 21500.88 = 22000.88
        self.client.get_account("3333").withdraw(Decimal("1000"))   # 22000.88 - 1000 = 21000.88
        result_sum = self.client.get_total_balance()
        # 1532.88 + 21000.88 = 22533.76
        self.assertAlmostEqual(result_sum, Decimal("22533.76")) #AssertionError: 22533.760000000002 != 22533.76

    def test_get_total_balance_single_account(self) -> None:
        """Teste le solde total avec un seul compte"""
        single_client = ClientFactory.create_client(5, "Paul", "Durand")
        single_account = AccountFactory.create_account("Livret A", "5555", Decimal("5000.0"), Decimal("22950"))
        single_client.accounts.append(single_account)
        result_sum = single_client.get_total_balance()
        self.assertEqual(result_sum, Decimal("5000.0"))

    # ==================== Tests de __str__ et __repr__ ====================

    def test_str(self) -> None:
        """Teste la représentation string"""
        result = str(self.client)  
        self.assertIn("John", result)
        self.assertIn("Doe", result)
        self.assertIn("12345", result) 
        self.assertIn("3333", result)  
    
    def test_str_without_accounts(self) -> None:
        """Teste __str__ pour un client sans compte"""
        empty_client = ClientFactory.create_client(3, "Marie", "Martin")
        result = str(empty_client)
        self.assertIn("Marie", result)
        self.assertIn("Martin", result)
        self.assertIn("Aucun compte", result)
    
    def test_repr(self) -> None:
        """Teste la représentation repr"""
        result = repr(self.client)
        self.assertIn("Client", result)
        self.assertIn("1", result)
        self.assertIn("John", result)
        self.assertIn("Doe", result)
        