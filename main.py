import os
import csv
import random
import pandas as pd
import datetime
import re
import testIntent

dayPd = 'morning'
class HAIChatBotMC:
    name = ''
    def __init__(self):
        self.patterns = {#Use regex strings and randoms to generate a more 'alive' feel
            r'question':[f"Sure, what would you like to ask {self.name}?"],
            r'hello|hi|hey':[f"Hi there {self.name}, what can I help you with?",
                             f"What's up {self.name}?",
                             f"Hey {self.name}, what can I do for you today?",
                             f"Good {dayPd} {self.name}, how can I help?",
                             f"What's on your mind {self.name}"],
            r'quit|exit|bye|goodbye|that\'s all|see you': [f"Thanks for chatting {self.name}!",
                                        f"See you later {self.name}, come back whenever you like",
                                        f"Have fun {self.name}",
                                        f"Goodbye",
                                        f"Bye {self.name}, have a good {dayPd}"],
        }
        self.defaultResponses = [#Fallback option
            "I'm not sure I quite understand, could you rephrase that?",
            "I'm quite new and I can't do that yet. What else would you like to talk about",
            "That's interesting, could you expand?",
            "I'm sorry, I couldn't understand that. Could you put it in different words?"
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
        while True:#Main loop. I want the pattern to be transaction->question/answer->small talk->hello/goodbye
            exiting = 0
            user_input = input(f"{self.name}: ")

            if(testIntent.testQuestion(user_input)):
                #question-answer goes here
                questArray = user_input.lower().split()
                dfAnswers = testIntent.answerQuestion(questArray)
                response = dfAnswers['answers'].values
                r = random.choice(response)
                print(r)
            else:
                if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye', 'that\'s all', 'see you']:
                    exiting = 1
                
                response = self.get_response(user_input)
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