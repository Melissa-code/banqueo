from decimal import Decimal
import unittest
from unittest import result
from unittest.mock import patch
from bank.account import Account
from tests.factories.account_factory import AccountFactory 

class TestAccount(unittest.TestCase): 

    def setUp(self): 
        """Initialise un compte avant chaque test"""
        self.account = AccountFactory.create_account(account_name="Livret A", account_number="444", balance='1500.50', max_balance='22950.00')

    # ================== Tests de deposit =================

    def test_deposit_valid(self) -> None: 
        """Teste un dépôt valide"""
        result = self.account.deposit(Decimal("200.00")) 
        self.assertEqual(result, Decimal("1700.50"))
        self.assertEqual(self.account.balance, Decimal("1700.50"))
        self.assertEqual(len(self.account.history), 1)
        self.assertEqual(self.account.history[0]['type'], 'dépôt')
        self.assertEqual(self.account.history[0]['amount'], Decimal("200.00"))
        self.assertEqual(self.account.history[0]['balance'], Decimal("1700.50"))
        self.assertEqual(self.account.history[0]['account_name'], 'Livret A')
        self.assertIn('date', self.account.history[0])
    
    def test_deposit_reaches_max(self) -> None:
        """Teste un dépôt qui atteint presque le plafond"""
        amount = Decimal("22950.00") - Decimal("1500.50") - Decimal("100.00")  # = 21349.5
        result = self.account.deposit(amount)
        self.assertEqual(result, Decimal("22850.00"))
        self.assertLess(result, self.account.max_balance)
        self.assertEqual(self.account.balance, Decimal("22850.00"))
        self.assertEqual(len(self.account.history), 1)

    def test_deposit_exceeds_max(self) -> None:
        """Teste un dépôt refusé qui dépasse le plafond"""
        initial_balance = self.account.balance
        with self.assertRaises(ValueError) as cm:
            self.account.deposit(Decimal("90000.00"))
        self.assertIn("plafond", str(cm.exception))
        # Le dépôt est refusé - le solde ne change pas
        self.assertEqual(self.account.balance, initial_balance)
        self.assertEqual(len(self.account.history), 0)

    def test_deposit_zero(self) -> None: 
        """Teste un dépôt de 0€"""
        result = self.account.deposit(Decimal("0.00"))
        self.assertEqual(result, Decimal("1500.50"))

    def test_deposit_history_structure(self) -> None:
        """Teste la structure de l'historique pour un dépôt"""
        self.account.deposit(Decimal("100.00"))
        self.assertEqual(len(self.account.history), 1)
        operation = self.account.history[0]
        # Vérifie la structure du dict
        self.assertEqual(operation['type'], 'dépôt')
        self.assertEqual(operation['amount'], Decimal("100.00"))
        self.assertEqual(operation['balance'], Decimal("1600.50"))
        self.assertEqual(operation['account_name'], 'Livret A')
        self.assertIn('date', operation)

    
    # =================== Tests de withdraw ===================

    def test_withdraw_valid(self) -> None: 
        """Teste un retrait valide (100€ sur un solde de 1500.50)"""
        result = self.account.withdraw(Decimal("100.00"))
        self.assertEqual(result, Decimal("1400.50"))
        self.assertEqual(self.account.balance, Decimal("1400.50"))
        self.assertEqual(len(self.account.history), 1)
    
    def test_withdraw_exact_balance(self) -> None:
        """Teste un retrait du solde complet (1500.50€ sur le compte)"""
        result = self.account.withdraw(Decimal("1500.50"))
        self.assertEqual(self.account.balance, 0)

    def test_withdraw_insufficient_funds(self) -> None:
        """Teste un retrait avec fonds insuffisants (refusé)"""
        initial_balance = self.account.balance
        with self.assertRaises(ValueError) as cm:
            self.account.withdraw(Decimal("90000.00"))
        self.assertIn("fonds insuffisants", str(cm.exception))
        # Le retrait est refusé
        self.assertEqual(self.account.balance, initial_balance)
        self.assertEqual(self.account.balance, Decimal("1500.50"))
        self.assertEqual(len(self.account.history), 0)

    def test_withdraw_negative_balance(self) -> None:
        """Teste un retrait qui rendrait le solde négatif"""
        initial_balance = self.account.balance
        with self.assertRaises(ValueError) as cm:
            self.account.withdraw(Decimal("1600.00"))
        # Refusé car 1500.50 - 1600 = -99.50 < 0
        self.assertIn("Retrait refusé : fonds insuffisants (solde: 1500.50 €)", str(cm.exception))
        self.assertEqual(self.account.balance, initial_balance)
        self.assertEqual(len(self.account.history), 0)

    def test_withdraw_history_structure(self) -> None:
        """Teste la structure de l'historique pour un retrait"""
        self.account.withdraw(Decimal("500.00"))
        self.assertEqual(len(self.account.history), 1)
        operation = self.account.history[0]
        # Vérifie la structure du dict
        self.assertEqual(operation['type'], 'retrait')
        self.assertEqual(operation['amount'], Decimal("500.00"))
        self.assertEqual(operation['balance'], Decimal("1000.50"))
        self.assertEqual(operation['account_name'], 'Livret A')
        self.assertIn('date', operation)


    # ================== Tests de get_history ======================

    def test_get_history_empty(self) -> None:
        """Teste get_history sur un compte sans opération"""
        history = self.account.get_history()
        self.assertEqual(history, [])
        self.assertIsInstance(history, list)
        self.assertEqual(len(self.account.history), 0)
    
    def test_get_history_with_operations(self) -> None:
        """Teste get_history avec plusieurs opérations"""
        self.account.deposit(Decimal("100.00"))
        self.account.withdraw(Decimal("50.00"))
        history = self.account.get_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]['type'], 'dépôt')
        self.assertEqual(history[1]['type'], 'retrait')
        self.assertEqual(len(self.account.history), 2)
    
    def test_get_history_returns_copy(self) -> None:
        """Teste que get_history retourne une copie (pas la liste originale)"""
        self.account.deposit(Decimal("100.00"))
        history = self.account.get_history()
        # Modifier la copie ne doit pas affecter l'original
        history.append({'fake': 'data'})
        self.assertEqual(len(self.account.get_history()), 1)
    

    # ================== Tests de multiple operations =====================

    def test_multiple_operations(self) -> None:
        """Teste une séquence d'opérations"""
        result1 = self.account.deposit(Decimal("500.00"))      # 1500.50 + 500 = 2000.50
        result2 = self.account.withdraw(Decimal("300.00"))     # 2000.50 - 300 = 1700.50
        result3 = self.account.deposit(Decimal("100.00"))      # 1700.50 + 100 = 1800.50
        self.assertTrue(result1, 2000.50)
        self.assertTrue(result2, 1700.50)
        self.assertTrue(result3, 1800.50)
        self.assertEqual(self.account.balance, 1800.50)
        self.assertEqual(len(self.account.history), 3)
    
    def test_failed_operations_no_history(self) -> None:
        """Teste que les opérations échouées n'apparaissent pas dans l'historique"""
        with self.assertRaises(ValueError):
            self.account.deposit(Decimal("90000.00"))  # Échec
        with self.assertRaises(ValueError):
            self.account.withdraw(Decimal("90000.00"))  # Échec
        self.assertEqual(len(self.account.history), 0)
        self.assertEqual(self.account.balance, 1500.50)
    
    
    # ============== Tests de __str__ et __repr__ ==============

    def test_str(self) -> None:
        """Teste la représentation string"""
        result = str(self.account)
        self.assertIn("Livret A", result)
        self.assertIn("1500.5", result)
        self.assertIn("22950", result)
    
    def test_repr(self) -> None:
        """Teste la représentation repr"""
        result = repr(self.account)
        self.assertIn("Account", result)
        self.assertIn("Livret A", result)
        self.assertIn("1500.5", result)
        self.assertIn("22950", result)
    

    # ================= Tests de date_now ======================

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

  