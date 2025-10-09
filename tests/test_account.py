import unittest
from unittest.mock import patch
from bank.account import Account 

class TestAccount(unittest.TestCase): 

    def setUp(self) -> None: 
        """Initialise avant chaque test"""
        self.account = Account("Livret A", "44444", 1500.50, 22950)

    def test_init(self) -> None: 
        """Teste la création d'un compte"""
        self.assertEqual(self.account.account_name, "Livret A")
        self.assertEqual(self.account.account_number, "44444")
        self.assertEqual(self.account.balance, 1500.50)
        self.assertEqual(self.account.max_balance, 22950)
        self.assertEqual(self.account.history, [])

    # ===== Tests de deposit =====

    def test_deposit_valid(self) -> None: 
        """Teste un dépôt valide"""
        result = self.account.deposit(200) 
        self.assertTrue(result['success'])
        self.assertEqual(result['balance'], 1700.50)
        self.assertIn("succès", result['message'])
        self.assertEqual(self.account.balance, 1700.50)
        self.assertEqual(len(self.account.history), 1)
        
    def test_deposit_reaches_max(self) -> None:
        """Teste un dépôt qui atteint presque le plafond"""
        amount = 22950 - 1500.50 - 100  # = 21349.5
        result = self.account.deposit(amount)
        self.assertTrue(result['success'])
        self.assertEqual(result['balance'], 22850.0)
        self.assertLess(result['balance'], self.account.max_balance)

    def test_deposit_exceeds_max(self) -> None:
        """Teste un dépôt refusé qui dépasse le plafond"""
        initial_balance = self.account.balance
        result = self.account.deposit(90000)
        # Le dépôt est refusé le solde ne change pas
        self.assertFalse(result['success'])
        self.assertEqual(result['balance'], initial_balance)
        self.assertIn("plafond", result['message'].lower())
        self.assertEqual(self.account.balance, 1500.50)
        self.assertEqual(len(self.account.history), 0)

    def test_deposit_zero(self) -> None: 
        """Teste un dépôt de 0€"""
        result = self.account.deposit(0)
        self.assertTrue(result['success'])
        self.assertEqual(result['balance'], 1500.50)

    def test_deposit_history_structure(self) -> None:
        """Teste la structure de l'historique pour un dépôt"""
        self.account.deposit(100)
        self.assertEqual(len(self.account.history), 1)
        operation = self.account.history[0]
        # Vérifie la structure du dict
        self.assertEqual(operation['type'], 'deposit')
        self.assertEqual(operation['amount'], 100)
        self.assertEqual(operation['balance'], 1600.50)
        self.assertEqual(operation['account_name'], 'Livret A')
        self.assertIn('date', operation)
    
    # ===== Tests de withdraw =====

    def test_withdraw_valid(self) -> None: 
        """Teste un retrait valide"""
        result = self.account.withdraw(1000)
        self.assertTrue(result['success'])
        self.assertEqual(result['balance'], 500.50)
        self.assertIn("succès", result['message'])
        self.assertEqual(self.account.balance, 500.50)
        self.assertEqual(len(self.account.history), 1)
    
    def test_withdraw_exact_balance(self) -> None:
        """Teste un retrait du solde complet"""
        result = self.account.withdraw(1500.50)
        self.assertTrue(result['success'])
        self.assertEqual(result['balance'], 0)
        self.assertEqual(self.account.balance, 0)

    def test_withdraw_insufficient_funds(self) -> None:
        """Teste un retrait avec fonds insuffisants (refusé)"""
        initial_balance = self.account.balance
        result = self.account.withdraw(90000)
        # Le retrait est refusé
        self.assertFalse(result['success'])
        self.assertEqual(result['balance'], initial_balance)
        self.assertIn("insuffisants", result['message'].lower())
        self.assertEqual(self.account.balance, 1500.50)
        self.assertEqual(len(self.account.history), 0)

    def test_withdraw_negative_balance(self) -> None:
        """Teste un retrait qui rendrait le solde négatif"""
        initial_balance = self.account.balance
        result = self.account.withdraw(1600)
        # Refusé car 1500.50 - 1600 = -99.50 < 0
        self.assertFalse(result['success'])
        self.assertEqual(result['balance'], initial_balance)
        self.assertEqual(len(self.account.history), 0)

    def test_withdraw_history_structure(self) -> None:
        """Teste la structure de l'historique pour un retrait"""
        self.account.withdraw(500)
        self.assertEqual(len(self.account.history), 1)
        operation = self.account.history[0]
        # Vérifie la structure du dict
        self.assertEqual(operation['type'], 'withdraw')
        self.assertEqual(operation['amount'], 500)
        self.assertEqual(operation['balance'], 1000.50)
        self.assertEqual(operation['account_name'], 'Livret A')
        self.assertIn('date', operation)

    # ===== Tests de get_history =====

    def test_get_history_empty(self) -> None:
        """Teste get_history sur un compte sans opération"""
        history = self.account.get_history()
        self.assertEqual(history, [])
        self.assertIsInstance(history, list)
    
    def test_get_history_with_operations(self) -> None:
        """Teste get_history avec plusieurs opérations"""
        self.account.deposit(100)
        self.account.withdraw(50)
        
        history = self.account.get_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]['type'], 'deposit')
        self.assertEqual(history[1]['type'], 'withdraw')
    
    def test_get_history_returns_copy(self) -> None:
        """Teste que get_history retourne une copie (pas la liste originale)"""
        self.account.deposit(100)
        history = self.account.get_history()
        # Modifier la copie ne doit pas affecter l'original
        history.append({'fake': 'data'})
        self.assertEqual(len(self.account.get_history()), 1)
    
    # ===== Tests de multiple operations =====

    def test_multiple_operations(self) -> None:
        """Teste une séquence d'opérations"""
        result1 = self.account.deposit(500)      # 1500.50 + 500 = 2000.50
        result2 = self.account.withdraw(300)     # 2000.50 - 300 = 1700.50
        result3 = self.account.deposit(100)      # 1700.50 + 100 = 1800.50
        
        self.assertTrue(result1['success'])
        self.assertTrue(result2['success'])
        self.assertTrue(result3['success'])
        self.assertEqual(self.account.balance, 1800.50)
        self.assertEqual(len(self.account.history), 3)
    
    def test_failed_operations_no_history(self) -> None:
        """Teste que les opérations échouées n'apparaissent pas dans l'historique"""
        self.account.deposit(90000)  # Échec
        self.account.withdraw(90000)  # Échec
        
        self.assertEqual(len(self.account.history), 0)
        self.assertEqual(self.account.balance, 1500.50)
    
    # ===== Tests de __str__ et __repr__ =====

    def test_str(self) -> None:
        """Teste la représentation string"""
        result = str(self.account)
        self.assertIn("Livret A", result)
        self.assertIn("44444", result)
        self.assertIn("1500.5", result)
        self.assertIn("22950", result)
    
    def test_repr(self) -> None:
        """Teste la représentation repr"""
        result = repr(self.account)
        self.assertIn("Account", result)
        self.assertIn("Livret A", result)
        self.assertIn("44444", result)
    
    # ===== Tests de date_now =====

    def test_date_now_format(self) -> None:
        """Teste le format de la date"""
        date_str = self.account.date_now()
        # Vérifie le format basique
        self.assertIn("-", date_str)
        self.assertIn("(", date_str)
        self.assertIn(":", date_str)
        self.assertIsInstance(date_str, str)
    
    @patch('bank.account.Account.date_now')
    def test_deposit_with_mocked_date(self, mock_date) -> None:
        """Teste un dépôt avec une date mockée"""
        mock_date.return_value = "07-10-2025 (14:30)"
        self.account.deposit(100)
        
        operation = self.account.history[0]
        self.assertEqual(operation['date'], "07-10-2025 (14:30)")