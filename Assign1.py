from random import randint
import sys
import copy
from Queue import *
from operator import itemgetter

#Cell structure
cell = {'u':0,
        'd':0,
        'l':0,
        'r':0,
        'v':0,
        'g':-1.0,
        'h':-1.0,
        'f':-1.0,
        'xRow':-1,
        'yCol':-1,
        'parent':[0,0]
}

#Creating empty Maze to start with (INITIALIZING MAZE)
initialMaze=[]
finalMaze=[]
def initializeMaze(xRow,yCol):
    for i in xrange(xRow):
        finalMaze.append([])
        for j in xrange(yCol):
            finalMaze[i].append(cell.copy())

#Creating cell, initializing with actual values when maze is read from 
def createCell(u,l,d,r):
    tempCell = cell.copy()
    tempCell['u']=u
    tempCell['l']=l
    tempCell['d']=d
    tempCell['r']=r
    tempCell['v']=1
    return tempCell

def isVisited(xRow,yCol):
    if finalMaze[xRow][yCol]['v'] == 1:
        return True
    else:
        return False

#Euclidean Distance
def hueristic(xCur,yCur,xEnd,yEnd):
    return ( ((xCur - xEnd) ** (2)) + ((yCur-yEnd)**2) ) ** (0.5)

#Reading Maze from the file
def readMaze(mazeFileName):
    with open(mazeFileName, 'r') as content_file:
        content = content_file.read()
        content = content.rstrip('\n')
        contentLines = content.splitlines()
        xMax,yMax=contentLines[0].split(' ')
        initializeMaze(int(xMax),int(yMax))
        numberOfLine = contentLines[1]
        lineLength=2
        for j in range(2,int(numberOfLine)+2):
            xC,yC,walls,gar = contentLines[j].split(' ')
            u,l,d,r=[1,1,1,1]
            if 'U' in walls:
                u=0
            if 'L' in walls:
                l=0
            if 'D' in walls:
                d=0
            if 'R' in walls:
                r=0
            tempCell = createCell(u,l,d,r)
            finalMaze[int(xC)][int(yC)]=tempCell.copy()

#Generating new Maze with DFS
def generateMaze(xRow,yCol):
    xMax = xRow
    yMax = yCol
    visited=1
    xCell=0
    yCell=0
    stack=[[xCell,yCell]]
    finalMaze[xCell][yCell]['v']=1
    while visited<(xMax*yMax):
        xNeighbour=-1
        yNeighbour=-1
        neighbourTemp=[]
        #Randomly getting Random 0=Left, 1=Up, 2=Right, 3=Down
        while (xNeighbour==-1 or yNeighbour==-1):
            neighbour = randint(0, 3)
            if neighbour not in neighbourTemp:
                neighbourTemp.append(neighbour)
            if neighbour == 0:
                if yCell>0:
                    #If cell has not been visited yet. Break the wall between the cells
                    if isVisited(xCell,yCell-1) == False:
                        xNeighbour=xCell
                        yNeighbour=yCell-1
                        finalMaze[xCell][yCell]['l']=1
                        finalMaze[xNeighbour][yNeighbour]['r']=1
            elif neighbour == 1:
                if xCell>0:
                    if isVisited(xCell-1,yCell) == False:
                        yNeighbour=yCell
                        xNeighbour=xCell-1
                        finalMaze[xCell][yCell]['u']=1
                        finalMaze[xNeighbour][yNeighbour]['d']=1
            elif neighbour == 2:
                if yCell<(yMax-1):
                    if isVisited(xCell,yCell+1) == False:
                        xNeighbour=xCell
                        yNeighbour=yCell+1
                        finalMaze[xCell][yCell]['r']=1
                        finalMaze[xNeighbour][yNeighbour]['l']=1
            elif neighbour == 3:
                if xCell<(xMax-1):
                    if isVisited(xCell+1,yCell) == False:
                        yNeighbour=yCell
                        xNeighbour=xCell+1
                        finalMaze[xCell][yCell]['d']=1
                        finalMaze[xNeighbour][yNeighbour]['u']=1
            if len(neighbourTemp) == 4:
                break
        if xNeighbour==-1 or yNeighbour==-1:
            if len(stack)==0:
                break
            xCell,yCell=stack.pop()
        else: 
            xCell = xNeighbour
            yCell = yNeighbour
            finalMaze[xCell][yCell]['v']=1
            stack.append([xCell,yCell])
            visited=visited+1

