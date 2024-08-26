import Class
import sys
import json
import os
from util import Flush, loginSuccessMsg, welcomeMsg, readData, joinInputs, createNewUser, sessionCheck, personDetailsWithoutPrivilege, personDetailsWithPrivilege


def loginFlow(Args, userMap):
    if len(Args) >= 3:
        for _, User in userMap.items():
            if User.getUsername() == Args[1]:
                if User.getPassword() == " ".join(Args[2:]):
                    User.generateSessionkey()
                    loginSuccessMsg(User)
                    return
        print("access denied: incorrect username or password")
        print("home: ./app")
        return
    if len(Args) == 2:
        print("incorrect username or password")
        print("home: ./app")
        return
    if len(Args) == 1:
        print("invalid request: missing username and password")
        print("home: ./app")

def createFlow(Args, userMap):
    requiredKeyList = { "Username": ' username=\"',
                       "Password": ' password=\"',
                        "Name": ' name=\"', 
                        "Status": ' status=\"' }
    creds = " " + " ".join(Args[1:])
    for key, value in requiredKeyList.items():
        start = creds.find(value)
        if start == -1:
            print("failed to create: missing {0}".format(key.lower()))
            return False
        end = creds.find("\"", start+len(value))
        if end == -1:
            print("invalid set of creds")
            return False
        requiredKeyList[key] = creds[start+len(value): end]
    return createNewUser(requiredKeyList, userMap)


def joinFlow(Args, userMap):
    if len(Args) > 1:
        print("invalid command. join cannot have any arguments")
        return False
    newUserData = joinInputs()
    if newUserData["Password"] != newUserData["ConfirmPassword"]:
        print("failed to join: passwords do not match")
        print("home: ./app")
        return False
    return createNewUser(newUserData, userMap)

def showFlow(Args, userMap, privilege, personal, personalKey):
    print(personal)
    if (len(Args) != 2 and not privilege) or (len(Args) != 4 and privilege):
        print("iinvalid request: missing username")
        print("home: ./app")
        return
    if (not privilege and Args[1] not in userMap.keys()) or (privilege and Args[3] not in userMap.keys()):
        print("username not found")
        print("home: ./app")
        return
    if not privilege:
        personDetailsWithoutPrivilege(userMap[Args[1]])
    else:
        personDetailsWithPrivilege(userMap[Args[3]], personal, personalKey)


def main():
    nArgs = len(sys.argv)
    if nArgs == 1 or nArgs == 2 and sys.argv[1] == 'home':
        pass
        welcomeMsg()
        return

    userMap, sessionMap = readData()

    Args = sys.argv[1].split(" ")
    if Args[0] == "login":
        loginFlow(Args, userMap)
    elif Args[0] == "create":
        userMap = createFlow(Args, userMap)
        if not userMap:
            return
        Flush(userMap)
    elif Args[0] == "join":
        userMap = joinFlow(Args, userMap)
        if not userMap:
            return
        Flush(userMap)
    elif Args[0] == "show":
        showFlow(Args, userMap, False, "NA", Args[1] if len(Args)==2 else "NA")
    elif Args[0] == "session" and len(Args) > 3:
        if not sessionCheck(Args, sessionMap):
            return
        if len(Args) == 3 and Args[2] == "home": 
            loginSuccessMsg(userMap[sessionMap[Args[1]].getUsername()])
        if Args[2] == "show": 
            showFlow(Args, userMap, True, sessionMap[Args[1]].getUsername()==Args[3], Args[1])
    elif Args[0] == "session" and len(Args) == 1:
        print("access denied: missing session token")
        
            

    

if __name__ == "__main__":
    main()






