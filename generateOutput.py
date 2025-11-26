import random
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

intentST = {
    'gen' : ["how are you", "how're you", "how are you doing", "how ya doin'", "how ya doin", "how is everything", "how is everything going", "how's everything going"], #Part of a list found: https://stackoverflow.com/questions/51575924/list-of-greetings-phrases-in-english-for-nlp-task
    'capability' : ['what can you do', 'what can you do for me', 'what tasks can you do for me', "what things can you do for me", "what can you help me with", "what can you do to help me", "what can you do to assist me", "what can you do to help me out"],
    'name': ['what is my name', 'what\'s my name', 'What is my name', 'What\'s my name'],
    'quit': ['quit', 'exit', 'bye', 'goodbye', 'that\'s all', 'see you'],
    'greet': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']
}

yesNoIntent ={
    'yes' : ["yes","yeah","sure","of course","ok","y"],
    'no' : ["no","nah", "no thanks", "no thank you", "i'm good", "n"]
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
goodbyeMsgs = ["Thanks for chatting $!",
    "See you later $, come back whenever you like",
    "Have fun $, come back soon!",
    "Goodbye",
    "Bye $, have a good £"]
greetings = ["Hi there $, what can I help you with?", "What's up $?","Hey $, what can I do for you today?","Good £ $, how can I help?","What's on your mind $"]

def generateQAOutput(answer,question:str,roundN:int):#Upgrade this. Currently outputs random choice if >1 answer. TODO: Make it add only new information. See todo in questionsAnswers
    answer = answer.tolist()
    outputStr = random.choice(qAGreetingsR1)
    select = random.choice(answer)
    outputStr += select
    answer = list(filter(lambda x: x != select,answer))#Filter array to exclude current output string
    outputStr = (outputStr, outputStr.replace('$',question))['$' in outputStr]
    return outputStr,answer

def getAnotherAnswer(leftover, userResponse):
    data = []
    labels = []
    for item in yesNoIntent:
        for string in yesNoIntent[item]:
            resp = string
            data.append(resp)
            labels.append(item)

    classifier, countVect = trainClassify(data,labels)

    nd = userResponse
    pnd = countVect.transform(nd)
    predictedV = classifier.predict(pnd)
    predictedV = predictedV[0]#Determined if user has entered a yes or no
    print(predictedV)
    

def generateSTOutput(question:str, addIn: str):
    data = []
    labels =[]
    for item in intentST:
        for string in intentST[item]:
            quest = string
            data.append(quest)
            labels.append(item)
            
    classifier, countVect = trainClassify(data,labels)

    nd = question
    pnd = countVect.transform(nd)
    
    predictedV = classifier.predict(pnd)#Replace below with working to generate output
    predictedV = predictedV[0]
    print(predictedV)
    if predictedV == 'gen':
        return [generateGeneral(addIn[0]),0]
    elif predictedV == 'capability':
        return [generateCapability(['small talk','answer questions']),0]
    elif predictedV == 'name':
        return [generateName(addIn[0]),0]
    elif predictedV == 'quit':
        return [generateGoodbye(addIn),-1]
    elif predictedV == 'greet':
        return [generateGreeting(addIn),0]
    else:
        return ['failed',0]
    
def trainClassify(data,labels):
    XTrain, XTest, yTrain,yTest = train_test_split(data,labels,stratify=labels, test_size=0.25, random_state=42)

    countVect=CountVectorizer()
    XTrainCounts = countVect.fit_transform(XTrain)

    tfidfTransformer_ = TfidfTransformer(use_idf=True,sublinear_tf=True).fit(XTrainCounts)

    XTrainTF = tfidfTransformer_.transform(XTrainCounts)

    classifier = LogisticRegression(random_state=0).fit(XTrainTF,yTrain)
    return classifier, countVect


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

def generateName(addIn):
    a = random.choice(basicResponse)
    a = (a, a.replace('$',addIn))['$' in a]
    return a

def generateGoodbye(addIn):
    a = random.choice(goodbyeMsgs)
    a = (a,a.replace('$', addIn[0]))['$' in a]
    a = (a,a.replace('$', addIn[1]))['£' in a]
    return a

def generateGreeting(addIn):
    a = random.choice(greetings)
    a = (a,a.replace('$', addIn[0]))['$' in a]
    a = (a,a.replace('$', addIn[1]))['£' in a]
    return a