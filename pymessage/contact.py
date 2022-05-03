class Contact:
    def __init__(self):
        self.name = ''
        self.phone_number = None

    def __str__(self):
        return 'Name: {:20} Phone:{:20}'.format(self.name, self.phone_number)
