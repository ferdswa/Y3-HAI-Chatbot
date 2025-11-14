from collections import Counter, defaultdict
import math
import re
import nltk
import csv,os,pandas as pd, numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from scipy import spatial
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

filename = "COMP3074-CW1-Dataset.csv"
lemmatize = WordNetLemmatizer()
analyzerA = CountVectorizer().build_analyzer()
nltk.download('wordnet')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger_eng')
WORD = re.compile(r"\w+")


class questionsAnswers:
    questions = []
    answers = []
    documents = []
    corpus = {}
    corpusDict = {}
    qaLocation = os.path.join(os.path.dirname(os.path.abspath(__file__)),filename)
    df = pd.DataFrame({'documents':documents, 'questions': questions, 'answers': answers})
    questionVs = []

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
        #allAs = self.df['answers'].values

        for i in range(len(allQs)):
            dWord = allDs[i]
            qWord = allQs[i]
            tokenQ = word_tokenize(qWord)
            taggedQ = pos_tag(tokenQ)
            lemmatizedQ = [lemmatize.lemmatize(word, pos='v' if tag.startswith('V') else 'n') for word, tag in taggedQ]
            self.corpus[dWord] = ' '.join(lemmatizedQ)
            self.corpusDict[dWord] = lemmatizedQ

        for y in self.corpus.values():
            self.questionVs.append(self.text_to_vector(y)) 

        # tfTransformer = TfidfTransformer(use_idf = True, sublinear_tf = True).fit(XTrainCounts)
        # XTrainTF = tfTransformer.transform(XTrainCounts)
        # #return XTrainTF

    def testQuestion(self,userInput:str):
        qWords = 'how','why','when','who','what'
        if(userInput.lower().startswith(qWords)):
            return True
        else:
            return False
        
    def answerQuestionLemmatized(self, userInput):
        tokenQ = word_tokenize(userInput)
        taggedQ = pos_tag(tokenQ)
        lemmatizedQ = [lemmatize.lemmatize(word, pos='v' if tag.startswith('V') else 'n') for word, tag in taggedQ]
        rejoinedQ = ' '.join(lemmatizedQ)
        return self.text_to_vector(rejoinedQ)

    def vectorizeText(self, stringToVectorize):#currently unused
        countVect = CountVectorizer(stop_words=stopwords.words('english'))

        XTrainCounts = countVect.fit_transform(stringToVectorize)
        featNames = countVect.get_feature_names_out()
        return XTrainCounts


    def answerQuestion(self,userInput):
        df = self.df
        cosinesQuestions = []
        queryVect = self.answerQuestionLemmatized(userInput)
        for x in self.questionVs:
            cosinesQuestions.append([self.getCosForPair(queryVect,x),x])

        cosinesQuestions.sort(reverse=True)#invert cosine calc from method (same as 1-getCosForPair.result)
        token2rf = cosinesQuestions[0][1].keys()
        reformedToken = ' '.join(token2rf)

        if reformedToken in self.corpus.values() and cosinesQuestions[0][0]>0.75:#FIXME: Needs refinement
            c2 = {v:k for k,v in self.corpus.items()}
            cv = c2.get(reformedToken)
            dfa = df.query(f'documents == "{cv}"', inplace=False)#Can return multiple vals. TODO: Get the generateOutput to handle them well. see todo in generateOutput.
            if(len(dfa)>0):
                return dfa#answer found
        else:
            documentsNF = ['none']
            questionsNF = [userInput]#Return failed question for use elsewhere. 
            answersNF = ['none']
            return pd.DataFrame({'documents':documentsNF, 'questions': questionsNF, 'answers': answersNF})#No question found
    
    def text_to_vector(self,text):
        words = WORD.findall(text)
        return Counter(words)
    
    def getCosForPair(self, queryVect, currentVectFrQuestions):
        
        intersection = set(queryVect.keys()) & set(currentVectFrQuestions.keys())
        numerator = sum([queryVect[x] * currentVectFrQuestions[x] for x in intersection])

        sum1 = sum([queryVect[x] ** 2 for x in list(queryVect.keys())])
        sum2 = sum([currentVectFrQuestions[x] ** 2 for x in list(currentVectFrQuestions.keys())])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator