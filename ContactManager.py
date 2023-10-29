import sqlite3
from datetime import datetime

class ContactManager:
    def __init__(self):
        self.make_connection()
    
    def make_connection(self):
        connection = sqlite3.connect("SQLite/contacts.sqlite3")
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                phone_number TEXT,
                email TEXT,
                creation_date TEXT,
                last_edit_date TEXT
            )
        """)
        connection.commit()
        connection.close()

    def add_contact(self):
        print("Enter the information for the new person to add:")
        first_name = input("Name: ")
        last_name = input("Surname: ")
        phone_number = input("Phone number: ")
        email = input("E-mail: ")
        creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        last_edit_date = creation_date
        
        # SQLite veritabanı bağlantısı oluşturma
        connection = sqlite3.connect("SQLite/contacts.sqlite3")
        cursor = connection.cursor()

        # Kişi bilgilerini ekleme
        cursor.execute("INSERT INTO contacts (first_name, last_name, phone_number, email, creation_date, last_edit_date) VALUES (?, ?, ?, ?, ?, ?)",
        (first_name, last_name, phone_number, email, creation_date, last_edit_date))

        connection.commit()
        connection.close()

    def delete_contact(self):
        print("Enter the information of the person to be deleted:")
        first_name = input("Name: ")
        last_name = input("Surname: ")

        # SQLite veritabanı bağlantısı oluştur
        connection = sqlite3.connect("SQLite/contacts.sqlite3")
        cursor = connection.cursor()

        # Kişiyi veritabanından sil
        cursor.execute("DELETE FROM contacts WHERE first_name = ? AND last_name = ?", (first_name, last_name))

        # Değişiklikleri kaydet ve bağlantıyı kapat
        connection.commit()
        connection.close()

    def list_contacts(self):
        print("Choose how you want to list contacts:")
        print("1. List by name")
        print("2. List by surname")
        print("3. List by Creation Date")
        print("4. List by Last Edited Date")

        choice = input("Choose listing type: ")

        if choice == "1":
            keyword = input("Enter the word containing the first or last name: ")
            # Kişileri isme veya soyada göre arama ve listeleme işlemlerini yaz
            results = self.search_contacts_by_name(keyword)
            self.display_contacts(results)
        elif choice == "2":
            keyword = input("Enter the word containing the first or last name: ")
            # Kişileri isme veya soyada göre arama ve listeleme işlemlerini yaz
            results = self.search_contacts_by_name(keyword)
            self.display_contacts(results)
        elif choice == "3":
            # Kişileri oluşturma tarihine göre sıralama ve listeleme işlemlerini yaz
            results = self.sort_contacts_by_creation_date()
            self.display_contacts(results)
        elif choice == "4":
            # Kişileri en son düzenleme tarihine göre sıralama ve listeleme işlemlerini yaz
            results = self.sort_contacts_by_last_edit_date()
            self.display_contacts(results)
        else:
            print("Invalid choice, please try again")

    def search_contacts_by_name(self, keyword):
        results = []
        for contact in self.contacts:
            if keyword.lower() in contact["first_name"].lower() or keyword.lower() in contact["last_name"].lower():
                results.append(contact)
        return results


    def sort_contacts_by_creation_date(self):
        sorted_contacts = sorted(self.contacts, key=lambda contact: contact["creation_date"])
        return sorted_contacts

    def sort_contacts_by_last_edit_date(self):
        sorted_contacts = sorted(self.contacts, key=lambda contact: contact["last_edit_date"])
        return sorted_contacts

    def display_contacts(self, results):
        if results:
            print("Matches found:")
        for contact in results:
            print(f"Name: {contact['first_name']}, Surname: {contact['last_name']}, Telefon: {contact['phone_number']}, E-Posta: {contact['email']}")
        else:
            print("No matches found.")

    def edit_contact(self):
        print("Enter information for the person to edit:")
        first_name = input("Name: ")
        last_name = input("Surname: ")

        contact = self.find_contact_by_name(first_name, last_name)

        if contact:
            print(f"Current information about: {contact['first_name']} {contact['last_name']}")
            self.display_contact(contact)

            new_first_name = input("New name: ")
            new_last_name = input("New surname: ")
            new_phone_number = input("New phone number: ")
            new_email = input("New e-mail: ")

            contact["first_name"] = new_first_name
            contact["last_name"] = new_last_name
            contact["phone_number"] = new_phone_number
            contact["email"] = new_email

            # Son düzenleme tarihini de güncelle
            contact["last_edit_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print("The contact has been updated successfully.")
        else:
            print("Contact not found.")

    def find_contact_by_name(self, first_name, last_name):
        for contact in self.contacts:
            if contact["first_name"].lower() == first_name.lower() and contact["last_name"].lower() == last_name.lower():
                return contact
        return None

    def display_contact(self, contact):
        print("Personal information:")
        print(f"Name: {contact['first_name']}")
        print(f"Surname: {contact['last_name']}")
        print(f"Phone number: {contact['phone_number']}")
        print(f"E-mail: {contact['email']}")
        print(f"Creation date: {contact['creation_date']}")
        print(f"Last edited date: {contact['last_edit_date']}")


    def restore_contact(self):
        print("Starting the restore process from backup...")

        # SQL veritabanından yedekten geri yükleme
        if self.restore_from_sql():
            print("Successfully restored from SQL database.")

        # CSV dosyasından yedekten geri yükleme
        if self.restore_from_csv():
            print("Successfully restored from CSV database.")

        # JSON dosyasından yedekten geri yükleme
        if self.restore_from_json():
            print("Successfully restored from JSON database.")

        # İsmetify dosyasından yedekten geri yükleme
        if self.restore_from_ugurify():
            print("Successfully restored from ugurify database.")

        print("Restoration from backup completed.")

    def restore_from_sql(self):
        try:
            connection = sqlite3.connect("SQLite/contacts.sqlite3")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM contacts")
            restored_data = cursor.fetchall()
            connection.close()

            # Geri yüklenen verileri mevcut verilere ekleyin
            for data in restored_data:
                self.contacts.append({
                    "first_name": data[0],
                    "last_name": data[1],
                    "phone_number": data[2],
                    "email": data[3],
                    "creation_date": data[4],
                    "last_edit_date": data[5]
                })

            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def restore_from_csv(self):
        try:
            import csv

            with open("CSV/contacts.csv", "r") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.contacts.append({
                        "first_name": row["first_name"],
                        "last_name": row["last_name"],
                        "phone_number": row["phone_number"],
                        "email": row["email"],
                        "creation_date": row["creation_date"],
                        "last_edit_date": row["last_edit_date"]
                    })

            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def restore_from_json(self):
        try:
            import json

            with open("JSON/contacts.json", "r") as jsonfile:
                data = json.load(jsonfile)
                self.contacts = data

            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def restore_from_ugurify(self):
        try:
            with open("Ugurify/contacts.db", "r") as ugurifyfile:
                data = ugurifyfile.read()
                #kendi dosyandaki verileri kıyaslayan işlemleri yaz

            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        
contactManager = ContactManager()
contactManager.make_connection()
        