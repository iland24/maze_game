import matplotlib.pyplot as plt
import maze

grid_length = 30
grid_graph = maze.GridGraphMaze(length=grid_length)

# check direction/number of neighbors
print('start:', grid_graph.start_coord)
print('end:', grid_graph.end_coord)
print()

st_i, st_j = grid_graph.start_coord
st_node = grid_graph.grid[st_i][st_j]

grid_graph.make_maze(st_node, path_length=50)

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

# print('===============is visited===============')
# print()
# for i in grid_graph.grid:
#     for j in i:
#         print(j.is_visited, end=' ')
#     print()
# print()
print('=========================================')

grid_graph.draw_maze(background_c_val=0, wall_c_val=1, start_c_val=1, end_c_val=1)
# Create a sample 2D array of values
data = grid_graph.drawing_board

# Create a heatmap plot
plt.imshow(data, cmap='summer', vmin=0, vmax=1)
# Blues, Purples, Greens, cividis, summer
# plt.colorbar()  # Add a color bar to the plot
plt.axis('off')
# Display the plot
plt.show()
# plt.savefig('summer_maze.png')