'''
Dijkstra's algorithm
-finds least cost path
-will be using Directed Acyclic Graph (DAG) structure, more specifically, a 2D grid. 
-will be implementing path finding out of a 2D grid maze 
    -new istance will generate new maze; 
    goal is to start from the border of the grid and find another way out
'''

length=3

class Node():
    def __init__(self,coordinates, neigh_n_weight=None):
        self.coordinates = coordinates
        
        if neigh_n_weight == None:
            self.neigh_n_weight=[]
        else:
            self.neigh_n_weight = neigh_n_weight

class Gridgraph():
    def __init__(self):
        self.grid = [[0 for _ in range(length)] for _ in range(length)]

    def make_grid_graph(self):
        '''
        -makes grid and inserts nodes in grid
        -initially, all nodes are connected
          8
        4   6
          2
        ^these numbers mean directions.
        They will always be in ascending order.
        2=down
        4=left
        6=right
        8=up
        '''
        for i in range(length):
            for j in range(length):
                if i==0 and j==0:
                    self.grid[i][j]=Node((i,j),[2,6])
                elif i==0 and j==length-1:
                    self.grid[i][j]=Node((i,j),[2,4])
                elif i==length-1 and j==0:
                    self.grid[i][j]=Node((i,j),[6,8])
                elif i==length-1 and j==length-1:
                    self.grid[i][j]=Node((i,j),[4,8])
                elif i==0:
                    self.grid[i][j]=Node((i,j),[2,4,6])
                elif j==0:
                    self.grid[i][j]=Node((i,j),[2,6,8])
                elif i==length-1:
                    self.grid[i][j]=Node((i,j),[2,4,8])
                elif j==length-1:
                    self.grid[i][j]=Node((i,j),[4,6,8])
                else:
                    self.grid[i][j]=Node((i,j),[2,4,6,8])

grid_graph = Gridgraph()
grid_graph.make_grid_graph()
print(grid_graph.grid)