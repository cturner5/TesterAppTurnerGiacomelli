import re
import sys
import pprint
import os
import quizParserTxt
import QuizParserXlsx
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

#login
def login():
    #to contain user info
    accounts = {}
    #file from which user info is taken
    accountsFile = open("accounts.txt", 'r+')
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

    #print(accountsFileList)    #testing

    #placing info from list into dictionary
    counter = 0
    place = 1
    for word in accountsFileList:
        if place % 3 == 0 and place != 0:
            accounts[accountsFileList[counter - 2]] = accountsFileList[counter - 1], accountsFileList[counter]
        counter += 1
        place += 1

    #pprint.pprint(accounts)    #testing

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

        #exit if not 1 or 2
        else:
            sys.exit()

    #place new account info into accountsFile
    accountsFile.writelines(insertionList)
    #close accountsFile
    accountsFile.close()

    return (usernameSubmit, email)
#login

# isStrong
def isStrong(password):
    # >= 8 characters
    # at least one uppercase, at least one lowercase
    # at least one digit

    # checking if password is atleast 8 characters long
    char = re.search('.{8}', password)
    if not char:
        return False

    # checking if password has an uppercase character
    upper = re.search('[A-Z]', password)
    if not upper:
        return False
    # checking if password has a lowercase character
    lower = re.search('[a-z]', password)
    if not lower:
        return False

    # checking if password has a digit
    digit = re.search('\d', password)
    if not digit:
        return False

    return True
# isStrong

# printQuizMenu
def printQuizMenu():
    # this function prints a quiz menu. this menu is generated based on the files in the quizFiles directory
    # menu data structure
    menuDict = {}
    # counter corresponds to the key press each quizFile is to be assigned
    counter = 1
    # creting a list of files in quizFiles directory
    files = os.listdir("quizFiles")
    fileNames = [x for x in files]
    # iterating over the list of quizFiles, assigning a key press to each, then printing.
    for i in fileNames:
        if i.endswith(".txt") or i.endswith(".xlsx"):
            menuDict[counter] = i
            print(str(counter) + ": " + i)
            counter += 1

    # return the menu dictionary
    return menuDict
# printQuizMenu

# selectQuiz
def selectQuiz():
    # this function asks user if they would like to take a quiz or exit the program.
    # if they choose to take a quiz, printQuizMenu() is called and user is prompted to select the quiz they want.

    #statement allowing user
    print("Press '1' to take a quiz, press any other key to exit: ")
    if input() != '1':
        print("Goodbye.")
        sys.exit()
    print("Enter the number corresponding to the quiz you would like to take: ")
    # calling the printQuizMenu function and assigning its returned dictionary to a variable
    menuSelect = printQuizMenu()
    # selection statement to select a quiz. handles exceptions if an invalid key press is inputted
    while True:
        try:
            selection = int(input())
            if selection not in menuSelect.keys():
                raise ValueError
            break
        except ValueError:
            print("Quiz not found, please select an existing quiz: ")

    # returns a list consisting the the number corresponding to their selected quiz and the file name of the
    # selected quiz
    return [selection, menuSelect[selection]]
#selectQuiz

#saveScore
def saveScore(username, score):
    # saving a score to its respecting user's stat file in the userStats directory

    filename = str("userStats\\" + username + "Stats.txt")
    scoreFile = open(filename, 'a')
    scoreFile.write(score + '\n')
    scoreFile.close()
#saveScore

