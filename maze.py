import random

random.seed(5)


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
        Makes grid and insert node obj in grid

        Directions/neighbors are represented using four numbers:
          8
        4   6
          2
        """
        self.cumulative_node_cnt = 0
        self.length = length

        # make length x length grid
        self.grid = [[0 for _ in range(length)] for _ in range(length)]

        self.q = []  # was a queue, but change to list in order to randomly sample nodes

        # list of visited nodes
        self.visited_nodes_ls = []

        # choose start/end points at a side of the grid
        self.start_coord, self.end_coord = self.choose_start_end_coord()

        # insert nodes with coordinate in grid
        for i in range(length):
            for j in range(length):
                self.grid[i][j] = Node((i, j))

                # mark start & end in Node inst
                # add start coord in GridGraph inst
                if self.grid[i][j].coordinate[0] == self.start_coord[0] and self.grid[i][j].coordinate[1] == \
                        self.start_coord[1]:
                    self.grid[i][j].mark_as_start_node()

                if self.grid[i][j].coordinate[0] == self.end_coord[0] and self.grid[i][j].coordinate[1] == \
                        self.end_coord[1]:
                    self.grid[i][j].mark_as_end_node()

    @staticmethod
    def rand_weight():
        return random.choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])[0]

    def choose_start_end_coord(self):
        start, end = (0, 0), (0, 0)
        while start == end:
            start, end = (
                random.choice([(0, random.choice(range(self.length))),
                               (self.length - 1, random.choice(range(self.length))),
                               (random.choice(range(self.length)), 0),
                               (random.choice(range(self.length)), self.length - 1)]),
                (random.choice(range(self.length)), random.choice(range(self.length)))
            )
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

    def choose_random_number_of_neighbors(self, curr_node):
        """
        Checks if accessible nodes(unvisited) are visited or not
        and adds only accessible nodes to curr_node's neighbors randomly
        1. end 면 fin 넣어줌
        2. deadend 면 deadend 넣어줌
        """
        # print('***curr node coord:', curr_node.coordinate)
        if curr_node.is_end:
            curr_node.neighbors = ['fin']
            return

        # if curr_node is deadend, don't add any directions (but it needs parent)
        if not curr_node.is_start and self.is_deadend(curr_node):
            curr_node.neighbors = ['deadend']
            return

        accessible_directions = self.find_accessible_directions_of_node(curr_node)

        # if curr_node is NOT starting node, remove direction toward curr node's parent in accessible_directions!
        # (shouldn't be able to go back toward parent)
        if not curr_node.is_start:
            p_dir = curr_node.parent_direction
            if p_dir == 2:
                accessible_directions.remove(2)
            elif p_dir == 4:
                accessible_directions.remove(4)
            elif p_dir == 6:
                accessible_directions.remove(6)
            else:
                accessible_directions.remove(8)

        # ****visit 된곳은 sample 자체가 안 되도록 지워 준다 ***** ㅠㅠ 이걸 sampling 하기 전 먼져 했어야 했다
        i, j = curr_node.coordinate
        for direction in accessible_directions:
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
        sampled_directions = random.sample(accessible_directions, random.randint(1, len(accessible_directions)))

        # 샘플링 한 방향을 neighbors 에 넣어 주면 된다
        # also, mark neighbors as visited ahead of time (here) to prevent collision
        for direction in sampled_directions:
            if direction == 2:
                if not self.grid[i + 1][j].is_visited and self.grid[i + 1][j] not in curr_node.neighbors:
                    curr_node.neighbors.append((2, self.rand_weight()))
                    self.grid[i + 1][j].is_visited = True
                    self.visited_nodes_ls.append(self.grid[i + 1][j])
                    self.q.append(self.grid[i + 1][j])
                    self.cumulative_node_cnt += 1
            elif direction == 4:
                if not self.grid[i][j - 1].is_visited and self.grid[i][j-1] not in curr_node.neighbors:
                    curr_node.neighbors.append((4, self.rand_weight()))
                    self.grid[i][j - 1].is_visited = True
                    self.visited_nodes_ls.append(self.grid[i][j - 1])
                    self.q.append(self.grid[i][j - 1])
                    self.cumulative_node_cnt += 1
            elif direction == 6:
                if not self.grid[i][j + 1].is_visited and self.grid[i][j + 1] not in curr_node.neighbors:
                    curr_node.neighbors.append((6, self.rand_weight()))
                    self.grid[i][j + 1].is_visited = True
                    self.visited_nodes_ls.append(self.grid[i][j + 1])
                    self.q.append(self.grid[i][j + 1])
                    self.cumulative_node_cnt += 1
            else:
                if not self.grid[i - 1][j].is_visited and self.grid[i - 1][j] not in curr_node.neighbors:
                    curr_node.neighbors.append((8, self.rand_weight()))
                    self.grid[i - 1][j].is_visited = True
                    self.visited_nodes_ls.append(self.grid[i - 1][j])
                    self.q.append(self.grid[i - 1][j])
                    self.cumulative_node_cnt += 1

    def set_curr_node_as_parent_of_neighbors(self, node):
        # if not node.is_start:
        #     print('**deadend 면 안됨(false 여야함)**', self.is_deadend(node))

        # no need to set end node or deadend node as parent of other nodes
        if node.is_end:
            return
        elif not node.is_start and self.is_deadend(node):
            return

        i, j = node.coordinate
        for neigh in node.neighbors:
            dir = neigh[0]
            # print('par dir 넣을 neighbor 의 direction: ', dir)

            if dir == 2:
                self.grid[i + 1][j].parent_direction = 8
                # print('neigh coord:', self.grid[i + 1][j].coordinate)
            elif dir == 4:
                self.grid[i][j - 1].parent_direction = 6
                # print('neigh coord:', self.grid[i][j - 1].coordinate)
            elif dir == 6:
                self.grid[i][j + 1].parent_direction = 4
                # print('neigh coord:', self.grid[i][j + 1].coordinate)
            elif dir == 8:
                self.grid[i - 1][j].parent_direction = 2
                # print('neigh coord:', self.grid[i - 1][j].coordinate)
        # print()

    def is_deadend(self, node):
        """
        checks if node is at a deadend:
        = all adjacent nodes are visited
        """
        acc_dir = self.find_accessible_directions_of_node(node)
        acc_dir.remove(node.parent_direction)  # exclude dir current node came from (parent direction)

        n_directions = len(acc_dir)
        n_visited_neigh_but_not_in_my_neigh = 0
        i, j = node.coordinate

        my_neigh = [neigh[0] for neigh in node.neighbors]

        for direction in acc_dir:
            if direction not in my_neigh:  # visit 했지만 현 노드의 이웃에 없을때 만 deadend!***
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

    def find_unvisited_nodes_from_visited(self, node):
        """
        given a node, finds unvisited(previously unselected) node,
        add direction & weight of newly added unvisited node in node,
        add parent_direction to newly added unvisited node

        returns a list of unvisited node(s)
        """
        if node in self.visited_nodes_ls:
            return

        accessible_directions = self.find_accessible_directions_of_node(node)
        accessible_directions.remove(node.parent_direction)

        i, j = node.coordinate
        for direction in accessible_directions:
            if direction == 2:
                if not self.grid[i + 1][j].is_visited:
                    node.neighbors.append((2, self.rand_weight()))
                    self.grid[i + 1][j].parent_direction = 8
                    self.q.append(self.grid[i + 1][j])
                    self.cumulative_node_cnt += 1
                    return  # return so that we just add one unvisited node
            elif direction == 4:
                if not self.grid[i][j - 1].is_visited:
                    node.neighbors.append((4, self.rand_weight()))
                    self.grid[i][j - 1].parent_direction = 6
                    self.q.append(self.grid[i][j - 1])
                    self.cumulative_node_cnt += 1
                    return
            elif direction == 6:
                if not self.grid[i][j + 1].is_visited:
                    node.neighbors.append((6, self.rand_weight()))
                    self.grid[i][j + 1].parent_direction = 4
                    self.q.append(self.grid[i][j + 1])
                    self.cumulative_node_cnt += 1
                    return
            else:
                if not self.grid[i - 1][j].is_visited:
                    node.neighbors.append((8, self.rand_weight()))
                    self.grid[i - 1][j].parent_direction = 2
                    self.q.append(self.grid[i - 1][j])
                    self.cumulative_node_cnt += 1
                    return

    def make_maze(self, st_node):

        self.q.append(st_node)
        st_node.is_visited = True
        self.visited_nodes_ls.append(st_node)

        self.cumulative_node_cnt += 1

        while len(self.q) > 0:
            # print('visited nodes list 길이(q 늘어 나는 만큼 cumulative 하게 늘어야 함):', len(self.visited_nodes_ls))

            node = random.sample(self.q, 1)[0]
            self.q.remove(node)  # need to sample deadend & end in order to label them in node's neighbors

            # making path step
            # choose random number of unvisited neighbors
            self.choose_random_number_of_neighbors(node)
            # make curr_node a parent of the neighbors of curr_node
            self.set_curr_node_as_parent_of_neighbors(node)

            # if meet end but still unvisited nodes in grid
            # => choose a new node from list of visited nodes to find node with unchosen accessible neighbor
            # add direction to that unchosen node
            # and add unchosen node to queue
            if node.neighbors[0] == 'fin' and len(self.visited_nodes_ls) <= self.length ** 2:
                for visited_node in self.visited_nodes_ls:
                    # skip searching end node from visited_nodes_ls (don't want to search new route from end node)
                    if visited_node.is_end:  # visited_node.neighbors[0] == 'deadend' or
                        print('그래서 end 노드는 스킵 되나?')
                        continue
                    self.find_unvisited_nodes_from_visited(visited_node)
