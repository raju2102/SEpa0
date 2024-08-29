import main
import re
import Class
from unittest.mock import patch
from io import StringIO
import sys, os

def test_welcomeMsg(capfd):
    main.welcomeMsg()
    expected_output = (
        "Welcome to the App!\n"
        "login: ./app 'login <username> <password>'\n"
        "join: ./app 'join'\n"
        "create: ./app 'create username=\"<value>\" password=\"<value>\" name=\"<value>\" status=\"<value>\"'\n"
        "people: ./app 'people'\n"
    )
    capture = capfd.readouterr()
    assert capture.out == expected_output
    
def test_createSuccessMsg(capfd):
    user = Class.User("username", "Name", "stat", "pass", "jW8tkyI2Rwrv", "NA")
    main.createSuccessMsg(user)
    capture = capfd.readouterr()
    pattern = r'^'
    pattern += r'\[account created\]\n'
    pattern += r'Person\n'
    pattern += r'------\n'
    pattern += r'name: Name\n'
    pattern += r'username: username\n'
    pattern += r'status: stat\n'
    pattern += r'updated: (NA|\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\n'
    pattern += r"edit: \./app 'session [A-Za-z0-9]{12} edit'\n"
    pattern += r"update: \./app 'session [A-Za-z0-9]{12} update \(name=\"<value>\"|status=\"<value>\"\)+'\n"
    pattern += r"delete: \./app 'session [A-Za-z0-9]{12} delete'\n"
    pattern += r"logout: \./app 'session [A-Za-z0-9]{12} logout'\n"
    pattern += r"people: \./app '\[session [A-Za-z0-9]{12} \]people'\n"
    pattern += r"home: \./app \['session [A-Za-z0-9]{12}'\]\n"

    # print(capture.out)
    assert re.match(pattern, capture.out)

def test_createNewUser(capfd):
    data = [
        {
        "Username": "username",
        "Name": "name",
        "Status": "stat",
        "Password": "pass",
        },
        {
        "Username": "u",
        "Name": "name",
        "Status": "stat",
        "Password": "pass",
        },
        {
        "Username": "dummydummydummydummydummydummy",
        "Name": "name",
        "Status": "stat",
        "Password": "pass",
        },
        {
        "Username": "username",
        "Name": "name",
        "Status": "stat\"",
        "Password": "pass",
        },
        {
        "Username": "username",
        "Name": "na\"me",
        "Status": "stat",
        "Password": "pass",
        },
        {
        "Username": "username",
        "Name": "name",
        "Status": "stat",
        "Password": "p\"ass",
        },
        {
        "Username": "use@rname",
        "Name": "name",
        "Status": "stat",
        "Password": "pass",
        },
        {
        "Username": "username",
        "Name": "name",
        "Status": "stat",
        "Password": "pas",
        },
        {
        "Username": "username",
        "Name": "",
        "Status": "stat",
        "Password": "pass",
        },
        {
        "Username": "username",
        "Name": "nameinvalidnameinvalidnameinvalidnameinvalid",
        "Status": "stat",
        "Password": "pass",
        },
        {
        "Username": "username",
        "Name": "name",
        "Status": "",
        "Password": "pass",
        },
        {
        "Username": "username",
        "Name": "name",
        "Status": "statusistoolongstatusistoolongstatusistoolongstatusistoolongstatusistoolongstatusistoolongstatusistoolongstatusistoolong",
        "Password": "pass",
        },
        ]
    userMap = main.createNewUser(data[0], {})
    
    assert userMap["username"].getUsername() == "username"
    assert userMap["username"].getStatus() == "stat"
    assert userMap["username"].getName() == "name"

    _ = main.createNewUser(data[1], {})
    assert "username is too short" in capfd.readouterr().out 
    _ = main.createNewUser(data[2], {})
    assert "username is too long" in capfd.readouterr().out 
    _ = main.createNewUser(data[3], {})
    assert "contains double quote" in capfd.readouterr().out
    _ = main.createNewUser(data[4], {})
    assert "contains double quote" in capfd.readouterr().out 
    _ = main.createNewUser(data[5], {})
    assert "contains double quote" in capfd.readouterr().out
    _ = main.createNewUser(data[6], {})
    assert "invalid username" in capfd.readouterr().out
    _ = main.createNewUser(data[7], {})
    assert "password is too short" in capfd.readouterr().out
    _ = main.createNewUser(data[8], {})
    assert "name is too short" in capfd.readouterr().out
    _ = main.createNewUser(data[9], {})
    assert "name is too long" in capfd.readouterr().out
    _ = main.createNewUser(data[10], {})
    assert "status is too short" in capfd.readouterr().out
    _ = main.createNewUser(data[11], {})
    assert "status is too long" in capfd.readouterr().out
    