#Writing Maze to the file
def writingMaze(fileName,xMax,yMax):
    fileMaze = open(fileName,"w") 
    fileMaze.write(str(xMax)+' '+str(yMax)+'\n')
    fileMaze.write(str(xMax*yMax)+'\n')
    for i in range(len(finalMaze)):
        for j in range(len(finalMaze[i])):
            fileMaze.write(str(i) + ' ' +str(j) + ' ')
            if finalMaze[i][j]['l'] == 0:
                fileMaze.write('L')
            if finalMaze[i][j]['r'] == 0:
                fileMaze.write('R')
            if finalMaze[i][j]['u'] == 0:
                fileMaze.write('U')
            if finalMaze[i][j]['d'] == 0:
                fileMaze.write('D')
            fileMaze.write(' \n')
    fileMaze.close()

#Writing discovered path into the file
def writingPath(pathMaze,fileName,xSource,ySource,xEnd,yEnd):
    xCell = xEnd
    yCell = yEnd
    tempArray = []
    #fileMaze = open(fileName,"w") 
    count = 0
    #Calculating path by backtracing parents.
    #Start with the End Cell, move to its parent, then to the parent of parent until we reach the Source Cell.
    while(True):
        count=count+1
        #fileMaze.write(str(xCell) +' ' +str(yCell)+'\n')
        tempArray.append(str(xCell)+' '+str(yCell))
        if xCell == xSource and yCell == ySource:
            break
        xCell,yCell = pathMaze[xCell][yCell]['parent']
    #fileMaze.close()
    fileMaze = open(fileName,"w")
    fileMaze.write(str(count)+'\n')
    for i in range(len(tempArray)):
        fileMaze.write(tempArray.pop()+'\n')
    fileMaze.close()

def generatePathWithDFS(xStart,yStart,xEnd,yEnd,pathFileName):
    xSource=xStart
    ySource=yStart
    xEnd=xEnd
    yEnd=yEnd
    pathMaze = copy.deepcopy(finalMaze)
    #Stack to implement DFS
    #Push source into Stack
    stack = [[xSource,ySource]]
    while(True):
        #Taking cell out of Stack
        xCell,yCell = stack.pop()
        if xCell == xEnd and yCell == yEnd:
            break
        #Push all the neighbours of the current cell into Stack
        if finalMaze[xCell][yCell]['r']==1:
            if pathMaze[xCell][yCell+1]['v']==1:
                pathMaze[xCell][yCell+1]['v']=0
                stack.append([xCell,yCell+1])
                pathMaze[xCell][yCell+1]['parent']=[xCell,yCell]

        if finalMaze[xCell][yCell]['l']==1:
            if pathMaze[xCell][yCell-1]['v']==1:
                pathMaze[xCell][yCell-1]['v']=0
                stack.append([xCell,yCell-1])
                pathMaze[xCell][yCell-1]['parent']=[xCell,yCell]

        if finalMaze[xCell][yCell]['u']==1:
            if pathMaze[xCell-1][yCell]['v']==1:
                pathMaze[xCell-1][yCell]['v']=0
                stack.append([xCell-1,yCell])
                pathMaze[xCell-1][yCell]['parent']=[xCell,yCell]

        if finalMaze[xCell][yCell]['d']==1:
            if pathMaze[xCell+1][yCell]['v']==1:
                pathMaze[xCell+1][yCell]['v']=0
                stack.append([xCell+1,yCell])
                pathMaze[xCell+1][yCell]['parent']=[xCell,yCell]

    writingPath(pathMaze,pathFileName,xSource,ySource,xEnd,yEnd)

