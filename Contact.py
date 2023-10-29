class Contact:
    def __init__(self, first_name, last_name, phone_number, email, creation_date, last_edit_date):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        self.creation_date = creation_date
        self.last_edit_date = last_edit_date
    
    def __str__(self):
        return f"Name: {self.first_name}, Surname: {self.last_name}, Telefon: {self.phone_number}, E-Posta: {self.email}, Creation date: {self.creation_date}, Last edited date: {self.last_edit_date}"