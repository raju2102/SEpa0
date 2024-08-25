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
    print(userMap)
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
    for key, value in userMap.items():
        
        if requiredKeyList["Username"] == value.getUsername():
            
            print(value.getUsername())
            print("username already exists. please try again with different username")
            return False
    userMap[requiredKeyList["Username"]] = Class.User(requiredKeyList["Username"], requiredKeyList["Name"], requiredKeyList["Status"], requiredKeyList["Password"], "NA")
    userMap[requiredKeyList["Username"]].generateSessionkey()
    createSuccessMsg(userMap[requiredKeyList["Username"]])
    return userMap


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
        
            

    

if __name__ == "__main__":
    main()






