import random
qAGreetingsR1 = [
    "Here's what I found: ",
    "Here's some information about $: ",
    "Here you go: ",
]
qAGreetingsRn = [
    "other ",
    "more ",
    "additional "
]

def generateQAOutput(answer:str,question:str,roundN:int):
    outputStr = random.choice(qAGreetingsR1)
    outputStr += answer
    outputStr = (outputStr, outputStr.replace('$',question))['$' in outputStr]
    return outputStr
