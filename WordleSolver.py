#!usr/bin/env python3

"""
Code written by Mattias
On 07/02/2022
The aim of this program is to solve wordle puzzle
sources :
https://www.powerlanguage.co.uk/wordle/
"""

import collections

import os
import sys

accentDict = {
    "a" : ["à", "â", "ä"],
    "e" : ["é", "ê", "è", "ë"],
    "u" : ["ù"],
    "o" : ["ö"],
    "c" : ["ç"],
}

def noAccent(word):
    noAccentWord = ""
    for c in word:
        accentChanged = False
        for i in accentDict:
            if c in accentDict[i]:
                noAccentWord += i
                accentChanged = True
        if not accentChanged:
            noAccentWord += c
    return(noAccentWord)

class WordleSolver(object):
    """
    A simple wordle solver
    """
    def __init__(self, langDictName, size=5):
        # Importing list of words from the english dictionnary
        # (only take len of 5)
        self.size = size
        self.langDictName = langDictName

        f = open(langDictName)
        self.Words = []
        for w in f.readlines():
            if(len(w) == size+1): # words have a \n at the end
                self.Words.append(w[:-1].lower())
        f.close()

        # removing accents
        self.Words = [noAccent(w) for w in self.Words]


        # Taking away proper nouns
        if "abdul" in self.Words:
            self.Words.remove("abdul")

    def update(self, testWord, answer):
        """
        answer is a string of 0 1 and 2
        0 = gray = the letter is not in the word
        1 = yellow = the letter is in the word but not on that place
        2 = the letter is in the word on that place
        """
        for i in range(self.size):
            if(answer[i] == "0"):
                # deleting words having that letter
                self.Words = [w for w in self.Words
                              if testWord[i] not in w]
            elif(answer[i] == "1"):
                # deleting words having that letter at that place
                self.Words = [w for w in self.Words
                              if testWord[i] != w[i]]
                # deleting words not having that letter
                self.Words = [w for w in self.Words
                              if testWord[i] in w]
            elif(answer[i] == "2"):
                # deleting words not having that letter at that place
                self.Words = [w for w in self.Words
                              if testWord[i] == w[i]]

    def newTest(self):
        # capped max
        l = len(self.Words)
        if l == 0:
            return("Sorry I don't have any matching word")
        i = 0
        maxIndex = 0
        maxNbLetters = 0
        maxed = False
        print(self.Words)
        while not maxed and i < l-1:
            nbLetters = len(collections.Counter(self.Words[i]))
            if nbLetters > maxNbLetters:
                maxNbLetters = nbLetters
                maxIndex = i
            if nbLetters == 5:
                maxed = True
            i += 1
        return(self.Words[maxIndex])

def main(parameters):
    WS = WordleSolver(parameters[1])
    c = True
    os.system('cls' if os.name == 'nt' else 'clear')
    print("0 = gray\n1 = yellow\n2 = green")
    print("user input exemple : 01102\n")
    while c:
        testWord = WS.newTest()
        print("test : " + testWord)
        answer = input("> ")
        if(len(answer) != 5 or answer == WS.size*"2"):
            c = False
        else:
            WS.update(testWord, answer)
    return(0)


if __name__ == "__main__":
    main(sys.argv)
