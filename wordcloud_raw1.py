#Sylvia Le
#10/27/19
#file: wordcloud(3).py
#This program create a word cloud from the text file the user input in

from graphics import *
from random import *
from tkinter import messagebox

def isOverlap(square, squList):    #given the first rectangle and a list of other rectangles, compare the the given rect with each of the rect in the list to see if overlap
    x, y, a, b = getCornerCoords(square)
    for item in squList:
        x1, y1, a1, b1 = getCornerCoords(item)

        if not (a < x1 or a1 < x or b < y1 or b1 < y):
            return True

    return False

def getCornerCoords(square):
    x1 = square.getP1().getX()
    y1 = square.getP1().getY()
    x2 = square.getP2().getX()
    y2 = square.getP2().getY()

    return x1, y1, x2, y2 
    
    
def removePunc(txt): #helper function used to remove all punctuation from given text
    punctuations = '!"“”#$%&()*+,-./:;<=>?<[\\]-_{|}-'
    for ch in txt:
        if (ch in punctuations) or (ch == '"'):
            txt = txt.replace(ch, '')

    return txt

def removeStopWords(wordList): #helper function used to remove all stopwords from given text
    swLib = open("ref/stopwords.txt", "r")
    stopWords = swLib.read().split() #stop words is stored in a seperate file, first read it and turn it into a list of words, then do the checking

    newWords = []
    for w in wordList:
        if w not in stopWords:
            newWords.append(w)   #if a word is not a stop word, it goes into the empty list declared before the loop.

    return newWords

def byFreq(pair):   #helper function used to sort the the word by frequency
    return pair[1]

def drawButton(pt1,pt2,color,labelText,window):  #Funtion to draw button
    button=Rectangle(pt1,pt2)
    button.setFill(color)
    button.draw(window)

    centerX = (pt1.getX()+pt2.getX())/2
    centerY = (pt1.getY()+pt2.getY())/2
    
    #Put label on button
    label = Text(Point(centerX,centerY),labelText)
    label.setFill("black")
    label.setSize(11)
    label.draw(window)

def isClick(pt, corner1, corner2, window):   #Function to check if user click a button
    x1 = corner1.getX()
    x2 = corner2.getX()
    y1 = corner1.getY()
    y2 = corner2.getY()

    if (pt.getX() >= x1 and pt.getX() <= x2) and pt.getY() >= y1 and pt.getY() <= y2:  #check if the mouse click is within the button
        return True
    else:
        return False
    
def getInput(window):
    #draw program name
    proName = Text(Point(300, 550), "Word Cloud Generator")
    proName.setFace("calibri")
    proName.setSize(30)
    proName.setTextColor("black")
    proName.setStyle('bold')
    proName.draw(window)
    
    #draw the prompt that tell users to input the text file they want
    choicePrompt = Text(Point(300, 505), "Type in the name of the file:")
    choicePrompt.setFace('arial')
    choicePrompt.setSize(11)
    choicePrompt.setTextColor('black')
    choicePrompt.draw(window)

    #draw entry box to type in the text file
    userInput = Entry(Point(300, 475), 50)
    userInput.setText("txt/His Last Bow.txt") #set the default file
    userInput.draw(window)

    drawButton(Point(250, 415), Point(350, 450), 'linen', "Create Word Cloud", window)
    pt = window.getMouse()
    
    if isClick(pt, Point(250, 415), Point(350, 450), window):
        fileName = userInput.getText()
        return fileName

def analyze(window):
    fileName = getInput(window) #call getInput function, save the value it returns to fileName variable
    file = open(fileName, "r", encoding = "utf8")
    text = file.read().lower()

    #remove punctuation and stop words
    text = removePunc(text)         
    words = text.split()
    newWords = removeStopWords(words)

    counts = {}
    for w in newWords:
        counts[w] = counts.get(w,0) + 1
    items = list(counts.items())
    items.sort()
    items.sort(key = byFreq, reverse=True)

    displayWords = []
    for i in range(25):
        words, count = items[i]
        displayWords.append(words)
    return displayWords

def WCGraphics(window):

    periBoxes = [Rectangle(Point(250, 415), Point(350, 450))]
    i = 0
    displayWords = analyze(window)
    for w in displayWords:
        x = randrange(50, 550)      #first, generate a random point
        y = randrange(15, 380)
        pt = Point(x, y)

        height = 55 - i  #determine the size of the word, base on its frequency (which, the position in the list already reflect it)
        width = float(len(w))

        calcHeight = ((1.5 * height) - 1)//2   #calculate the estimated height and width of the box that entrap the word. Number will be explained in documentation
        calcWidth = (width * calcHeight) / 2.4

        corner1 = Point(x - calcWidth, y - calcHeight)  #calculate the two corner of the box 
        corner2 = Point(x + calcWidth, y + calcHeight)

        periBox = Rectangle(corner1, corner2)

        while isOverlap(Rectangle(corner1, corner2), periBoxes) == True:   #check if the box overlap, if yes, create another box and check again(ALSO WHERE THE PROBLEM ARISE T>T)
            x = randrange(50, 550)
            y = randrange(15, 380)
            pt = Point(x, y)

            height = 55 - i 
            width = float(len(w))

            calcHeight = ((1.5 * height) - 1)//2
            calcWidth = (width * calcHeight)/2.4

            corner1 = Point(x - calcWidth, y - calcHeight)
            corner2 = Point(x + calcWidth, y + calcHeight)

            periBox = Rectangle(corner1, corner2)

        #periBox.draw(window)
        periBoxes.append(periBox)
        
        r = randrange(255)
        g = randrange(255)
        b = randrange(255)
        color = color_rgb(r, g, b)
        
        word = Text(pt, w)
        word.setTextColor(color)
        word.setFace('calibri')
        word.setSize(height)
        word.draw(window)

        i += 1

def main():
    win = GraphWin("Word Cloud", 800, 600)
    win.setCoords(0, 0, 600, 600)
    win.setBackground("white")

    WCGraphics(win)

    win.getMouse()
    win.close()
main()
