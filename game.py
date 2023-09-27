import pygame
import numpy as np
import random
import maze as mz
import button as bn


pygame.init()
pygame.mixer.init()

# Constants
ROTATION_SPEED = 1
# Colors
BRIGHT_YELLOW = (254, 232, 56)
YELLOW = (235, 176, 0)
# DARKBL = (0.0, 34, 78)
RED = (200, 0, 0)

WALL_COLOR = YELLOW
# BACKGROUND_COLOR = DARKBL
START_COLOR = YELLOW
END_COLOR = YELLOW

LEVELS = {'easy': [10, 12], 'med': [25, 30], 'hard': [50, 60]}

# Window size
WINDOW_LENGTH = 600  # *
FPS = 60
# music
pygame.mixer.music.load('assets/enigmatic.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0)
END_SOUND = pygame.mixer.Sound('assets/win.mp3')
END_SOUND.set_volume(0.3)

# Display window
WIN = pygame.display.set_mode((WINDOW_LENGTH, WINDOW_LENGTH + 40))  # size in pixels
pygame.display.set_caption("ZenMaze")
BACKGROUND1 = pygame.image.load("assets/darkbl_bg.png")
BACKGROUND2 = pygame.image.load("assets/darkbl_bg2.png")


class Sprite(pygame.sprite.Sprite):
    def __init__(self, init_x, init_y, width, height, color, center=False):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        if center:
            self.rect = self.image.get_rect(center=(init_x, init_y))
        else:
            self.rect = self.image.get_rect()
            self.rect.x = init_x
            self.rect.y = init_y


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, player_color, init_x, init_y):
        super().__init__()
        self.original_image = pygame.Surface([PLAYER_SIZE, PLAYER_SIZE]).convert_alpha()  # convert alpha help
        self.image = self.original_image
        self.image.fill(player_color)
        self.rect = self.image.get_rect(center=(init_x, init_y))
        self.vel = SQ_LENGTH * 0.5
        self.play_end_sound = True
        self.keep_moving = True

    def idle(self, angle):
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def move(self):
        old_player_x, old_player_y = self.rect.center
        keys_pressed = pygame.key.get_pressed()
        if self.keep_moving:
            if keys_pressed[pygame.K_LEFT] and self.rect.centerx - self.rect.width * 0.5 > 0:
                self.rect.centerx -= self.vel
            elif keys_pressed[pygame.K_RIGHT] and self.rect.centerx + self.rect.width * 0.5 < WINDOW_LENGTH:
                self.rect.centerx += self.vel
            elif keys_pressed[pygame.K_UP] and self.rect.centery - self.rect.height * 0.5 > 0:
                self.rect.centery -= self.vel
            elif keys_pressed[pygame.K_DOWN] and self.rect.centery + self.rect.height < WINDOW_LENGTH:
                self.rect.centery += self.vel

            collided_sprites = pygame.sprite.spritecollide(self, WALLS, False)
            if collided_sprites:
                self.rect.center = old_player_x, old_player_y

            pygame.time.wait(35)
        else:
            pass
            
        if pygame.Rect.colliderect(self.rect, END_RECT) and self.rect.center == END_RECT.rect.center:
            if self.play_end_sound:
                self.play_end_sound = False
                END_SOUND.play()
                self.keep_moving = False


