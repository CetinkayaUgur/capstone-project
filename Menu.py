from ContactManager import ContactManager
from simple_term_menu import TerminalMenu

class Menu:
    contactManager = ContactManager()

    def __init__(self):
        # self.menu_items = ["Add contact", "Delete contact", "Edit contact", "List contacts",  "Restore", "exit"]
        # self.menu = TerminalMenu(self.menu_items, title="Choose an option")

        self.contacts = []

    def simple_term_menu(self):
        # Simple term menu işlemlerini buraya yap
        menu_items = ["1. Add contact", "2. Edit contact", "3. Delete contact", "4. List contacts", "5. Restore contact", "6. Exit"]
        menu = TerminalMenu(menu_items)
        menu_entry_index = menu.show()
        if menu_entry_index == 0:
            ContactManager.add_contact(self)
        elif menu_entry_index == 1:
            ContactManager.edit_contact(self)
        elif menu_entry_index == 2:
            ContactManager.delete_contact(self)
        elif menu_entry_index == 3:
            ContactManager.list_contacts(self)
        elif menu_entry_index == 4:
            ContactManager.restore_contact(self)
        elif menu_entry_index == 5:
            print("Exitting...")


if __name__ == "__main__":
    contact_manager = Menu()
    contact_manager.run()
