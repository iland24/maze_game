import random
import numpy as np
import matplotlib.pyplot as plt


class Node:
    def __init__(self, coordinate, neighbors=None):
        """
        coordinate: node's coordinate in the grid

        initialize is_visited as False

        If node is start node,
        self.is_start=True, else self.is_start=None

        If node is end node,
        self.is_end=True, else self.is_end=None

        neighbors: list of neighbors / directions node can access
        Each element is a tuple of direction and random weight that ranges [0:9]
        """
        self.coordinate = coordinate
        self.is_visited = False
        # each node can have many children but only one parent node
        self.parent_direction = None
        self.is_start = False
        self.is_end = False

        if neighbors is None:
            self.neighbors = []
        else:
            self.neighbors = neighbors

    def mark_as_start_node(self):
        """
        marks is_start True if
        the node is start node
        """
        self.is_start = True

    def mark_as_end_node(self):
        """
        marks is_end True if
        the node is start node
        """
        self.is_end = True


# noinspection PyUnresolvedReferences
class GridGraphMaze:
    def __init__(self, length):
        """
        Makes grid and insert Node obj in grid
        Marks start and end nodes
        Directions/neighbors are represented using four numbers:
          8
        4   6
          2
        """
        # make length x length grid
        self.length = length
        self.grid = [[0 for _ in range(length)] for _ in range(length)]
        self.q = []
        # self.q = deque()
        # self.q = QAndRandom()

        # list of visited / unvisited nodes
        self.visited_nodes_ls = []
        self.unvisited_nodes_ls = []

        # choose start/end points at a side of the grid
        self.start_coord, self.end_coord = self.choose_start_end_coord()

        # variables related to drawing maze
        self.drawing_board = None
        self.wall_color_val = None
        self.background_color_val = None
        self.start_color_val = None
        self.end_color_val = None

        # insert nodes with coordinate in grid
        for i in range(length):
            for j in range(length):
                self.grid[i][j] = Node((i, j))
                self.unvisited_nodes_ls.append(self.grid[i][j])
                # mark start & end in Node
                if self.grid[i][j].coordinate[0] == self.start_coord[0] and \
                        self.grid[i][j].coordinate[1] == self.start_coord[1]:
                    self.grid[i][j].mark_as_start_node()

                if self.grid[i][j].coordinate[0] == self.end_coord[0] and \
                        self.grid[i][j].coordinate[1] == \
                        self.end_coord[1]:
                    self.grid[i][j].mark_as_end_node()

    @staticmethod
    def rand_weight():
        return random.choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])[0]

    def choose_start_end_coord(self):
        start, end = random.choice([
            ((0, random.choice(range(self.length))), (self.length - 1, random.choice(range(self.length)))),
            ((self.length - 1, random.choice(range(self.length))), (0, random.choice(range(self.length)))),
            ((random.choice(range(self.length)), 0), (random.choice(range(self.length)), self.length - 1)),
            ((random.choice(range(self.length)), self.length - 1), (random.choice(range(self.length)), 0)),
        ])
        return start, end

    def find_accessible_directions_of_node(self, node):
        i, j = node.coordinate
        # adjacent node directions
        if i == 0 and j == 0:
            accessible_directions = [2, 6]
        elif i == 0 and j == self.length - 1:
            accessible_directions = [2, 4]
        elif i == self.length - 1 and j == 0:
            accessible_directions = [6, 8]
        elif i == self.length - 1 and j == self.length - 1:
            accessible_directions = [4, 8]
        elif i == 0:
            accessible_directions = [2, 4, 6]
        elif j == 0:
            accessible_directions = [2, 6, 8]
        elif i == self.length - 1:
            accessible_directions = [4, 6, 8]
        elif j == self.length - 1:
            accessible_directions = [2, 4, 8]
        else:
            accessible_directions = [2, 4, 6, 8]
        return accessible_directions

    def set_node_as_parent_of_neighbors(self, node):
        print('node is start?', node.coordinate, node.is_start)
        # no need to set end node or deadend node as parent of other nodes
        if node.is_end:
            return
        elif not node.is_start and self.is_deadend(node):
            return
        print('node is start?', node.coordinate, node.is_start)

        i, j = node.coordinate
        for neigh in node.neighbors:
            dir = neigh[0]

            if dir == 2:
                self.grid[i + 1][j].parent_direction = 8
            elif dir == 4:
                self.grid[i][j - 1].parent_direction = 6
            elif dir == 6:
                self.grid[i][j + 1].parent_direction = 4
            elif dir == 8:
                self.grid[i - 1][j].parent_direction = 2

    def is_deadend(self, node):
        """
        checks if node is a deadend:
        = all adjacent nodes are visited
        """
        acc_dir = self.find_accessible_directions_of_node(node)
        print('acc_dir: ', acc_dir)
        print('node.parent: ', node.parent_direction)
        acc_dir.remove(node.parent_direction)  # exclude dir current node came from (parent direction)

        n_directions = len(acc_dir)
        n_visited_neigh_but_not_in_my_neigh = 0
        i, j = node.coordinate

        my_neigh = [neigh[0] for neigh in node.neighbors]

        for direction in acc_dir:
            if direction not in my_neigh:
                if direction == 2:
                    if self.grid[i + 1][j].is_visited:
                        n_visited_neigh_but_not_in_my_neigh += 1
                elif direction == 4:
                    if self.grid[i][j - 1].is_visited:
                        n_visited_neigh_but_not_in_my_neigh += 1
                elif direction == 6:
                    if self.grid[i][j + 1].is_visited:
                        n_visited_neigh_but_not_in_my_neigh += 1
                else:
                    if self.grid[i - 1][j].is_visited:
                        n_visited_neigh_but_not_in_my_neigh += 1

        if n_visited_neigh_but_not_in_my_neigh == n_directions:
            return True
        else:
            return False

    def find_out_if_node_has_zero_unvisited_neighbors(self, node):
        """
        Finds out if all neighbors of current node have been visited
        :param node: Node() instance
        :return: True if all neigh are visited else False
        """
        accessible_directions = self.find_accessible_directions_of_node(node)
        i, j = node.coordinate
        n_visited_neigh = 0
        for direction in accessible_directions:
            if direction == 2:
                if self.grid[i + 1][j].is_visited:
                    n_visited_neigh += 1
            elif direction == 4:
                if self.grid[i][j - 1].is_visited:
                    n_visited_neigh += 1
            elif direction == 6:
                if self.grid[i][j + 1].is_visited:
                    n_visited_neigh += 1
            else:
                if self.grid[i - 1][j].is_visited:
                    n_visited_neigh += 1

        if n_visited_neigh == len(accessible_directions):
            return True
        else:
            return False

    def find_unvisited_nodes_from_visited_and_add_to_q(self, node):
        """
        given a node, finds unvisited (previously unselected) neighbor node,
        add direction & weight of newly added unvisited node in node,
        add parent_direction to newly added unvisited node

        returns True if node with unvisited direction is added to q else False
        """
        # if encounter a node that has only been added as neighbor, and no neighbor added yet
        if len(node.neighbors) == 0:
            return False

        accessible_directions = self.find_accessible_directions_of_node(node)

        if not node.is_start:
            accessible_directions.remove(node.parent_direction)

        i, j = node.coordinate
        for direction in accessible_directions:
            if direction == 2:
                if not self.grid[i + 1][j].is_visited:
                    node.neighbors.append((2, self.rand_weight()))
                    self.grid[i + 1][j].is_visited = True
                    self.grid[i + 1][j].parent_direction = 8
                    self.q.append(self.grid[i + 1][j])
                    self.unvisited_nodes_ls.remove(self.grid[i + 1][j])
                    return True
            elif direction == 4:
                if not self.grid[i][j - 1].is_visited:
                    node.neighbors.append((4, self.rand_weight()))
                    self.grid[i][j - 1].is_visited = True
                    self.grid[i][j - 1].parent_direction = 6
                    self.q.append(self.grid[i][j - 1])
                    self.unvisited_nodes_ls.remove(self.grid[i][j - 1])
                    return True
            elif direction == 6:
                if not self.grid[i][j + 1].is_visited:
                    node.neighbors.append((6, self.rand_weight()))
                    self.grid[i][j + 1].is_visited = True
                    self.grid[i][j + 1].parent_direction = 4
                    self.q.append(self.grid[i][j + 1])
                    self.unvisited_nodes_ls.remove(self.grid[i][j + 1])
                    return True
            else:
                if not self.grid[i - 1][j].is_visited:
                    node.neighbors.append((8, self.rand_weight()))
                    self.grid[i - 1][j].is_visited = True
                    self.grid[i - 1][j].parent_direction = 2
                    self.q.append(self.grid[i - 1][j])
                    self.unvisited_nodes_ls.remove(self.grid[i - 1][j])
                    return True
        return False

    def choose_random_number_of_neighbors(self, node):
        """
        Checks if accessible nodes(unvisited) are visited or not
        and adds only accessible nodes to node's neighbors randomly
        1. end 면 fin 넣어줌
        2. deadend 면 deadend 넣어줌
        """
        if node.is_end:
            node.neighbors = ['fin']
            return None

        # if node is deadend, don't add any directions (but it needs parent)
        if not node.is_start and self.is_deadend(node):
            node.neighbors = ['deadend']
            return None

        accessible_directions = self.find_accessible_directions_of_node(node)

        # if node is NOT starting node, remove direction toward curr node's parent in accessible_directions!
        # (shouldn't be able to go back toward parent)
        if not node.is_start:
            p_dir = node.parent_direction
            if p_dir == 2:
                accessible_directions.remove(2)
            elif p_dir == 4:
                accessible_directions.remove(4)
            elif p_dir == 6:
                accessible_directions.remove(6)
            else:
                accessible_directions.remove(8)

        #  delete visited nodes from directions to avoid sampling them
        i, j = node.coordinate
        for direction in accessible_directions[:]:
            if direction == 2:
                if self.grid[i + 1][j].is_visited:
                    accessible_directions.remove(2)
            elif direction == 4:
                if self.grid[i][j - 1].is_visited:
                    accessible_directions.remove(4)
            elif direction == 6:
                if self.grid[i][j + 1].is_visited:
                    accessible_directions.remove(6)
            else:
                if self.grid[i - 1][j].is_visited:
                    accessible_directions.remove(8)

        # now choose random number of directions
        if len(accessible_directions) == 3:
            n_dir = random.choices([1, 2, 3], weights=[0.79, 0.2, 0.01])[0]
        elif len(accessible_directions) == 2:
            n_dir = random.choices([1, 2], weights=[0.95, 0.05])[0]
        else:
            n_dir = 1

        if n_dir == 1:
            sampled_direction = random.sample(accessible_directions, n_dir)[0]
            # this one direction => return next node right away

            # mark neighbors as visited ahead of time (here) to prevent collision
            if sampled_direction == 2:
                if not self.grid[i + 1][j].is_visited:
                    node.neighbors.append((2, self.rand_weight()))
                    self.grid[i + 1][j].is_visited = True
                    self.visited_nodes_ls.append(self.grid[i + 1][j])
                    self.unvisited_nodes_ls.remove(self.grid[i + 1][j])
                    self.set_node_as_parent_of_neighbors(node)
                    self.set_node_as_parent_of_neighbors(node)
                    return self.grid[i + 1][j]
            elif sampled_direction == 4:
                if not self.grid[i][j - 1].is_visited:
                    node.neighbors.append((4, self.rand_weight()))
                    self.grid[i][j - 1].is_visited = True
                    self.visited_nodes_ls.append(self.grid[i][j - 1])
                    self.unvisited_nodes_ls.remove(self.grid[i][j - 1])
                    self.set_node_as_parent_of_neighbors(node)
                    return self.grid[i][j - 1]
            elif sampled_direction == 6:
                if not self.grid[i][j + 1].is_visited:
                    node.neighbors.append((6, self.rand_weight()))
                    self.grid[i][j + 1].is_visited = True
                    self.visited_nodes_ls.append(self.grid[i][j + 1])
                    self.unvisited_nodes_ls.remove(self.grid[i][j + 1])
                    self.set_node_as_parent_of_neighbors(node)
                    return self.grid[i][j + 1]
            else:
                if not self.grid[i - 1][j].is_visited:
                    node.neighbors.append((8, self.rand_weight()))
                    self.grid[i - 1][j].is_visited = True
                    self.visited_nodes_ls.append(self.grid[i - 1][j])
                    self.unvisited_nodes_ls.remove(self.grid[i - 1][j])
                    self.set_node_as_parent_of_neighbors(node)
                    return self.grid[i - 1][j]

        else:
            sampled_direction = random.sample(accessible_directions, n_dir)[0]
            accessible_directions.remove(sampled_direction)
            # reserved direction(s) => append to list for random selection
            # sampled direction => return as next node right away

            for reserved_direction in accessible_directions:
                if reserved_direction == 2:
                    if not self.grid[i + 1][j].is_visited:
                        node.neighbors.append((2, self.rand_weight()))
                        self.grid[i + 1][j].is_visited = True
                        self.visited_nodes_ls.append(self.grid[i + 1][j])
                        self.unvisited_nodes_ls.remove(self.grid[i + 1][j])
                        self.q.append(self.grid[i + 1][j])
                elif reserved_direction == 4:
                    if not self.grid[i][j - 1].is_visited:
                        node.neighbors.append((4, self.rand_weight()))
                        self.grid[i][j - 1].is_visited = True
                        self.visited_nodes_ls.append(self.grid[i][j - 1])
                        self.unvisited_nodes_ls.remove(self.grid[i][j - 1])
                        self.q.append(self.grid[i][j - 1])
                elif reserved_direction == 6:
                    if not self.grid[i][j + 1].is_visited:
                        node.neighbors.append((6, self.rand_weight()))
                        self.grid[i][j + 1].is_visited = True
                        self.visited_nodes_ls.append(self.grid[i][j + 1])
                        self.unvisited_nodes_ls.remove(self.grid[i][j + 1])
                        self.q.append(self.grid[i][j + 1])
                else:
                    if not self.grid[i - 1][j].is_visited:
                        node.neighbors.append((8, self.rand_weight()))
                        self.grid[i - 1][j].is_visited = True
                        self.visited_nodes_ls.append(self.grid[i - 1][j])
                        self.unvisited_nodes_ls.remove(self.grid[i - 1][j])
                        self.q.append(self.grid[i - 1][j])

            # mark neighbors as visited ahead of time (here) to prevent collision
            if sampled_direction == 2:
                if not self.grid[i + 1][j].is_visited:
                    node.neighbors.append((2, self.rand_weight()))
                    self.grid[i + 1][j].is_visited = True
                    self.visited_nodes_ls.append(self.grid[i + 1][j])
                    self.unvisited_nodes_ls.remove(self.grid[i + 1][j])
                    self.set_node_as_parent_of_neighbors(node)
                    return self.grid[i + 1][j]
            elif sampled_direction == 4:
                if not self.grid[i][j - 1].is_visited:
                    node.neighbors.append((4, self.rand_weight()))
                    self.grid[i][j - 1].is_visited = True
                    self.visited_nodes_ls.append(self.grid[i][j - 1])
                    self.unvisited_nodes_ls.remove(self.grid[i][j - 1])
                    self.set_node_as_parent_of_neighbors(node)
                    return self.grid[i][j - 1]
            elif sampled_direction == 6:
                if not self.grid[i][j + 1].is_visited:
                    node.neighbors.append((6, self.rand_weight()))
                    self.grid[i][j + 1].is_visited = True
                    self.visited_nodes_ls.append(self.grid[i][j + 1])
                    self.unvisited_nodes_ls.remove(self.grid[i][j + 1])
                    self.set_node_as_parent_of_neighbors(node)
                    return self.grid[i][j + 1]
            else:
                if not self.grid[i - 1][j].is_visited:
                    node.neighbors.append((8, self.rand_weight()))
                    self.grid[i - 1][j].is_visited = True
                    self.visited_nodes_ls.append(self.grid[i - 1][j])
                    self.unvisited_nodes_ls.remove(self.grid[i - 1][j])
                    self.set_node_as_parent_of_neighbors(node)
                    return self.grid[i - 1][j]

    def make_maze(self, start_node):
        node = start_node
        self.q.append(node)
        node.is_visited = True
        self.visited_nodes_ls.append(node)
        self.unvisited_nodes_ls.remove(node)

        path_counter = 1
        while len(self.q) > 0:
            print('node coord: ', node.coordinate, node.is_start)
            # making paths
            if path_counter > 7:
                node = random.sample(self.q, 1)[0]
                self.q.remove(node)  # need to sample deadend & end in order to label them in node's neighbors
                node = self.choose_random_number_of_neighbors(node)
                if node is None:
                    path_counter = 100
                    continue
                path_counter += 1
            else:
                if node.is_start:
                    self.q.remove(node)
                # choose random number of unvisited neighbors
                node = self.choose_random_number_of_neighbors(node)
                path_counter += 1
                if node is None:
                    path_counter = 100
                    continue

            # if meet end node but there's still unvisited nodes in grid,
            # choose a new node from visited nodes to find node with unchosen accessible neighbor
            if node.neighbors[0] == 'fin' or node.neighbors[0] == 'deadend':
                if len(self.unvisited_nodes_ls) != 0:
                    random.shuffle(self.visited_nodes_ls)
                    for visited_node in self.visited_nodes_ls[:]:
                        # remove node if there are no unvisited neighbors (= fully explored node)
                        if self.find_out_if_node_has_zero_unvisited_neighbors(visited_node):
                            self.visited_nodes_ls.remove(visited_node)
                        else:
                            # skip searching end node from visited_nodes_ls
                            # (don't want to search new route from end node)
                            if visited_node.is_end:
                                continue
                            self.find_unvisited_nodes_from_visited_and_add_to_q(visited_node)

    def draw_maze(self, background_c_val, wall_c_val, start_c_val, end_c_val):
        self.wall_color_val = wall_c_val
        self.background_color_val = background_c_val
        self.start_color_val = start_c_val
        self.end_color_val = end_c_val

        self.drawing_board = np.full((self.length * 8, self.length * 8), self.background_color_val)

        x_axis = np.linspace(0, self.length - 1, self.length)
        y_axis = np.linspace(0, self.length - 1, self.length)
        x_grid, y_grid = np.meshgrid(x_axis, y_axis)

        # go to each cell/node of grid and draw on an 8 by 8 square
        for x, y in zip(x_grid.flatten(), y_grid.flatten()):
            x = int(x)
            y = int(y)

            node = self.grid[x][y]

            if node.is_start:
                self.decide_entrance_direction_of_maze_from_start_node(node, x, y)
                parent_dir = node.parent_direction
                self.color_start(x, y)
            elif node.is_end:
                self.color_end(x, y)
                parent_dir = node.parent_direction
            else:
                parent_dir = node.parent_direction

            directions = set([neigh[0] for neigh in node.neighbors])

            # 15 different drawing patterns for each cell
            if 'f' in directions or 'd' in directions:  # (ㄷ), f=fin, d=deadend
                if parent_dir == 2:
                    self.draw_pattern1(x, y)
                elif parent_dir == 4:
                    self.draw_pattern2(x, y)
                elif parent_dir == 6:
                    self.draw_pattern3(x, y)
                elif parent_dir == 8:
                    self.draw_pattern4(x, y)
            # 2 ways cell/node
            elif len(directions) == 1:
                one_dir = list(directions)[0]
                # (ㅡ, ㅣ)
                if (one_dir == 2 and parent_dir == 8) or (one_dir == 8 and parent_dir == 2):
                    self.draw_pattern5(x, y)
                elif (one_dir == 4 and parent_dir == 6) or (one_dir == 6 and parent_dir == 4):
                    self.draw_pattern6(x, y)
                # (ㄱ, ㄴ)
                elif (one_dir == 2 and parent_dir == 6) or (one_dir == 6 and parent_dir == 2):
                    self.draw_pattern7(x, y)
                elif (one_dir == 2 and parent_dir == 4) or (one_dir == 4 and parent_dir == 2):
                    self.draw_pattern8(x, y)
                elif (one_dir == 4 and parent_dir == 8) or (one_dir == 8 and parent_dir == 4):
                    self.draw_pattern9(x, y)
                elif (one_dir == 6 and parent_dir == 8) or (one_dir == 8 and parent_dir == 6):
                    self.draw_pattern10(x, y)
                else:
                    print("여기서 에러 났음1: ", node.coordinate)
                    print("neighbors: ", node.neighbors)
                    print("parent_dir: ", parent_dir)
            # 3 ways cell/node
            elif len(directions) == 2:
                if (({2, 4}.issubset(directions) and parent_dir == 6) or
                        ({2, 6}.issubset(directions) and parent_dir == 4) or
                        ({4, 6}.issubset(directions) and parent_dir == 2)):
                    self.draw_pattern11(x, y)
                elif (({2, 4}.issubset(directions) and parent_dir == 8) or
                      ({2, 8}.issubset(directions) and parent_dir == 4) or
                      ({4, 8}.issubset(directions) and parent_dir == 2)):
                    self.draw_pattern12(x, y)
                elif (({4, 6}.issubset(directions) and parent_dir == 8) or
                      ({4, 8}.issubset(directions) and parent_dir == 6) or
                      ({6, 8}.issubset(directions) and parent_dir == 4)):
                    self.draw_pattern13(x, y)
                elif (({2, 6}.issubset(directions) and parent_dir == 8) or
                      ({2, 8}.issubset(directions) and parent_dir == 6) or
                      ({6, 8}.issubset(directions) and parent_dir == 2)):
                    self.draw_pattern14(x, y)
                else:
                    print("여기서 에러 났음2: ", node.coordinate)
                    print("neighbors: ", node.neighbors)
                    print("parent_dir: ", parent_dir)
            # 4 ways cell/node
            elif (({4, 6, 8}.issubset(directions) and parent_dir == 2) or
                  ({2, 6, 8}.issubset(directions) and parent_dir == 4) or
                  ({2, 4, 8}.issubset(directions) and parent_dir == 6) or
                  ({2, 4, 6}.issubset(directions) and parent_dir == 8)):
                self.draw_pattern15(x, y)
            # Shouldn't be any other types of cells/nodes
            else:
                print("여기서 에러 났음3: ", node.coordinate)
                print("neighbors: ", node.neighbors)
                print("parent_dir: ", parent_dir)

        # mode='constant' parameter indicates that we want to pad with constant values.
        self.drawing_board = np.pad(self.drawing_board, ((1, 1), (1, 1)), mode='constant',
                                    constant_values=self.wall_color_val)
        self.rid_of_padding_at_start_node()

    def color_start(self, x_start, y_start):
        x_end = (x_start + 1) * 8
        y_end = (y_start + 1) * 8
        x_start = x_start * 8
        y_start = y_start * 8
        for x in range(x_start + 2, x_end - 2):
            for y in range(y_start + 2, y_end - 2):
                # if x!=x_start and x!=x_end-1:
                #     if y!=y_start and y!=y_end-1:
                self.drawing_board[x][y] = self.start_color_val

    def color_end(self, x_start, y_start):
        x_end = (x_start + 1) * 8
        y_end = (y_start + 1) * 8
        x_start = x_start * 8
        y_start = y_start * 8
        for x in range(x_start + 2, x_end - 2):
            for y in range(y_start + 2, y_end - 2):
                self.drawing_board[x][y] = self.end_color_val

    def decide_entrance_direction_of_maze_from_start_node(self, start_node, x_start, y_start):
        """
        entrance direction here refers to parent direction of start node
        """
        if x_start == 0 and y_start == 0:
            # top_left=True
            start_node.parent_direction = [4, 8]
        elif x_start == 0 and y_start == self.length - 1:
            # top_right=True
            start_node.parent_direction = [6, 8]
        elif x_start == self.length - 1 and y_start == 0:
            # bottom_left=True
            start_node.parent_direction = [2, 4]
        elif x_start == self.length - 1 and y_start == self.length - 1:
            # bottom_right=True
            start_node.parent_direction = [2, 6]
        elif x_start == 0:
            # top=True
            start_node.parent_direction = [8]
        elif x_start == self.length - 1:
            # bottom=True
            start_node.parent_direction = [2]
        elif y_start == 0:
            # left=True
            start_node.parent_direction = [4]
        elif y_start == self.length - 1:
            # right=True
            start_node.parent_direction = [6]

        # pick one entrance direction (from node perspective)
        start_node.parent_direction = random.sample(start_node.parent_direction, 1)[0]

    def draw_pattern1(self, x_start, y_start):
        x_end = (x_start + 1) * 8
        y_end = (y_start + 1) * 8
        x_start = x_start * 8
        y_start = y_start * 8
        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                if x == x_start:
                    self.drawing_board[x][y] = self.wall_color_val
                elif y == y_start or y == (y_end - 1):
                    self.drawing_board[x][y] = self.wall_color_val

    def draw_pattern2(self, x_start, y_start):
        x_end = (x_start + 1) * 8
        y_end = (y_start + 1) * 8
        x_start = x_start * 8
        y_start = y_start * 8
        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                if x == x_start or x == (x_end - 1):
                    self.drawing_board[x][y] = self.wall_color_val
                elif y == (y_end - 1):
                    self.drawing_board[x][y] = self.wall_color_val

    def draw_pattern3(self, x_start, y_start):
        x_end = (x_start + 1) * 8
        y_end = (y_start + 1) * 8
        x_start = x_start * 8
        y_start = y_start * 8
        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                if x == x_start or x == (x_end - 1):
                    self.drawing_board[x][y] = self.wall_color_val
                elif y == y_start:
                    self.drawing_board[x][y] = self.wall_color_val

    def draw_pattern4(self, x_start, y_start):
        x_end = (x_start + 1) * 8
        y_end = (y_start + 1) * 8
        x_start = x_start * 8
        y_start = y_start * 8
        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                if x == (x_end - 1):
                    self.drawing_board[x][y] = self.wall_color_val
                elif y == y_start or y == (y_end - 1):
                    self.drawing_board[x][y] = self.wall_color_val

    def draw_pattern5(self, x_start, y_start):
        x_end = (x_start + 1) * 8
        y_end = (y_start + 1) * 8
        x_start = x_start * 8
        y_start = y_start * 8
        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                if y == y_start:
                    self.drawing_board[x][y] = self.wall_color_val
                elif y == (y_end - 1):
                    self.drawing_board[x][y] = self.wall_color_val

    def draw_pattern6(self, x_start, y_start):
        x_end = (x_start + 1) * 8
        y_end = (y_start + 1) * 8
        x_start = x_start * 8
        y_start = y_start * 8
        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                if x == x_start:
                    self.drawing_board[x][y] = self.wall_color_val
                elif x == (x_end - 1):
                    self.drawing_board[x][y] = self.wall_color_val

    def draw_pattern7(self, x_start, y_start):
        x_end = (x_start + 1) * 8
        y_end = (y_start + 1) * 8
        x_start = x_start * 8
        y_start = y_start * 8
        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                if x == x_start:
                    self.drawing_board[x][y] = self.wall_color_val
                elif y == y_start:
                    self.drawing_board[x][y] = self.wall_color_val
                elif x == (x_end - 1) and y == (y_end - 1):
                    self.drawing_board[x][y] = self.wall_color_val

    def draw_pattern8(self, x_start, y_start):
        x_end = (x_start + 1) * 8
        y_end = (y_start + 1) * 8
        x_start = x_start * 8
        y_start = y_start * 8
        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                if x == x_start:
                    self.drawing_board[x][y] = self.wall_color_val
                elif y == (y_end - 1):
                    self.drawing_board[x][y] = self.wall_color_val
                elif x == (x_end - 1) and y == y_start:
                    self.drawing_board[x][y] = self.wall_color_val

    def draw_pattern9(self, x_start, y_start):
        x_end = (x_start + 1) * 8
        y_end = (y_start + 1) * 8
        x_start = x_start * 8
        y_start = y_start * 8
        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                if x == (x_end - 1):
                    self.drawing_board[x][y] = self.wall_color_val
                elif y == (y_end - 1):
                    self.drawing_board[x][y] = self.wall_color_val
                elif x == x_start and y == y_start:
                    self.drawing_board[x][y] = self.wall_color_val

    def draw_pattern10(self, x_start, y_start):
        x_end = (x_start + 1) * 8
        y_end = (y_start + 1) * 8
        x_start = x_start * 8
        y_start = y_start * 8
        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                if x == (x_end - 1):
                    self.drawing_board[x][y] = self.wall_color_val
                elif y == y_start:
                    self.drawing_board[x][y] = self.wall_color_val
                elif x == x_start and y == (y_end - 1):
                    self.drawing_board[x][y] = self.wall_color_val

    def draw_pattern11(self, x_start, y_start):
        x_end = (x_start + 1) * 8
        y_end = (y_start + 1) * 8
        x_start = x_start * 8
        y_start = y_start * 8
        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                if x == x_start:
                    self.drawing_board[x][y] = self.wall_color_val
                elif x == (x_end - 1) and y == y_start:
                    self.drawing_board[x][y] = self.wall_color_val
                elif x == (x_end - 1) and y == (y_end - 1):
                    self.drawing_board[x][y] = self.wall_color_val

    def draw_pattern12(self, x_start, y_start):
        x_end = (x_start + 1) * 8
        y_end = (y_start + 1) * 8
        x_start = x_start * 8
        y_start = y_start * 8
        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                if y == (y_end - 1):
                    self.drawing_board[x][y] = self.wall_color_val
                elif x == x_start and y == y_start:
                    self.drawing_board[x][y] = self.wall_color_val
                elif x == (x_end - 1) and y == y_start:
                    self.drawing_board[x][y] = self.wall_color_val

    def draw_pattern13(self, x_start, y_start):
        x_end = (x_start + 1) * 8
        y_end = (y_start + 1) * 8
        x_start = x_start * 8
        y_start = y_start * 8
        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                if x == (x_end - 1):
                    self.drawing_board[x][y] = self.wall_color_val
                elif x == x_start and y == y_start:
                    self.drawing_board[x][y] = self.wall_color_val
                elif x == x_start and y == (y_end - 1):
                    self.drawing_board[x][y] = self.wall_color_val

    def draw_pattern14(self, x_start, y_start):
        x_end = (x_start + 1) * 8
        y_end = (y_start + 1) * 8
        x_start = x_start * 8
        y_start = y_start * 8
        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                if y == y_start:
                    self.drawing_board[x][y] = self.wall_color_val
                elif x == x_start and y == (y_end - 1):
                    self.drawing_board[x][y] = self.wall_color_val
                elif x == (x_end - 1) and y == (y_end - 1):
                    self.drawing_board[x][y] = self.wall_color_val

    def draw_pattern15(self, x_start, y_start):
        x_end = (x_start + 1) * 8
        y_end = (y_start + 1) * 8
        x_start = x_start * 8
        y_start = y_start * 8
        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                if x == x_start and y == y_start:
                    self.drawing_board[x][y] = self.wall_color_val
                elif x == x_start and y == (y_end - 1):
                    self.drawing_board[x][y] = self.wall_color_val
                elif x == (x_end - 1) and y == y_start:
                    self.drawing_board[x][y] = self.wall_color_val
                elif x == (x_end - 1) and y == (y_end - 1):
                    self.drawing_board[x][y] = self.wall_color_val

    def rid_of_padding_at_start_node(self):
        x_start, y_start = self.start_coord
        start_node = self.grid[x_start][y_start]
        parent_dir = start_node.parent_direction

        x_end = (x_start + 1) * 8 + 1  # dealing with padded grid; add 1
        y_end = (y_start + 1) * 8 + 1
        x_start = x_start * 8 + 1
        y_start = y_start * 8 + 1
        # x_val and y_val 딱 원래 8x8 cell loop
        if parent_dir == 2:
            for x_val in range(x_start, x_end):
                for y_val in range(y_start, y_end):
                    if x_val == x_end - 1 and y_val != y_start and y_val != y_end - 1:
                        self.drawing_board[x_val + 1][y_val] = self.background_color_val
        elif parent_dir == 4:
            for x_val in range(x_start, x_end):
                for y_val in range(y_start, y_end):
                    if y_val == y_start and x_val != x_start and x_val != x_end - 1:
                        self.drawing_board[x_val][y_val - 1] = self.background_color_val
        elif parent_dir == 6:
            for x_val in range(x_start, x_end):
                for y_val in range(y_start, y_end):
                    if y_val == y_end - 1 and x_val != x_start and x_val != x_end - 1:
                        self.drawing_board[x_val][y_val + 1] = self.background_color_val
        else:
            for x_val in range(x_start, x_end):
                for y_val in range(y_start, y_end):
                    if x_val == x_start and y_val != y_start and y_val != y_end - 1:
                        self.drawing_board[x_val - 1][y_val] = self.background_color_val