import string
import random

class User:
    SessionKey = "NA"
    def __init__(self, username, name, status, password, sesskey) -> None:
        self.Username = username
        self.Name = name
        self.Password = password
        self.Status = status
        self.SessionKey = sesskey

    def getUsername(self):
        return self.Username
    
    def getName(self):
        return self.Name
    
    def getPassword(self):
        return self.Password
    
    def getStatus(self):
        return self.Status
    
    def getSessionkey(self):
        return self.SessionKey
    
    def generateSessionkey(self):
        if self.SessionKey == "NA":
            self.SessionKey = ''.join(random.choices(string.ascii_lowercase + 
                                                 string.digits + string.ascii_uppercase, k=12))
    
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