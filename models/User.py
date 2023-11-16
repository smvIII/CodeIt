class User(object):
    def __init__(self, Username, Password, EmailAddress, IsAdmin):
        self.Username = Username
        self.Password = Password
        self.EmailAddress = EmailAddress
        self.IsAdmin = IsAdmin