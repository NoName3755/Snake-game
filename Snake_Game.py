import pygame
import random
import os
import time

pygame.mixer.init()

# screen width and height
screen_width = 700
screen_height = 400

# color define in RGB
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 200, 50)
pink = (248, 185, 235)

# music list
musics = ["screen/bgm.mp3", "screen/bgm1.mp3", "screen/bgm2.mp3"]


# iniitializing the pygame
pygame.init()

gamewindow = pygame.display.set_mode((screen_width, screen_height))

# making the backgroung image
bgimg2 = pygame.image.load("screen/bg2.jpg")
bgimg2 = pygame.transform.scale(bgimg2, (screen_width, screen_height)).convert_alpha()

bgimg1 = pygame.image.load("screen/intro.png")
bgimg1= pygame.transform.scale(bgimg1, (screen_width, screen_height)).convert_alpha()

bgimg = pygame.image.load("screen/outro.png")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()


pygame.display.set_caption("My Game")
pygame.display.update()

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)


# making function to showing the score
def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gamewindow.blit(screen_text, [x, y])


# making the function to make the head
def plot_snake(gamewindow, color, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.rect(gamewindow, color, [x, y, snake_size, snake_size])


def welcome():
    exit_game = False
    # selecting music randomly
    select_music = random.choice(musics)
    pygame.mixer.music.load(select_music)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
    gamewindow.blit(bgimg1, (0, 0))
    while not exit_game:
        '''uncomment this if you dont want image'''
        # gamewindow.fill(pink)
        # text_screen("Welcome to the Snake Game", black, 95, 150)
        # text_screen("Press Space Bar to play game", black, 85, 190)
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                exit_game = True
            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_SPACE:
                    # pygame.mixer.music.stop()
                    gameloop()
        pygame.display.update()
        clock.tick(30)
    pygame.quit()
    exit()


def gameloop():
    # game specific variable
    exit_game = False
    game_over = False
    snake_x = 50
    snake_y = 60
    snake_size = 10
    fps = 30
    init_velocity = 4
    velocity_x = 0
    velocity_y = 0
    food_x = random.randint(30, screen_width - 10)
    food_y = random.randint(50, screen_height - 10)
    snake_length = 5
    snake_list = []
    score = 0
    
    if not (os.path.exists("HighScore.txt")):
        with open("HighScore.txt", "w") as f:
            f.write("0")
    with open("HighScore.txt") as f:
        high_score = f.read()

    # running the function until exit
    while not exit_game:
        if game_over:
            pygame.mixer.music.stop()
            time.sleep(1)
            # gamewindow.fill(white)
            gamewindow.blit(bgimg, (0, 0))
            # text_screen("Game Over!! Press enter to play again", red, 7, 175)

            with open("HighScore.txt", "w") as f:
                f.write(str(high_score))

            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    exit_game = True
                if events.type == pygame.KEYDOWN:
                    if events.key == pygame.K_RETURN:
                        gameloop()
        else:
            for events in pygame.event.get():
                if events.type == pygame.QUIT:  # if click the close button exit_game will be True
                    exit_game = True

                if events.type == pygame.KEYDOWN:  # if click the keyboard
                    if events.key == pygame.K_RIGHT:  # if click the right arrow key
                        velocity_x = init_velocity
                        velocity_y = 0

                    if events.key == pygame.K_LEFT:  # if click the left arrow key
                        velocity_x = -init_velocity
                        velocity_y = 0

                    if events.key == pygame.K_UP:  # if click the up arrow key
                        velocity_y = -init_velocity
                        velocity_x = 0

                    if events.key == pygame.K_DOWN:  # if click the down arrow key
                        velocity_y = init_velocity
                        velocity_x = 0

                    if events.key == pygame.K_q:
                        score += 10

            snake_x += velocity_x
            snake_y += velocity_y

            # if the distance between the center of head and food is less than 8 then it execute
            if abs(snake_x - food_x) < 8 and abs(snake_y - food_y) < 8:
                # pygame.mixer.music.load("screen/snakeeat.wav")
                # pygame.mixer.music.play()
                eat_sound = pygame.mixer.Sound("screen/snakeeat.wav")
                pygame.mixer.Sound.play(eat_sound)
                score += 10
                food_x = random.randint(30, screen_width - 30)
                food_y = random.randint(30, screen_height - 30)
                snake_length += 5

            head = [snake_x, snake_y]
            snake_list.append(head)

            # this will delete the first head
            if len(snake_list) > snake_length:
                del snake_list[0]

            # the game will be over if the head on the other head
            if head in snake_list[:-5]:
                game_over = True

            # if the snake goes out of the screen then game will be over
            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True

            if score > int(high_score):
                high_score = score

            # gamewindow.fill(green)
            gamewindow.blit(bgimg2, (0, 0))
            '''where, color, [pos-x, pos-y and the size in length and breadth]'''
            text_screen(f"Score: {score}     High Score: {high_score}", red, 5, 5)
            plot_snake(gamewindow, black, snake_list, snake_size)
            pygame.draw.rect(gamewindow, red, [food_x, food_y, 10, 10])

        pygame.display.update()

        clock.tick(fps)

    pygame.quit()
    exit()


welcome()

