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

        neighbors: list of neighbors / directions node can access.
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
        Marks is_start True if
        the node is start node
        """
        self.is_start = True

    def mark_as_end_node(self):
        """
        Marks is_end True if
        the node is start node
        """
        self.is_end = True


# noinspection PyUnresolvedReferences
class GridGraphMaze:
    def __init__(self, length):
        """
        Makes grid and insert Node instances in grid (nested list).
        Marks start and end nodes.
        Directions/neighbors are represented using four numbers:
          8
        4   6
          2
        Instance variables necessary for making maze and drawing maze
        are all initialized here.
        Start and end nodes are initialized as well.

        param length of one side of the square grid
        """
        # make length x length grid
        self.length = length
        self.grid = [[0 for _ in range(length)] for _ in range(length)]

        self.next_node = None
        self.nodes_put_on_hold_ls = []

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
        """
        Start and end nodes are put diagonally far apart.
        :return: start and end coordinates as tuples ((1x2 tuple),(1x2 tuple))
        """
        start, end = random.choice([
            ((0, random.choice(range(int(self.length / 2)))), (self.length - 1, self.length - 1)),

            ((self.length - 1, random.choice(range(int(self.length / 2), self.length))), (0, 0)),

            ((random.choice(range(int(self.length / 2), self.length)), 0), (0, self.length - 1)),

            ((random.choice(range(int(self.length / 2))), self.length - 1), (self.length - 1, 0)),
        ])
        return start, end

    def find_accessible_directions_of_node(self, node):
        """
        Finds directions current node can go based only on
        position of the node in the grid graph.
        :return: list of directions node can go
        """
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
        # no need to set end node or deadend node as parent of other nodes
        if node.is_end:
            return
        elif not node.is_start and self.is_deadend(node):
            return

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
        Checks if node is a deadend.
        => all adjacent nodes are visited
        """
        acc_dir = self.find_accessible_directions_of_node(node)
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

    def find_out_if_node_visited_all_its_neighbors(self, node):
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
        Given a node, finds unvisited (previously unselected) neighbor node,
        add direction & weight of newly added unvisited node in node,
        add parent_direction to newly added unvisited node

        return True if node with unvisited direction is added to reserved_nodes_ls else False
        """
        # if encounter a node that has only been added as neighbor, and no neighbor added yet
        # should be fine without the code below. Handled beforehand.
        if len(node.neighbors) == 0:
            print('Error: visited node has no neighbor!')

        accessible_directions = self.find_accessible_directions_of_node(node)

        if not node.is_start:
            accessible_directions.remove(node.parent_direction)

        i, j = node.coordinate
        random.shuffle(accessible_directions)
        for direction in accessible_directions:
            if direction == 2:
                if not self.grid[i + 1][j].is_visited:
                    node.neighbors.append((2, self.rand_weight()))
                    self.grid[i + 1][j].is_visited = True
                    self.grid[i + 1][j].parent_direction = 8
                    self.visited_nodes_ls.append(self.grid[i + 1][j])
                    self.unvisited_nodes_ls.remove(self.grid[i + 1][j])
                    self.nodes_put_on_hold_ls.append(self.grid[i + 1][j])
                    # return # if return here, we're adding only one neighbor from accessible direction on hold
            elif direction == 4:
                if not self.grid[i][j - 1].is_visited:
                    node.neighbors.append((4, self.rand_weight()))
                    self.grid[i][j - 1].is_visited = True
                    self.grid[i][j - 1].parent_direction = 6
                    self.visited_nodes_ls.append(self.grid[i][j - 1])
                    self.unvisited_nodes_ls.remove(self.grid[i][j - 1])
                    self.nodes_put_on_hold_ls.append(self.grid[i][j - 1])
                    # return
            elif direction == 6:
                if not self.grid[i][j + 1].is_visited:
                    node.neighbors.append((6, self.rand_weight()))
                    self.grid[i][j + 1].is_visited = True
                    self.grid[i][j + 1].parent_direction = 4
                    self.visited_nodes_ls.append(self.grid[i][j + 1])
                    self.unvisited_nodes_ls.remove(self.grid[i][j + 1])
                    self.nodes_put_on_hold_ls.append(self.grid[i][j + 1])
                    # return
            else:
                if not self.grid[i - 1][j].is_visited:
                    node.neighbors.append((8, self.rand_weight()))
                    self.grid[i - 1][j].is_visited = True
                    self.grid[i - 1][j].parent_direction = 2
                    self.visited_nodes_ls.append(self.grid[i - 1][j])
                    self.unvisited_nodes_ls.remove(self.grid[i - 1][j])
                    self.nodes_put_on_hold_ls.append(self.grid[i - 1][j])
                    # return

    def visit_parent_to_get_direction_towards_wall_from_three_possible_dir(self, node):
        """
        visit current node's parent node to find direction towards wall/visited node
        """
        i, j = node.coordinate
        p_dir = node.parent_direction

        # get parent node
        if p_dir == 2:
            parent_node = self.grid[i + 1][j]
        elif p_dir == 4:
            parent_node = self.grid[i][j - 1]
        elif p_dir == 6:
            parent_node = self.grid[i][j + 1]
        else:
            parent_node = self.grid[i - 1][j]

        # get parent node's accessible directions
        parent_accessible_directions = self.find_accessible_directions_of_node(parent_node)
        # all neigh of parent visited
        if len(parent_accessible_directions) == 0:
            return self.turn_sideways_given_three_possible_dir(p_dir)
        else:
            # handle when parent node is start node
            if parent_node.is_start:
                if len(parent_accessible_directions) == 1:
                    return get_opposite_direction(parent_accessible_directions[0])
                else:
                    return self.turn_sideways_given_three_possible_dir(p_dir)

            # parent node and parent node's parent are in straight line & curr node has 3 possible directions
            if node.parent_direction == parent_node.parent_direction:
                # choose dir that parent can't access (towards wall)
                if len(parent_accessible_directions) == 1:
                    return get_opposite_direction(parent_accessible_directions[0])
                # when parent has 2 accessible direction, turn to side
                else:
                    return self.turn_sideways_given_three_possible_dir(p_dir)
            # curr node and parent node NOT in straight line & curr node has 3 possible directions
            else:
                return parent_node.parent_direction

    @staticmethod
    def get_opposite_direction(direction):
        """
        :param direction: one of four directions (2,4,6,8)
        :return: opposite direction of given direction
        """
        if direction == 2:
            return 8
        elif direction == 4:
            return 6
        elif direction == 6:
            return 4
        else:
            return 2

    @staticmethod
    def turn_sideways_given_three_possible_dir(p_dir):
        """
        return right or left direction based on parent's direction
        """
        if p_dir == 2 or p_dir == 8:
            return random.sample([4, 6], 1)[0]
        else:
            return random.sample([2, 8], 1)[0]

    def choose_direction_with_bias(self, node, accessible_directions):
        """
        Choose next neighbor node in a biased manner so that
        next decision is the inclined to be the same as parent's direction.
        * Makes maze less branchy.
        :param node: curr node
        :param p_dir: direction to parent (int)
        :param accessible_directions: list of accessible directions ([int]
        :return: direction to neighbor
        """
        p_dir = node.parent_direction

        if len(accessible_directions) == 2:
            if p_dir == 2 and 8 in accessible_directions:
                accessible_directions = [x for x in accessible_directions if x != 8] + [8]
                sampled_direction = random.choices(accessible_directions, weights=[0.1, 0.9])[0]
            elif p_dir == 4 and 6 in accessible_directions:
                accessible_directions = [x for x in accessible_directions if x != 6] + [6]
                sampled_direction = random.choices(accessible_directions, weights=[0.1, 0.9])[0]
            elif p_dir == 6 and 4 in accessible_directions:
                accessible_directions = [x for x in accessible_directions if x != 4] + [4]
                sampled_direction = random.choices(accessible_directions, weights=[0.1, 0.9])[0]
            elif p_dir == 8 and 2 in accessible_directions:
                accessible_directions = [x for x in accessible_directions if x != 2] + [2]
                sampled_direction = random.choices(accessible_directions, weights=[0.1, 0.9])[0]
            else:
                sampled_direction = random.sample(accessible_directions, 1)[0]

        elif len(accessible_directions) == 3:
            sampled_direction = self.visit_parent_to_get_direction_towards_wall_from_three_possible_dir(node)
            n_dir = random.choices([1, 2], weights=[0.9, 0.1])[0]
            if n_dir == 1:
                accessible_directions = [sampled_direction]
            else:
                accessible_directions.remove(sampled_direction)
                del accessible_directions[random.choices([0, 1])[0]]
                accessible_directions.append(sampled_direction)

        elif len(accessible_directions) == 3:
            sampled_direction = self.visit_parent_to_get_direction_towards_wall_from_three_possible_dir(node)

        return sampled_direction

    def mark_neighbors_visited_and_choose_next_node(self, node, sampled_direction, reserve_this_node=False, accessible_directions=None):
        """
        Marks neighbors of node visited,
        even the ones stored/reserved for random selection in the future
        once path_length is reached.
        """
        i, j = node.coordinate
        if sampled_direction == 2:
            if not self.grid[i + 1][j].is_visited:
                node.neighbors.append((2, self.rand_weight()))
                self.grid[i + 1][j].is_visited = True
                self.visited_nodes_ls.append(self.grid[i + 1][j])
                self.unvisited_nodes_ls.remove(self.grid[i + 1][j])
                self.next_node = self.grid[i + 1][j]
        elif sampled_direction == 4:
            if not self.grid[i][j - 1].is_visited:
                node.neighbors.append((4, self.rand_weight()))
                self.grid[i][j - 1].is_visited = True
                self.visited_nodes_ls.append(self.grid[i][j - 1])
                self.unvisited_nodes_ls.remove(self.grid[i][j - 1])
                self.next_node = self.grid[i][j - 1]
        elif sampled_direction == 6:
            if not self.grid[i][j + 1].is_visited:
                node.neighbors.append((6, self.rand_weight()))
                self.grid[i][j + 1].is_visited = True
                self.visited_nodes_ls.append(self.grid[i][j + 1])
                self.unvisited_nodes_ls.remove(self.grid[i][j + 1])
                self.next_node = self.grid[i][j + 1]
        else:
            if not self.grid[i - 1][j].is_visited:
                node.neighbors.append((8, self.rand_weight()))
                self.grid[i - 1][j].is_visited = True
                self.visited_nodes_ls.append(self.grid[i - 1][j])
                self.unvisited_nodes_ls.remove(self.grid[i - 1][j])
                self.next_node = self.grid[i - 1][j]

    def choose_next_neighbor(self, node):
        """
        1. Marks dead end and end node in node.neighbors.
        2. Finds accessible (unvisited) neighbor nodes
        3. adds selected directions to node.neighbors.

        Bias1: next direction is biased to be tangent to wall or visited node
        to make the maze tightly packed with continuous paths.
        Bias2: next direction is biased to follow parent node's direction.
        """
        if node.is_end:
            node.neighbors = ['fin']
            self.next_node = node  # super necessary, trust me
            return

        # if node is deadend, don't add any directions (but it needs parent)
        if not node.is_start and self.is_deadend(node):
            node.neighbors = ['deadend']
            self.next_node = node  # this one too
            return

        accessible_directions = self.find_accessible_directions_of_node(node)

        # if node is NOT starting node, remove direction toward curr node's parent in accessible_directions!
        # (shouldn't be able to go back toward parent)
        p_dir = node.parent_direction
        if not node.is_start:
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

        if len(accessible_directions) == 1:
            # this one direction => return next node right away
            sampled_direction = accessible_directions[0]
            # mark neighbors as visited ahead of time (here) to prevent collision
            self.mark_neighbors_visited_and_choose_next_node(node, sampled_direction)
        else:
            if node.is_start:
                sampled_direction = random.sample(accessible_directions, 1)[0]
            else:
                sampled_direction = self.choose_direction_with_bias(node, accessible_directions)

            # mark neighbors as visited ahead of time (here) to prevent collision
            self.mark_neighbors_visited_and_choose_next_node(node, sampled_direction)

    def go_to_visited_nodes_to_find_new_node(self, bud_node_cnt):
        # if meet deadend/fin but there's still unvisited nodes in grid,
        # choose a new node from visited nodes to find node with unchosen accessible neighbor
        random.shuffle(self.visited_nodes_ls)
        for n, visited_node in enumerate(self.visited_nodes_ls[:]):

            # remove node if end node or if there are no unvisited neighbors (= fully explored node)
            if self.find_out_if_node_visited_all_its_neighbors(visited_node) or visited_node.is_end:
                self.visited_nodes_ls.remove(visited_node)
            else:
                self.find_unvisited_nodes_from_visited_and_add_to_q(visited_node)
                if n > bud_node_cnt:  # new nodes where new path can bud and make branch
                    return

    def make_maze(self, start_node, path_length, bud_node_cnt):
        """
        Makes maze by searching and adding neighboring node every step starting from start node.
        If deadend/end node is encountered and grid is not fully explored, this function finds
        new directions from visited nodes that have not been explored.

        :param start_node: making maze start from this start node
        :param path_length: path length value should be determined based on the size of the maze.
        Bigger path_length leads to longer trails of path without meeting a dead end. Once max path_length
        is reached, next node is randomly selected from neighbors of nodes encountered while path was being
        made.

        * path_counter range = [3, +inf]
        """
        self.next_node = start_node
        start_node.is_visited = True
        self.visited_nodes_ls.append(start_node)
        self.unvisited_nodes_ls.remove(start_node)

        path_counter = 1
        while True:
            # making paths
            if path_counter < path_length:
                node = self.next_node

                # if meet deadend/fin but there's still unvisited nodes in grid,
                # choose a new node from visited nodes to find node with unchosen accessible neighbor
                # choose random number of unvisited neighbors
                self.choose_next_neighbor(node)
                self.set_node_as_parent_of_neighbors(node)

                # if meet deadend/end before meeting expected length
                if node.neighbors[0] == 'fin' or node.neighbors[0] == 'deadend':
                    # add a few nodes (branching from single node) to self.nodes_put_on_hold_ls
                    if len(self.nodes_put_on_hold_ls) == 0:
                        self.go_to_visited_nodes_to_find_new_node(bud_node_cnt)
                    path_counter = float('inf')
                    continue

                path_counter += 1
                # once we reach designated path length, put the next node on hold to be revisited later
                if path_counter == path_length:
                    self.nodes_put_on_hold_ls.append(self.next_node)
            else:
                if len(self.unvisited_nodes_ls) == 0 and len(self.visited_nodes_ls) == 0:
                    break
                path_counter = 0
                node = random.sample(self.nodes_put_on_hold_ls, 1)[0]
                self.nodes_put_on_hold_ls.remove(node)

                # choose random number of unvisited neighbors
                self.choose_next_neighbor(node)
                self.set_node_as_parent_of_neighbors(node)
                path_counter += 1

    def draw_maze(self, background_c_val, wall_c_val, start_c_val, end_c_val):
        """
        Draws maze on drawing board based on directions of grid graph
        :param background_c_val: color value of background
        :param wall_c_val: color value of maze wall
        :param start_c_val: color value of start node's marking
        :param end_c_val: color value of end node's marking
        """
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
            print(x,y)
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
                    print("while drawing error occurred @ node coordinate: ", node.coordinate)
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
                    print("while drawing error occurred @ node coordinate: ", node.coordinate)
            # 4 ways cell/node
            elif (({4, 6, 8}.issubset(directions) and parent_dir == 2) or
                  ({2, 6, 8}.issubset(directions) and parent_dir == 4) or
                  ({2, 4, 8}.issubset(directions) and parent_dir == 6) or
                  ({2, 4, 6}.issubset(directions) and parent_dir == 8)):
                self.draw_pattern15(x, y)
            # Shouldn't be any other types of cells/nodes
            else:
                print("while drawing error occurred @ node coordinate: ", node.coordinate)

        # mode='constant' parameter indicates that we want to pad with constant values.
        self.drawing_board = np.pad(self.drawing_board, ((1, 1), (1, 1)), mode='constant',
                                    constant_values=self.wall_color_val)
        self.rid_of_padding_at_start_node()

    def color_start(self, x_start, y_start):
        """
        Colors start node with start_color_value
        :param x_start: x coordinate of grid graph
        :param y_start: y coordinate of grid graph
        """
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
        """
        Colors end node with start_color_value
        :param x_start: x coordinate of grid graph
        :param y_start: y coordinate of grid graph
        """
        x_end = (x_start + 1) * 8
        y_end = (y_start + 1) * 8
        x_start = x_start * 8
        y_start = y_start * 8
        for x in range(x_start + 2, x_end - 2):
            for y in range(y_start + 2, y_end - 2):
                self.drawing_board[x][y] = self.end_color_val

    def decide_entrance_direction_of_maze_from_start_node(self, start_node, x_start, y_start):
        """
        Entrance direction saved as parent direction of start node.
        :param start_node: start node in grid graph
        :param x_start: x coordinate of grid graph
        :param y_start: y coordinate of grid graph
        """
        if x_start == 0 and y_start == 0:
            start_node.parent_direction = [4, 8]
        elif x_start == 0 and y_start == self.length - 1:
            start_node.parent_direction = [6, 8]
        elif x_start == self.length - 1 and y_start == 0:
            start_node.parent_direction = [2, 4]
        elif x_start == self.length - 1 and y_start == self.length - 1:
            start_node.parent_direction = [2, 6]
        elif x_start == 0:
            start_node.parent_direction = [8]
        elif x_start == self.length - 1:
            start_node.parent_direction = [2]
        elif y_start == 0:
            start_node.parent_direction = [4]
        elif y_start == self.length - 1:
            start_node.parent_direction = [6]

        # pick one entrance direction (from node perspective)
        start_node.parent_direction = random.sample(start_node.parent_direction, 1)[0]

    def draw_pattern1(self, x_start, y_start):
        """
        Draws below pattern in 8 by 8 grid:
            @@@@@@
            @    @
            @    @
        """
        print('draw_pattern_in_game_1')
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
        """
        Draws below pattern in 8 by 8 grid:
            @@@@@@
                 @
            @@@@@@
        """
        print('draw_pattern_in_game_2')
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
        """
        Draws below pattern in 8 by 8 grid:
            @@@@@@
            @
            @@@@@@
        """
        print('draw_pattern_in_game_3')
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
        """
        Draws below pattern in 8 by 8 grid:
            @    @
            @    @
            @@@@@@
        """
        print('draw_pattern_in_game_4')
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
        """
        Draws below pattern in 8 by 8 grid:
            @    @
            @    @
            @    @
        """
        print('draw_pattern_in_game_5')
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
        """
        Draws below pattern in 8 by 8 grid:
            @@@@@@

            @@@@@@
        """
        print('draw_pattern_in_game_6')
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
        """
        Draws below pattern in 8 by 8 grid:
            @@@@@@
            @
            @    @
        """
        print('draw_pattern_in_game_7')
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
        """
        Draws below pattern in 8 by 8 grid:
            @@@@@@
                 @
            @    @
        """
        print('draw_pattern_in_game_8')
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
        """
        Draws below pattern in 8 by 8 grid:
            @    @
                 @
            @@@@@@
        """
        print('draw_pattern_in_game_9')
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
        """
        Draws below pattern in 8 by 8 grid:
            @    @
            @
            @@@@@@
        """
        print('draw_pattern_in_game_10')
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
        """
        Draws below pattern in 8 by 8 grid:
            @@@@@@

            @    @
        """
        print('draw_pattern_in_game_11')
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
        """
        Draws below pattern in 8 by 8 grid:
            @    @
                 @
            @    @
        """
        print('draw_pattern_in_game_12')
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
        """
        Draws below pattern in 8 by 8 grid:
            @    @

            @@@@@@
        """
        print('draw_pattern_in_game_13')
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
        """
        Draws below pattern in 8 by 8 grid:
            @    @
            @
            @    @
        """
        print('draw_pattern_in_game_14')
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
        """
        Draws below pattern in 8 by 8 grid:
            @    @

            @    @
        """
        print('draw_pattern_in_game_15')
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
        """
        To mark start position in drawing_board,
        wall of start node's parent is deleted.
        """
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


if __name__ == "__main__":
    random.seed(0)
    grid_length = 2
    length_of_path = 10
    bud_count = 5

    if grid_length < 2:
        print("Error: Choose maze size bigger than 2!")
        exit()

    if length_of_path < 3:
        print("Error: Choose longer path length!")
        exit()

    grid_graph = GridGraphMaze(length=grid_length)

    print('start:', grid_graph.start_coord)
    print('end:', grid_graph.end_coord)
    print()

    st_i, st_j = grid_graph.start_coord
    st_node = grid_graph.grid[st_i][st_j]

    grid_graph.make_maze(st_node, path_length=length_of_path, bud_node_cnt=bud_count)

    # 100 by 100 grid => 0.5 second
    # 300 by 300 grid => 44 seconds

    # print('=============== neighbors ===============')
    # for i in grid_graph.grid:
    #     for j in i:
    #         print(''.join([str(x[0]) for x in j.neighbors]), end='\t')
    #     print()
    # print()
    #
    # print('===============parent direction===============')
    # print()
    # for i in grid_graph.grid:
    #     for j in i:
    #         print(j.parent_direction, end='\t')
    #     print()
    # print()
    #
    # print('===============is visited===============')
    # print()
    # for i in grid_graph.grid:
    #     for j in i:
    #         print(j.is_visited, end=' ')
    #     print()
    # print()
    # print('=========================================')

    grid_graph.draw_maze(background_c_val=0, wall_c_val=1, start_c_val=1, end_c_val=1)
    # Create a sample 2D array of values
    data = grid_graph.drawing_board

    # Create a heatmap plot
    plt.imshow(data, cmap='cividis', vmin=0, vmax=1)
    # Blues, Purples, Greens, cividis, summer
    # plt.colorbar()  # Add a color bar to the plot
    plt.axis('off')
    # Display the plot
    plt.savefig('gift_maze.png')
    plt.show()
