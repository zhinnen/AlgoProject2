import sys
import numpy as np
import itertools
from collections import defaultdict

#WRITTEN BY ZACHARY HINNEN

class GraphTraversal:
    def __init__(self): # default dictionary to store graph
        self.graph = defaultdict(list)
        self.rows = 0
        self.cols = 0
        self.input = sys.argv[1]   #file name for inputted
        self.output = sys.argv[2]  #file name for output

    def addEdge(self, u, v):
        self.graph[u].append(v) #Add edge from vertex u to v
    
    def north(self, i, j, dp, val):
        for k in range(0,i+1,1): #N: moves up, alters i witk k
            if (dp[i-k][j][2] != val):
                self.addEdge(dp[i][j],dp[i-k][j])
    
    def east(self, i, j, dp, val):
        for k in range(0,self.cols-j,1):#E: moves right, alters J with k
            if (dp[i][j+k][2] != val):
                self.addEdge(dp[i][j],dp[i][j+k])

    def south(self, i, j, dp, val):
        for k in range(0,self.rows-i,1):#S: moves down, alters i with k
            if (dp[i+k][j][2] != val):
                self.addEdge(dp[i][j],dp[i+k][j])

    def west(self, i, j, dp, val):
        for k in range(0,j+1,1):#W: moves left, alters J with k
            if (dp[i][j-k][2] != val):
                self.addEdge(dp[i][j],dp[i][j-k])

    def northEast(self, i, j, dp, val):
        for k in range(0,min(i+1,self.cols-j),1):#NE: moves diagonally to the upper right, changes I and j with k
                if (dp[i-k][j+k][2] != val):
                    self.addEdge(dp[i][j],dp[i-k][j+k])

    def southEast(self, i, j, dp, val):
        for k in range(0,min(self.rows-i,self.cols-j),1):#SE: moves diagonally to the lower right, changes I and j with k
            if (dp[i+k][j+k][2] != val):
                self.addEdge(dp[i][j],dp[i+k][j+k])

    def southWest(self, i, j, dp, val):
        for k in range(0,min(self.rows-i,j+1),1):#SW: moves diagonally to the lower left, changes I and j with k
            if (dp[i+k][j-k][2] != val):
                self.addEdge(dp[i][j],dp[i+k][j-k])

    def northWest(self, i, j, dp, val):
        for k in range(0,min(i+1,j+1),1):#NW: moves diagonally to the upper left, changes I and j with k
            if (dp[i-k][j-k][2] != val):
                self.addEdge(dp[i][j],dp[i-k][j-k])

    def DFSUtil(self, dp): #generate the graph using input of matrix rows and columns and outputs nodes and edges       
        for i, j in itertools.product(range(self.rows), range(self.cols)): #the code work off of i and j to iterate through the rows and columns
            dir = dp[i][j][3] #getting direciton of the dp
            val = dp[i][j][2] #getting comparsion value for the dp to add edge or not
            if dir == 'N':
                self.north(i, j, dp, val)
            elif dir == 'E':
                self.east(i, j, dp, val)
            elif dir == 'S':
                self.south(i, j, dp, val)
            elif dir == 'W':
                self.west(i, j, dp, val)
            elif dir == 'NE':
                self.northEast(i, j, dp, val)
            elif dir == 'SE':
                self.southEast(i, j, dp, val)
            elif dir == 'SW':
                self.southWest(i, j, dp, val)
            elif dir == 'NW':
                self.northWest(i, j, dp, val)
            else:
                break   

    def DFS(self, first, last): #finding path by dfs, input the graph and starting vertex. Outputs the path
        queue = [(first, [first])] #add first vertex to the queue
        visited = set()
        while True: #traverse through queue and get vertex
            (vertex, path) = queue.pop()
            if vertex not in visited:
                for neighbor in self.graph[vertex]: #recur for all vertices
                    queue.append((neighbor, path + [neighbor])) #append neighbor onto the queue
                if vertex == last:
                    print("path found")
                    return path
                else:
                    pass
                visited.add(vertex)
                

    def mapping(self, arr):
        arr[self.rows-1][self.cols-1] = 'O-O'
        dp = [ [0 for k in range(self.rows)] for q in range(self.cols)] #initialize a rxc matrix dp
        for i, j in itertools.product(range(self.rows), range(self.cols)):  #transfer elements from arr to dp, with it's index, color and direction
           dp[i][j] = (i, j, arr[i][j].split('-')[0], arr[i][j].split('-')[1])  
        return dp

    def filereader(self): #code reads in the 
        file = open(self.input,'r')
        data = file.readline()
        split_data = data.split()
        m = [[w for w in line.split()] for line in file]
        arr = np.array(m)

        self.rows = int(split_data[0])
        self.cols = int(split_data[1])
        return arr

    def filewriter(self, Path):
        out = open(self.output,'a')
        out.truncate(0)
        for i in range(len(Path)-1): #outputs the distance for x and y.
            num = max(abs(Path[i+1][0]-Path[i][0]),abs(Path[i+1][1]-Path[i][1]))
            dir = Path[i][3]
            out.write(str(num)+dir)
            out.write(' ')
    
    def Main(self):
        arr = self.filereader()
        dp = self.mapping(arr)
        self.DFSUtil(dp) 
        Path = self.DFS(dp[0][0], dp[self.rows-1][self.cols-1])
        self.filewriter(Path)

if __name__ == "__main__":
    GT = GraphTraversal()
    GT.Main()
    
