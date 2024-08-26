from util import Flush, loginSuccessMsg, welcomeMsg, joinInputs, createNewUser, personDetailsWithoutPrivilege, personDetailsWithPrivilege, editUser, printPeople, findMatchingUsers
import time

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
        if not (end+1 == len(creds) or creds[end+1] == " "):
            if key == "Username":
                print("failed to create: invalid username")
            else:
                print("failed to create: {0} contains double quote".format(key.lower()))
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
        print("invalid request: missing username")
        print("home: ./app")
        return
    if (not privilege and not (Args[1] in userMap.keys() or Args[1] == "people")) or (privilege and Args[3] not in userMap.keys()):
        print("username not found")
        print("home: ./app")
        return
    if not privilege:
        if Args[1] == "people":
            listOfPeopleToPrint = sorted(userMap, key=lambda User:time.mktime(time.strptime(userMap[User].getUpdatedTime(), '%Y-%m-%d %H:%M:%S')), reverse=True)
            printPeople(listOfPeopleToPrint, userMap, False, "NA", False, "")
            return
        personDetailsWithoutPrivilege(userMap[Args[1]])
    else:
        personDetailsWithPrivilege(userMap[Args[3]], personal, personalKey)

def deleteFlow(sessionKeyToDelete, userMap, sessionMap):
    userMap.pop(sessionMap[sessionKeyToDelete].getUsername())
    Flush(userMap)
    print("[account deleted]")
    welcomeMsg()
    return

def editFlow(Args, sessionMap, userMap):
    userMap, updateStat = editUser(Args, sessionMap, userMap)
    Flush(userMap)
    print("[{0} updated]".format(updateStat))
    personDetailsWithPrivilege(userMap[sessionMap[Args[1]].getUsername()], True, Args[1])
    return

def logoutFlow(Args, userMap, sessionMap):
    userMap[sessionMap[Args[1]].getUsername()].deleteSessionkey()
    Flush(userMap)
    print("[you are now logged out]")
    welcomeMsg()

def peopleFlow(userMap, privileged, sessKey, sessionMap, fromSessFind):
    listOfPeopleToPrint = sorted(userMap, key=lambda User:time.mktime(time.strptime(userMap[User].getUpdatedTime(), '%Y-%m-%d %H:%M:%S')), reverse=True)
    printPeople(listOfPeopleToPrint, userMap, privileged, sessKey, sessionMap, "" if fromSessFind else "(find all)")

def sortFlow(Args, userMap):
    sortMsg = ""
    if len(Args) == 1 or (len(Args) == 3 and Args[1] == "updated" and Args[2] == "desc") or (len(Args) == 2 and Args[1] == "updated"):
        listOfPeopleToPrint = sorted(userMap, key=lambda User:time.mktime(time.strptime(userMap[User].getUpdatedTime(), '%Y-%m-%d %H:%M:%S')), reverse=True)
        sortMsg = "(sorted by updated, newest)"
        printPeople(listOfPeopleToPrint, userMap, False, "NA", False, sortMsg)
    if (len(Args) == 2 or (len(Args) == 3 and Args[2] == "asc")) and Args[1] in ["username", "name", "status", "updated"]:
        if Args[1] == "username":
            listOfPeopleToPrint = sorted(userMap, key=lambda User:userMap[User].getUsername())
            sortMsg = "(sorted by username, a-z)"
        elif Args[1] == "name":
            listOfPeopleToPrint = sorted(userMap, key=lambda User:userMap[User].getName())
            sortMsg = "(sorted by name, a-z)"
        elif Args[1] == "status":
             listOfPeopleToPrint = sorted(userMap, key=lambda User:userMap[User].getStatus())
             sortMsg = "(sorted by status, a-z)"
        elif Args[1] == "updated":
            listOfPeopleToPrint = sorted(userMap, key=lambda User:time.mktime(time.strptime(userMap[User].getUpdatedTime(), '%Y-%m-%d %H:%M:%S')))
            sortMsg = "(sorted by updated, oldest)"
        printPeople(listOfPeopleToPrint, userMap, False, "NA", False, sortMsg)
    if len(Args) == 3 and Args[2] == "desc":
        if Args[1] == "username":
            listOfPeopleToPrint = sorted(userMap, key=lambda User:userMap[User].getUsername(), reverse=True)
            sortMsg = "(sorted by username, z-a)"
        elif Args[1] == "name":
            listOfPeopleToPrint = sorted(userMap, key=lambda User:userMap[User].getName(), reverse=True)
            sortMsg = "(sorted by name, z-a)"
        elif Args[1] == "status":
             listOfPeopleToPrint = sorted(userMap, key=lambda User:userMap[User].getStatus(), reverse=True)
             sortMsg = "(sorted by status, z-a)"
        printPeople(listOfPeopleToPrint, userMap, False, "NA", False, sortMsg)
    else:
        print("sort field not found")