def draw_maze(grid):
    """
    Adds all walls of maze as sprites into pygame.sprite.Group() based on directions of grid_graph.

    :param grid: grid_graph (will be named "maze") object outputted by make_maze in maze.py
    """
    x_axis = np.linspace(0, GRID_LENGTH - 1, GRID_LENGTH)
    y_axis = np.linspace(0, GRID_LENGTH - 1, GRID_LENGTH)
    x_grid, y_grid = np.meshgrid(x_axis, y_axis)

    for x, y in zip(x_grid.flatten(), y_grid.flatten()):
        # go to each cell/node of grid and draw on an 8 by 8 square
        x = int(x)
        y = int(y)
        node = grid[x][y]

        if node.is_start:
            decide_entrance_direction_of_maze_from_start_node(node, x, y)
            parent_dir = node.parent_direction

        elif node.is_end:
            decide_exit_direction_of_maze_from_end_node(node)
            parent_dir = node.parent_direction
        else:
            parent_dir = node.parent_direction

        directions = set([neigh[0] for neigh in node.neighbors])

        # 15 different drawing patterns for each cell
        if 'f' in directions or 'd' in directions:  # (ㄷ), f=fin, d=deadend
            if parent_dir == 2:
                draw_pattern_in_game_1(y, x)
            elif parent_dir == 4:
                draw_pattern_in_game_2(y, x)
            elif parent_dir == 6:
                draw_pattern_in_game_3(y, x)
            elif parent_dir == 8:
                draw_pattern_in_game_4(y, x)
        # 2 ways cell/node
        elif len(directions) == 1:
            one_dir = list(directions)[0]
            # (ㅡ, ㅣ)
            if (one_dir == 2 and parent_dir == 8) or (one_dir == 8 and parent_dir == 2):
                draw_pattern_in_game_5(y, x)
            elif (one_dir == 4 and parent_dir == 6) or (one_dir == 6 and parent_dir == 4):
                draw_pattern_in_game_6(y, x)
            # (ㄱ, ㄴ)
            elif (one_dir == 2 and parent_dir == 6) or (one_dir == 6 and parent_dir == 2):
                draw_pattern_in_game_7(y, x)
            elif (one_dir == 2 and parent_dir == 4) or (one_dir == 4 and parent_dir == 2):
                draw_pattern_in_game_8(y, x)
            elif (one_dir == 4 and parent_dir == 8) or (one_dir == 8 and parent_dir == 4):
                draw_pattern_in_game_9(y, x)
            elif (one_dir == 6 and parent_dir == 8) or (one_dir == 8 and parent_dir == 6):
                draw_pattern_in_game_10(y, x)
            else:
                print("while drawing error occurred @ node coordinate: ", node.coordinate)
        # 3 ways cell/node
        elif len(directions) == 2:
            if (({2, 4}.issubset(directions) and parent_dir == 6) or
                    ({2, 6}.issubset(directions) and parent_dir == 4) or
                    ({4, 6}.issubset(directions) and parent_dir == 2)):
                draw_pattern_in_game_11(y, x)
            elif (({2, 4}.issubset(directions) and parent_dir == 8) or
                  ({2, 8}.issubset(directions) and parent_dir == 4) or
                  ({4, 8}.issubset(directions) and parent_dir == 2)):
                draw_pattern_in_game_12(y, x)
            elif (({4, 6}.issubset(directions) and parent_dir == 8) or
                  ({4, 8}.issubset(directions) and parent_dir == 6) or
                  ({6, 8}.issubset(directions) and parent_dir == 4)):
                draw_pattern_in_game_13(y, x)
            elif (({2, 6}.issubset(directions) and parent_dir == 8) or
                  ({2, 8}.issubset(directions) and parent_dir == 6) or
                  ({6, 8}.issubset(directions) and parent_dir == 2)):
                draw_pattern_in_game_14(y, x)
            else:
                print("while drawing error occurred @ node coordinate: ", node.coordinate)
        # 4 ways cell/node
        elif (({4, 6, 8}.issubset(directions) and parent_dir == 2) or
              ({2, 6, 8}.issubset(directions) and parent_dir == 4) or
              ({2, 4, 8}.issubset(directions) and parent_dir == 6) or
              ({2, 4, 6}.issubset(directions) and parent_dir == 8)):
            draw_pattern_in_game_15(y, x)
        # Shouldn't be any other types of cells/nodes
        else:
            print("while drawing error occurred @ node coordinate: ", node.coordinate)


