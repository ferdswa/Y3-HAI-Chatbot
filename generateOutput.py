import random

qAGreetingsR1 = [
    "Here's what I found, ",
    "Here's some information about $: ",
    "Here you go, ",
    "Of course, ",
    ""
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
qANoAdditionalInfo = [
    "OK, no worries",
    "No problem, what else would you like to talk about",
    "Sure, anything else you'd like to talk about $?"
]
goodbyeMsgs = ["Thanks for chatting $!",
    "See you later $, come back whenever you like",
    "Have fun $, come back soon!",
    "Goodbye",
    "Bye $, have a good £"]
greetings = ["Hi there $, what can I help you with?", "What's up $?","Hey $, what can I do for you today?","Good £ $, how can I help?","What's on your mind $"]

defaultResponses = [#Fallback option
    f"I'm not sure I quite understand $, could you rephrase that?",
    f"I'm quite new and I can't do that yet. Anything else you'd like to talk about $?",
    f"That's interesting, could you expand $?",
    f"I'm sorry $, I couldn't understand that. Could you put it in different words?"
]

noQuestionsFoundResponses = [
    f"I don't have access to that information £. Would you like to talk about anything else?",
    f"I'm not quite sure £. Do you want to know about something else?",
    f"I couldn't find anything about $, can I help you with anything else £?"
]


def generateQAOutput(answer:list,question:str):#Upgrade this. Currently outputs random choice if >1 answer. TODO: Make it add only new information. See todo in questionsAnswers
    outputStr = random.choice(qAGreetingsR1)
    select = random.choice(answer)
    outputStr += select
    answer = list(filter(lambda x: x != select,answer))#Filter array to exclude current output string
    outputStr = (outputStr, outputStr.replace('$',question))['$' in outputStr]
    return outputStr,answer

def generateNoMoreAnswers(addIn):
    outputStr = random.choice(qANoAdditionalInfo)
    outputStr = (outputStr, outputStr.replace('$',addIn))['$' in outputStr]
    return outputStr
    
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
    a = (a,a.replace('£', addIn[1]))['£' in a]
    return a

def generateGreeting(addIn):
    a = random.choice(greetings)
    a = (a,a.replace('$', addIn[0]))['$' in a]
    a = (a,a.replace('£', addIn[1]))['£' in a]
    return a

def getDefault(addIn):
    ret = random.choice(defaultResponses)
    ret = (ret, ret.replace('$',addIn))['$' in ret]
    return ret

def generateQuestionUnAnswerable(addIn):
    a = random.choice(noQuestionsFoundResponses)
    a = (a,a.replace('$', addIn[0]))['$' in a]
    a = (a,a.replace('£', addIn[1]))['£' in a]
    return a