import Class

print("Welcome to the App!")
print("login: ./app 'login <username> <password>'")
print("join: ./app 'join'")
print("create: ./app 'create username=\"<value>\" password=\"<value>\" name=\"<value>\" status=\"<value>\"'")
print("people: ./app 'people'")

s = Class.Session("1", "2")
print(s.getName())