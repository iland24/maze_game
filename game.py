import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, player_color, init_x, init_y):
        super().__init__()
        self.width = 3
        self.height = 3
        self.image = pygame.Surface((self.width, self.height))  # Create a surface for the player
        self.image.fill(player_color)  # Fill the surface with a red color
        # 보여 주는건 이미지 ^

        # Initial position (움직이는 건 player rect)
        self.rect = self.image.get_rect(center=(init_x, init_y))

    def update(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT] and self.rect.x - VEL > 0:  # 일단 화면 나가면 못 움직이게
            self.rect.x -= VEL  # VEL = number of pixels moved left (-x dir)
        if keys_pressed[pygame.K_RIGHT] and self.rect.x + VEL + self.rect.width < WIDTH:
            self.rect.x += VEL
        if keys_pressed[pygame.K_UP] and self.rect.y - VEL > 0:
            self.rect.y -= VEL
        if keys_pressed[pygame.K_DOWN] and self.rect.y + VEL + self.rect.height < HEIGHT:
            self.rect.y += VEL
        # 여기에 else 넣어서 대기중 일때 움직임
        pygame.time.wait(20)


# COLOR
WHITE = (255, 255, 255)
YELLOW = (0.995737 * 255, 0.909344 * 255, 0.217772 * 255)
DARKBL = (0.0, 0.135112 * 255, 0.304751 * 255)


# WINDOW SIZE
grid_length = 85
WIDTH, HEIGHT = 8 * grid_length, 8 * grid_length

# WINDOW
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # size in pixels
pygame.display.set_caption("ZenMaze")

# PLAYER
# resize imported img
# scale size to 30 by 50
# here player is surface
# PLAYER = pygame.transform.scale(PLAYER_IMG, (PLAYER_WIDTH, PLAYER_HEIGHT))

VEL = 5

# Frames per second. Without designated fps,
# computer draws as many times as it is capable of per second!
# (100~1000 frames/sec). So, limit fps.
FPS = 60

# Border
# x, y, width, height *다시 중요한 점: 위에서 부터 시작
# 예시)
#                       x, y, width, height
BORDER1 = pygame.Rect(WIDTH / 2, 0, 1, HEIGHT)
BORDER2 = pygame.Rect(WIDTH / 2 + 20, 0, 1, HEIGHT)


# y가 0인 이유는 맨 위에서 부터 아래로 (HEIGHT 만큼) 내려 오는 border 이기 때문
# x에 -5를 한 이유는 width 가 10이니까 WIDTH/2 하면 바로 중간이기 때문에 10의 절반을 뺴준것


def draw_window(player):
    """
    *draw on a separate function instead of in the while loop
    """
    # give color to fill screen
    # (param: RGB=tuple(red val, green val, blue val) each 0~255)
    # pygame color = RGB
    WIN.fill(DARKBL)

    # param: surface you're drawing on, color, thing we're drawing(pygame.Rect())
    # 사실상 **바로 여기서** 매번 모든 미로를 그려야 한다... 못 뚫게 하려면 어떻게 했더라?
    pygame.draw.rect(WIN, YELLOW, BORDER1)
    pygame.draw.rect(WIN, YELLOW, BORDER2)

    # blit => draw "surface" on to another surface(screen) = blit surface on to screen
    # param: surface, (destination coord) (here, needs to be within window size)

    # sim to layering of drawing tools, need to draw on top of background!
    WIN.blit(player.image, (player.rect.x, player.rect.y))  # player coordinate*

    # pygame needs to update once things are added to screen
    pygame.display.update()


def main():
    # represents player
    # param: x,y,width,height
    player = Player(YELLOW, 100,100)
    clock = pygame.time.Clock()
    run = True
    while run:
        # this controls the speed of while loop (cap=FPS)
        # FPS times / second
        clock.tick(FPS)

        # loop & check for all the events and execute based on events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # everytime this point is reached (60 times/sec),
        # this checks keys currently being pressed. Checks ALL keys being pressed
        player.update()
        draw_window(player)

    pygame.quit()


if __name__ == "__main__":
    main()
