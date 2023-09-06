import random


# random.seed(14)

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
        self.neighbors = []


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
        self.length = length
        # make length x length grid
        self.grid = [[0 for _ in range(length)] for _ in range(length)]

        self.q = []  # before queue, now changed to list to randomly sample nodes

        # list of visited / unvisited nodes
        self.visited_nodes_ls = []
        self.unvisited_nodes_ls = []

        # choose start/end points at a side of the grid
        self.start_coord, self.end_coord = self.choose_start_end_coord()

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
        start, end = (0, 0), (0, 0)
        start_end_dist = 0
        min_dist = int(self.length / 2)
        while start_end_dist < min_dist:
            start, end = (
                random.choice([(0, random.choice(range(self.length))),
                               (self.length - 1, random.choice(range(self.length))),
                               (random.choice(range(self.length)), 0),
                               (random.choice(range(self.length)), self.length - 1)]),
                (random.choice(range(self.length)), random.choice(range(self.length)))
            )
            x1 = start[0]
            x2 = start[1]
            y1 = end[0]
            y2 = end[1]
            start_end_dist = int((abs(x1 - x2) ** 2 + abs(y1 - y2) ** 2) ** 1 / 2)
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

    def choose_random_number_of_neighbors(self, node):
        """
        Checks if accessible nodes(unvisited) are visited or not
        and adds only accessible nodes to node's neighbors randomly
        1. end 면 fin 넣어줌
        2. deadend 면 deadend 넣어줌
        """
        if node.is_end:
            node.neighbors = ['fin']
            return

        # if node is deadend, don't add any directions (but it needs parent)
        if not node.is_start and self.is_deadend(node):
            node.neighbors = ['deadend']
            return

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
            n_dir = random.choices([1, 2, 3], weights=[0.75, 0.2, 0.05])[0]
        elif len(accessible_directions) == 2:
            n_dir = random.choices([1, 2], weights=[0.9, 0.1])[0]
        else:
            n_dir = 1

        sampled_directions = random.sample(accessible_directions, n_dir)

        # mark neighbors as visited ahead of time (here) to prevent collision
        for direction in sampled_directions:
            if direction == 2:
                if not self.grid[i + 1][j].is_visited:
                    node.neighbors.append((2, self.rand_weight()))
                    self.grid[i + 1][j].is_visited = True
                    self.visited_nodes_ls.append(self.grid[i + 1][j])
                    self.unvisited_nodes_ls.remove(self.grid[i + 1][j])
                    self.q.append(self.grid[i + 1][j])
            elif direction == 4:
                if not self.grid[i][j - 1].is_visited:
                    node.neighbors.append((4, self.rand_weight()))
                    self.grid[i][j - 1].is_visited = True
                    self.visited_nodes_ls.append(self.grid[i][j - 1])
                    self.unvisited_nodes_ls.remove(self.grid[i][j - 1])
                    self.q.append(self.grid[i][j - 1])
            elif direction == 6:
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
        checks if node is a deadend:
        = all adjacent nodes are visited
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

    def find_unvisited_nodes_from_visited(self, node):
        """
        given a node, finds unvisited(previously unselected) node,
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

    def make_maze(self, start_node):
        self.q.append(start_node)
        start_node.is_visited = True
        self.visited_nodes_ls.append(start_node)
        self.unvisited_nodes_ls.remove(start_node)
        while len(self.q) > 0:
            node = random.sample(self.q, 1)[0]
            self.q.remove(node)  # need to sample deadend & end in order to label them in node's neighbors

            # making path step
            # choose random number of unvisited neighbors
            self.choose_random_number_of_neighbors(node)
            # make node a parent of the neighbors of node
            self.set_node_as_parent_of_neighbors(node)

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
                            if visited_node.is_end:
                                continue
                            self.find_unvisited_nodes_from_visited(visited_node)
