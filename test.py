from graphics import * 
def isOverlap(square, squList): 
    x, y, a, b = getCornerCoords(square)
    for item in squList:
        x1, y1, a1, b1 = getCornerCoords(item)

        if (x>x1 and x<a1) and (y>y1 and y<b1):
            print('True')
            return True
        elif (x1>x and x1<a) and (y1>y and y1<b):
            print('True')    
            return True
        elif (x<x1 and x>a1) and (y<y1 and y>b1):
            print('True')
            return True
        elif (x1<x and x1>a) and (y1<y and y1>b):
            print('True')
            return True
        else:
            print('False')
            return False

def getCornerCoords(square):
    x1 = square.getP1().getX()
    y1 = square.getP1().getY()
    x2 = square.getP2().getX()
    y2 = square.getP2().getY()

    return x1, y1, x2, y2 
    
def main():
    rec = Rectangle(Point(3,3), Point(5, 5))
    recList = [Rectangle(Point(9,9), Point(18, 17)), Rectangle(Point(30, 50), Point(40, 60)), Rectangle(Point(10, 10), Point(12, 13))]
    isOverlap(rec, recList)

#Rectangle(Point(0, 0), Point(4, 4)), Rectangle(Point(4, 4), Point(0, 6)), Rectangle(Point(4, 4), Point(6, 0)), Rectangle(Point(4, 4), Point(8, 8))
main()
    
    
