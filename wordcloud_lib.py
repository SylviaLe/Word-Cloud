from os import read
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud, STOPWORDS
import PIL.Image
from graphics import *
from os.path import dirname, join
current_dir = dirname(__file__)


def removePunc(txt): #helper function used to remove all punctuation from given text
    punctuations = '!"“”#$%&()*+,-./:;<=>?<[\\]-_{|}-'
    for ch in txt:
        if (ch in punctuations) or (ch == '"'):
            txt = txt.replace(ch, '')

    return txt

def readStopWords(): #helper function used to remove all stopwords from given text
    swLib = open(join(current_dir, "ref/stopwords.txt"), "r")
    stopWords = swLib.read().split() #stop words is stored in a seperate file, first read it and turn it into a list of words, then do the checking

    return stopWords


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

def analyze(file):
    fileName = file
    file = open(join(current_dir, fileName), "r", encoding = "utf8")
    text = file.read().lower()

    #remove punctuation and stop words
    text = removePunc(text).split()
    stopwords = set(readStopWords())

    counts = {}
    for w in text:
        counts[w] = counts.get(w,0) + 1
    items = list(counts.items())
    items.sort()
    items.sort(key = byFreq, reverse=True)
    #print(items)

    displayWordsList = []
    for i in range(len(items)):
        words, count = items[i]
        displayWordsList.append(words)
    
    displayWords = ' '.join(displayWordsList)

    mask = np.array(PIL.Image.open(join(current_dir, 'ref/mask.png')))

    wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                font_path = 'calibri',
                stopwords = stopwords,
                colormap = 'magma',
                mask = mask,
                min_font_size = 10).generate(displayWords)
    #colormap list: https://matplotlib.org/stable/tutorials/colors/colormaps.html
  
    # plot the WordCloud image                       
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    plt.savefig('Word Cloud.png')
    
    
    #plt.show()

def main():
    win = GraphWin("Word Cloud", 500, 300)
    win.setCoords(0, 0, 300, 300)
    win.setBackground("white")

    #draw program name
    proName = Text(Point(150, 250), "Word Cloud Generator")
    proName.setFace("calibri")
    proName.setSize(30)
    proName.setTextColor("black")
    #proName.setStyle('bold')
    proName.draw(win)
    
    #draw the prompt that tell users to input the text file they want
    choicePrompt = Text(Point(150, 200), "Type in the name of the file:")
    choicePrompt.setFace('calibri')
    choicePrompt.setSize(11)
    choicePrompt.setTextColor('black')
    choicePrompt.draw(win)

    #draw entry box to type in the text file
    userInput = Entry(Point(150, 160), 50)
    userInput.setText("txt/His Last Bow.txt") #set the default file
    userInput.draw(win)

    drawButton(Point(125, 100), Point(175, 130), 'linen', "Create", win)
    #drawButton(Point(275, 275), Point(300, 300), 'red', "X", win)

    pt = win.getMouse()
    
    
    if isClick(pt, Point(125, 100), Point(175, 130), win):
        fileName = userInput.getText()
        analyze(fileName)
    win.close()



    win2 = GraphWin("Result", 800, 800)
    win2.setCoords(0, 0, 400, 400)
    win2.setBackground("white")
    res = Image(Point(200,200), 'WordCloud.png')
    res.draw(win2)
    win2.getMouse()
    win2.close()
main()
    
