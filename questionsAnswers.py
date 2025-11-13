import nltk
import csv,os,pandas as pd, numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

filename = "COMP3074-CW1-Dataset.csv"
lemmatize = WordNetLemmatizer()
analyzer = CountVectorizer().build_analyzer()
nltk.download('wordnet')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger_eng')


class questionsAnswers:
    questions = []
    answers = []
    documents = []
    qaLocation = os.path.join(os.path.dirname(os.path.abspath(__file__)),filename)
    df = pd.DataFrame({'documents':documents, 'questions': questions, 'answers': answers})
    qM:any

    def __init__(self):
        with open(self.qaLocation, encoding="utf8", errors='ignore', mode='r') as questionsAnswers:
            next(questionsAnswers)
            qaCSV = csv.reader(questionsAnswers)
            for line in qaCSV:
                self.questions.append(line[1].lower())
                self.answers.append(line[2].lower())
                self.documents.append(line[3].lower())

        self.df = pd.DataFrame({'documents':self.documents, 'questions': self.questions, 'answers': self.answers}) #topics = documents

        dfQ = self.df.drop('answers',axis=1,inplace=False)
        dfQ = dfQ.drop_duplicates()

        allQs = dfQ['questions'].values
        allDs = dfQ['documents'].values
        allAs = self.df['answers'].values
        corpus = {}

        for i in range(len(allQs)):
            dWord = allDs[i]
            qWord = allQs[i]
            tokenQ = word_tokenize(qWord)
            taggedQ = pos_tag(tokenQ)
            lemmatizedQ = [lemmatize.lemmatize(word, pos='v' if tag.startswith('V') else 'n') for word, tag in taggedQ]
            corpus[dWord] = ' '.join(lemmatizedQ)

            
        print(corpus)

        questions = corpus.values()

        self.qM = self.preproc(questions)
        print(self.qM)
        

    def preproc(self,string):
        countVect = CountVectorizer(stop_words = stopwords.words('english'))

        XTrainCounts = countVect.fit_transform(string)
        print("Feature names: ", countVect.get_feature_names_out())

        tfTransformer = TfidfTransformer(use_idf = True, sublinear_tf = True).fit(XTrainCounts)
        XTrainTF = tfTransformer.transform(XTrainCounts)
        return XTrainTF

    def testQuestion(self,userInput:str):
        qWords = 'how','why','when','who','what'
        if(userInput.lower().startswith(qWords)):
            return True
        else:
            return False

    def answerQuestion(self,userInput):
        df = self.df
        for string in userInput:
            df.query(f'questions.str.contains("{string}")', inplace=True)
        if(len(df)>0):
            return df#answer found
        else:
            documentsNF = ['none']
            questionsNF = [userInput]
            answersNF = ['none']
            return pd.DataFrame({'documents':documentsNF, 'questions': questionsNF, 'answers': answersNF})#No question found