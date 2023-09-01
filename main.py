import maze

grid_length = 6
grid_graph \
    = maze.GridGraphMaze(length=grid_length)

# check initialization
for i in grid_graph.grid:
    for j in i:
        print(j.coordinate, end='')
    print()
print()

print('start:', grid_graph.start_coord)
print('end:', grid_graph.end_coord)
print()

st_i, st_j = grid_graph.start_coord
st_node = grid_graph.grid[st_i][st_j]

grid_graph.make_maze(st_node)

print()
for i in grid_graph.grid:
    for j in i:
        print(j.neighbors, end='')
    print()
print()

print(grid_graph.cumulative_node_cnt)
