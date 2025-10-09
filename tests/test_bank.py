import unittest
from bank.bank import Bank
from bank.client import Client
from bank.account import Account


class TestBank(unittest.TestCase):
    def setUp(self): 
        """Initialise avant chaque test"""
        self.bank = Bank(1, "Banque Populaire")
        self.client1 = Client(101, "Jean", "Dupont")
        self.client2 = Client(102, "Julien", "Duprés")

    def test_init(self) -> None:
        """Teste la création d'une banque"""
        self.assertEqual(self.bank.id, 1)
        self.assertEqual(self.bank.name, "Banque Populaire")
        self.assertEqual(self.bank.clients, [])
        self.assertEqual(self.bank.accounts, [])

    # ===== Tests de add_client =====

    def test_add_client_success(self) -> None:
        """Teste l'ajout d'un client"""
        result = self.bank.add_client(self.client1)
        self.assertTrue(result['success'])
        self.assertEqual(result['client'], self.client1)
        self.assertIn("succès", result['message'])
        self.assertEqual(len(self.bank.clients), 1)
        self.assertIn(self.client1, self.bank.clients)

    def test_add_multiple_clients(self) -> None:
        """Teste l'ajout de plusieurs clients"""
        result1 = self.bank.add_client(self.client1)
        result2 = self.bank.add_client(self.client2)
        self.assertTrue(result1['success'])
        self.assertTrue(result2['success'])
        self.assertEqual(len(self.bank.clients), 2)

    def test_add_duplicate_client(self) -> None:
        """Teste l'ajout d'un client avec le même ID (refusé)"""
        self.bank.add_client(self.client1)
        # Créer un autre client avec le même ID
        duplicate = Client(101, "Pierre", "Durand")
        result = self.bank.add_client(duplicate)
        self.assertFalse(result['success'])
        self.assertIsNone(result['client'])
        self.assertIn("existe déjà", result['message'])
        self.assertEqual(len(self.bank.clients), 1)

    # ===== Tests de get_client_by_id =====

    def test_get_client_by_id_found(self) -> None:
        """Teste la récupération d'un client par ID"""
        self.bank.add_client(self.client1)
        result = self.bank.get_client_by_id(101)
        self.assertTrue(result['success'])
        self.assertEqual(result['client'], self.client1)
        self.assertIn("trouvé", result['message'])

    def test_get_client_by_id_not_found(self) -> None:
        """Teste la récupération d'un client inexistant"""
        result = self.bank.get_client_by_id(999)
        self.assertFalse(result['success'])
        self.assertIsNone(result['client'])
        self.assertIn("introuvable", result['message'])
    
    # ===== Tests de get_all_clients =====

    def test_get_all_clients_empty(self) -> None:
        """Teste get_all_clients sans client"""
        clients = self.bank.get_all_clients()
        self.assertEqual(clients, [])
    
    def test_get_all_clients_with_clients(self) -> None:
        """Teste get_all_clients avec plusieurs clients"""
        self.bank.add_client(self.client1)
        self.bank.add_client(self.client2)
        clients = self.bank.get_all_clients()
        self.assertEqual(len(clients), 2)
        self.assertIn(self.client1, clients)
        self.assertIn(self.client2, clients)

    # ===== Tests de open_account =====
    
    def test_open_account_success(self) -> None:
        """Teste l'ouverture d'un compte"""
        self.bank.add_client(self.client1)
        result = self.bank.open_account(self.client1, "Compte Courant", "12345", 1000, 10000)
        self.assertTrue(result['success'])
        self.assertIsNotNone(result['account'])
        self.assertEqual(result['account'].account_number, "12345")
        self.assertIn("succès", result['message'])
        # Vérifier que le compte est dans la banque
        self.assertEqual(len(self.bank.accounts), 1)
        # Vérifier que le compte est dans le client
        self.assertEqual(len(self.client1.accounts), 1)
        self.assertIn(result['account'], self.client1.accounts)

    def test_open_account_client_not_registered(self) -> None:
        """Teste l'ouverture d'un compte pour un client non enregistré"""
        # Ne pas ajouter le client à la banque
        result = self.bank.open_account(self.client1, "Compte Courant", "12345")
        self.assertFalse(result['success'])
        self.assertIsNone(result['account'])
        self.assertIn("pas enregistré", result['message'])

    def test_open_account_duplicate_number(self) -> None:
        """Teste l'ouverture d'un compte avec un numéro existant"""
        self.bank.add_client(self.client1)
        self.bank.add_client(self.client2)
        self.bank.open_account(self.client1, "Compte 1", "12345")
        result = self.bank.open_account(self.client2, "Compte 2", "12345")  # Même numéro
        self.assertFalse(result['success'])
        self.assertIsNone(result['account'])
        self.assertIn("existe déjà", result['message'])

    def test_open_multiple_accounts_for_client(self) -> None:
        """Teste l'ouverture de plusieurs comptes pour un client"""
        self.bank.add_client(self.client1)
        result1 = self.bank.open_account(self.client1, "Compte Courant", "12345")
        result2 = self.bank.open_account(self.client1, "Livret A", "67890")
        self.assertTrue(result1['success'])
        self.assertTrue(result2['success'])
        self.assertEqual(len(self.client1.accounts), 2)
        self.assertEqual(len(self.bank.accounts), 2)

    # ===== Tests de get_account_by_number =====

    def test_get_account_by_number_found(self) -> None:
        """Teste la récupération d'un compte par numéro"""
        self.bank.add_client(self.client1)
        self.bank.open_account(self.client1, "Compte Courant", "12345")
        result = self.bank.get_account_by_number("12345")
        self.assertTrue(result['success'])
        self.assertIsNotNone(result['account'])
        self.assertEqual(result['account'].account_number, "12345")
    
    def test_get_account_by_number_not_found(self) -> None:
        """Teste la récupération d'un compte inexistant"""
        result = self.bank.get_account_by_number("99999")
        self.assertFalse(result['success'])
        self.assertIsNone(result['account'])
    
    # ===== Tests de delete_account_by_number =====

    def test_delete_account_by_number_success(self) -> None:
        """Teste la suppression d'un compte"""
        self.bank.add_client(self.client1)
        self.bank.open_account(self.client1, "Compte Courant", "12345")
        result = self.bank.delete_account_by_number("12345")
        self.assertTrue(result['success'])
        self.assertIn("supprimé avec succès", result['message'])
        self.assertEqual(len(self.bank.accounts), 0)
        self.assertEqual(len(self.client1.accounts), 0)
    
    def test_delete_account_by_number_not_found(self) -> None:
        """Teste la suppression d'un compte inexistant"""
        result = self.bank.delete_account_by_number("99999")
        self.assertFalse(result['success'])
        self.assertIn("introuvable", result['message'])
    
    def test_delete_one_account_keeps_others(self) -> None:
        """Teste que la suppression d'un compte n'affecte pas les autres"""
        self.bank.add_client(self.client1)
        self.bank.open_account(self.client1, "Compte 1", "11111")
        self.bank.open_account(self.client1, "Compte 2", "22222")
        result = self.bank.delete_account_by_number("11111")
        self.assertTrue(result['success'])
        self.assertEqual(len(self.bank.accounts), 1)
        self.assertEqual(len(self.client1.accounts), 1)
        self.assertEqual(self.client1.accounts[0].account_number, "22222")
    
    # ===== Tests de delete_client_by_id =====

    def test_delete_client_by_id_success(self) -> None:
        """Teste la suppression d'un client sans compte"""
        self.bank.add_client(self.client1)
        result = self.bank.delete_client_by_id(101)
        self.assertTrue(result['success'])
        self.assertIn("supprimé avec succès", result['message'])
        self.assertEqual(len(self.bank.clients), 0)
    
    def test_delete_client_by_id_not_found(self) -> None:
        """Teste la suppression d'un client inexistant"""
        result = self.bank.delete_client_by_id(999)
        self.assertFalse(result['success'])
        self.assertIn("introuvable", result['message'])
    
    def test_delete_client_with_accounts(self) -> None:
        """Teste que la suppression d'un client supprime aussi ses comptes"""
        self.bank.add_client(self.client1)
        self.bank.open_account(self.client1, "Compte 1", "11111")
        self.bank.open_account(self.client1, "Compte 2", "22222")
        result = self.bank.delete_client_by_id(101)
        self.assertTrue(result['success'])
        self.assertEqual(len(self.bank.clients), 0)
        self.assertEqual(len(self.bank.accounts), 0)
    
    def test_delete_one_client_keeps_others(self) -> None:
        """Teste que la suppression d'un client n'affecte pas les autres"""
        self.bank.add_client(self.client1)
        self.bank.add_client(self.client2)
        self.bank.open_account(self.client1, "Compte 1", "11111")
        self.bank.open_account(self.client2, "Compte 2", "22222")
        result = self.bank.delete_client_by_id(101)
        self.assertTrue(result['success'])
        self.assertEqual(len(self.bank.clients), 1)
        self.assertEqual(self.bank.clients[0], self.client2)
        # Le compte du client2 doit toujours exister
        self.assertEqual(len(self.bank.accounts), 1)
        self.assertEqual(self.bank.accounts[0].account_number, "22222")
    
    # ===== Tests de __str__ et __repr__ =====

    def test_str(self) -> None:
        """Teste __str__"""
        self.bank.add_client(self.client1)
        self.bank.open_account(self.client1, "Compte 1", "11111")
        result = str(self.bank)
        self.assertIn("Banque Populaire", result)
        self.assertIn("1", result)  # ID
        self.assertIn("Clients: 1", result)
        self.assertIn("Comptes: 1", result)
    
    def test_repr(self) -> None:
        """Teste __repr__"""
        result = repr(self.bank)
        self.assertIn("Bank", result)
        self.assertIn("1", result)
        self.assertIn("Banque Populaire", result)