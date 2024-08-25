import Class
import sys
import json
import os

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
            sessionMap[value["SessionKey"]] = Class.Session(value["SessionKey"], value["Name"])
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
    print("updated: 2024-07-19 15:34:26")

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