def test_personDetailsWithoutPrivilege(capfd):
    user = Class.User("username", "name", "stat", "pass", "NA", "NA")
    user.generateSessionkey()
    main.personDetailsWithoutPrivilege(user)
    capture = capfd.readouterr()
    pattern = r'^'
    pattern += r"Person\n"
    pattern += r"------\n"
    pattern += r"name: name\n"
    pattern += r"username: username\n"
    pattern += r"status: stat\n"
    pattern += r'updated: (NA|\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\n'
    pattern += r"people: ./app 'people'\n"
    pattern += r"home: ./app\n"

    print(capture.out)

    assert re.match(pattern, capture.out)

def test_readData():
    if os.path.exists('users.json'):
        os.remove('users.json')
    umap = main.createNewUser({
        "Username": "username",
        "Name": "name",
        "Status": "stat",
        "Password": "pass",
        }, {})
    main.Flush(umap)
    userMap, _ = main.readData()
    assert "username" in userMap.keys()
    assert userMap["username"].getName() == "name"
    assert userMap["username"].getStatus() == "stat"   

def test_loginSuccessMsg(capfd):
    user = Class.User("username", "name", "stat", "pass", "NA", "NA")
    user.generateSessionkey()
    main.loginSuccessMsg(user)
    capture = capfd.readouterr()
    pattern = r'^'
    pattern += r'Welcome back to the App, name!\n'
    pattern += r'stat\n'
    pattern += r"edit: ./app 'session [A-Za-z0-9]{12} edit'\n"
    pattern += r"update: ./app 'session [A-Za-z0-9]{12} update \(name=\"<value>\"|status=\"<value>\"\)+'\n"
    pattern += r"logout: ./app 'session [A-Za-z0-9]{12} logout'\n"
    pattern += r"people: ./app '\[session [A-Za-z0-9]{12} \]people'\n"
    print(capture.out)
    assert re.match(pattern, capture.out)

def test_joinInputs():
    inputs = [
        "testuser",    # username
        "password123", # password
        "password123", # confirm password
        "Test User",   # name
        "active"       # status
    ]
    with patch('builtins.input', side_effect=inputs):
        data = main.joinInputs()

    assert data["Username"] == inputs[0]
    assert data["Password"] == inputs[1]
    assert data["ConfirmPassword"] == inputs[2]
    assert data["Name"] == inputs[3]
    assert data["Status"] == inputs[4]

def test_findMatchingUsers():
    userMap = {
        "alice": Class.User("alice","Alice","listening to bob", "password","5JNslQYc7DDL","2024-08-28 13:10:25"),
        "bob": Class.User("bob","Bob","talking to alice", "password","flcENUAND1TS","2024-08-28 13:10:24"),
        "eve": Class.User("eve","Eve","listening to alice and bob", "password","zYjpG0Dedmk9","2024-08-28 13:10:26"),
        "dave": Class.User("dave","Dave","zzz","d6gGlcrMnocd", "password","2024-08-28 13:10:23"),
        "carol": Class.User("carol","Carol","i'm like: to where?", "password","Sdfib9wC4cHv","2024-08-28 13:10:27")
    }
    main.printPeople([], userMap, False, "NA", {}, "")
    key = "like: to"
    fieldsToSearch = "status"
    users = main.findMatchingUsers(userMap, key, fieldsToSearch)
    assert set(users) == set(["carol"])

    main.printPeople([], userMap, True, "NA", {}, "")
    key = "alice"
    fieldsToSearch = ""
    users = main.findMatchingUsers(userMap, key, fieldsToSearch)
    assert set(users) == set(['alice', 'bob', 'eve'])

    main.printPeople([], userMap, True, "NA", {}, "NA")
    key = "Caro"
    fieldsToSearch = "name"
    users = main.findMatchingUsers(userMap, key, fieldsToSearch)
    assert set(users) == set(['carol'])

    main.printPeople(["dave"], userMap, False, "NA", {}, "NA")
    key = "dave"
    fieldsToSearch = "username"
    users = main.findMatchingUsers(userMap, key, fieldsToSearch)
    assert set(users) == set(['dave'])

    key = "13:10:23"
    fieldsToSearch = "updated"
    users = main.findMatchingUsers(userMap, key, fieldsToSearch)
    assert set(users) == set(['dave'])

