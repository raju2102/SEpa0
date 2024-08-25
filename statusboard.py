import Class
import sys
import json
import os

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
    print(type(data))
    for key, value in data["users"].items():
        userMap[key] = Class.User(**value)
    return userMap

nArgs = len(sys.argv)
if nArgs == 1 or nArgs == 2 and sys.argv[1] == 'home':
    pass
    welcomeMsg()
else:
    print("invalid")

print(readData())





# s = Class.Session("1", "2")
# print(s.getName())

