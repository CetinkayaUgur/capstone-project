from ContactManager import ContactManager
from Menu import Menu

def main():
    contactManager = ContactManager()
    menu = Menu()
    menu.simple_term_menu()

if __name__ == '__main__':
    main()