def generatePathWithBFS(xStart,yStart,xEnd,yEnd,pathFileName):
    xSource=xStart
    ySource=yStart
    xEnd=xEnd
    yEnd=yEnd
    pathMaze = copy.deepcopy(finalMaze)
    #Queue to impletment BFS
    q = Queue()
    #Put source into Queue
    q.put([xSource,ySource])
    while(True):
        xCell,yCell = q.get()
        if xCell == xEnd and yCell == yEnd:
            break
        #Put all neighbours of current cell into Queue
        if finalMaze[xCell][yCell]['r']==1:
            if pathMaze[xCell][yCell+1]['v']==1:
                pathMaze[xCell][yCell+1]['v']=0
                q.put([xCell,yCell+1])
                pathMaze[xCell][yCell+1]['parent']=[xCell,yCell]

        if finalMaze[xCell][yCell]['l']==1:
            if pathMaze[xCell][yCell-1]['v']==1:
                pathMaze[xCell][yCell-1]['v']=0
                q.put([xCell,yCell-1])
                pathMaze[xCell][yCell-1]['parent']=[xCell,yCell]

        if finalMaze[xCell][yCell]['u']==1:
            if pathMaze[xCell-1][yCell]['v']==1:
                pathMaze[xCell-1][yCell]['v']=0
                q.put([xCell-1,yCell])
                pathMaze[xCell-1][yCell]['parent']=[xCell,yCell]

        if finalMaze[xCell][yCell]['d']==1:
            if pathMaze[xCell+1][yCell]['v']==1:
                pathMaze[xCell+1][yCell]['v']=0
                q.put([xCell+1,yCell])
                pathMaze[xCell+1][yCell]['parent']=[xCell,yCell]
                
    writingPath(pathMaze,pathFileName,xSource,ySource,xEnd,yEnd)

def generatePathWithAstarZero(xStart,yStart,xEnd,yEnd,pathFileName):
    xSource=xStart
    ySource=yStart
    xEnd=xEnd
    yEnd=yEnd
    pathMaze = copy.deepcopy(finalMaze)

    pathMaze[xSource][ySource]['xRow']=xSource
    pathMaze[xSource][ySource]['yCol']=ySource
    pathMaze[xSource][ySource]['g']=0.0
    pathMaze[xSource][ySource]['h']=0.0
    pathMaze[xSource][ySource]['f']=0.0
    #Creating open and closed lists used in AStar
    #Will keep the lists sorted to use them as priority queue
    openList=[]
    closeList=[]
    
    openList.append(pathMaze[xSource][ySource])
    while len(openList)>0:
        #Sorting openlist, so that cell with lowest 'f' is always at the start
        openList = sorted(openList, key=itemgetter('f'))
        curCell = openList.pop()

        if curCell['xRow'] == xEnd and curCell['yCol'] == yEnd:
            break
        xCell = curCell['xRow']
        yCell = curCell['yCol']
        #Putting neighbours into openList, and assigning g,h,f with g,h, and f of the current cell
        if finalMaze[xCell][yCell]['r']==1:
            tempF = curCell['g'] + 1
            sucCell = pathMaze[xCell][yCell+1]
            if sucCell['f']>tempF or sucCell['f']==-1.0:
                sucCell['g']=curCell['g'] + 1
                sucCell['h'] = 0
                sucCell['f'] = tempF
                sucCell['xRow']=curCell['xRow']
                sucCell['yCol']=curCell['yCol']+1
                sucCell['parent']=[xCell,yCell]
                openList.append(sucCell)

        if finalMaze[xCell][yCell]['l']==1:
            tempF = curCell['g'] + 1
            sucCell = pathMaze[xCell][yCell-1]
            if sucCell['f']>tempF or sucCell['f']==-1.0:
                sucCell['g']=curCell['g'] + 1
                sucCell['h'] = 0
                sucCell['f'] = tempF
                sucCell['xRow']=curCell['xRow']
                sucCell['yCol']=curCell['yCol']-1
                sucCell['parent']=[xCell,yCell]
                openList.append(sucCell)

        if finalMaze[xCell][yCell]['u']==1:
            tempF = curCell['g'] + 1
            sucCell = pathMaze[xCell-1][yCell]
            if sucCell['f']>tempF or sucCell['f']==-1.0:
                sucCell['g']=curCell['g'] + 1
                sucCell['h'] = 0
                sucCell['f'] = tempF
                sucCell['xRow']=curCell['xRow']-1
                sucCell['yCol']=curCell['yCol']
                sucCell['parent']=[xCell,yCell]
                openList.append(sucCell)

        if finalMaze[xCell][yCell]['d']==1:
            tempF = curCell['g'] + 1
            sucCell = pathMaze[xCell+1][yCell]
            if sucCell['f']>tempF or sucCell['f']==-1.0:
                sucCell['g']=curCell['g'] + 1
                sucCell['h'] = 0
                sucCell['f'] = tempF
                sucCell['xRow']=curCell['xRow']+1
                sucCell['yCol']=curCell['yCol']
                sucCell['parent']=[xCell,yCell]
                openList.append(sucCell)
        closeList.append(curCell)
    writingPath(pathMaze,pathFileName,xSource,ySource,xEnd,yEnd)
    
