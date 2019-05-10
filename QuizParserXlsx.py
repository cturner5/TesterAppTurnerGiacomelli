import openpyxl


class Quiz:
    def __init__(self):
        self.fileName = "" #name of file to be used
        self.questions = [] #list of questions
        self.answers = [] #list of answers, answers list corresponds with the questions in the questions list
        self.quiz = {} #dictionary made by combining questions and answers

    def parseQuestionsXlsx(self, fileName):
        location = "quizFiles\\" + fileName
        quizFile = openpyxl.load_workbook(location)
        sheet_names = quizFile.sheetnames
        sheet = quizFile[sheet_names[0]]

        tempString = ""
        for cellObj in sheet['B']:
            if cellObj.value != None and sheet['C'][cellObj.row - 1].value == None:
                tempString = tempString + str(cellObj.value) + "\n"
            elif cellObj.value != None and sheet['C'][cellObj.row - 1].value != None:
                tempString = tempString + str(cellObj.value) + " " + str(sheet['C'][cellObj.row - 1].value) + "\n"
            elif cellObj.value == None:
                self.questions.append(tempString)
                tempString = ""

        self.questions.append(tempString)

        for x in range(len(self.questions)):
            print(selfquestions[x])


#Quiz.parseQuestionsXlsx("",'textxlsx.xlsx') #for testing