def test_sessionCheck():
    user = Class.User("username", "name", "stat", "pass", "NA", "NA")
    user.generateSessionkey()
    sessionMap = {
        user.getSessionkey(): Class.Session(user.getSessionkey(), user.getUsername())
    }
    assert main.sessionCheck(["session", f"{user.getSessionkey()}"], sessionMap)
    assert not main.sessionCheck(["session", f"dummy"], sessionMap)
    assert not main.sessionCheck(["session"], sessionMap)

def test_editUser():
    user = Class.User("username", "name", "stat", "pass", "NA", "NA")
    user.generateSessionkey()
    umap = {
        "username": user
    }
    sessionMap = {
        user.getSessionkey(): Class.Session(user.getSessionkey(), user.getUsername())
    }
    main.Flush(umap)

    inputs = iter(['Bob', ''])
    print(user.getStatus())
    with patch('builtins.input', side_effect=inputs):
        map, stat = main.editUser(['session', user.getSessionkey(), 'edit'], sessionMap, umap)
    assert map["username"].getName() == "Bob"
    assert map["username"].getStatus() == "stat"
    assert not ("status" in stat)
    
    inputs = iter(['', 'Inactive'])
    with patch('builtins.input', side_effect=inputs):
        map, stat = main.editUser(['session', user.getSessionkey(), 'edit'], sessionMap, umap)
    assert map["username"].getName() == "Bob"
    assert map["username"].getStatus() == "Inactive"
    assert not ("name" in stat)

    inputs = iter(['Bob', 'Inactive'])
    with patch('builtins.input', side_effect=inputs):
        map, stat = main.editUser(['session', user.getSessionkey(), 'edit'], sessionMap, umap)
    assert map["username"].getName() == "Bob"
    assert map["username"].getStatus() == "Inactive"
    assert "name and status" in stat

def test_personDetailsWithPrivilege(capfd):
    user = Class.User("username", "name", "stat", "pass", "NA", "NA")
    user.setCurrenttime()
    user.generateSessionkey()
    pattern = r'^'
    pattern += r"Person\n"
    pattern += r"------\n"
    pattern += r"name: {0}\n".format(user.getName())
    pattern += r"username: {0}\n".format(user.getUsername())
    pattern += r"status: {0}\n".format(user.getStatus())
    pattern += r"updated: {0}\n".format(user.getUpdatedTime())
    patternForPersonal = r"edit: ./app 'session {0} edit'\n".format(user.getSessionkey())
    patternForPersonal += r"update: ./app 'session {0} update \(name=\"<value>\"|status=\"<value>\"\)+'\n".format(user.getSessionkey())
    patternForPersonal += r"delete: ./app 'session {0} delete'\n".format(user.getSessionkey())
    patternForNotPersonal = r"logout: ./app 'session {0} logout'\n".format(user.getSessionkey())
    patternForNotPersonal += r"people: ./app '\[session {0} \]people'\n".format(user.getSessionkey())
    patternForNotPersonal += r"home: ./app \['session {0}'\]\n".format(user.getSessionkey())
    

    main.personDetailsWithPrivilege(user, False, user.getSessionkey())
    capture = capfd.readouterr()
    assert re.match(pattern+patternForNotPersonal, capture.out)


    main.personDetailsWithPrivilege(user, True, user.getSessionkey())
    capture = capfd.readouterr()
    assert re.match(pattern+patternForPersonal+patternForNotPersonal, capture.out)


