import re
import pprint

# parse the questions, then select ask user for number/range of questions, then parse the quiz out of the questions,
# then parse answers, combine into dictionary ultimate purpose of this class is to create a data structure called
# "quiz" of the form {question:{number:answer}} when making the answers list, it must be a list of lists. Every list
# must contain every possible answer to the question. i.e., if a question has two possible answers, then the answers
# for that question must be a list with every possible answer. the correctness of the user's submission will be tested
# just by checking if the user's answer is in the answer list for that particular question.

class Quiz:
    def __init__(self):
        self.fileName = ""  # name of file to be used
        self.questions = []  # list of questions
        self.answers = []  # list of answers, answers list corresponds with the questions in the questions list
        self.numbers = []  # list of question numberts
        self.numbers_answers = [] # list of dictionaries, each element's key is a number and its value is the answer to its corresponding question
        self.quiz = {}  # dictionary made by combining questions and answers, and numbers

    #parseQuestionsTxt
    def parseQuestionsTxt(self, fileName):

        questionRegex = re.compile(r'\d+[.]\s.+\n', re.IGNORECASE)

        location = "quizFiles\\" + fileName
        quizFile = open(location, 'r')

        temp = quizFile.readlines()

        temp = [x.strip() for x in temp]
        temp = [x + "\n" for x in temp]

        quizFile.close()

        questions = []
        tempString = ""
        for string in temp:
            qMatch = questionRegex.search(string)
            if qMatch:
                if tempString:
                    questions.append(tempString)
                tempString = string
            elif not qMatch:
                tempString = tempString + string
        questions.append(tempString)

        self.questions = questions

        return self.questions
    #parseQuestionsTxt

    #questions_or_questionRange
    def questions_or_questionRange(self):
        # in order to ask for number/range of questions, it must first know what questions are in the quiz
        # to do this, it must find the number of the first question
        counter = 1
        numberList = []
        pprint.pprint(self.questions)
        for i in self.questions:
            numberList.append(counter)
            counter += 1
        print(numberList)
        # ^^this is the only part that is suspect, it would be BEST if it directly scans self.questions and creates the
        # numberList from the actual questions in the quiz rather than basing it on how many questions
        # are in self.questions

        # this function returns a tuple. if the user selects a number, if will output a tuple where the first element
        # is the number of questions to be randomly chosen, and the second is 0
        # if the user selects a range of questions, the first element of the tuple will be the lower bound and the
        # second element will be the upper bound

        print("Press '1' to enter a number of questions:")
        print("\t\t\t-or-")
        print("Press '2' to enter a range of questions:")
        while True:
            try:
                option = int(input())
                if option != 1 and option != 2:
                    raise ValueError
                break
            except ValueError:
                print("Invalid entry, reenter:")


        if option == 1:
            print("Enter how many questions you want on your quiz:")
            while True:
                try:
                    numbers = int(input())
                    if isinstance(numbers, int) != True or numbers > len(numberList) or numbers < 1:
                        raise ValueError
                    break
                except ValueError:
                    print("Invalid entry, reenter:")

            return (numbers, 0)

        elif option == 2:
            print("Enter the lower bound:")
            while True:
                try:
                    lower = int(input())
                    if isinstance(lower, int) != True or lower not in numberList:
                        raise ValueError
                    break
                except ValueError:
                    print("Invalid entry, reenter:")
            print("Enter the upper bound:")
            while True:
                try:
                    upper = int(input())
                    if isinstance(upper, int) != True or upper not in numberList or upper < lower:
                        raise ValueError
                    break
                except ValueError:
                    print("Invalid entry, reenter:")
            return (lower, upper)
    # questions_or_questionRange

    # parseAnswersTxt
    def parseAnswersTxt(self, fileName):

        # makes a list of dictionaries, wherein each dictionary's key is the question number, and the keys value is the
        # corresponding answer(s) this list iwll then be combined with the question list in parseQuestionsTxT() to
        # create the main dictionary structure described in at the top of this file

        for i in range(4):
            fileName = fileName[:-1]

        location = "quizFiles\\quizAnswers\\" + fileName + "Answers.txt"

        answersFile = open(location, 'r')

        temp = answersFile.readlines()

        answersFile.close()

        samp = ""
        for i in temp:
            samp = samp + i

        answersRegex = re.compile(r'[A-Za-z]', re.IGNORECASE)
        numbersRegex = re.compile(r'\d+')

        self.numbers = [x for x in numbersRegex.findall(samp)]

        temp = []
        for i in range(len(samp)):
            if samp[i] == '\n':
                self.answers.append(temp)
                temp = []
            entry = answersRegex.search(samp[i])
            if entry:
                temp.append(samp[i].upper())
        self.answers.append(temp)
        print(self.answers)
        print(self.numbers)

        for i in range(len(self.numbers)):
            self.numbers_answers.append({self.numbers[i]: self.answers[i]})

        pprint.pprint(self.numbers_answers)

        return self.numbers_answers

    def parseQuizTxt(self):
        # creates final data structure of form {question:{number:answer}}
        # needs only self.numbers_answers and self.questions

        for i in range(len(self.questions)):
            self.quiz[self.questions[i]] = self.numbers_answers[i]

        return self.quiz