def decide_entrance_direction_of_maze_from_start_node(start_node, x_start, y_start):
    """
    Entrance direction saved as parent direction of start node.
    :param start_node: start node in grid graph
    :param x_start: x coordinate of grid graph
    :param y_start: y coordinate of grid graph
    """
    if x_start == 0 and y_start == 0:
        start_node.parent_direction = [4, 8]
    elif x_start == 0 and y_start == GRID_LENGTH - 1:
        start_node.parent_direction = [6, 8]
    elif x_start == GRID_LENGTH - 1 and y_start == 0:
        start_node.parent_direction = [2, 4]
    elif x_start == GRID_LENGTH - 1 and y_start == GRID_LENGTH - 1:
        start_node.parent_direction = [2, 6]
    elif x_start == 0:
        start_node.parent_direction = [8]
    elif x_start == GRID_LENGTH - 1:
        start_node.parent_direction = [2]
    elif y_start == 0:
        start_node.parent_direction = [4]
    elif y_start == GRID_LENGTH - 1:
        start_node.parent_direction = [6]

    # pick one entrance direction (from node perspective)
    start_node.parent_direction = random.sample(start_node.parent_direction, 1)[0]


def decide_exit_direction_of_maze_from_end_node(end_node):
    """
    Entrance direction saved as parent direction of start node.
    :param end_node: end node in grid graph
    """
    possible_exits_ls = []
    accessible_directions = MAZE.find_accessible_directions_of_node(end_node)
    for direction in accessible_directions:
        if direction == 2:
            possible_exits_ls.append(8)
        elif direction == 4:
            possible_exits_ls.append(6)
        elif direction == 6:
            possible_exits_ls.append(4)
        else:
            possible_exits_ls.append(2)

    # pick one entrance direction (from node perspective)
    end_node.neighbors = [(random.sample(possible_exits_ls, 1)[0], MAZE.rand_weight())]


def get_end_node_marker_rect():
    """
    Make end of maze sprite and return it
    """
    x = MAZE.end_coord[1] * SQ_LENGTH + SQ_LENGTH / 2
    y = MAZE.end_coord[0] * SQ_LENGTH + SQ_LENGTH / 2
    return Sprite(x, y, SQ_LENGTH * 0.4, SQ_LENGTH * 0.4, color=RED, center=True)


def draw_pattern_in_game_1(x_start, y_start):
    """
    Draws below pattern in 8 by 8 grid:
             2
          @@@@@@
        1 @    @ 3
          @    @
    """
    x_start = x_start * SQ_LENGTH
    y_start = y_start * SQ_LENGTH
    wall_1 = Sprite(x_start, y_start, WALL_WIDTH, SQ_LENGTH, color=WALL_COLOR)
    wall_2 = Sprite(x_start, y_start, SQ_LENGTH, WALL_WIDTH, color=WALL_COLOR)
    wall_3 = Sprite(x_start + SQ_LENGTH - WALL_WIDTH + 1, y_start, WALL_WIDTH, SQ_LENGTH, color=WALL_COLOR)
    WALLS.add(wall_1, wall_2, wall_3)


def draw_pattern_in_game_2(x_start, y_start):
    """
    Draws below pattern in 8 by 8 grid:
           3
        @@@@@@
             @ 2
        @@@@@@
           1
    """
    x_start = x_start * SQ_LENGTH
    y_start = y_start * SQ_LENGTH
    wall_1 = Sprite(x_start, y_start + SQ_LENGTH - WALL_WIDTH + 1, SQ_LENGTH, WALL_WIDTH, color=WALL_COLOR)
    wall_2 = Sprite(x_start + SQ_LENGTH - WALL_WIDTH + 1, y_start + 1, WALL_WIDTH, SQ_LENGTH, color=WALL_COLOR)
    wall_3 = Sprite(x_start, y_start, SQ_LENGTH, WALL_WIDTH, color=WALL_COLOR)
    WALLS.add(wall_1, wall_2, wall_3)


