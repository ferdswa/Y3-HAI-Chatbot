import csv,os,pandas as pd

filename = "COMP3074-CW1-Dataset.csv"

questions = []
answers = []
documents = []
qaLocation = os.path.join(os.path.dirname(os.path.abspath(__file__)),filename)


def fetchQAData():
    with open(qaLocation, encoding="utf8", errors='ignore', mode='r') as questionsAnswers:
        next(questionsAnswers)
        qaCSV = csv.reader(questionsAnswers)
        for line in qaCSV:
            questions.append(line[1].lower())
            answers.append(line[2].lower())
            documents.append(line[3].lower())

    df = pd.DataFrame({'documents':documents, 'questions': questions, 'answers': answers}) #topics = documents
    return df

def testQuestion(userInput):
    df = fetchQAData()
    