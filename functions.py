import re
import sys
import pprint

#login
def login():
    #to contain user info
    accounts = {}
    #file from which user info is taken
    accountsFile = open("accounts", 'r+')
    #list into which user info from the file is placed
    accountsFileList = []
    #list to be used to place new user info into accounts
    insertionList = []

    #placing info from accounts file into list
    for line in accountsFile:
        #removing newline character, if present
        if line[-1] == "\n":
            line = line[:-1]
        accountsFileList.append(line)

    #placing info from list into dictionary
    counter = 0
    for word in accountsFileList:
        if counter % 2 == 1:
            accounts[accountsFileList[counter - 1]] = word
        counter += 1

    loggingin = True
    while loggingin == True:
        #printing menu + asking for user input
        print("Log in or sign up:")
        print("1. Log in ")
        print("2. Sign up ")
        select = int(input())

        #if log in
        if select == 1:
           done = False
           while not done:
                try:
                    #take username and password
                    print("Enter your username: ")
                    usernameSubmit = input()
                    print("Enter your password: ")
                    passwordSubmit = input()
                    #if username is not in accounts.keys(), raises an error. if the username is present, check if password is. if not, raise error
                    if usernameSubmit not in accounts.keys():
                        raise Exception("Wrong password or username. ")
                    elif usernameSubmit in accounts.keys():
                        if accounts[usernameSubmit] != passwordSubmit:
                            raise Exception("Wrong password or username")
                    #if both username and password correct, print a welcome message and break out of loop
                    print("Welcome " + usernameSubmit + ".")
                    loggingin = False
                    break
                #if username and/or password is wrong, output message and loop back
                except Exception as wrong:
                    print(wrong)

        #if sign up
        elif select == 2:
            #asks for a username, if username is already taken, reprompt
            print("Enter a username: ")
            while True:
                username = str(input())
                if username in accountsFileList:
                    print("That username is taken, choose a different one: ")
                else:
                    break
            #ask for a password
            print("Enter a password: ")
            while True:
                password = str(input())
                #password must be a "strong password"
                if isStrong(password) == False:
                    print("Weak password, a password must have more than 8 characters, one lowercase letter, one uppercase letter, and at least one digit.")
                    print("Reenter password: ")
                #if password is "strong", then user must enter their password again to confirm. if they fai lto do so, they must resubmit a password
                if isStrong(password) == True:
                    print("Confirm your password by reentering it: ")
                    passwordConfirm = str(input())
                    if password == passwordConfirm:
                        break
                    elif password != passwordConfirm:
                        print("Passwords do not match. ")
                        print("Enter a password: ")
            #new account is placed in accounts dictionary
            accounts[username] = password
            #username and password placed into list for later placement into accounts file
            insertionList.append("\n" + username)
            insertionList.append("\n" + password)
        #if user presses something other than 1 or 2, program terminates
        else:
            sys.exit()

    #place new account info into accountsFile
    accountsFile.writelines(insertionList)
    #close accountsFile
    accountsFile.close()
#login

#isStrong
def isStrong(password):
    #>= 8 characters
    #at least one uppercase, at least one lowercase
    #at least one digit

    #checking if password is atleast 8 characters long
    char = re.search('.{8}', password)
    if not char:
        return False

    #checking if password has an uppercase character
    upper = re.search('[A-Z]', password)
    if not upper:
        return False
    #checking if password has a lowercase character
    lower = re.search('[a-z]', password)
    if not lower:
        return False

    #checking if password has a digit
    digit = re.search('\d', password)
    if not digit:
        return False

    return True
#isStrong

login()