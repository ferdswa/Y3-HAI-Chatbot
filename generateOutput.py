import random

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

intentST = {
    'gen' : ["how are you", "how're you", "how are you doing", "how ya doin'", "how ya doin", "how is everything", "how is everything going", "how's everything going"], #Part of a list found: https://stackoverflow.com/questions/51575924/list-of-greetings-phrases-in-english-for-nlp-task
    'capability' : ['what can you do', 'what can you do for me', 'what tasks can you do for me', "what things can you do for me", "what can you help me with", "what can you do to help me", "what can you do to assist me", "what can you do to help me out"]
}

qAGreetingsR1 = [
    "Here's what I found: ",
    "Here's some information about $: ",
    "Here you go: ",
    "Of course: ",
]
botFeelings = [
    "Great $!",
    "Great, thank you!",
    "Fantastic, and you $?",
    "Nothing to complain about $",
    "Ready for further development $!"
]
basicResponse = [
    "your name is $",
    "you're $",
    "you're called $",
    "you've asked me to call you $"
]
capabilityResponse = [
    "I can do: ",
    "I'm currently capable of: ",
    "I'm still in development, but I can help with: "
]
qAGreetingsRn = [
    "other ",
    "more ",
    "additional "
]


def generateQAOutput(answer:str,question:str,roundN:int):#Upgrade this
    outputStr = random.choice(qAGreetingsR1)
    outputStr += answer
    outputStr = (outputStr, outputStr.replace('$',question))['$' in outputStr]
    return outputStr

def generateSTOutput(question:str, type: int, addIn: str):
    if type == 0:
        a = random.choice(basicResponse)
        a = (a, a.replace('$',addIn))['$' in a]
        a = generateQAOutput(a,question,0)
        return a
    elif type == 1:
        data = []
        labels =[]
        for item in intentST:
            for string in intentST[item]:
                quest = string
                data.append(quest)
                labels.append(item)
                
        XTrain,yTrain = train_test_split(data,labels,stratify=labels, test_size=0.25, random_state=42)

        countVect=CountVectorizer()
        XTrainCounts = countVect.fit_transform(XTrain)

        tfidfTransformer_ = TfidfTransformer(use_idf=True,sublinear_tf=True).fit(XTrainCounts)

        XTrainTF = tfidfTransformer_.transform(XTrainCounts)

        classifier = LogisticRegression(random_state=0).fit(XTrainTF,yTrain)

        nd = question
        pnd = countVect.transform(nd)
        
        predictedV = classifier.predict(pnd)#Replace below with working to generate output
        predictedV = predictedV[0]
        if predictedV == 'gen':
            return generateGeneral(addIn)
        elif predictedV == 'capability':
            return generateCapability(['small talk','answer questions'])
        else:
            return 'failed'
    else:
        return 'failed'
    
def generateGeneral(addIn):
    outputStr = random.choice(botFeelings)
    outputStr = (outputStr, outputStr.replace('$',addIn))['$' in outputStr]
    return outputStr

def generateCapability(addIn):
    outputStr = random.choice(capabilityResponse)
    outputStr += addIn[0]
    for x in range(1,len(addIn)):
        outputStr += ', '
        outputStr += addIn[x]
    return outputStr
