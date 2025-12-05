from collections import Counter
import math
import random
import datetime
import re
import questionsAnswers
import generateOutput
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
import numpy as np
from numpy.linalg import norm

import util

lemmatize = WordNetLemmatizer()

dayPd = 'morning'



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
class HAIChatBotMC:
    name = ''
    questionsAnswersC = questionsAnswers.questionsAnswers()
    def __init__(self):
        self.patterns = {#Very basic response templates
        }
        self.defaultResponses = [#Fallback option
            f"I'm not sure I quite understand {self.name}, could you rephrase that?",
            f"I'm quite new and I can't do that yet. Anything else you'd like to talk about {self.name}?",
            f"That's interesting, could you expand {self.name}?",
            f"I'm sorry {self.name}, I couldn't understand that. Could you put it in different words?"
        ]
        self.noQuestionsFoundResponses = [
            f"I don't have access to that information {self.name}. Would you like to talk about anything else?",
            f"I'm not quite sure {self.name}. Do you want to know about something else?",
            f"I couldn't find anything about $, can I help you with anything else {self.name}?"
        ]
    def get_response(self, user_input):
        user_input = user_input.lower().strip()
        
        # Check each pattern for matches
        for pattern, responses in self.patterns.items():
            if re.search(pattern, user_input, re.IGNORECASE):
                return random.choice(responses)
    
        # Return default response if no pattern matches
        return random.choice(self.defaultResponses)
    
    def introSelf(self):
        print("Hello and welcome to Maxim Carr's HAI Chatbot")
        print("Please enter a prompt below")
        print("-" * 50)
        self.name = self.getUserName()
        self.__init__()#Reinitialise to grab name
        response = self.smallTalkIntent(["hi"],self.name)
        print(f"HAIBot: {response[0]}")
        while True:
            exiting = 0
            userInput = input(f"{self.name}: ").lower()
            processSelect = self.findMostSimilarProc(userInput)

            if processSelect[0] == 0:
                dfAnswers = self.questionsAnswersC.answerQuestion(processSelect[1])
                if 'none' in dfAnswers['documents'].values:#Question wasn't able to be answered
                    ret = random.choice(self.noQuestionsFoundResponses)
                    ret = (ret, ret.replace('$',userInput))['$' in ret]
                    print(f"HAIBot: {ret}")
                else:#Question was answered
                    response = dfAnswers['answers'].values
                    resp, leftOver = generateOutput.generateQAOutput(response.tolist(),userInput)
                    print(f"HAIBot: {resp}")
                    while(leftOver is not None):
                        if(len(leftOver)>0):
                            print("HAIBot: Would you like to know more?")
                            ur = input(f"{self.name}: ").lower()
                            resp, leftOver = self.getAnotherAnswer(leftOver,[ur],userInput)
                            print(f"HAIBot: {resp}")
                        else:
                            print("HAIBot: That's all I've got on that topic")
                            leftOver = None
                    response = self.smallTalkIntent(["hi"],self.name)
                    print(f"HAIBot: {response[0]}")
                    
            elif processSelect[0] == 1:
                ret = self.smallTalkIntent([userInput],self.name)
                print(f"HAIBot: {ret[0]}")
                if(ret[1]==-1):
                    break
            else:
                response = self.get_response(userInput)
                print(f"HAIBot: {response}")
                

    def getUserName(self):
        print("HAIBot: Hello!\nWhat is your name?")
        n = input("You: ")
        if(len(n)==0):
            print("HAIBot: Names cannot be zero characters long.")
            self.getUserName()
        else:
            return n
        
    #Find cos similarity for each process and return which is most similar
    def findMostSimilarProc(self,uI):
        datasetQA = self.questionsAnswersC.questionVs#Vectors of questions in qa
        datasetST = []
        datasetTA = []
        highQA = 0
        highQ = []
        highST = 0
        a = 0
        uIC = self.queryLemmatize(uI)
        for item in intentST:
            for string in intentST[item]:
                datasetST.append(string)
        for curQuestion in datasetQA:
            a = self.getCosForPair(uIC,curQuestion)
            if a>highQA:
                highQA = a
                highQ = curQuestion
        for curSmallTalk in datasetST:
            cSTL = self.queryLemmatize(curSmallTalk)
            a = self.getCosForPair(uIC,cSTL)
            if a>highST:
                highST = a
        if max(highQA,highST) == highQA and highQA>0.7:
            return [0,highQ]
        elif max(highQA,highST) == highST and highST>0.7:
            return [1,None]
        else:
            return [-1,None]
        
    def getCosForPair(self, queryVect, currentVectFrQuestions):
        #Keys = tokens, values = numbers
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
    
    def queryLemmatize(self, userInput):
        tokenQ = word_tokenize(userInput)
        taggedQ = pos_tag(tokenQ)
        lemmatizedQ = [lemmatize.lemmatize(word, pos='v' if tag.startswith('V') else 'n') for word, tag in taggedQ]
        return Counter(lemmatizedQ)
    
    def smallTalkIntent(self,question:str, addIn):
        data = []
        labels =[]
        for item in intentST:
            for string in intentST[item]:
                quest = string
                data.append(quest)
                labels.append(item)
                
        classifier, countVect = util.trainClassify(data,labels)

        nd = question
        pnd = countVect.transform(nd)
        
        predictedV = classifier.predict(pnd)#Replace below with working to generate output
        predictedV = predictedV[0]
        if predictedV == 'gen':
            return [generateOutput.generateGeneral(addIn),0]
        elif predictedV == 'capability':
            return [generateOutput.generateCapability(['small talk','answer questions']),0]
        elif predictedV == 'name':
            return [generateOutput.generateName(addIn),0]
        elif predictedV == 'quit':
            return [generateOutput.generateGoodbye([addIn,dayPd]),-1]
        elif predictedV == 'greet':
            return [generateOutput.generateGreeting([addIn,dayPd]),0]
        else:
            return ['failed',0]
        
    def getAnotherAnswer(self, leftover, userResponse, question):
        data = []
        labels = []
        for item in yesNoIntent:
            for string in yesNoIntent[item]:
                resp = string
                data.append(resp)
                labels.append(item)

        classifier, countVect = util.trainClassify(data,labels)

        nd = userResponse
        pnd = countVect.transform(nd)
        predictedV = classifier.predict(pnd)
        predictedV = predictedV[0]#Determined if user has entered a yes or no
        if predictedV == 'yes':
            resp, leftOver = generateOutput.generateQAOutput(leftover,question)
            return resp, leftOver
        else:
            return generateOutput.generateNoMoreAnswers(self.name), None

if(__name__ == '__main__'):
    x = datetime.datetime.now().hour
    if(x>=17):
        dayPd = 'evening'
    elif(x>=12):
        dayPd = 'afternoon'
    else:
        dayPd = 'morning'
    if(__name__=='__main__'):
        cb = HAIChatBotMC()
        cb.introSelf()

