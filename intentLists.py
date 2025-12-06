intentST = {
    'gen' : ["how are you", "howre you", "how are you doing", "how ya doin", "how ya doin", "how is everything", "how is everything going", "hows everything going"], #Part of a list found: https://stackoverflow.com/questions/51575924/list-of-greetings-phrases-in-english-for-nlp-task
    'capability' : ['what can you do', 'what can you do for me', 'what tasks can you do for me', "what things can you do for me", "what can you help me with", "what can you do to help me", "what can you do to assist me", "what can you do to help me out"],
    'name': ['what is my name', 'whats my name', 'what is my name', 'whats my name'],
    'quit': ['quit', 'exit', 'bye', 'goodbye', 'thats all', 'see you'],
    'greet': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening'],
    'weather': ['whats the weather', 'hows the weather', 'what is the weather','what is the weather', 'what is the weather like'],
    'im': ['call me', 'my name is', 'my names', 'change my name to']
}

playListIntent = {
    'new': ["id like to add a new playlist", "create a new playlist", "add playlist", "make a new", "create a new", "new playlist", "add a new", "new", "create new", "make new", "add new", "create a new playlist called"],
    'add': ["id like to add a song to", "add to", "add a song to", "add a song to my playlist", "add to my playlist", "add"],
    'remove': ["remove from", "id like to remove from", "id like to delete from", "i want to remove from", "delete from"],
    'delete': ['delete', 'remove', 'delete playlist'],
    'clear': ['clear', 'wipe', 'delete all from', 'delete all in', 'clear all from', 'wipe all from', 'wipe all in', "clear playlist", "wipe playlist"],
    'shuffle': ['shuffle','randomise'],
    'show': ['what songs are in', "what is in", "whats in", "what does contain", "show songs in", "show"]
}

yesNoIntent ={
    'yes' : ["yes","yeah","sure","of course","ok","y"],
    'no' : ["no","nah", "no thanks", "no thank you", "i'm good", "n"]
}