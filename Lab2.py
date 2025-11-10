import os
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,f1_score,confusion_matrix

labelDir = {
    "positive":"data/positive",
    "negative":"data/negative" 
}

data = []
labels = [
]

for label in labelDir.keys():
    cwd = os.path.dirname(os.path.abspath(__file__))
    print(os.listdir(os.path.join(cwd,labelDir[label])))
    for file in os.listdir(os.path.join(cwd,labelDir[label])):
        filepath = os.path.join(cwd,labelDir[label])+os.sep+file
        with open(filepath,encoding='utf8',errors='ignore',mode='r') as review:
            content = review.read()
            data.append(content)
            labels.append(label)

XTrain, XTest, yTrain,yTest = train_test_split(data,labels,stratify=labels, test_size=0.25, random_state=42)

countVect=CountVectorizer(stop_words=stopwords.words('english'))
XTrainCounts = countVect.fit_transform(XTrain)

tfidfTransformer_ = TfidfTransformer(use_idf=True,sublinear_tf=True).fit(XTrainCounts)

XTrainTF = tfidfTransformer_.transform(XTrainCounts)

classifier = LogisticRegression(random_state=0).fit(XTrainTF,yTrain)

X_new_counts = countVect.transform ( XTest )
X_new_tfidf = tfidfTransformer_ . transform ( X_new_counts )

predicted = classifier . predict ( X_new_tfidf )

print ( confusion_matrix ( yTest , predicted ) )
print ( accuracy_score ( yTest , predicted ) )
print ( f1_score ( yTest , predicted , pos_label='positive'))

nd = ['this is new data and it is fantastic']
pnd = countVect.transform(nd)
pnd = tfidfTransformer_.transform(pnd)

ndn = ['this is new data and it is horrible']
pndn = countVect.transform(ndn)
pndn = tfidfTransformer_.transform(pndn)

print(classifier.predict(pnd))
print(classifier.predict(pndn))