def draw_pattern_in_game_3(x_start, y_start):
    """
    Draws below pattern in 8 by 8 grid:
             3
          @@@@@@
        1 @
          @@@@@@
             2
    """
    x_start = x_start * SQ_LENGTH
    y_start = y_start * SQ_LENGTH
    wall_1 = Sprite(x_start, y_start, WALL_WIDTH, SQ_LENGTH, color=WALL_COLOR)
    wall_2 = Sprite(x_start, y_start + SQ_LENGTH - WALL_WIDTH + 1, SQ_LENGTH, WALL_WIDTH, color=WALL_COLOR)
    wall_3 = Sprite(x_start, y_start, SQ_LENGTH, WALL_WIDTH, color=WALL_COLOR)
    WALLS.add(wall_1, wall_2, wall_3)


def draw_pattern_in_game_4(x_start, y_start):
    """
    Draws below pattern in 8 by 8 grid:
          @    @
        1 @    @ 3
          @@@@@@
             2
    """
    x_start = x_start * SQ_LENGTH
    y_start = y_start * SQ_LENGTH
    wall_1 = Sprite(x_start, y_start, WALL_WIDTH, SQ_LENGTH, color=WALL_COLOR)
    wall_2 = Sprite(x_start, y_start + SQ_LENGTH - WALL_WIDTH + 1, SQ_LENGTH, WALL_WIDTH, color=WALL_COLOR)
    wall_3 = Sprite(x_start + SQ_LENGTH - WALL_WIDTH + 1, y_start, WALL_WIDTH, SQ_LENGTH, color=WALL_COLOR)
    WALLS.add(wall_1, wall_2, wall_3)


def draw_pattern_in_game_5(x_start, y_start):
    """
    Draws below pattern in 8 by 8 grid:
          @    @
        1 @    @ 2
          @    @
    """
    x_start = x_start * SQ_LENGTH
    y_start = y_start * SQ_LENGTH
    wall_1 = Sprite(x_start, y_start, WALL_WIDTH, SQ_LENGTH+1, color=WALL_COLOR)
    wall_2 = Sprite(x_start + SQ_LENGTH - WALL_WIDTH + 1, y_start, WALL_WIDTH, SQ_LENGTH+1, color=WALL_COLOR)
    WALLS.add(wall_1, wall_2)


def draw_pattern_in_game_6(x_start, y_start):
    """
    Draws below pattern in 8 by 8 grid:
           2
        @@@@@@

        @@@@@@
           1
    """
    x_start = x_start * SQ_LENGTH
    y_start = y_start * SQ_LENGTH
    wall_1 = Sprite(x_start, y_start + SQ_LENGTH - WALL_WIDTH + 1, SQ_LENGTH, WALL_WIDTH, color=WALL_COLOR)
    wall_2 = Sprite(x_start, y_start, SQ_LENGTH, WALL_WIDTH, color=WALL_COLOR)
    WALLS.add(wall_1, wall_2)


def draw_pattern_in_game_7(x_start, y_start):
    """
    Draws below pattern in 8 by 8 grid:
             3
          @@@@@@
        1 @
          @    @ 2
    """
    x_start = x_start * SQ_LENGTH
    y_start = y_start * SQ_LENGTH
    wall_1 = Sprite(x_start, y_start, WALL_WIDTH, SQ_LENGTH+1, color=WALL_COLOR)
    wall_2 = Sprite(x_start + SQ_LENGTH - WALL_WIDTH + 1, y_start + SQ_LENGTH - WALL_WIDTH + 1, WALL_WIDTH, WALL_WIDTH,
                    color=WALL_COLOR)
    wall_3 = Sprite(x_start, y_start, SQ_LENGTH, WALL_WIDTH, color=WALL_COLOR)
    WALLS.add(wall_1, wall_2, wall_3)


