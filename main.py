"""'''
- Dijkstra's algorithm finds the least cost path on Directed Acyclic Graph (DAG).
- A 2D grid structured DAG will be used as a maze.
- Goal is to use Dijkstra to navigate from start to finish.
- Maze starts from a random point in the border and finishes at a random point in the maze.
"""

import maze

grid_length = 6
grid_graph = maze.GridGraphMaze(length=grid_length)

# check direction/number of neighbors
print('start:', grid_graph.start_coord)
print('end:', grid_graph.end_coord)
print()

st_i,st_j = grid_graph.start_coord
st_node = grid_graph.grid[st_i][st_j]

grid_graph.make_maze(st_node)

# 100 by 100 grid => 0.5 second
# 300 by 300 grid => 44 seconds

print('=============== neighbors ===============')
for i in grid_graph.grid:
    for j in i:
        print(''.join([str(x[0]) for x in j.neighbors]), end='\t')
    print()
print()

# print('===============parent direction===============')
# print()
# for i in grid_graph.grid:
#     for j in i:
#         print(j.parent_direction, end='\t')
#     print()
# print()

print('===============is visited===============')
print()
for i in grid_graph.grid:
    for j in i:
        print(j.is_visited, end=' ')
    print()
print()
print('=========================================')
