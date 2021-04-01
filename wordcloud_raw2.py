#Sylvia Le
#10/27/19
#file: wordcloud(3).py
#This program create a word cloud from the text file the user input in

from graphics import *
from random import *
from tkinter import messagebox
    
    
def removePunc(txt): #helper function used to remove all punctuation from given text
    punctuations = '!"“”#$%&()*+,-./:;<=>?<[\\]-_{|}-'
    for ch in txt:
        if (ch in punctuations):
            txt = txt.replace(ch, '')

    return txt

def removeStopWords(wordList): #helper function used to remove all stopwords from given text
    swLib = open("ref/stopwords.txt", "r")
    stopWords = swLib.read().split()  #stop words is stored in a seperate file, first read it and turn it into a list of words, then do the checking

    newWords = [w for w in wordList if not w in stopWords]  #short form, this or the things under
##    for w in wordList:
##        if not w in stopWords:
##            newWords.append(w)  #if a word is not a stop word, it goes into the empty list declared before the loop.
##            

    return newWords

def byFreq(pair):  #helper function used to sort the the word by frequency
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
    #message box to print program introduction
    messagebox.showinfo("Information","This program generate word cloud. Type in the file name, click the button and let the program do its job")

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

    #count the frequency of words
    counts = {}
    for w in newWords:
        counts[w] = counts.get(w,0) + 1

    #begin sorting
    items = list(counts.items())
    items.sort() #first sort by alphabetical order
    items.sort(key = byFreq, reverse=True) #then sort by frequency

    displayWords = []
    if len(items) > 30:
        for i in range(30):
            words, count = items[i]
            displayWords.append(words)
        return displayWords
    else:  #in this case, the length of the file is < 30 words, so set the number of looping time to the file's length
        for i in range(len(items)):
            words, count = items[i]
            displayWords.append(words)
        return displayWords

        
def WCGraphics(window):
    displayWords = analyze(window) #call this function to get the list of words to display

    #read the documentation for more info
    points = []
    selectedPoints = []
    i = 0
    #create a grid of points as a centre point of theh words
    for x in range (50, 560, 100):
        for y in range(40, 390, 35):
            points.append(Point(x, y)) #append the point to a list to choose from (slot)

    #for each word in the list, randomly choose a a point from the list. If it's a point already been chosen, choose again    
    for word in displayWords:
        index = randrange(50-i)
        pt = points[index]
        points.pop(index)
##        while pt in selectedPoints:
##            index = randrange(60)
##            pt = points[index]
##
##        selectedPoints.append(pt) #make a list of 'omitted points' that should not be chosen again

        #make the size decrease as the frequency decrease. Generate random color for the word
        size = 35 - i
        r = randrange(255)
        g = randrange(255)
        b = randrange(255)
        color = color_rgb(r, g, b)
            
        word = Text(pt, word)
        word.setTextColor(color)
        word.setFace('calibri')
        word.setSize(size)
        word.draw(window)

        i += 1
        
def main():
    #create graphic window
    win = GraphWin("Word Cloud", 800, 600)
    win.setCoords(0, 0, 600, 600)
    win.setBackground("white")

    #since wcgraphics() call (by chain) all the other function, just need to call wcgraphics now
    WCGraphics(win)

    #messagebox to tell user how to quit
    messagebox.showinfo("Information","Click anywhere to close the program")
    win.getMouse()
    win.close()
main()