def draw_pattern_in_game_8(x_start, y_start):
    """
    Draws below pattern in 8 by 8 grid:
             3
          @@@@@@
               @ 2
        1 @    @
    """
    x_start = x_start * SQ_LENGTH
    y_start = y_start * SQ_LENGTH
    wall_1 = Sprite(x_start, y_start + SQ_LENGTH - WALL_WIDTH + 1, WALL_WIDTH, WALL_WIDTH, color=WALL_COLOR)
    wall_2 = Sprite(x_start + SQ_LENGTH - WALL_WIDTH + 1, y_start, WALL_WIDTH, SQ_LENGTH+1, color=WALL_COLOR)
    wall_3 = Sprite(x_start, y_start, SQ_LENGTH, WALL_WIDTH, color=WALL_COLOR)
    WALLS.add(wall_1, wall_2, wall_3)


def draw_pattern_in_game_9(x_start, y_start):
    """
    Draws below pattern in 8 by 8 grid:
        1 @    @
               @ 3
          @@@@@@
             2
    """
    x_start = x_start * SQ_LENGTH
    y_start = y_start * SQ_LENGTH
    wall_1 = Sprite(x_start, y_start, WALL_WIDTH, WALL_WIDTH, color=WALL_COLOR)
    wall_2 = Sprite(x_start, y_start + SQ_LENGTH - WALL_WIDTH + 1, SQ_LENGTH+1, WALL_WIDTH, color=WALL_COLOR)
    wall_3 = Sprite(x_start + SQ_LENGTH - WALL_WIDTH + 1, y_start, WALL_WIDTH, SQ_LENGTH, color=WALL_COLOR)
    WALLS.add(wall_1, wall_2, wall_3)


def draw_pattern_in_game_10(x_start, y_start):
    """
    Draws below pattern in 8 by 8 grid:
          @    @ 3
        1 @
          @@@@@@
             2
    """
    x_start = x_start * SQ_LENGTH
    y_start = y_start * SQ_LENGTH
    wall_1 = Sprite(x_start, y_start, WALL_WIDTH, SQ_LENGTH, color=WALL_COLOR)
    wall_2 = Sprite(x_start, y_start + SQ_LENGTH - WALL_WIDTH + 1, SQ_LENGTH, WALL_WIDTH, color=WALL_COLOR)
    wall_3 = Sprite(x_start + SQ_LENGTH - WALL_WIDTH + 1, y_start, WALL_WIDTH, WALL_WIDTH, color=WALL_COLOR)
    WALLS.add(wall_1, wall_2, wall_3)


def draw_pattern_in_game_11(x_start, y_start):
    """
    Draws below pattern in 8 by 8 grid:
             3
          @@@@@@

        1 @    @ 2
    """
    x_start = x_start * SQ_LENGTH
    y_start = y_start * SQ_LENGTH
    wall_1 = Sprite(x_start, y_start + SQ_LENGTH - WALL_WIDTH + 1, WALL_WIDTH, WALL_WIDTH, color=WALL_COLOR)
    wall_2 = Sprite(x_start + SQ_LENGTH - WALL_WIDTH + 1, y_start + SQ_LENGTH - WALL_WIDTH + 1, WALL_WIDTH, WALL_WIDTH,
                    color=WALL_COLOR)
    wall_3 = Sprite(x_start, y_start, SQ_LENGTH, WALL_WIDTH, color=WALL_COLOR)
    WALLS.add(wall_1, wall_2, wall_3)


def draw_pattern_in_game_12(x_start, y_start):
    """
    Draws below pattern in 8 by 8 grid:
        3
        @    @
             @ 2
        @    @
        1
    """
    x_start = x_start * SQ_LENGTH
    y_start = y_start * SQ_LENGTH
    wall_1 = Sprite(x_start, y_start + SQ_LENGTH - WALL_WIDTH + 1, WALL_WIDTH, WALL_WIDTH, color=WALL_COLOR)
    wall_2 = Sprite(x_start + SQ_LENGTH - WALL_WIDTH + 1, y_start, WALL_WIDTH, SQ_LENGTH, color=WALL_COLOR)
    wall_3 = Sprite(x_start, y_start, WALL_WIDTH, WALL_WIDTH, color=WALL_COLOR)
    WALLS.add(wall_1, wall_2, wall_3)


