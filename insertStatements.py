from numpy import nan, short
import requests
import pandas as pd
import random

mapping = []

def cleanElement(el):
    try:
        return str(int(el))
    except:
        return str(el)

url = "https://raw.githubusercontent.com/IshaanKarvir/CSC366-Team-DropTables-Lab5/main/data/Data-v03.xlsx%20-%20Work%20Profile-copy-values.csv"
df = pd.read_csv(url)
mapping = list(df.columns)[1:]
print("mapping", mapping)


def getSurveyInsert(record):
    surveyId = record[0]
    name = str(record[1])
    shortName = str(record[2])
    desc = str(record[3])
    values = f"{surveyId},'{name}','{shortName}','{desc}'"
    insertStatement = f"INSERT INTO Surveys (SurveyID, ShortName, Name, Description) VALUES ({values});"
    return insertStatement

def getUserInsert(record):
    id = record[0]
    name = record[1]
    email = record[2]
    num = random.randint(0,1)
    role = 'user' if num else 'admin'
    values = f"{id},'{name}','{email}','{role}'"
    insertStatement = f"INSERT INTO Users (AccountID, Name, Email, Role) VALUES ({values});"
    return insertStatement

def getResponseOptionsInsert(record):
    id = record[0]
    pos = record[1]
    resVal = record[2]
    resPrompt = record[3]
    comment = 'null' if record[4] == "nan" else record[4]
    values = f"{id},{pos},{resVal},'{resPrompt}','{comment}'"
    insertStatement = f"INSERT INTO ResponseOptions (SurveyID, Position, ResponseValue, ResponsePrompt, Comment) VALUES ({values});"
    return insertStatement

def getQuestionsInsert(record):
    id = record[0]
    pos = record[1]
    prompt = record[2]
    type = record[3]
    cha = record[4]
    notes = record[5]
    if cha == 'nan':
        values = f"{id},{pos},'{prompt}',{type}"
        insertStatement = f"INSERT INTO MultipleChoiceQuestions (SurveyID, Position, Prompt, Type) VALUES ({values});"
    elif notes == 'nan':
        values = f"{id},{pos},'{prompt}',{type},'{cha}'"
        insertStatement = f"INSERT INTO MultipleChoiceQuestions (SurveyID, Position, Prompt, Type, Characteristic) VALUES ({values});"
    else:
        values = f"{id},{pos},'{prompt}',{type},'{cha}','{notes}'"
        insertStatement = f"INSERT INTO MultipleChoiceQuestions (SurveyID, Position, Prompt, Type, Characteristic, Notes) VALUES ({values});"
    return insertStatement

def getUREInsert(record):
    if record[0].strip() == "Cases":
        return None
    caseText = record[0]
    caseNumber = caseText.strip().split()[-1]
    surveyId = 1
    dateCompleted = "Null"
    category = "URE"
    userId = record[1]
    values = f"{caseNumber},{surveyId},{dateCompleted},{category},{userId}"
    insertStatement = f"INSERT INTO SurveyResponses (SurveyResponseID, SurveyID, DateCompleted, Category, UserID) VALUES ({values});"
    return insertStatement

def getUREResponses(record):
    # print(record)
    if record[0].strip() == "Cases" or record[0].strip() == "nan":
        return None
    caseText = record[0]
    responseId = caseText.strip().split()[-1]
    questionNumber = 1
    surveyId = 1
    insertStatement = ""
    for answer in record[2:]:
        values = f"{responseId},{surveyId},{questionNumber},{answer}"
        insertStatement += f"INSERT INTO Responses (ResponseID, SurveyID, QuestionNo, Answer) VALUES ({values});\n"
        questionNumber += 1
    return insertStatement

def getWorkExpInsert(record):
    if record[0].strip() == "Cases":
        return None
    caseText = record[0]
    caseNumber = caseText.strip().split()[-1]
    surveyId = 2
    dateCompleted = "Null"
    category = "Work"
    userId = record[1]
    values = f"{caseNumber},{surveyId},{dateCompleted},{category},{userId}"
    insertStatement = f"INSERT INTO SurveyResponses (SurveyResponseID, SurveyID, DateCompleted, Category, UserID) VALUES ({values});"
    return insertStatement

def getWorkResponses(record):
    if record[0].strip() == "Cases" or record[0].strip() == "nan":
        return None
    caseText = record[0]
    responseId = caseText.strip().split()[-1]
    questionNumber = 1
    surveyId = 2
    insertStatement = ""
    for answer in record[2:]:
        values = f"{responseId},{surveyId},{questionNumber},{answer}"
        insertStatement += f"INSERT INTO Responses (ResponseID, SurveyID, QuestionNo, Answer) VALUES ({values});\n"
        questionNumber += 1
    return insertStatement

