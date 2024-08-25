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
    sessionMap = {}
    for key, value in data["users"].items():
        if value["sesskey"] != "NA":
            sessionMap[value["sesskey"]] = Class.Session(value["sesskey"], value["name"])
        userMap[key] = Class.User(**value)
    return userMap, sessionMap

def loginSuccessMsg(User):
    print("Welcome back to the App, {0}!".format(User.getName()))

    print(User.getStatus())

    print("edit: ./app 'session {0} edit'".format(User.getSessionkey()))
    print("update: ./app 'session {0} update (name=\"<value>\"|status=\"<value>\")+'".format(User.getSessionkey()))
    print("logout: ./app 'session {0} logout'".format(User.getSessionkey()))
    print("people: ./app '[session {0} ]people'".format(User.getSessionkey()))

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
            

    

if __name__ == "__main__":
    main()





# s = Class.Session("1", "2")
# print(s.getName())