def draw_pattern_in_game_13(x_start, y_start):
    """
    Draws below pattern in 8 by 8 grid:
        1  @    @ 3

           @@@@@@
              2
    """
    x_start = x_start * SQ_LENGTH
    y_start = y_start * SQ_LENGTH
    wall_1 = Sprite(x_start, y_start, WALL_WIDTH, WALL_WIDTH, color=WALL_COLOR)
    wall_2 = Sprite(x_start, y_start + SQ_LENGTH - WALL_WIDTH + 1, SQ_LENGTH, WALL_WIDTH, color=WALL_COLOR)
    wall_3 = Sprite(x_start + SQ_LENGTH - WALL_WIDTH + 1, y_start, WALL_WIDTH, WALL_WIDTH, color=WALL_COLOR)
    WALLS.add(wall_1, wall_2, wall_3)


def draw_pattern_in_game_14(x_start, y_start):
    """
    Draws below pattern in 8 by 8 grid:
               3
          @    @
        1 @
          @    @
               2
    """
    x_start = x_start * SQ_LENGTH
    y_start = y_start * SQ_LENGTH
    wall_1 = Sprite(x_start, y_start, WALL_WIDTH, SQ_LENGTH, color=WALL_COLOR)
    wall_2 = Sprite(x_start + SQ_LENGTH - WALL_WIDTH + 1, y_start + SQ_LENGTH - WALL_WIDTH + 1, WALL_WIDTH, WALL_WIDTH,
                    color=WALL_COLOR)
    wall_3 = Sprite(x_start + SQ_LENGTH - WALL_WIDTH + 1, y_start, WALL_WIDTH, WALL_WIDTH, color=WALL_COLOR)
    WALLS.add(wall_1, wall_2, wall_3)


def draw_pattern_in_game_15(x_start, y_start):
    """
    Draws below pattern in 8 by 8 grid:
        4  @    @ 3

        1  @    @ 2
    """
    x_start = x_start * SQ_LENGTH
    y_start = y_start * SQ_LENGTH
    wall_1 = Sprite(x_start, y_start + SQ_LENGTH - WALL_WIDTH + 1, WALL_WIDTH, WALL_WIDTH, color=WALL_COLOR)
    wall_2 = Sprite(x_start + SQ_LENGTH - WALL_WIDTH + 1, y_start + SQ_LENGTH - WALL_WIDTH + 1, WALL_WIDTH, WALL_WIDTH,
                    color=WALL_COLOR)
    wall_3 = Sprite(x_start + SQ_LENGTH - WALL_WIDTH + 1, y_start, WALL_WIDTH, WALL_WIDTH, color=WALL_COLOR)
    wall_4 = Sprite(x_start, y_start, WALL_WIDTH, WALL_WIDTH, color=WALL_COLOR)

    WALLS.add(wall_1, wall_2, wall_3, wall_4)


def draw_window(player, end_of_maze, button):
    """
    *draw on a separate function instead of in the while loop
    """
    # WIN.fill(DARKBL)
    WIN.blit(BACKGROUND2, (0, 0))
    button.update(WIN)
    WIN.blit(end_of_maze.image, (end_of_maze.rect.x, end_of_maze.rect.y))

    WIN.blit(player.image, player.rect.topleft)

    WALLS.draw(WIN)
    # pygame needs to update once things are added to WIN
    pygame.display.flip()