def expInsert(record):
    if record[0].strip() == "Cases":
        return None
    caseText = record[0]
    caseNumber = caseText.strip().split()[-1]
    insertStatement = f"INSERT INTO ExpProfiles (ExpPID, SurveyResponseID) VALUES ({caseNumber},{caseNumber});"
    return insertStatement

def expSurveyScore(record):
    if record[0].strip() == "Cases":
        return None
    caseText = record[0]
    surveyResponseId = caseText.strip().split()[-1]

    counter = 0
    insertStatement = ""
    for answer in record[1:]:
        characteristic = mapping[counter]
        insertStatement += f"INSERT INTO SurveyScores (SurveyResponseID, Characteristic, Value) VALUES ({surveyResponseId}, {characteristic}, {answer});\n"
        counter += 1
    return insertStatement

def insertDesiredProfiles(record):
    try:
        int(record[0])
    except:
        return None
    id = record[0]
    name = record[1]
    user = record[2]
    insertStatement = f"INSERT INTO DesiredProfiles (DesPID, Name, UserId) VALUES ({id},{name},{user});"
    return insertStatement

def insertDesScores(record):
    try:
        int(record[0])
    except:
        return None
    counter = 0
    insertStatement = ""
    print(record)
    for i in range(3, len(record), 2):
        preference = record[i]
        importance = record[i+1]
        characteristic = mapping[counter]
        values = f"{record[0]},{characteristic},{preference},{importance}"
        insertStatement += f"INSERT INTO DesiredScores (DesPID, Characteristic, Value, Importance) VALUES ({values})\n"
        counter += 1
    return insertStatement

def getRecords(url):
    df = pd.read_csv(url)
    records = [[cleanElement(el) for el in record] for record in df.values]
    return records

def printInsertStatements(url, createStatement):
    records = getRecords(url)
    for record in records:
        if len(record) == 0:
            continue
        insertStatement = createStatement(record)
        if insertStatement:
            print(insertStatement)


def main():
    surveyUrl = "https://raw.githubusercontent.com/IshaanKarvir/CSC366-Team-DropTables-Lab5/main/data/Data-v03.xlsx%20-%20Surveys.csv"
    userUrl = "https://raw.githubusercontent.com/IshaanKarvir/CSC366-Team-DropTables-Lab5/main/data/Data-v03.xlsx%20-%20Users.csv"
    questionReponseUrl = "https://raw.githubusercontent.com/IshaanKarvir/CSC366-Team-DropTables-Lab5/main/data/Data-v03.xlsx%20-%20QuestionResponses.csv"
    questionsUrl = "https://raw.githubusercontent.com/IshaanKarvir/CSC366-Team-DropTables-Lab5/main/data/Data-v03.xlsx%20-%20Survey%20Questions%20New.csv"
    ureExperienceUrl = "https://raw.githubusercontent.com/IshaanKarvir/CSC366-Team-DropTables-Lab5/main/data/Data-v03.xlsx%20-%20URE%20Experience.csv"
    workExperienceUrl = "https://raw.githubusercontent.com/IshaanKarvir/CSC366-Team-DropTables-Lab5/main/data/Data-v03.xlsx%20-%20Work%20Experience.csv"
    expUrl = "https://raw.githubusercontent.com/IshaanKarvir/CSC366-Team-DropTables-Lab5/main/data/Data-v03.xlsx%20-%20Work%20Profile-copy-values.csv"
    despUrl = "https://raw.githubusercontent.com/IshaanKarvir/CSC366-Team-DropTables-Lab5/main/data/Data-v03.xlsx%20-%20Work%20Preferences.csv"
    # printInsertStatements(surveyUrl, getSurveyInsert)
    # printInsertStatements(userUrl, getUserInsert)
    # printInsertStatements(questionsUrl, getQuestionsInsert)

    printInsertStatements(questionReponseUrl, getResponseOptionsInsert)
    # printInsertStatements(ureExperienceUrl, getUREInsert)
    # printInsertStatements(ureExperienceUrl, getUREResponses)
    # printInsertStatements(workExperienceUrl, getWorkExpInsert)
    # printInsertStatements(workExperienceUrl, getWorkResponses)
    # printInsertStatements(expUrl, expInsert)
    # printInsertStatements(despUrl, insertDesiredProfiles)
    # printInsertStatements(despUrl, insertDesScores)


if __name__ == "__main__":
    main()