def findFlow(Args, userMap):
    if len(Args) == 1:
        printPeople(userMap.keys(), userMap, False, "NA", False, "(find all)")
    elif len(Args) == 2 and Args[1][-1] != ":":
        listOfPeopleToPrint = findMatchingUsers(userMap,  Args[1][:-1], "")
        printPeople(listOfPeopleToPrint, userMap, False, "NA", False, "(find \"{0}\" in any)".format(Args[1]))
    elif len(Args) >= 3 and Args[1][-1] == ":" and Args[1][:-1] in ["username", "name", "status", "updated"]:
        listOfPeopleToPrint = findMatchingUsers(userMap, " ".join(Args[2:]), Args[1][:-1])
        printPeople(listOfPeopleToPrint, userMap, False, "NA", False, "(find \"{0}\" in {1})".format(Args[2], Args[1][:-1]))
    else:
        listOfPeopleToPrint = findMatchingUsers(userMap, " ".join(Args[1:]), "")
        printPeople(listOfPeopleToPrint, userMap, False, "NA", False, "(find \"{0}\" in any)".format(" ".join(Args[1:])))

def updateFlow(Args, userMap, sessionMap):
    requiredKeyList = { "Name": ' name=\"', 
                        "Status": ' status=\"' }
    creds = " " + " ".join(Args[2:])
    for key, value in requiredKeyList.items():
        start = creds.find(value)
        if start == -1:
            requiredKeyList[key] = "@NA@"
            continue
        end = creds.find("\"", start+len(value))
        if end == -1:
            print("invalid set of creds")
            return False
        if not (end+1 == len(creds) or creds[end+1] == " "):    
            print("failed to update: {0} contains double quote".format(key.lower()))
            return False
        requiredKeyList[key] = creds[start+len(value): end]
    msg = ""
    if requiredKeyList["Name"] != "@NA@" and requiredKeyList["Name"] != userMap[sessionMap[Args[1]].getUsername()].getName():
        userMap[sessionMap[Args[1]].getUsername()].setName(requiredKeyList["Name"])
        msg += "name"

    if requiredKeyList["Status"] != "@NA@" and requiredKeyList["Status"] != userMap[sessionMap[Args[1]].getUsername()].getStatus():
        userMap[sessionMap[Args[1]].getUsername()].setStatus(requiredKeyList["Status"])
        if msg == "":
            msg = "status"
        else:
            msg += " and status"

    if msg == "" and (requiredKeyList["Name"] != "@NA@" and requiredKeyList["Status"] != "@NA@"):
        personDetailsWithPrivilege(userMap[sessionMap[Args[1]].getUsername()], True, Args[1])
        return

    if msg == "":
        print("failed to update: missing name and status")
        return

    if requiredKeyList["Name"] != "@NA@" and len(requiredKeyList["Name"]) > 30:
        print("failed to update: name is too long")
        return
    
    if requiredKeyList["Name"] != "@NA@" and len(requiredKeyList["Name"]) == 0:
        print("failed to update: name is too short")
        return
    
    if requiredKeyList["Status"] != "@NA@" and len(requiredKeyList["Status"]) > 100:
        print("failed to update: status is too long")
        return
    
    if requiredKeyList["Status"] != "@NA@" and len(requiredKeyList["Status"]) == 0:
        print("failed to update: status is too short")
        return

    
    Flush(userMap)
    print("[{0} updated]".format(msg))
    personDetailsWithPrivilege(userMap[sessionMap[Args[1]].getUsername()], True, Args[1])
    return