def play(level):
    clock = pygame.time.Clock()

    # Maze setting & Make maze (global var)
    global GRID_LENGTH
    GRID_LENGTH = random.choice(LEVELS[level])  # *HAS TO BE a denominator of WINDOW_LENGTH!
    global SQ_LENGTH
    SQ_LENGTH = WINDOW_LENGTH / GRID_LENGTH
    global WALL_WIDTH
    WALL_WIDTH = SQ_LENGTH * 0.1
    global PLAYER_SIZE
    PLAYER_SIZE = SQ_LENGTH * 0.4

    # Container for collection of walls
    global WALLS
    WALLS = pygame.sprite.Group()
    global MAZE
    MAZE = mz.GridGraphMaze(length=GRID_LENGTH)

    # End marker rect
    global END_RECT
    END_RECT = get_end_node_marker_rect()
    ########################################

    st_i, st_j = MAZE.start_coord
    st_node = MAZE.grid[st_i][st_j]

    length_of_path = random.randint(10, GRID_LENGTH * 2)  # 10  # int:[3,inf]
    bud_count = random.randint(0, 4)  # int:[0:inf]

    MAZE.make_maze(st_node, path_length=length_of_path, bud_node_cnt=bud_count)

    # Draw maze
    draw_maze(MAZE.grid)  # <= add all sprites (walls) to sprite group (WALLS)

    # player rect initial center coordinate
    init_x = MAZE.start_coord[1] * SQ_LENGTH + SQ_LENGTH / 2
    init_y = MAZE.start_coord[0] * SQ_LENGTH + SQ_LENGTH / 2
    player = Player(BRIGHT_YELLOW, init_x, init_y)

    rotation_angle = 0

    while True:
        # this controls the speed of while loop (cap=FPS)
        # FPS times / second
        clock.tick(FPS)

        mouse_pos = pygame.mouse.get_pos()
        back_to_menu_button = bn.Button(image=pygame.image.load("assets/yellow_arrow.png"), pos=(22, WINDOW_LENGTH+21),
                                        text_input=" ", font=get_font(1), base_color="#d7fcd4",
                                        hovering_color="White")
        back_to_menu_button.change_color(mouse_pos)

        # loop & check for all the events and execute based on events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_to_menu_button.check_for_input(mouse_pos):
                    return True

        if rotation_angle == 360:
            rotation_angle = 0

        rotation_angle += ROTATION_SPEED
        player.idle(rotation_angle)

        player.move()

        draw_window(player, END_RECT, back_to_menu_button)


def get_font(size):
    return pygame.font.Font("assets/pixel_font.ttf", size)


def main_menu():
    clock = pygame.time.Clock()
    title = get_font(50).render("Zen Maze", True, "#b68f40")
    menu_rect = title.get_rect(center=(300, 200))

    easy_button = bn.Button(image=pygame.image.load("assets/four_letters_rect.png"), pos=(150, 350),
                            text_input="easy", font=get_font(20), base_color="#d7fcd4", hovering_color="White")
    med_button = bn.Button(image=pygame.image.load("assets/three_letters_rect.png"), pos=(300, 350),
                           text_input="med", font=get_font(20), base_color="#d7fcd4", hovering_color="White")
    hard_button = bn.Button(image=pygame.image.load("assets/four_letters_rect.png"), pos=(450, 350),
                            text_input="hard", font=get_font(20), base_color="#d7fcd4", hovering_color="White")
    # on_off_button = bn.Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
    #                           text_input="music", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    # choose_next_button = bn.Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
    #                                text_input="", font=get_font(75), base_color="#d7fcd4",
    #                                hovering_color="White")
    run = True
    while run:
        clock.tick(FPS)
        WIN.blit(BACKGROUND1, (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        WIN.blit(title, menu_rect)

        for button in [easy_button, med_button, hard_button]:  # , on_off_button, choose_next_button:
            button.change_color(mouse_pos)
            button.update(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.check_for_input(mouse_pos):
                    run = play('easy')
                if med_button.check_for_input(mouse_pos):
                    run = play('med')
                if hard_button.check_for_input(mouse_pos):
                    run = play('hard')
                # if on_off_button.check_for_input(mouse_pos):
                #     pygame.quit()
                # if choose_next_button.check_for_input(mouse_pos):
                #     pygame.quit()
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main_menu()
