import random
import string

def generateSeed(length=6):
    characters = string.ascii_letters + string.digits 
    random_string = ''.join(random.choices(characters, k=length))
    return random_string

def generateQuiz(seed=generateSeed):
    #ici faire la génération du quiz 
    #flemme atm de bdd 
    return {"seed": seed, "themes": [{"theme": "meme", "questions": [{"question": "qui?", "answer": "coubeh"}]}, {"theme": "histoire", "questions": [{"question": "qua?", "answer": "coubeh"}]}]}
