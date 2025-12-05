import random
import datetime
import questionsAnswers
import generateOutput
import util

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
    questionsAnswersC = questionsAnswers.QuestionsAnswers()
    
    def introSelf(self):
        print("Hello and welcome to Maxim Carr's HAI Chatbot")
        print("Please enter a prompt below")
        print("-" * 50)
        self.name = self.getUserName()
        self.__init__()#Reinitialise to grab name
        response = self.smallTalkIntent(["hi"],self.name)
        print(f"HAIBot: {response[0]}")
        while True:
            userInput = input(f"{self.name}: ").lower()
            processSelect = self.findMostSimilarProc(userInput)

            if processSelect[0] == 0:
                dfAnswers = self.questionsAnswersC.answerQuestion(processSelect[1])
                if 'none' in dfAnswers['documents'].values:#Question wasn't able to be answered
                    print(f"HAIBot: {generateOutput.generateQuestionUnAnswerable([userInput,self.name])}")
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
                print(f"HAIBot: {generateOutput.getDefault(self.name)}")
                

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
        uIC = util.queryLemmatize(uI)
        for item in intentST:
            for string in intentST[item]:
                datasetST.append(string)
        for curQuestion in datasetQA:
            a = util.getCosForPair(uIC,curQuestion)
            if a>highQA:
                highQA = a
                highQ = curQuestion
        for curSmallTalk in datasetST:
            cSTL = util.queryLemmatize(curSmallTalk)
            a = util.getCosForPair(uIC,cSTL)
            if a>highST:
                highST = a
        print(highQA, highST)
        if max(highQA,highST) == highQA and highQA>0.7:
            return [0,highQ]
        elif max(highQA,highST) == highST and highST>0.7:
            return [1,None]
        else:
            return [-1,None]
    
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

