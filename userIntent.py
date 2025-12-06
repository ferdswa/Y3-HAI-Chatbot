import csv
import datetime
import os
import re
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
import questionsAnswers
import generateOutput
import playlistManager
import util
import intentLists

dayPd = 'morning'
intentST = intentLists.intentST
yesNoIntent = intentLists.yesNoIntent
playListIntent = intentLists.playListIntent
#https://huggingface.co/datasets/OpenVoiceOS/yes_no_answers
yesNoDir = os.path.dirname(os.path.abspath(__file__))+os.sep+"datasets"+os.sep+"yesno.csv"

class HAIChatBotMC:
    name = ''
    questionsAnswersC = questionsAnswers.QuestionsAnswers()
    pm = playlistManager.PlaylistManager()
    classifier = LogisticRegression()
    countVect = CountVectorizer()

    #Setup by getting yes/no dataset
    def __init__(self):
        try:
            with open(yesNoDir, 'r') as yesnoCSV:
                yesNoIntent["yes"]=[]
                yesNoIntent["no"]=[]
                csvFile = csv.reader(yesnoCSV)
                for line in csvFile:
                    if line[1] == 'yes':
                        yesNoIntent['yes'].append(line[0])
                    elif line[1] == 'no':
                        yesNoIntent['no'].append(line[0])
                
        except FileNotFoundError:
            print("HAIBot: I'm missing the yes/no dataset csv file. Falling back to default yes no classification, accuraccy may be reduced.")
            
    #Main bot loop method
    def introSelf(self):
        print("Hello and welcome to Maxim Carr's HAI Chatbot")
        print("Please enter a prompt below")
        print("-" * 50)
        self.name = self.getUserName()
        self.__init__()#Reinitialise to grab name
        response = self.smallTalkIntent(["hi"],self.name,"")
        print(f"HAIBot: {response[0]}")
        while True:#Main loop
            userInput = input(f"{self.name}: ").lower()
            userInput = re.sub(r'[^\w\s]','',userInput)#remove punctuation as all the datasets ignore it
            processSelect = self.findMostSimilarProc(userInput)

            if processSelect[0] == 0:#Question Answering
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
                    response = self.smallTalkIntent(["hi"],self.name,"")
                    print(f"HAIBot: {response[0]}")
                    
            elif processSelect[0] == 1:#Small Talk
                getPtNewName = userInput.split(" ")
                ret = self.smallTalkIntent([processSelect[1]],self.name, getPtNewName[len(getPtNewName)-1])
                print(f"HAIBot: {ret[0]}")
                if(ret[1]==-1):#Quit is a subset of small talk
                    break

            elif processSelect[0] == 2:#Playlist Management
                ret = self.playlistIntent(processSelect[1],userInput)
                print(f"HAIBot: {ret[0]}")
                
                if "do you want me to make it" in ret[0] or "Maybe you'd want to create it" in ret[0]:
                    createNEPlaylist = input(f"HAIBot: Should I do that for you?\n{self.name}: ").lower()
                    createNEPlaylist = re.sub(r'[^\w\s]','',createNEPlaylist)

                    nd = [createNEPlaylist]
                    pnd = self.countVect.transform(nd)
                    predictedV = self.classifier.predict(pnd)
                    predictedV = predictedV[0]#Determined if user has entered a yes or no
                    if predictedV == 'yes':
                        pName = ret[1][len(ret[1])-1]
                        ret1 = self.pm.createPlaylist(pName)
                        print(f"HAIBot: {ret1}")
                        ret[1].remove(pName)
                        for song in ret[1]:
                            ret1 = self.pm.addToPlaylist(pName,[song])
                            print(f"HAIBot: {ret1}")
                        response = self.smallTalkIntent(["hi"],self.name,"")
                    else:
                        ret1 = generateOutput.generateNoMoreAnswers(self.name)
                        print(f"HAIBot: {ret1}")

            else:
                print(f"HAIBot: {generateOutput.getDefault(self.name)}")
                
    #Get the user's name
    def getUserName(self):
        print("HAIBot: Hello!\nWhat is your name?")
        n = input("You: ")
        if(len(n)==0):
            print("HAIBot: Names cannot be zero characters long.")
            self.getUserName()
        else:
            return n
        
    #Find cos similarity for each process and return which is most similar
    def findMostSimilarProc(self,userInput):
        datasetQA = self.questionsAnswersC.questionVs#Vectors of questions in qa
        datasetST = []
        datasetTA = []
        highQA = 0
        highQLemmatized = []
        highST = 0
        highTA = 0
        highTAQ = ""
        highSmallTalkQ = ""
        a = 0
        userInputLemmatized = util.queryLemmatize(userInput)
        for item in intentST:
            for string in intentST[item]:
                datasetST.append(string)
        for item in playListIntent:
            for string in playListIntent[item]:
                datasetTA.append(string)
        for curQuestion in datasetQA:
            a = util.getCosForPair(userInputLemmatized,curQuestion)
            if a>highQA:
                highQA = a
                highQLemmatized = curQuestion
        for curSmallTalk in datasetST:
            lemmatizedSmallTalk = util.queryLemmatize(curSmallTalk)
            a = util.getCosForPair(userInputLemmatized,lemmatizedSmallTalk)
            if a>highST:
                highST = a
                highSmallTalkQ = curSmallTalk
        resultRound1 = max(highQA,highST)
        #Run against the winner of the previous round of Cos Similarity
        if(resultRound1 == highQA):
            for curPlaylistOp in datasetTA:
                currentOpLemmatized = util.queryLemmatize(curPlaylistOp)
                a = util.getCosForPair(currentOpLemmatized,userInputLemmatized)
                if a>highQA and a>highTA:
                    highTA = a
                    highTAQ = curPlaylistOp
        else:
            for curPlaylistOp in datasetTA:
                currentOpLemmatized = util.queryLemmatize(curPlaylistOp)
                a = util.getCosForPair(currentOpLemmatized,userInputLemmatized)
                if a>highST and a>highTA:
                    highTA = a
                    highTAQ = curPlaylistOp
        if highTA == 0:#Transaction less similar
            if max(highQA,highST) == highQA and highQA>0.7:
                return [0,highQLemmatized]
            elif max(highQA,highST) == highST and highST>0.6:
                return [1,highSmallTalkQ]
            else:
                return [-1,None]
        elif highTA>0.4:#Transaction more similar
            return[2,highTAQ]
        else:
            return [-1,None]
        
    #See what type of small talk the user wants and perform that task
    def smallTalkIntent(self,question:str, addIn, newName):
        predictedV = ""
        for userIntent in intentST:
            if question[0] in intentST[userIntent]:
                predictedV = userIntent

        if predictedV == 'gen':
            return [generateOutput.generateGeneral(addIn),0]
        elif predictedV == 'capability':
            return [generateOutput.generateCapability(['small talk','answer questions','get weather','playlist management']),0]
        elif predictedV == 'quit':
            return [generateOutput.generateGoodbye([addIn,dayPd]),-1]
        elif predictedV == 'greet':
            return [generateOutput.generateGreeting([addIn,dayPd]),0]
        elif predictedV == 'weather':
            return [generateOutput.generateWeather(),0]
        elif predictedV == 'im':
            self.name = newName
            return self.smallTalkIntent(["hi"],self.name,"")
        elif predictedV == 'name':
            return [generateOutput.generateName(addIn),0]
        else:
            return ['failed',0]
        
    #See what type of operation the user wants to do on the playlist and perform it    
    def playlistIntent(self, predictedQ, userInput):
        predictedAsList = predictedQ.split(" ")
        inputAsList = userInput.split(" ")

        listUnique = list(set(predictedAsList).symmetric_difference(set(inputAsList)))
        for label in playListIntent:
            for prompt in playListIntent[label]:
                for string in listUnique:
                    if string in prompt:
                        listUnique.remove(string)

        #regain user intended order
        final = []
        final2 = []
        for part in inputAsList:
            for part2 in listUnique:
                if(part2 == part):
                    final.append(part2)

        #Get op type
        predictedV = ""
        for k in playListIntent:
            for v in playListIntent[k]:
                if v == predictedQ:
                    predictedV=k

        if(len(final)>0):
            final2 = ' '.join(final)
        else:
            return ["Names for playlists/songs with first strings < 2 aren't allowed"]
        
        listPlaylists = playlistManager.listOfPlayLists.keys()

        existPlaylistCount = 0
        
        if predictedV == "new":
            return [self.pm.createPlaylist(final2)]
        elif predictedV == "delete":
            try:
                return [self.pm.deletePlaylist(final2)]
            except FileNotFoundError:
                return ["This playlist doesn't exist, so there is nothing for me to delete"]
        elif predictedV == "clear":
            firstFound = ""
            for v in final:
                if v in listPlaylists:
                    final.remove(v)
                    existPlaylistCount += 1
                    firstFound = v
            if(existPlaylistCount == 0):
                return ["This playlist doesn't exist! Maybe you'd want to create it?",final]#Set prompt for asking if user wants to create 
            else:
                return [self.pm.showPlaylist(firstFound),firstFound]
        elif predictedV == "show":
            firstFound = ""
            for v in final:
                if v in listPlaylists:
                    final.remove(v)
                    existPlaylistCount += 1
                    firstFound = v
            if(existPlaylistCount == 0):
                return ["This playlist doesn't exist! Maybe you'd want to create it?",final]#Set prompt for asking if user wants to create 
            else:
                return [self.pm.showPlaylist(firstFound),firstFound]
        elif predictedV == "add":
            firstFound = ""
            for v in final:
                if v in listPlaylists:
                    final.remove(v)
                    existPlaylistCount += 1
                    firstFound = v
            if(existPlaylistCount == 0):
                return ["This playlist doesn't exist! Maybe you'd want to create it?",final]#Set prompt for asking if user wants to create 
            else:
                return [self.pm.addToPlaylist(firstFound,final),firstFound]
        elif predictedV == "remove":
            firstFound = ""
            for v in final:
                if v in listPlaylists:
                    final.remove(v)
                    existPlaylistCount += 1
                    firstFound = v
            if(existPlaylistCount == 0):
                return ["This playlist doesn't exist! Maybe you'd want to create it?",final]#Set prompt for asking if user wants to create 
            else:
                return [self.pm.removeFromPlaylist(firstFound,final),firstFound]
        else:
            return generateOutput.getDefault(self.name)
        
    #See if the user wants another answer for docs with >1 answer in dataset
    def getAnotherAnswer(self, leftover, userResponse, question):
        nd = userResponse
        pnd = self.countVect.transform(nd)
        predictedV = self.classifier.predict(pnd)
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
        data = []
        labels = []
        for item in yesNoIntent:
            for string in yesNoIntent[item]:
                resp = string
                data.append(resp)
                labels.append(item)

        cb.classifier, cb.countVect = util.trainClassify(data,labels)
        cb.introSelf()