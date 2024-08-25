import json

with open('users.json', 'w') as fp:
    fp.write(json.dumps({"users": {}}, indent=4))