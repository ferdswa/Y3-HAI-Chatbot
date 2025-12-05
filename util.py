import random
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

def trainClassify(data,labels):
    XTrain, XTest, yTrain,yTest = train_test_split(data,labels,stratify=labels, test_size=0.25, random_state=42)

    countVect=CountVectorizer()
    XTrainCounts = countVect.fit_transform(XTrain)

    tfidfTransformer_ = TfidfTransformer(use_idf=True,sublinear_tf=True).fit(XTrainCounts)

    XTrainTF = tfidfTransformer_.transform(XTrainCounts)

    classifier = LogisticRegression(random_state=0).fit(XTrainTF,yTrain)
    return classifier, countVect
