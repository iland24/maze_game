def youfool(self, coordinate):
    i,j=coordinate
    curr_node = self.grid[i][j]

    # mark current node visited
    curr_node.visited = True
    self.num_visited_nodes+=1

    # *base case1*: found end node
    if coordinate==self.end_coord:
        curr_node.neighbors.append('fin')
        print("Found end of the maze!")
        return None
    
    # *base case 2*: reach dead end
    elif self.is_deadend(curr_node):# true if deadend, else false
        if self.length**2==self.num_visited_nodes: # if all nodes have been visited
            return None
        else: # dead end but all nodes have not been visited
            print('met deadend')
            return 'backtrack'
    
    # *recursive case*
    
    # making path step
    # choose random number of unvisited neighbors
    self.choose_random_number_of_neighbors(curr_node)
    # make curr_node a parent of the neighbors of curr_node
    self.set_curr_node_as_parent_of_neighbors(curr_node)

    # deploy recursion step (only on neighbors' of curr node)
    for neigh in curr_node.neighbors:
        dir = neigh[0]
        if dir==2:
            neighboring_node=self.grid[i+1][j]
        elif dir==4:
            neighboring_node=self.grid[i][j-1]
        elif dir==6:
            neighboring_node=self.grid[i][j+1]
        else:
            neighboring_node=self.grid[i-1][j]

        make_maze_out=self.make_maze(neighboring_node.coordinate)       # ============callstack builds here until hitting base case============ 

        # some make_maze() will return 'backtrack'
        if make_maze_out=='backtrack':
            
            # check if there is unselected/unvisited adjacent node in PARENT node
            # if there is, use that coordinate to deploy makemaze(),
            # else go back further

            # get parent node using direction to parent(parent_direction)
            p_dir = neighboring_node.parent_direction

            neigh_coord_i, neigh_coord_j = neighboring_node.coordinate
            if p_dir==2:
                parent_node=self.grid[neigh_coord_i+1][neigh_coord_j]
            elif p_dir==4:
                parent_node=self.grid[neigh_coord_i][neigh_coord_j-1]
            elif p_dir==6:
                parent_node=self.grid[neigh_coord_i][neigh_coord_j+1]
            else:
                parent_node=self.grid[neigh_coord_i-1][neigh_coord_j]
            
            # find unvisited neighbors of parent node
            unvisited_neigh_ls = self.find_unvisited_neighbors(parent_node)

            if len(unvisited_neigh_ls)!=0: # if there are unvisited nodes
                for unvisited_coord in unvisited_neigh_ls:
                    print('backtracking worked: finding new path')
                    self.make_maze(unvisited_coord)                     # ============callstack builds here too until hitting base case============ 
            else:
                return 'backtrack'
            
        # else => didn't reach dead end (make_maze() returned None) => don't need to do anything