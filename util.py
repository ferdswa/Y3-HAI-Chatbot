import math
from nltk import pos_tag
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

lemmatize = WordNetLemmatizer()

def trainClassify(data,labels):
    XTrain, XTest, yTrain,yTest = train_test_split(data,labels,stratify=labels, test_size=0.25, random_state=42)

    countVect=CountVectorizer()
    XTrainCounts = countVect.fit_transform(XTrain)

    tfidfTransformer_ = TfidfTransformer(use_idf=True,sublinear_tf=True).fit(XTrainCounts)

    XTrainTF = tfidfTransformer_.transform(XTrainCounts)

    classifier = LogisticRegression(random_state=0).fit(XTrainTF,yTrain)
    return classifier, countVect

def getCosForPair( queryVect, currentVectFrQuestions):
    #Formula: https://en.wikipedia.org/wiki/Cosine_similarity#Definition
    intersection = set(queryVect.keys()) & set(currentVectFrQuestions.keys())
    numerator = sum([queryVect[x] * currentVectFrQuestions[x] for x in intersection])

    sum1 = sum([queryVect[x] ** 2 for x in list(queryVect.keys())])
    sum2 = sum([currentVectFrQuestions[y] ** 2 for y in list(currentVectFrQuestions.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator
    
def queryLemmatize(userInput):
    tokenQ = word_tokenize(userInput)
    taggedQ = pos_tag(tokenQ)
    lemmatizedQ = [lemmatize.lemmatize(word, pos='v' if tag.startswith('V') else 'n') for word, tag in taggedQ]
    return Counter(lemmatizedQ)