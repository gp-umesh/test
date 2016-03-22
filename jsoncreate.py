accounts = []
def autoSave():
    with open("/home/grampower/Accounts.json", "w") as outfile:
        json.dump(accounts, outfile)
def createUser():
    global accounts
    nUsername = raw_input("Create Username")
    for item in accounts:
        if item[0] == nUsername:
            return "Already Exsists!"
            a=1
        else:
            nPassword = input("Create Password")
            entry = [nUsername, nPassword]
            accounts.append(entry)
            accounts = accounts[:500000]
            autoSave()
            a=1
a=0            
while(a==0):

    createUser()