def generatePathWithAstarEculidean(xStart,yStart,xEnd,yEnd,pathFileName):
    xSource=xStart
    ySource=yStart
    xEnd=xEnd
    yEnd=yEnd
    pathMaze = copy.deepcopy(finalMaze)
    pathMaze[xSource][ySource]['xRow']=xSource
    pathMaze[xSource][ySource]['yCol']=ySource
    pathMaze[xSource][ySource]['g']=0.0
    pathMaze[xSource][ySource]['h']=0.0
    pathMaze[xSource][ySource]['f']=0.0
    openList=[]
    closeList=[]
    openList.append(pathMaze[xSource][ySource])
    while len(openList)>0:
        openList = sorted(openList, key=itemgetter('f'))
        curCell = openList.pop()

        if curCell['xRow'] == xEnd and curCell['yCol'] == yEnd:
            break
        xCell = curCell['xRow']
        yCell = curCell['yCol']
        if finalMaze[xCell][yCell]['r']==1:
            #Using hueristic for 'h' instead of 0 now. 
            tempF = curCell['g'] + 1 + curCell['h'] + hueristic(xCell, yCell, xEnd, yEnd)
            sucCell = pathMaze[xCell][yCell+1]
            if sucCell['f']>tempF or sucCell['f']==-1.0:
                sucCell['g']=curCell['g'] + 1
                sucCell['h'] = curCell['h'] + hueristic(xCell, yCell, xEnd, yEnd)
                sucCell['f'] = tempF
                sucCell['xRow']=curCell['xRow']
                sucCell['yCol']=curCell['yCol']+1
                sucCell['parent']=[xCell,yCell]
                openList.append(sucCell)

        if finalMaze[xCell][yCell]['l']==1:
            tempF = curCell['g'] + 1+curCell['h'] + hueristic(xCell, yCell, xEnd, yEnd)
            sucCell = pathMaze[xCell][yCell-1]
            if sucCell['f']>tempF or sucCell['f']==-1.0:
                sucCell['g']=curCell['g'] + 1
                sucCell['h'] = curCell['h'] + hueristic(xCell, yCell, xEnd, yEnd)
                sucCell['f'] = tempF
                sucCell['xRow']=curCell['xRow']
                sucCell['yCol']=curCell['yCol']-1
                sucCell['parent']=[xCell,yCell]
                openList.append(sucCell)

        if finalMaze[xCell][yCell]['u']==1:
            tempF = curCell['g'] + 1 +curCell['h'] + hueristic(xCell, yCell, xEnd, yEnd)
            sucCell = pathMaze[xCell-1][yCell]
            if sucCell['f']>tempF or sucCell['f']==-1.0:
                sucCell['g']=curCell['g'] + 1
                sucCell['h'] = curCell['h'] + hueristic(xCell, yCell, xEnd, yEnd)
                sucCell['f'] = tempF
                sucCell['xRow']=curCell['xRow']-1
                sucCell['yCol']=curCell['yCol']
                sucCell['parent']=[xCell,yCell]
                openList.append(sucCell)

        if finalMaze[xCell][yCell]['d']==1:
            tempF = curCell['g'] + 1 +curCell['h'] + hueristic(xCell, yCell, xEnd, yEnd)
            sucCell = pathMaze[xCell+1][yCell]
            if sucCell['f']>tempF or sucCell['f']==-1.0:
                sucCell['g']=curCell['g'] + 1 
                sucCell['h'] = curCell['h'] + hueristic(xCell, yCell, xEnd, yEnd)
                sucCell['f'] = tempF
                sucCell['xRow']=curCell['xRow']+1
                sucCell['yCol']=curCell['yCol']
                sucCell['parent']=[xCell,yCell]
                openList.append(sucCell)
        closeList.append(curCell)
    writingPath(pathMaze,pathFileName,xSource,ySource,xEnd,yEnd)

    
