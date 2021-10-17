import getpass
import cordra
from alive_progress import alive_bar

local = input("Local?(y/n) ")

if local == 'y':
    host = 'https://localhost:8443'
    username = 'admin'
    password = getpass.getpass()
    token = cordra.Token.create(host, username, password, verify = False)
else:
    host = input("Cordra's host: ")
    username = input("Username: ")
    password = getpass.getpass()
    token = cordra.Token.create(host, username, password, verify = False)


r = cordra.CordraObject.find(host, '/CamiloExplore:1', ids = True, token = token, verify = False, full = True)
ids = r["results"]
with alive_bar(len(ids), title = "Deleting objects", spinner = "arrow", bar ="classic") as bar:
    for x in ids:
        cordra.CordraObject.delete(host, x, token = token, verify = False)
        bar()
