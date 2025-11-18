from collections import Counter
import random
import datetime
import re
import questionsAnswers
import generateOutput
from nltk.tokenize import word_tokenize

dayPd = 'morning'
class HAIChatBotMC:
    name = ''
    questionsAnswersC = questionsAnswers.questionsAnswers()
    def __init__(self):
        self.patterns = {#Very basic response templates
            r'question':[f"Sure, what would you like to ask {self.name}?"],
            r'hello|hi|hey':[f"Hi there {self.name}, what can I help you with?",
                             f"What's up {self.name}?",
                             f"Hey {self.name}, what can I do for you today?",
                             f"Good {dayPd} {self.name}, how can I help?",
                             f"What's on your mind {self.name}"],
            r'quit|exit|bye|goodbye|that\'s all|see you': [f"Thanks for chatting {self.name}!",
                                        f"See you later {self.name}, come back whenever you like",
                                        f"Have fun {self.name}, come back soon!",
                                        f"Goodbye",
                                        f"Bye {self.name}, have a good {dayPd}"],
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
        response = self.get_response("hi")
        print(f"HAIBot: {response}")
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
                    r = random.choice(response)
                    print(f"HAIBot: {generateOutput.generateQAOutput(r,userInput,0)}")
            elif processSelect[0] == 1:
                ret = generateOutput.generateSTOutput([userInput],self.name)
                print(f"HAIBot: {ret}")
            else:
                if userInput.lower() in ['quit', 'exit', 'bye', 'goodbye', 'that\'s all', 'see you']:
                    exiting = 1
                
                response = self.get_response(userInput)
                print(f"HAIBot: {response}")
                if(exiting):
                    break

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
        dsA = self.questionsAnswersC.questionVs#Vectors of questions in qa
        dsB = []
        highQA = 0
        highQ = []
        highST = 0
        a = 0
        uIC = self.questionsAnswersC.queryLemmatize(uI)
        for item in generateOutput.intentST:
            for string in generateOutput.intentST[item]:
                dsB.append(string)
        for curQuestion in dsA:
            a = self.questionsAnswersC.getCosForPair(uIC,curQuestion)
            if a>highQA:
                highQA = a
                highQ = curQuestion
        for curSmallTalk in dsB:
            cSTL = self.questionsAnswersC.queryLemmatize(curSmallTalk)
            a = self.questionsAnswersC.getCosForPair(uIC,cSTL)
            if a>highST:
                highST = a
        print(highQA,highST)
        if max(highQA,highST) == highQA and highQA>0.7:
            return [0,highQ]
        elif max(highQA,highST) == highST and highST>0.7:
            return [1,None]
        else:
            return [-1,None]

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