#Similar to AStar, but Euclidean Distance as the hueristic, and Dynamic Weight to find more promising direction
def generatePathWithAstarDynamic(xStart,yStart,xEnd,yEnd,pathFileName):
    xSource=xStart
    ySource=yStart
    xEnd=xEnd
    yEnd=yEnd
    pathMaze = copy.deepcopy(finalMaze)
    pathMaze[xSource][ySource]['xRow']=xSource
    pathMaze[xSource][ySource]['yCol']=ySource
    pathMaze[xSource][ySource]['g']=0.0
    pathMaze[xSource][ySource]['h']=0.0
    pathMaze[xSource][ySource]['f']=0.0
    #Using distance between Source, and End as optimal Solution length 'N'
    N = hueristic(xSource, ySource, xEnd, yEnd)
    #E is usually very small, so we will keep it at 0.5
    E = 0.5
    #d Will be x-distance of node getting explored from the source, initially zero as starting from source itself
    d = 0.0
    openList=[]
    closeList=[]
    openList.append(pathMaze[xSource][ySource])
    while len(openList)>0:
        openList = sorted(openList, key=itemgetter('f'))
        curCell = openList.pop()

        if curCell['xRow'] == xEnd and curCell['yCol'] == yEnd:
            break
        xCell = curCell['xRow']
        yCell = curCell['yCol']
        if finalMaze[xCell][yCell]['r']==1:
            #Using hueristic for 'h' 
            #Using Dynamice Weight
            #We get this from section 2.3.2 of weighted A* Search
            tempF = curCell['g'] + 1 + curCell['h'] + hueristic(xCell, yCell, xEnd, yEnd) + (E*(1-(xCell-xSource)/N))*hueristic(xCell, yCell, xEnd, yEnd)
            sucCell = pathMaze[xCell][yCell+1]
            if sucCell['f']>tempF or sucCell['f']==-1.0:
                sucCell['g']=curCell['g'] + 1
                sucCell['h'] = curCell['h'] + hueristic(xCell, yCell, xEnd, yEnd)
                sucCell['f'] = tempF
                sucCell['xRow']=curCell['xRow']
                sucCell['yCol']=curCell['yCol']+1
                sucCell['parent']=[xCell,yCell]
                openList.append(sucCell)

        if finalMaze[xCell][yCell]['l']==1:
            tempF = curCell['g'] + 1 + curCell['h'] + hueristic(xCell, yCell, xEnd, yEnd) + (E*(1-(xCell-xSource)/N))*hueristic(xCell, yCell, xEnd, yEnd)
            sucCell = pathMaze[xCell][yCell-1]
            if sucCell['f']>tempF or sucCell['f']==-1.0:
                sucCell['g']=curCell['g'] + 1
                sucCell['h'] = curCell['h'] + hueristic(xCell, yCell, xEnd, yEnd)
                sucCell['f'] = tempF
                sucCell['xRow']=curCell['xRow']
                sucCell['yCol']=curCell['yCol']-1
                sucCell['parent']=[xCell,yCell]
                openList.append(sucCell)

        if finalMaze[xCell][yCell]['u']==1:
            tempF = curCell['g'] + 1 + curCell['h'] + hueristic(xCell, yCell, xEnd, yEnd) + (E*(1-(xCell-xSource)/N))*hueristic(xCell, yCell, xEnd, yEnd)
            sucCell = pathMaze[xCell-1][yCell]
            if sucCell['f']>tempF or sucCell['f']==-1.0:
                sucCell['g']=curCell['g'] + 1
                sucCell['h'] = curCell['h'] + hueristic(xCell, yCell, xEnd, yEnd)
                sucCell['f'] = tempF
                sucCell['xRow']=curCell['xRow']-1
                sucCell['yCol']=curCell['yCol']
                sucCell['parent']=[xCell,yCell]
                openList.append(sucCell)

        if finalMaze[xCell][yCell]['d']==1:
            tempF = curCell['g'] + 1 + curCell['h'] + hueristic(xCell, yCell, xEnd, yEnd) + (E*(1-(xCell-xSource)/N))*hueristic(xCell, yCell, xEnd, yEnd)
            sucCell = pathMaze[xCell+1][yCell]
            if sucCell['f']>tempF or sucCell['f']==-1.0:
                sucCell['g']=curCell['g'] + 1 
                sucCell['h'] = curCell['h'] + hueristic(xCell, yCell, xEnd, yEnd)
                sucCell['f'] = tempF
                sucCell['xRow']=curCell['xRow']+1
                sucCell['yCol']=curCell['yCol']
                sucCell['parent']=[xCell,yCell]
                openList.append(sucCell)
        closeList.append(curCell)
    writingPath(pathMaze,pathFileName,xSource,ySource,xEnd,yEnd)
    
