from decimal import Decimal
from config.dictConfig import logger
from bank.client import Client
from bank.bank import Bank
import logging

logger = logging.getLogger(__name__)


class BanqueoApp: 

    def __init__(self): 
        """Création de Banqueo au démarrage de l'application"""
        self.bank = Bank(1, "Banqueo")
        print("\n" + "="*50)
        print(f"   🏦 Bienvenue chez {self.bank.name} 🏦")
        print("="*50)
        self.is_running = True

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
            self.bank.add_client(client)
            print(f"\n✓ Client {firstname} {lastname} créé avec succès !")
        
        except ValueError as e:
            print(f"\n✗ Erreur : {e}")
    

    def display_clients(self):
        """Affiche tous les clients"""
        clients = self.bank.get_all_clients()
        print("\n--- LISTE DES CLIENTS ---")

        try: 
            if not clients:
                print("Aucun client enregistré.")
                return
            
            for client in clients:
                print(f"  • {client}")
            print(f"\nTotal : {len(clients)} client(s)")

        except Exception as e:
            print(f"\n✗ Erreur : {e}")


    def search_client(self):
        """Recherche un client par ID"""
        print("\n--- RECHERCHE DE CLIENT ---")

        try:
            client_id = int(input("ID du client à rechercher : "))
            client = self.bank.get_client_by_id(client_id)
            print(f"\n✓ Client trouvé :")
            print(f"  {client}")
            print(f"  Nombre de comptes : {len(client.accounts)}")
            print(f"  Solde total : {client.get_total_balance()} €")
            
        except ValueError as e:
            print(f"\n✗ Erreur : {e}")


    def open_account(self):
        """Ouvre un compte pour un client"""
        print("\n--- OUVERTURE DE COMPTE ---")

        try:
            client_id = int(input("ID du client : "))
            client = self.bank.get_client_by_id(client_id)
            print(f"Client : {client.firstname} {client.lastname}")
            
            account_name = input("Nom du compte (ex: Compte Courant, Livret A) : ").strip()
            account_number = input("Numéro de compte : ").strip()
            initial_balance = Decimal(input("Solde initial (défaut 0) : ") or "0")
            max_balance = Decimal(input("Plafond (défaut 20 000 €) : ") or "20000")
            
            if not account_name or not account_number:
                print("✗ Erreur : Le nom et le numéro de compte ne peuvent pas être vides")
                return
            
            self.bank.open_account(client, account_name, account_number, 
                                        initial_balance, max_balance)
        
            print(f"\n✓ Compte {account_name} créé avec succès !")
            print(f"  Solde initial : {initial_balance:.2f} €")
            print(f"  Plafond : {max_balance:.2f} €")
          
        except ValueError as e:
            print(f"\n✗ Erreur : {e}")

    
    def display_accounts(self):
        """Affiche tous les comptes de la banque (interface Administrateur)"""
        accounts = self.bank.get_all_accounts()
        print("\n--- LISTE DES COMPTES ---") 

        try: 
            if not accounts:
                print("Aucun compte enregistré.")
                return
            
            for account in accounts:
                print(f"  • {account}")
            print(f"\nTotal : {len(accounts)} compte(s)")

        except Exception as e:
            print(f"\n✗ Erreur : {e}") 


    def make_deposit(self):
        """Effectue un dépôt sur un compte"""
        print("\n--- DÉPÔT ---")

        try:
            account_number = input("Numéro de compte : ").strip()
            amount = Decimal(input("Montant à déposer : "))
            
            if amount <= 0:
                print("✗ Erreur : Le montant doit être positif")
                return
            
            # recherche le compte
            account_obj = self.bank.get_account_by_number(account_number)
            new_balance = account_obj.deposit(amount) 
            print(f"\n✓ Dépôt effectué avec succès. Nouveau solde : {new_balance} €")

        except ValueError as e :
            print(f"\n✗ Erreur : {e}")

    
    def make_withdrawal(self):
        """Effectue un retrait sur un compte"""
        print("\n--- RETRAIT ---")

        try:
            account_number = input("Numéro de compte : ").strip()
            amount = Decimal(input("Montant à retirer : "))
            
            if amount <= 0:
                print("✗ Erreur : Le montant doit être positif")
                return
            
            # recherche le compte
            account_obj = self.bank.get_account_by_number(account_number)
            new_balance = account_obj.withdraw(amount)   
            print(f"\n✓ Retrait effectué avec succès. Nouveau solde : {new_balance} €")
         
        except ValueError:
            print("\n✗ Erreur : Montant invalide") 


    def check_balance(self):
        """Consulte le solde d'un compte spécifique"""
        print("\n--- CONSULTATION DE SOLDE ---")

        try: 
            account_number = input("Numéro de compte : ").strip()
            account_obj = self.bank.get_account_by_number(account_number)
            print(f"\n✓ Solde du compte {account_obj.account_name} N° {account_obj.account_number} : {account_obj.balance:.2f} €")

        except ValueError as e:
            print(f"\n✗ Erreur : {e}")


    def display_account_history(self):
        """Affiche l'historique des opérations d'un compte"""
        print("\n--- HISTORIQUE DE COMPTE ---")

        try:         
            account_number = input("Numéro de compte : ").strip()
            account_obj = self.bank.get_account_by_number(account_number)
            history = account_obj.get_history()

            if not history:
                print(f"Aucune opération enregistrée pour le compte {account_obj.account_name} N° {account_obj.account_number}.")
                return
            
            print(f"\n✓ Historique du compte {account_obj.account_name} N° {account_obj.account_number} :")
            for operation in history:
                print(f"  • [{operation['date']}] {operation['type'].capitalize()} de {operation['amount']:.2f} € (solde après opération: {operation['balance']:.2f} €)")

        except ValueError as e:
            print(f"\n✗ Erreur : {e}")


    def display_client_dashboard(self):
        """Affiche tous les comptes et le solde total d'un client"""
        print("\n--- TABLEAU DE BORD CLIENT ---")

        try:
            client_id = int(input("ID du client : "))
            client = self.bank.get_client_by_id(client_id)
            accounts = client.get_all_accounts()
            total_balance = client.get_total_balance()

            print(f"\n✓ Tableau de bord pour {client.firstname} {client.lastname} (ID: {client.id})")
            print(f"  Nombre de comptes : {len(accounts)}")
            print(f"  Solde total : {total_balance} €")
            print("  Comptes :")
            for account in accounts:
                print(f"    - {account.account_name} N° {account.account_number} (solde: {account.balance} €)")
        
        except ValueError as e: 
            print(f"\n✗ Erreur : {e}")      
            
    
    def delete_account(self):
        """ Supprime un compte"""
        print("\n--- SUPPRESSION DE COMPTE ---")

        try:
            account_number = input("Numéro de compte à supprimer : ").strip()
            self.bank.delete_account_by_number(account_number)
            print(f"\n✓ Compte n° {account_number} supprimé avec succès !")
        
        except ValueError as e:
            print(f"\n✗ Erreur : {e}")
        

    def delete_client(self):
        """Supprime un client et tous ses comptes"""
        print("\n--- SUPPRESSION DE CLIENT ---")

        try:
            client_id = int(input("ID du client à supprimer : "))
            self.bank.delete_client_by_id(client_id)
            print(f"\n✓ Client ID : {client_id} supprimé avec succès !")
        
        except ValueError as e: 
            print(f"\n✗ Erreur : {e}")


    def exit_app(self):
        """Quitte l'application"""  

        print("\nSauvegarde des données en cours...")
        print("\nMerci d'avoir utilisé Banqueo. À bientôt ! 👋")
        self.is_running = False


    def run(self): 
        """Lance l'application"""

        while self.is_running:
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
                self.display_accounts()
            elif choice == "6":
                self.make_deposit()
            elif choice == "7":
                self.make_withdrawal()
            elif choice == "8":
                self.check_balance()
            elif choice == "9":
                self.display_account_history()
            elif choice == "10":
                self.display_client_dashboard()
            elif choice == "11":
                self.delete_account()
            elif choice == "12":
                self.delete_client()
            elif choice == "0":
                self.exit_app()
            else:
                print("✗ Choix invalide. Veuillez choisir entre 0 et 12.")
            
            if self.is_running: 
                # Pause pour que l'utilisateur puisse lire le résultat
                input("\nAppuyez sur Entrée pour continuer...")


def main(): 
    """Point d'entrée de l'application"""
    app = BanqueoApp()
    app.run()


if __name__ == "__main__":
    main()

