import random
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

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
    "I'm not sure I quite understand $, could you rephrase that?",
    "I'm quite new and I can't do that yet. Anything else you'd like to talk about $?",
    "That's interesting, could you expand $?",
    "I'm sorry $, I couldn't understand that. Could you put it in different words?"
]

noQuestionsFoundResponses = [
    "I don't have access to that information £. Would you like to talk about anything else?",
    "I'm not quite sure £. Do you want to know about something else?",
    "I couldn't find anything about $, can I help you with anything else £?"
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

def generateWeather():
    #Below code can be found at https://open-meteo.com/en/docs?latitude=52.9536&longitude=-1.1505&forecast_days=1&timezone=GMT&hourly=&current=temperature_2m,weather_code&wind_speed_unit=mph, date last accessed: 5/12/2025
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 52.9536,
        "longitude": -1.1505,#Nottingham coords
        "current": ["temperature_2m", "weather_code"],
        "timezone": "GMT",
        "forecast_days": 1,
        "wind_speed_unit": "mph",
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]

    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_weather_code = current.Variables(1).Value()

    weather = ""
    current_weather_code = 91
    #Weather code information: www.nodc.noaa.gov/archive/arc0021/0002199/1.1/data/0-data/HTML/WMO-CODE/WMO4677.HTM
    if current_weather_code<49:
        weather = "currently dry"
        if current_weather_code == 19:
            weather += " with a tornado"
        elif current_weather_code == 17:
            weather += " but thunderstorming"
        elif 20<=current_weather_code<30:
            weather += " with precipitation in the previous hour"
        elif 30<=current_weather_code<36:
            weather += " with duststorm conditions"
        elif 36<=current_weather_code<40:
            weather += " with snowstorm conditions"
        elif 40<=current_weather_code:
            weather += " and foggy"
    elif 50<=current_weather_code<59:
        weather = "drizzling"
    elif 60<=current_weather_code<70:
        weather = "raining"
    elif 70<=current_weather_code<79:
        weather = "snowing"
    elif current_weather_code == 79:
        weather = "hailing"
    else:
        weather = "there are showers of"
        if current_weather_code <= 82 or 91<=current_weather_code<=92:
            weather += " rain"
        elif current_weather_code <= 84:
            weather += " a mixture of rain and snow"
        elif current_weather_code<=86:
            weather += " snow"
        elif current_weather_code<=90:
            weather += " hail"
        elif 93<=current_weather_code<=94:
            weather += " mixture"
        else:
            weather = "thunderstorming"
    return f"Right now in Nottingham, it is {int(current_temperature_2m)} degrees C and {weather}"