def generatePathWithFringe(xStart,yStart,xEnd,yEnd,pathFileName):
    xSource=xStart
    ySource=yStart
    xEnd=xEnd
    yEnd=yEnd
    pathMaze = copy.deepcopy(finalMaze)
    pathMaze[xSource][ySource]['xRow']=xSource
    pathMaze[xSource][ySource]['yCol']=ySource
    pathMaze[xSource][ySource]['g']=0.0
    pathMaze[xSource][ySource]['h']=0.0
    pathMaze[xSource][ySource]['f']=0.0

    #Calculating huerestic (distance) of all nodes from source node
    for i in xrange(10):
        for j in xrange(10):
            d = hueristic(xSource,ySource,i,j)
            pathMaze[i][j]['f']=d
    #NowList and LaterList required in Fringe Search
    nowList=[]
    laterList=[]
    visited=[]
  
    fCurrent=1.0
    nowList.append(pathMaze[xSource][ySource])
    found = 0
    count = 0
 
    while(found==0):
        while(len(nowList)>0):
            curCell = nowList.pop()
            xCell = curCell['xRow']
            yCell = curCell['yCol']
            
            if curCell['f']>fCurrent:
                laterList.append(curCell)
            else:
                visited.append([xCell,yCell])
                if xCell == xEnd and yCell == yEnd:
                    found=1
                    break
                if finalMaze[xCell][yCell]['r']==1:
                    if [xCell,yCell+1] not in visited:
                        pathMaze[xCell][yCell+1]['parent']=[xCell,yCell]
                        pathMaze[xCell][yCell+1]['xRow']=xCell
                        pathMaze[xCell][yCell+1]['yCol']=yCell+1
                        nowList.append(pathMaze[xCell][yCell+1])

                if finalMaze[xCell][yCell]['l']==1:
                    if [xCell,yCell-1] not in visited:
                        pathMaze[xCell][yCell-1]['parent']=[xCell,yCell]
                        pathMaze[xCell][yCell-1]['xRow']=xCell
                        pathMaze[xCell][yCell-1]['yCol']=yCell-1
                        nowList.append(pathMaze[xCell][yCell-1])

                if finalMaze[xCell][yCell]['u']==1:
                    if [xCell-1,yCell] not in visited:
                        pathMaze[xCell-1][yCell]['parent']=[xCell,yCell]
                        pathMaze[xCell-1][yCell]['xRow']=xCell-1
                        pathMaze[xCell-1][yCell]['yCol']=yCell
                        nowList.append(pathMaze[xCell-1][yCell])

                if finalMaze[xCell][yCell]['d']==1:
                    if [xCell+1,yCell] not in visited:
                        pathMaze[xCell+1][yCell]['parent']=[xCell,yCell]
                        pathMaze[xCell+1][yCell]['xRow']=xCell+1
                        pathMaze[xCell+1][yCell]['yCol']=yCell
                        nowList.append(pathMaze[xCell+1][yCell])
        #Updating fInitial
        fCurrent=fCurrent+1.0
        nowList = copy.deepcopy(laterList)
        laterList=[]
    writingPath(pathMaze,pathFileName,xSource,ySource,xEnd,yEnd)

