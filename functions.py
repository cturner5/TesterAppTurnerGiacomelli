import re
import sys
import pprint
import os
import quizParserTxt
import QuizParserXlsx
import smtplib

'''
current constraints: 
quizFile and answerFile must start with 1
hence, they must be in sync with one another, or else it doesn't fucking work :)))))))))))))
this is reasonable, as a quiz must have an answer for every question in it. else there is no point in 
giving someone a quiz if it can't be graded, is there? 
'''

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

    print(accountsFileList)

    #placing info from list into dictionary
    counter = 0
    place = 1
    for word in accountsFileList:
        if place % 3 == 0 and place != 0:
            accounts[accountsFileList[counter - 2]] = accountsFileList[counter - 1], accountsFileList[counter]
        counter += 1
        place += 1

    pprint.pprint(accounts)

    while True:
        #printing menu + asking for user input
        print("Log in or sign up:")
        print("Press '1' to log in")
        print("Press '2' to sign up")
        print("Press any other key to exit")
        try:
            select = int(input())
            if select != 1 and select != 2:
                raise ValueError
        except ValueError:
            print("Exiting...")
            break

        #if log in
        if select == 1:
            while True:
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
                        if accounts[usernameSubmit][1] != passwordSubmit:
                            raise Exception("Wrong password or username")
                    #if both username and password correct, print a welcome message and break out of loop
                    print("Welcome " + usernameSubmit + ".")
                    email = accounts[usernameSubmit][0]
                    break
                #if username and/or password is wrong, output message and loop back
                except Exception as wrong:
                    print(wrong)
            break

        #if sign up
        elif select == 2:
            print("Would you like to associate an email? ")
            yesNo = input().upper()
            if yesNo == 'YES':
                print("Enter an email: ")
                email = input()
            elif yesNo == 'NO':
                email = ""

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
            entry = [email, password]
            accounts[username] = entry
            #username and password placed into list for later placement into accounts file
            insertionList.append("\n" + username)
            insertionList.append("\n" + email)
            insertionList.append("\n" + password)
        #if user presses something other than 1 or 2, program terminates

        else:
            sys.exit()

    #place new account info into accountsFile
    accountsFile.writelines(insertionList)
    #close accountsFile
    accountsFile.close()

    return (usernameSubmit, email)
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

#printQuizMenu
def printQuizMenu():
    menuDict = {}
    counter = 1
    files = os.listdir("quizFiles")
    fileNames = [x for x in files]
    for i in fileNames:
        if i[-4:] == ".txt":
            menuDict[counter] = i
            print(str(counter) + ": " + i)
            counter += 1

    return menuDict
#printQuizMenu

#selectQuiz
def selectQuiz():
    print("Press '1' to take a quiz, press any other key to exit: ")
    if input() != '1':
        print("Goodbye.")
        sys.exit()
    print("Enter the number corresponding to the quiz you would like to take: ")
    menuSelect = printQuizMenu()
    while True:
        try:
            selection = int(input())
            if selection not in menuSelect.keys():
                raise ValueError
            break
        except ValueError:
            print("Quiz not found, please select an existing quiz: ")

    return [selection, menuSelect[selection]]
    #print menu of available quizzes
#selectQuiz

#saveScore
def saveScore(username, score):
    filename = str(username + "Stats.txt")
    scoreFile = open(filename, 'a')
    scoreFile.append(score)
    scoreFile.close()
#saveScore

#emailScore
def emailScore(score, email):
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)

    if email != None:
        message = "Subject: Your quiz score is" + str(score)
        smtpObj.login('testerappcs3030@gmail.com', 'generic1234')
        smtpObj.sendmail(email, 'testerappcs3030@gmail.com', message)
        smtpObj.quit()
#emailScore

'''
#administerQuiz
def administerQuiz(questionsOrQuestionRange, quiz):
    if questionsOrQuestionRange[1] == 0:
        #if the second element of the tuple is 0, then the quizzer gives each question sequentially 
        for question in quiz: 
            #print the question
            print(question.key())
            
    else:
        #if second element is not 0, gives questions in range specified by tuple 
#administerQuiz
'''

sessionOwner = login()
selection = selectQuiz()
username = sessionOwner[0]
email = sessionOwner[1]

if selection[1].endswith('.txt'):
    quizObj = quizParserTxt.Quiz()
elif selection[1].endswith('.xlsx'):
    quizObj = QuizParserXlsx.Quiz()

#selection[1] is the file name
questions = quizObj.parseQuestionsTxt(selection[1])
answers = quizObj.parseAnswersTxt(selection[1])
options = quizObj.questions_or_questionRange()
quiz = quizObj.parseQuizTxt()
quiz = quizObj.parseQuizTxt()
pprint.pprint(quiz)

#score = administerQuiz(options, quiz)

#for i in quiz: print(i, end='')

#for i in answers: print(i, end='')


