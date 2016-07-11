import random
import csv

# list of 227 popular English adjectives
with open('dict/english-adjectives.csv', 'rb') as adjectivesfile:
    adjectivesreader = list(csv.reader(adjectivesfile, delimiter=','))
lengthofadjectivefile = len(adjectivesreader)

# list of 484 popular English nouns
with open('dict/english-nouns.csv', 'rb') as nounssfile:
    nounsreader = list(csv.reader(nounssfile, delimiter=','))
lengthofnounsfile = len(nounsreader)

positionadj = random.randrange(0, lengthofadjectivefile)
anadjective = adjectivesreader[positionadj]
positionnoun = random.randrange(0, lengthofnounsfile)
anoun = nounsreader[positionnoun]
twowords = " ".join(anadjective[0:1]) + " " + " ".join(anoun[0:1])
randomcomment = "What a " + twowords + " of an exercise dude!"

print randomcomment
