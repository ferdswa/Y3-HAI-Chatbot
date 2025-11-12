import os
import csv
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

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
