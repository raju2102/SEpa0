import Class
import sys
import json
import os
import re

def Flush(userMap):
    userMapToFlush = {}
    for key, value in userMap.items():
        userMapToFlush[key] = json.loads(json.dumps(value.__dict__))
    if os.path.exists('users.json'):
        os.remove('users.json')
    with open('users.json', 'w') as fp:
        fp.write(json.dumps({"users": userMapToFlush}, indent=4))

def welcomeMsg():
    print("Welcome to the App!")
    print("login: ./app 'login <username> <password>'")
    print("join: ./app 'join'")
    print("create: ./app 'create username=\"<value>\" password=\"<value>\" name=\"<value>\" status=\"<value>\"'")
    print("people: ./app 'people'")

def readData():
    f = open('users.json')
    if not os.path.exists('users.json'):
        return {}
    data = json.load(f)
    userMap = {}
    sessionMap = {}
    for key, value in data["users"].items():
        if value["SessionKey"] != "NA":
            sessionMap[value["SessionKey"]] = Class.Session(value["SessionKey"], value["Username"])
        userMap[key] = Class.User(**value)
    return userMap, sessionMap

def loginSuccessMsg(User):
    print("Welcome back to the App, {0}!".format(User.getName()))

    print(User.getStatus())

    print("edit: ./app 'session {0} edit'".format(User.getSessionkey()))
    print("update: ./app 'session {0} update (name=\"<value>\"|status=\"<value>\")+'".format(User.getSessionkey()))
    print("logout: ./app 'session {0} logout'".format(User.getSessionkey()))
    print("people: ./app '[session {0} ]people'".format(User.getSessionkey()))

def createSuccessMsg(user):
    print("[account created]")
    print("Person")
    print("------")
    print("name: {0}".format(user.getName()))
    print("username: {0}".format(user.getUsername()))
    print("status: {0}".format(user.getStatus()))
    print("updated: {0}".format(user.getUpdatedTime()))

    print("edit: ./app 'session {0} edit'".format(user.getSessionkey()))
    print("update: ./app 'session {0} update (name=\"<value>\"|status=\"<value>\")+'".format(user.getSessionkey()))
    print("delete: ./app 'session {0} delete'".format(user.getSessionkey()))
    print("logout: ./app 'session {0} logout'".format(user.getSessionkey()))
    print("people: ./app '[session {0} ]people'".format(user.getSessionkey()))
    print("home: ./app ['session {0}']".format(user.getSessionkey()))

def joinInputs():
    print("New Person")
    print("------")
    newUserData = {}
    newUserData["Username"] = input("username: ")
    newUserData["Password"] = input("password: ")
    newUserData["ConfirmPassword"] = input("confirm password: ")
    newUserData["Name"] = input("name: ")
    newUserData["Status"] = input("status: ")

    return newUserData


def createNewUser(newUserData, userMap):
    print(newUserData)
    if '"' in newUserData["Username"]:
        print("failed to create: invalid username")
        return False
    
    givenUsername = newUserData["Username"]
    newUserData["Username"] = newUserData["Username"].lower()
    if len(newUserData["Username"]) < 3:
        # print("aaaa", newUserData["Username"])
        print("failed to create: username is too short")
        return False
    
    if len(newUserData["Username"]) > 20:
        print("failed to create: username is too long")
        return False

    if '"' in newUserData["Status"]:
        print("failed to create: status contains double quote")
        return False
    
    if '"' in newUserData["Name"]:
        print("failed to create: name contains double quote")
        return False
    
    if '"' in newUserData["Password"]:
        print("failed to create: password contains double quote")
        return False

    pattern = re.compile(r'^[a-zA-Z0-9_]+$')
    if not bool(pattern.match(newUserData["Username"])):
        print("failed to create: invalid username")
        return False  
    
    if len(newUserData["Password"]) < 4:
        print(newUserData["Password"])
        print("failed to create: password is too short")
        return False
    
    if len(newUserData["Name"]) == 0:
        print("failed to create: name is too short")
        return False
    
    if len(newUserData["Name"]) > 30:
        print("failed to create: name is too long")
        return False
    
    if len(newUserData["Status"]) == 0:
        print("failed to create: status is too short")
        return False
    
    if len(newUserData["Status"]) > 100:
        print("failed to create: status is too long")
        return False
    

    for _, value in userMap.items():
        if newUserData["Username"] == value.getUsername():
            print("failed to create: {0} is already registered".format(givenUsername))
            return False
    userMap[newUserData["Username"]] = Class.User(newUserData["Username"], newUserData["Name"], newUserData["Status"], newUserData["Password"], "NA")
    userMap[newUserData["Username"]].generateSessionkey()
    userMap[newUserData["Username"]].setCurrenttime()
    createSuccessMsg(userMap[newUserData["Username"]])
    return userMap

