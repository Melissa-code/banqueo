import unittest
from decimal import Decimal

from bank.bank import Bank
from bank.client import Client


class TestBank(unittest.TestCase):

    def setUp(self) -> None:
        """Initialise avant chaque test"""
        self.bank = Bank(1, "Banque Populaire")
        self.client1 = Client(101, "Jean", "Dupont")
        self.client2 = Client(102, "Julien", "Duprés")

    def test_init(self) -> None:
        self.assertEqual(self.bank.id, 1)
        self.assertEqual(self.bank.name, "Banque Populaire")
        self.assertEqual(self.bank.clients, [])
        self.assertEqual(self.bank.accounts, [])

    # ======================= add_client ========================

    def test_add_client_success(self) -> None:
        result = self.bank.add_client(self.client1)
        self.assertEqual(result, self.client1)
        self.assertIn(self.client1, self.bank.clients)

    def test_add_multiple_clients(self) -> None:
        self.bank.add_client(self.client1)
        self.bank.add_client(self.client2)
        self.assertEqual(len(self.bank.clients), 2)

    def test_add_duplicate_client(self) -> None:
        self.bank.add_client(self.client1)
        duplicate = Client(101, "Pierre", "Durand")
        with self.assertRaises(ValueError) as ctx:
            self.bank.add_client(duplicate)
        self.assertIn("existe déjà", str(ctx.exception))
        self.assertEqual(len(self.bank.clients), 1)

    # ==================== get_client_by_id ======================

    def test_get_client_by_id_found(self) -> None:
        self.bank.add_client(self.client1)
        result = self.bank.get_client_by_id(101)
        self.assertEqual(result, self.client1)

    def test_get_client_by_id_not_found(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            self.bank.get_client_by_id(999)
        self.assertIn("n'existe pas", str(ctx.exception))

    # ====================== get_all_clients ======================

    def test_get_all_clients_empty(self) -> None:
        self.assertEqual(self.bank.get_all_clients(), [])

    def test_get_all_clients_with_clients(self) -> None:
        self.bank.add_client(self.client1)
        self.bank.add_client(self.client2)
        clients = self.bank.get_all_clients()
        self.assertEqual(len(clients), 2)
        self.assertIn(self.client1, clients)
        self.assertIn(self.client2, clients)

    # ======================= open_account ========================

    def test_open_account_success(self) -> None:
        self.bank.add_client(self.client1)
        account = self.bank.open_account(
            self.client1, "Compte Courant", "12345",
            Decimal("1000.00"), Decimal("10000.00")
        )
        self.assertEqual(account.account_number, "12345")
        self.assertEqual(account.balance, Decimal("1000.00"))
        self.assertEqual(len(self.bank.accounts), 1)
        self.assertEqual(len(self.client1.accounts), 1)
        self.assertIn(account, self.client1.accounts)

    def test_open_account_client_not_registered(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            self.bank.open_account(self.client1, "Compte Courant", "12345")
        self.assertIn("n'appartient pas", str(ctx.exception))
        self.assertEqual(len(self.bank.accounts), 0)
        self.assertEqual(len(self.client1.accounts), 0)

    def test_open_account_duplicate_number(self) -> None:
        self.bank.add_client(self.client1)
        self.bank.add_client(self.client2)
        self.bank.open_account(self.client1, "Compte 1", "12345")
        with self.assertRaises(ValueError) as ctx:
            self.bank.open_account(self.client2, "Compte 2", "12345")
        self.assertIn("existe déjà", str(ctx.exception))
        self.assertEqual(len(self.bank.accounts), 1)
        self.assertEqual(len(self.client2.accounts), 0)

    def test_open_multiple_accounts_for_client(self) -> None:
        self.bank.add_client(self.client1)
        self.bank.open_account(self.client1, "Compte Courant", "12345")
        self.bank.open_account(self.client1, "Livret A", "67890")
        self.assertEqual(len(self.client1.accounts), 2)
        self.assertEqual(len(self.bank.accounts), 2)

    # ================== get_account_by_number ====================

    def test_get_account_by_number_found(self) -> None:
        self.bank.add_client(self.client1)
        account = self.bank.open_account(self.client1, "Compte Courant", "12345")
        result = self.bank.get_account_by_number("12345")
        self.assertEqual(result, account)

    def test_get_account_by_number_not_found(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            self.bank.get_account_by_number("99999")
        self.assertIn("n'existe pas", str(ctx.exception))

    # =================== delete_account_by_number =================

    def test_delete_account_by_number_success(self) -> None:
        self.bank.add_client(self.client1)
        self.bank.open_account(self.client1, "Compte Courant", "12345")
        self.bank.delete_account_by_number("12345")
        self.assertEqual(len(self.bank.accounts), 0)
        self.assertEqual(len(self.client1.accounts), 0)

    def test_delete_account_by_number_not_found(self) -> None:
        with self.assertRaises(ValueError):
            self.bank.delete_account_by_number("99999")

    def test_delete_one_account_keeps_others(self) -> None:
        self.bank.add_client(self.client1)
        self.bank.open_account(self.client1, "Compte 1", "11111")
        self.bank.open_account(self.client1, "Compte 2", "22222")
        self.bank.delete_account_by_number("11111")
        self.assertEqual(len(self.bank.accounts), 1)
        self.assertEqual(len(self.client1.accounts), 1)
        self.assertEqual(self.client1.accounts[0].account_number, "22222")

    # =================== delete_client_by_id =====================

    def test_delete_client_by_id_success(self) -> None:
        self.bank.add_client(self.client1)
        self.bank.delete_client_by_id(101)
        self.assertEqual(len(self.bank.clients), 0)

    def test_delete_client_by_id_not_found(self) -> None:
        with self.assertRaises(ValueError):
            self.bank.delete_client_by_id(999)

    def test_delete_client_with_accounts(self) -> None:
        self.bank.add_client(self.client1)
        self.bank.open_account(self.client1, "Compte 1", "11111")
        self.bank.open_account(self.client1, "Compte 2", "22222")
        self.bank.delete_client_by_id(101)
        self.assertEqual(len(self.bank.clients), 0)
        self.assertEqual(len(self.bank.accounts), 0)

    def test_delete_one_client_keeps_others(self) -> None:
        self.bank.add_client(self.client1)
        self.bank.add_client(self.client2)
        self.bank.open_account(self.client1, "Compte 1", "11111")
        self.bank.open_account(self.client2, "Compte 2", "22222")
        self.bank.delete_client_by_id(101)
        self.assertEqual(len(self.bank.clients), 1)
        self.assertEqual(self.bank.clients[0], self.client2)
        self.assertEqual(len(self.bank.accounts), 1)
        self.assertEqual(self.bank.accounts[0].account_number, "22222")

    # ==================== __str__ et __repr__ ====================

    def test_str(self) -> None:
        self.bank.add_client(self.client1)
        self.bank.open_account(self.client1, "Compte 1", "11111")
        result = str(self.bank)
        self.assertIn("Banque Populaire", result)
        self.assertIn("Clients: 1", result)
        self.assertIn("Comptes: 1", result)

    def test_repr(self) -> None:
        result = repr(self.bank)
        self.assertIn("Bank", result)
        self.assertIn("1", result)
        self.assertIn("Banque Populaire", result)