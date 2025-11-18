from collections import Counter
import re
import nltk
import csv,os,pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

filename = "COMP3074-CW1-Dataset.csv"
lemmatize = WordNetLemmatizer()
nltk.download('wordnet')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger_eng')


class questionsAnswers:
    questions = []
    answers = []
    documents = []
    corpusDict = {}
    qaLocation = os.path.join(os.path.dirname(os.path.abspath(__file__)),filename)
    df = pd.DataFrame({'documents':documents, 'questions': questions, 'answers': answers})
    questionVs = []

    def __init__(self):
        with open(self.qaLocation, encoding="utf8", errors='ignore', mode='r') as questionsAnswers:
            next(questionsAnswers)
            qaCSV = csv.reader(questionsAnswers)
            for line in qaCSV:
                self.questions.append(re.sub(r'[^\w\s]','',line[1].lower()))#Remove punct
                self.answers.append(line[2].lower())
                self.documents.append(line[3].lower())

        self.df = pd.DataFrame({'documents':self.documents, 'questions': self.questions, 'answers': self.answers}) #topics = documents

        dfQ = self.df.drop('answers',axis=1,inplace=False)
        dfQ = dfQ.drop_duplicates()

        allQs = dfQ['questions'].values
        allDs = dfQ['documents'].values
        #allAs = self.df['answers'].values

        for i in range(len(allQs)):
            dWord = allDs[i]
            qWord = allQs[i]
            tokenQ = word_tokenize(qWord)
            taggedQ = pos_tag(tokenQ)
            lemmatizedQ = [lemmatize.lemmatize(word, pos='v' if tag.startswith('V') else 'n') for word, tag in taggedQ]
            self.corpusDict[dWord] = lemmatizedQ

        for y in self.corpusDict.values():
            self.questionVs.append(Counter(y))

    def answerQuestion(self,highestQuestionVector):
        df = self.df
        ldocs = list(self.corpusDict.keys())
        try:
            indexOfHQV = self.questionVs.index(highestQuestionVector)
            token2rf = ldocs[indexOfHQV]

            if token2rf in self.corpusDict.keys():#FIXME: Needs refinement
                dfa = df.query(f'documents == "{token2rf}"', inplace=False)#Can return multiple vals. TODO: Get the generateOutput to handle them well. see todo in generateOutput.
                if(len(dfa)>0):
                    return dfa#answer found
            else: 
                raise ValueError("A value for token2rf was given that wasn't in documents. This shouldn't happen.")
        except ValueError:
            documentsNF = ['none']
            questionsNF = ['none']#Return failed question for use elsewhere. 
            answersNF = ['none']
            return pd.DataFrame({'documents':documentsNF, 'questions': questionsNF, 'answers': answersNF})#No question found