#emailScore
def emailScore(score, email, username):

    if email != None:
        # message = "Subject: Your quiz score is " + str(score)

        # placing the contents of the user's score file into a string to be placed in the body of the email
        filename = str("userStats\\" + username + "Stats.txt")
        scoreFile = open(filename, 'r')
        body = scoreFile.readlines()
        bodyMsg = ''
        for i in body:
            bodyMsg += i
        scoreFile.close()

        # making a formatted string to put date+time in subject line
        d = datetime.datetime.today()
        year = str(d.year)
        month = str(d.month)
        day = str(d.day)
        hour = str(d.hour)
        minute = str(d.minute)
        currentDateTime = month + "/" + day + "/" + year + "  " + hour + ":" + minute

        # loging information for the program's email account
        me = r"testerappcs3030@gmail.com"
        my_password = r"generic1234"
        # email address of user
        you = email

        # formatting message
        message = MIMEMultipart()
        message['From'] = me
        message['To'] = you
        message['Subject'] = username + ", your quiz scores - " + currentDateTime + ""
        message.attach(MIMEText(bodyMsg))

        # using gmail's regular server
        s = smtplib.SMTP_SSL('smtp.gmail.com')
        # s.set_debuglevel(1)   # testing
        # s.ehlo()  # testing
        s.login(me, my_password)

        # sending email
        s.sendmail(me, you, message.as_string())
        s.quit()
# emailScore

# administerQuiz
def administerQuiz(questionsOrQuestionRange, quiz):
    # gives quiz to user, question by question.
    if questionsOrQuestionRange[1] == 0:
        # if the second element of the tuple is 0, then the quizzer gives each question sequentially
        right = 0
        wrong = 0
        for i in range(questionsOrQuestionRange[0]):
            print('\n')
            quizList = quiz.keys()
            quizList = [x for x in quizList]
            print(quizList[i])
            print("Enter your answer: ")
            answer = input()
            temp = quiz.get(quizList[i])
            temp = [x for x in temp.values()]
            for j in temp:
                answers = j
            if answer.upper() in answers:
                right += 1
            elif answer.upper() not in answers:
                wrong += 1
            numQuestions = right + wrong
            score = right / numQuestions
    else:
    # if second element is not 0, gives questions in range specified by tuple
        right = 0
        wrong = 0
        for i in range(questionsOrQuestionRange[0] - 1, questionsOrQuestionRange[1]):
            print('\n')
            quizList = quiz.keys()
            quizList = [x for x in quizList]
            print(quizList[i])
            print("Enter your answer: ")
            answer = input()
            temp = quiz.get(quizList[i])
            temp = [x for x in temp.values()]
            for j in temp:
                answers = j
            if answer.upper() in answers:
                right += 1
            elif answer.upper() not in answers:
                wrong += 1
            numQuestions = right + wrong
            score = right / numQuestions
    score = str(score * 100)
    print("You got " + score + "% on this quiz.")
    return score
# administerQuiz

# making a the session owner by calling login() function
sessionOwner = login()

# main loop for program. loop belongs to session owner
while True:
    # selecting a quiz
    selection = selectQuiz()
    # placing session owner's username and email into separate variables for ease of use
    username = sessionOwner[0]
    email = sessionOwner[1]

    # #two separate statements for txt files and xlsx files. each creates a quiz from its txt or xlsx file
    # selection[1] is the file name
    if selection[1].endswith('.txt'):
        quizObj = quizParserTxt.Quiz()
        questions = quizObj.parseQuestionsTxt(selection[1])
        answers = quizObj.parseAnswersTxt(selection[1])
        options = quizObj.questions_or_questionRange()
        quiz = quizObj.parseQuizTxt()
    elif selection[1].endswith('.xlsx'):
        quizObj = QuizParserXlsx.Quiz()
        questions = quizObj.parseQuestionsXlsx(selection[1])
        answers = quizObj.parseAnswersXlsx(selection[1])
        options = quizObj.questions_or_questionRange()
        quiz = quizObj.parseQuizXlsx()

    # pprint.pprint(quiz)   # testing

    # calling administerQuiz() and placing its return value in a variable
    score = administerQuiz(options, quiz)


    print("Would you like to save this score?")
    ifSave = input()
    if ifSave.upper() == 'YES':
        saveScore(username, score)
    else:
        pass

    print("Would you like an email of your quiz statistics?")
    ifEmail = input()
    if ifEmail.upper() == 'YES':
        emailScore(score, email, username)
    else:
        pass



