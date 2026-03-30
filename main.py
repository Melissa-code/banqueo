from config.dictConfig import logger
from bank.client import Client
from bank.bank import Bank
import logging

logger = logging.getLogger(__name__)


class BanqueoApp: 
    def __init__(self): 
        # Création de Banqueo au démarrage 
        self.bank = Bank(1, "Banqueo")
        print("\n" + "="*50)
        print(f"   🏦 Bienvenue chez {self.bank.name} 🏦")
        print("="*50)


    def display_menu(self): 
        """Affiche le menu principal"""
        print("\n" + "-" * 50)
        print("MENU PRINCIPAL")
        print("-"*50)
        print("1.  Créer un nouveau client")
        print("2.  Afficher tous les clients")
        print("3.  Rechercher un client par ID")
        print("4.  Ouvrir un compte pour un client")
        print("5.  Afficher tous les comptes")
        print("6.  Effectuer un dépôt")
        print("7.  Effectuer un retrait")
        print("8.  Consulter le solde d'un compte")
        print("9.  Voir l'historique d'un compte")
        print("10. Voir tous les comptes d'un client")
        print("11. Supprimer un compte")
        print("12. Supprimer un client")
        print("0.  Quitter")
        print("-"*50)

    
    def create_client(self):
        """Crée un nouveau client"""
        print("\n--- CRÉATION DE CLIENT ---")
        
        try:
            client_id = int(input("ID du client : "))
            firstname = input("Prénom : ").strip()
            lastname = input("Nom : ").strip()
            
            if not firstname or not lastname:
                print("✗ Erreur : Le prénom et le nom ne peuvent pas être vides")
                return
            
            client = Client(client_id, firstname, lastname)
            result = self.bank.add_client(client)
            
            if result['success']:
                print(f"\n✓ {result['message']}")
            else:
                print(f"\n✗ {result['message']}")
        
        except ValueError:
            print("\n✗ Erreur : L'ID doit être un nombre entier")
    

    def display_clients(self):
        """Affiche tous les clients"""
        clients = self.bank.get_all_clients()
        
        print("\n--- LISTE DES CLIENTS ---")
        if not clients:
            print("Aucun client enregistré.")
            return
        
        for client in clients:
            print(f"  • {client}")
        print(f"\nTotal : {len(clients)} client(s)")


    def search_client(self):
        """Recherche un client par ID"""
        print("\n--- RECHERCHE DE CLIENT ---")
        try:
            client_id = int(input("ID du client à rechercher : "))
            result = self.bank.get_client_by_id(client_id)
            
            if result['success']:
                client = result['client']
                print(f"\n✓ Client trouvé :")
                print(f"  {client}")
                print(f"  Nombre de comptes : {len(client.accounts)}")
                print(f"  Solde total : {client.get_total_balance():.2f} €")
            else:
                print(f"\n✗ {result['message']}")
        
        except ValueError:
            print("\n✗ Erreur : L'ID doit être un nombre entier")


    def open_account(self):
        """Ouvre un compte pour un client"""
        print("\n--- OUVERTURE DE COMPTE ---")

        try:
            client_id = int(input("ID du client : "))
            result_client = self.bank.get_client_by_id(client_id)
            
            if not result_client['success']:
                print(f"\n✗ {result_client['message']}")
                return
            
            client = result_client['client']
            print(f"Client : {client.firstname} {client.lastname}")
            
            account_name = input("Nom du compte (ex: Compte Courant, Livret A) : ").strip()
            account_number = input("Numéro de compte : ").strip()
            initial_balance = float(input("Solde initial (défaut 0) : ") or 0)
            max_balance = float(input("Plafond (défaut 20 000 €) : ") or 20000)
            
            if not account_name or not account_number:
                print("✗ Erreur : Le nom et le numéro de compte ne peuvent pas être vides")
                return
            
            result = self.bank.open_account(client, account_name, account_number, 
                                           initial_balance, max_balance)
            
            if result['success']:
                print(f"\n✓ {result['message']}")
                print(f"  Solde initial : {initial_balance:.2f} €")
                print(f"  Plafond : {max_balance:.2f} €")
            else:
                print(f"\n✗ {result['message']}")
        
        except ValueError:
            print("\n✗ Erreur : Valeurs numériques invalides")

    
    def diplay_accounts(self):
        """Affiche tous les comptes de la banque (interface "Administrateur")"""
        accounts = self.bank.get_all_accounts()
        print("\n--- LISTE DES COMPTES ---") 

        if not accounts:
            print("Aucun compte enregistré.")
            return
        
        for account in accounts:
            print(f"  • {account}")
        print(f"\nTotal : {len(accounts)} compte(s)")

    def make_deposit(self):
        """Effectue un dépôt sur un compte"""
        print("\n--- DÉPÔT ---")

        try:
            account_number = input("Numéro de compte : ").strip()
            amount = float(input("Montant à déposer : "))
            
            if amount <= 0:
                print("✗ Erreur : Le montant doit être positif")
                return
            
            # recherche le compte
            result_search = self.bank.get_account_by_number(account_number)

            if result_search['success']:
                account_obj = result_search['account']

                result_deposit = account_obj.deposit(amount)   
            
            if result_deposit['success']:
                print(f"\n✓ {result_deposit['message']}")
            else:
                print(f"\n✗ {result_deposit['message']}")
        
        except ValueError:
            print("\n✗ Erreur : Montant invalide")

    
    def make_withdrawal(self):
        """Effectue un retrait sur un compte"""
        print("\n--- RETRAIT ---")

        try:
            account_number = input("Numéro de compte : ").strip()
            amount = float(input("Montant à retirer : "))
            
            if amount <= 0:
                print("✗ Erreur : Le montant doit être positif")
                return
            
            # recherche le compte
            result_search = self.bank.get_account_by_number(account_number)

            if result_search['success']:
                account_obj = result_search['account']

                result_withdrawal = account_obj.withdraw(amount)   
            
            if result_withdrawal['success']:
                print(f"\n✓ {result_withdrawal['message']}")
            else:
                print(f"\n✗ {result_withdrawal['message']}")
        
        except ValueError:
            print("\n✗ Erreur : Montant invalide") 

    def check_balance(self):
        """Consulte le solde d'un compte spécifique"""
        print("\n--- CONSULTATION DE SOLDE ---")

        account_number = input("Numéro de compte : ").strip()
        
        result_search = self.bank.get_account_by_number(account_number)

        if result_search['success']:
            account_obj = result_search['account']
            print(f"\n✓ Solde du compte {account_obj.account_name} N° {account_obj.account_number} : {account_obj.balance:.2f} €")
        else:
            print(f"\n✗ {result_search['message']}")


    def run(self): 
        """Lance l'application"""
        while True:
            self.display_menu()
            choice = input("\nVotre choix: ").strip()

            if choice == "1": 
                self.create_client()
            elif choice == "2":
                self.display_clients()
            elif choice == "3":
                self.search_client()
            elif choice == "4":
                self.open_account()
            elif choice == "5":
                self.diplay_accounts()
            elif choice == "6":
                self.make_deposit()
            elif choice == "7":
                self.make_withdrawal()
            elif choice == "8":
                self.check_balance()
            
         
            # Pause pour que l'utilisateur puisse lire le résultat
            input("\nAppuyez sur Entrée pour continuer...")



def main(): 
    """Point d'entrée de l'application"""
    app = BanqueoApp()
    app.run()


if __name__ == "__main__":
    main()

