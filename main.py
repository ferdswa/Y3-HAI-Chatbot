import random
import datetime
import re
import questionsAnswers
import generateOutput

dayPd = 'morning'
class HAIChatBotMC:
    name = ''
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
        questionsAnswersC = questionsAnswers.questionsAnswers()
        print("Hello and welcome to Maxim Carr's HAI Chatbot")
        print("Please enter a prompt below")
        print("-" * 50)
        self.name = self.getUserName()
        self.__init__()#Reinitialise to grab name
        response = self.get_response("hi")
        print(f"HAIBot: {response}")#If finish within time, replace with better intent matcher.
        while True:#Main loop. FIXME: See todo below
            exiting = 0
            userInput = input(f"{self.name}: ")
            #TODO: Reorder to do NL intent matching
            if questionsAnswersC.testQuestion(userInput):
                dfAnswers = questionsAnswersC.answerQuestion(userInput)
                if 'none' in dfAnswers['documents'].values:
                    ret = generateOutput.generateSTOutput(dfAnswers['questions'],1,self.name)#Use a classifier to find if this is a 'name' question, a 'general' question, or a 'capability' question 
                    if ret == 'failed':#Doesn't match any pattern
                        ret = random.choice(self.noQuestionsFoundResponses)
                        ret = (ret, ret.replace('$',userInput))['$' in ret]
                        print(f"HAIBot: {ret}")
                    else:#Smalltalk intent matching works
                        print(f"HAIBot: {ret}")
                else:
                    response = dfAnswers['answers'].values
                    r = random.choice(response)
                    print(f"HAIBot: {generateOutput.generateQAOutput(r,userInput,0)}")
            else:
                if userInput.lower() in ['quit', 'exit', 'bye', 'goodbye', 'that\'s all', 'see you']:
                    exiting = 1
                
                response = self.get_response(userInput)
                print(f"HAIBot: {response}")
                if(exiting):
                    break

    def getUserName(self):
        print("HAIBot: Please tell me your name to personalise your response")
        n = input("You: ")
        if(len(n)==0):
            print("HAIBot: Names cannot be zero characters long.")
            self.getUserName()
        else:
            return n

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