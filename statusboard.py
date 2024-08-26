import sys
from util import Flush, loginSuccessMsg, welcomeMsg, readData, sessionCheck
from flows import loginFlow, createFlow, joinFlow, showFlow, deleteFlow, editFlow, logoutFlow, peopleFlow, sortFlow, findFlow, updateFlow

def main():
    nArgs = len(sys.argv)
    if nArgs == 1 or nArgs == 2 and sys.argv[1] == 'home':
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
        showFlow(Args[:2], userMap, False, "NA", Args[1] if len(Args)==2 else "NA")
    elif Args[0] == 'people':
        peopleFlow(userMap, False, "NA", sessionMap, False)
    elif Args[0] == "session":
        if not sessionCheck(Args, sessionMap):
            return
        if len(Args) == 3 and Args[2] == "home": 
            loginSuccessMsg(userMap[sessionMap[Args[1]].getUsername()])
        elif Args[2] == "show": 
            showFlow(Args[:4], userMap, True, sessionMap[Args[1]].getUsername()==Args[3], Args[1])
        elif Args[2] == "delete":
            deleteFlow(Args[1], userMap, sessionMap)
        elif Args[2] == "edit" and len(Args) == 3:
            editFlow(Args, sessionMap, userMap)
        elif Args[2] == "logout" and len(Args) == 3:
            logoutFlow(Args, userMap, sessionMap)
        elif Args[2] == "people":
            peopleFlow(userMap, True, Args[1], sessionMap, False)
        elif Args[2] == "update":
            updateFlow(Args, userMap, sessionMap)
        elif Args[2] == "find":
            peopleFlow(userMap, True, Args[1], sessionMap, False)
        else:
            print("resource not found")
            print("home: ./app")
            return
    elif Args[0] == "delete" or Args[0] == "edit" or Args[0] == "logout":
        print("invalid request: missing session token")
        print("home: ./app")
    elif Args[0] == 'sort':
        sortFlow(Args, userMap)
    elif Args[0] == 'find':
        findFlow(Args, userMap)
    elif Args[0] == 'update':
        print("invalid request: missing session token")

    else:
        print("resource not found")
        print("home: ./app")
        
        
            

    

if __name__ == "__main__":
    main()






