import requests
import pandas as pd

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
    values = ",".join(record)
    insertStatement = f"INSERT INTO Surveys (SurveyID, ShortName, Name, Description) VALUES ({values});"
    return insertStatement

def getUserInsert(record):
    values = ",".join(record+["None"])
    insertStatement = f"INSERT INTO Users (AccountID, Name, Email, Role) VALUES ({values});"
    return insertStatement

def getResponseOptionsInsert(record):
    values = ",".join(record)
    insertStatement = f"INSERT INTO ResponseOptions (SurveyID, Position, ResponseValue, ResponsePrompt, Comment) VALUES ({values});"
    return insertStatement

def getQuestionsInsert(record):
    values = ",".join(record)
    insertStatement = f"INSERT INTO MultipleChoiceQuestions (SurveyID, Position, Prompt, Type, Characteristics, Notes) VALUES ({values});"
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
    insertStatement = ""
    for answer in record[2:]:
        values = f"{responseId},{questionNumber},{answer}"
        insertStatement += f"INSERT INTO Responses (ResponseID, QuestionNo, Answer) VALUES ({values});\n"
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
    # printInsertStatements(questionReponseUrl, getResponseOptionsInsert)
    # printInsertStatements(questionsUrl, getQuestionsInsert)
    # printInsertStatements(ureExperienceUrl, getUREInsert)
    # printInsertStatements(ureExperienceUrl, getUREResponses)
    # printInsertStatements(workExperienceUrl, getWorkExpInsert)
    # printInsertStatements(workExperienceUrl, getUREResponses)
    # printInsertStatements(expUrl, expInsert)
    printInsertStatements(despUrl, insertDesiredProfiles)
    printInsertStatements(despUrl, insertDesScores)
    # printUserInsertStatements()
    # printResponseInsertStatements()


if __name__ == "__main__":
    main()