def sessionCheck(Args, sessionMap):
    if len(Args) == 1:
        print("access denied: missing session token")
        return False
    else:
        if Args[1] in sessionMap.keys():
            return True
        else:
            print("invalid request: invalid session token")
            print("home: ./app")
    return False

def editUser(Args, sessionMap, userMap):
    print("Edit Person")
    print("------")
    print("leave blank to keep [current value]")
    newName = input("name [{0}]: ".format(userMap[sessionMap[Args[1]].getUsername()].getName()))
    updateStat = ""
    if newName != "":
        userMap[sessionMap[Args[1]].getUsername()].setName(newName)
        userMap[sessionMap[Args[1]].getUsername()].setCurrenttime()
        updateStat += "name"
    
    newStatus = input("status [{0}]: ".format(userMap[sessionMap[Args[1]].getUsername()].getStatus()))
    if newStatus != "":
        userMap[sessionMap[Args[1]].getUsername()].setStatus(newStatus)
        userMap[sessionMap[Args[1]].getUsername()].setCurrenttime()
        if updateStat != "":
            updateStat += " and "
        updateStat += "status"
    return userMap, updateStat


def personDetailsWithoutPrivilege(user):
    print("Person")
    print("------")
    print("name: {0}".format(user.getName()))
    print("username: {0}".format(user.getUsername()))
    print("status: {0}".format(user.getStatus()))
    print("updated: {0}".format(user.getUpdatedTime()))

    print("people: ./app 'people'")
    print("home: ./app")

def personDetailsWithPrivilege(user, personal, personalKey):
    print("Person")
    print("------")
    print("name: {0}".format(user.getName()))
    print("username: {0}".format(user.getUsername()))
    print("status: {0}".format(user.getStatus()))
    print("updated: {0}".format(user.getUpdatedTime()))
    if personal:
        print("edit: ./app 'session {0} edit'".format(personalKey))
        print("update: ./app 'session {0} update (name=\"<value>\"|status=\"<value>\")+'".format(personalKey))
        print("delete: ./app 'session {0} delete'".format(personalKey))
    print("logout: ./app 'session {0} logout'".format(personalKey))
    print("people: ./app '[session {0} ]people'".format(personalKey))
    print("home: ./app ['session {0}']".format(personalKey))
    
def printPeople(listOfPeopleToPrint, userMap, privileged, sessKey, sessionMap, sortMsg):
    if sortMsg != "":
        print("People {0}".format(sortMsg))
    else:
        print("People")
    print("------")
    for name in listOfPeopleToPrint:
        print("{0} @{1} (./app 'show {1}')".format(userMap[name].getName(), userMap[name].getUsername()))
        print("  {0}".format(userMap[name].getStatus()))
        print("  @ {0}".format(userMap[name].getUpdatedTime()))
        if privileged and sessionMap[sessKey].getUsername() == name:
            print("  edit: ./app 'session {0} edit'".format(sessKey))
    if len(listOfPeopleToPrint) == 0:
        print("No one is here...")
    print("find: ./app 'find <pattern>'")
    print("sort: ./app 'sort[ username|name|status|updated[ asc|desc]]'")
    if privileged:
        print("update: ./app 'session {0} update (name=\"<value>\"|status=\"<value>\")+'".format(sessKey))
        print("home: ./app ['session {0}']".format(sessKey))
    else:
        print("join: ./app 'join'")
        print("create: ./app 'create username=\"<value>\" password=\"<value>\" name=\"<value>\" status=\"<value>\"'")
        print("home: ./app")

def findMatchingUsers(userMap, key, fieldsToSearch):
    listOfPeopleToPrint = []
    funcs = []
    if fieldsToSearch == "":
        funcs = [Class.User.getUsername, Class.User.getName, Class.User.getStatus, Class.User.getUpdatedTime]
    elif fieldsToSearch == "username":
        funcs = [Class.User.getUsername]
    elif fieldsToSearch == "name":
        funcs = [Class.User.getName]
    elif fieldsToSearch == "status":
        funcs = [Class.User.getStatus]
    elif fieldsToSearch == "updated":
        funcs = [Class.User.getUpdatedTime]
    for uname, user in userMap.items():
        for func in funcs:
            if key in func(user):
                listOfPeopleToPrint.append(uname) 
    return listOfPeopleToPrint