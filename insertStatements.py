from numpy import insert
import requests
import pandas as pd

def cleanElement(el):
    try:
        return str(int(el))
    except:
        return str(el)

def getSurveyInsert(record):
    values = ",".join(record)
    insertStatement = f"INSERT INTO Surveys (SurveyID, ShortName, Name, Description) VALUES ({values}"
    return insertStatement

def getUserInsert(record):
    values = ",".join(record+["None"])
    insertStatement = f"INSERT INTO Users (AccountID, Name, Email, Role) VALUES ({values})"
    return insertStatement

def getResponseOptionsInsert(record):
    values = ",".join(record[1:])
    insertStatement = f"INSERT INTO ResponseOptions (Survey, Position, ResponseValue, ResponsePrompt, Comment) VALUES ({values})"
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
        print(insertStatement)


def main():
    surveyUrl = "https://raw.githubusercontent.com/IshaanKarvir/CSC366-Team-DropTables-Lab5/main/data/Data-v03.xlsx%20-%20Surveys.csv"
    userUrl = "https://raw.githubusercontent.com/IshaanKarvir/CSC366-Team-DropTables-Lab5/main/data/Data-v03.xlsx%20-%20Users.csv"
    questionReponseUrl = "https://raw.githubusercontent.com/IshaanKarvir/CSC366-Team-DropTables-Lab5/main/data/Data-v03.xlsx%20-%20QuestionResponses.csv"
    printInsertStatements(surveyUrl, getSurveyInsert)
    printInsertStatements(userUrl, getUserInsert)
    printInsertStatements(questionReponseUrl, getResponseOptionsInsert)
    # printUserInsertStatements()
    # printResponseInsertStatements()


if __name__ == "__main__":
    main()