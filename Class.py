import string
import random
from datetime import datetime

class User:
    SessionKey = "NA"
    def __init__(self, Username, Name, Status, Password, SessionKey, UpdatedTime="NA") -> None:
        self.Username = Username
        self.Name = Name
        self.Password = Password
        self.Status = Status
        self.SessionKey = SessionKey
        self.UpdatedTime = UpdatedTime

    def getUsername(self):
        return self.Username
    
    def getUpdatedTime(self):
        return self.UpdatedTime
    
    def setCurrenttime(self):
        self.UpdatedTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def getName(self):
        return self.Name
    
    def setName(self, name):
        self.Name = name
    
    def getPassword(self):
        return self.Password
    
    def getStatus(self):
        return self.Status
    
    def setStatus(self, status):
        self.Status = status
    
    def getSessionkey(self):
        return self.SessionKey
    
    def generateSessionkey(self):
        if self.SessionKey == "NA":
            self.SessionKey = ''.join(random.choices(string.ascii_lowercase + 
                                                 string.digits + string.ascii_uppercase, k=12))
            
    def deleteSessionkey(self):
        self.SessionKey = "NA"
    
    def modifyUsername(self, uname):
        self.Username = uname

    def modifyStatus(self, status):
        self.Status = status

class Session:
    def __init__(self, SessionToken, Username) -> None:
        self.SessionToken = SessionToken
        self.Username = Username

    def getUsername(self):
        return self.Username