if len(sys.argv) == 4:
    xRow = int(sys.argv[1])
    yCol = int(sys.argv[2])
    mazeFile = sys.argv[3]
    initializeMaze(xRow,yCol)
    print ('Generating Maze')
    generateMaze(xRow,yCol)
    print ('Maze Stored in ' + mazeFile)
    writingMaze(mazeFile,xRow,yCol)
elif len(sys.argv) == 8:
    func = sys.argv[1]
    mazeFile = sys.argv[2]
    xStart = int(sys.argv[3])
    yStart = int(sys.argv[4])
    xEnd = int(sys.argv[5])
    yEnd = int(sys.argv[6])
    pathFile = sys.argv[7]
    readMaze(mazeFile)
    if func == 'DFS':
        print 'Calculating Path with DFS'
        generatePathWithDFS(xStart,yStart,xEnd,yEnd,pathFile)
        print ('Path stored in '+pathFile)
    elif func == 'BFS':
        print 'Calculating Path with BFS'
        generatePathWithBFS(xStart,yStart,xEnd,yEnd,pathFile)
        print ('Path stored in '+pathFile)
    elif func == 'AStarZero':
        print 'Calculating Path with AStarZero'
        generatePathWithAstarZero(xStart,yStart,xEnd,yEnd,pathFile)
        print ('Path stored in '+pathFile)
    elif func == 'AStarEuclidean':
        print 'Calculating Path with AStarEuclidean'
        generatePathWithAstarEculidean(xStart,yStart,xEnd,yEnd,pathFile)
        print ('Path stored in '+pathFile)
    elif func == 'AStarDynamic':
        print 'Calculating Path with AstarDynamic'
        generatePathWithAstarDynamic(xStart,yStart,xEnd,yEnd,pathFile)
        print ('Path stored in '+pathFile)
    elif func == 'Fringe':
        print 'Calculating Path with Fringe'
        generatePathWithFringe(xStart,yStart,xEnd,yEnd,pathFile)
        print ('Path stored in '+pathFile)
    else:
        print "Method undefined, please use DFS, BFS, AStarZero, AStarEuclidean,AStarDynamic or Fringe"
else:
    print "Argument Mismismatch"
    print "USAGE:"
    print "Maze Generation: python Assign1.py nrRows nrCols mazeFile"
    print "Maze Search:     Python method mazeFile rstart cstart rend cend pathFile"