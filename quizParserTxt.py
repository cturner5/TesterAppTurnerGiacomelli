import re

#parse the questions, then select ask user for number/range of questions, then parse the quiz out of the questions, then parse ansers, combine into dictionary

class Quiz:
    def __init__(self):
        self.fileName = "" #name of file to be used
        self.questions = [] #list of questions
        self.answers = [] #list of answers, answers list corresponds with the questions in the questions list
        self.quiz = {} #dictionary made by combining questions and answers

    def parseQuestionsTxt(self, fileName):

        location = "quizFiles\\" + fileName
        quizFile = open(location, 'r')

        temp = quizFile.readlines()

        quizFile.close()

        samp = ""
        for i in temp:
            samp = samp + i

        #print(samp)
        questionRegex = re.compile(r'.+[\n\n]')

        self.questions = [x for x in questionRegex.findall(samp)]

        return self.questions

    def parseAnswersTxt(self, fileName):

        for i in range(4):
            fileName = fileName[:-1]

        location = "quizFiles\\quizAnswers\\" + fileName + "Answers.txt"

        answersFile = open(location, 'r')

        #this needs the selected range of questions