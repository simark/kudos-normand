import random
import csv


def get_random_comment():
    # list of popular English adjectives
    with open('dict/english-adjectives.csv') as adjectivesfile:
        adjectivesreader = list(csv.reader(adjectivesfile, delimiter=','))
    lengthofadjectivefile = len(adjectivesreader)

    # list of popular English nouns
    with open('dict/english-nouns.csv') as nounssfile:
        nounsreader = list(csv.reader(nounssfile, delimiter=','))
    lengthofnounsfile = len(nounsreader)

    positionadj = random.randrange(0, lengthofadjectivefile)
    anadjective = adjectivesreader[positionadj]
    positionnoun = random.randrange(0, lengthofnounsfile)
    anoun = nounsreader[positionnoun]
    twowords = " ".join(anadjective[0:1]) + " " + " ".join(anoun[0:1])
    randomcomment = "What a " + twowords + " of an exercise dude!"

    return randomcomment
