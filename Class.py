class User:
    def __init__(self, username, name, status, password) -> None:
        self.Username = username
        self.Name = name
        self.Password = password
        self.Status = status

    def getUsername(self):
        return self.Username
    
    def getName(self):
        return self.Name
    
    def getPassword(self):
        return self.Password
    
    def getStatus(self):
        return self.Status
    
    def modifyUsername(self, uname):
        self.Username = uname

    def modifyStatus(self, status):
        self.Status = status

class Session:
    def __init__(self, sessionToken, name) -> None:
        self.SessionToken = sessionToken
        self.Name = name

    def getName(self):
        return self.Name