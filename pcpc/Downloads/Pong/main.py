import pygame


pygame.init()
pygame.mixer.init()

FPS = 60
WINDOW_CAPTION = "Pong"
SCREEN_SIZE = 1000, 750

# Game start wait
GAME_START_WAIT = 1500

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Seperator
SEPERATOR_WIDTH = 3
SEPERATOR_LINES = 31
SEPERATOR_GAP_HEIGHT = 9

# Frame
FRAME_WIDTH = 3

# Paddle
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 30
PADDLE_WALL_DISTANCE = 50

# Ball
BALL_WIDTH = 15


# Score
FONT = pygame.font.Font("bit.ttf", 120)
SCORE_SEPERATOR_DISTANCE = 50
SCORE_TOP_DISTANCE = 20


def play_ping():
    pygame.mixer.music.load("Sounds\\ping.mp3")
    pygame.mixer.music.play()


def play_pong():
    pygame.mixer.music.load("Sounds\\pong.mp3")
    pygame.mixer.music.play()


def draw_rectangle(x, y, width, height, surface, color=WHITE):
    pygame.draw.rect(surface, color, (x, y, width, height))


def draw_field(screen):
    screen_width, screen_height = SCREEN_SIZE

    # Draw frame
    screen.fill(WHITE)
    draw_rectangle(0 + FRAME_WIDTH, 0 + FRAME_WIDTH, screen_width - FRAME_WIDTH * 2, screen_height - FRAME_WIDTH * 2, screen, BLACK)

    # Draw seperator
    x = int(round(screen_width / 2 + SEPERATOR_WIDTH / 2))
    y = 0
    line_width = SEPERATOR_WIDTH
    line_height = int(round((screen_height - SEPERATOR_GAP_HEIGHT * (SEPERATOR_LINES - 1)) / SEPERATOR_LINES))
    for i in range(SEPERATOR_LINES):
        # Draw line
        draw_rectangle(x, y, line_width, line_height, screen)
        # Move Down
        y += (line_height + SEPERATOR_GAP_HEIGHT)


def draw_paddle(x, y, screen):
    draw_rectangle(x, y, PADDLE_WIDTH, PADDLE_HEIGHT, screen)


def draw_ball(x, y, screen):
    draw_rectangle(x, y, BALL_WIDTH, BALL_WIDTH, screen)


def handle_collision(ball_x, ball_y, ball_speed_x, ball_speed_y, left_paddle_y, left_paddle_x, right_paddle_y, right_paddle_x):
    # left paddle
    if left_paddle_x <= ball_x <= (left_paddle_x + PADDLE_WIDTH):
        if left_paddle_y <= (ball_y + BALL_WIDTH) and ball_y <= (left_paddle_y + PADDLE_HEIGHT):
            if ball_speed_x < 0:
                play_ping()
                ball_speed_x = -ball_speed_x

    # right paddle
    if right_paddle_x <= (ball_x + BALL_WIDTH) <= (right_paddle_x + PADDLE_WIDTH):
        if right_paddle_y <= (ball_y + BALL_WIDTH) and ball_y <= (right_paddle_y + PADDLE_HEIGHT):
            if ball_speed_x > 0:
                play_ping()
                ball_speed_x = -ball_speed_x

    # Top edge
    if ball_y <= FRAME_WIDTH:
        play_pong()
        ball_speed_y = -ball_speed_y

    # Bottom edge
    if (ball_y + BALL_WIDTH) >= SCREEN_SIZE[1] - FRAME_WIDTH:
        play_pong()
        ball_speed_y = -ball_speed_y

    return ball_speed_x, ball_speed_y


def draw_score(left_score, right_score, surface):
    score_y = SCORE_TOP_DISTANCE

    left_text = str(left_score).zfill(2)
    left_score_x = SCREEN_SIZE[0] // 2 - SCORE_SEPERATOR_DISTANCE - FONT.size(left_text)[0]
    surface.blit(FONT.render(left_text, False, WHITE), (left_score_x, score_y))

    right_text = str(right_score).zfill(2)
    right_score_x = SCREEN_SIZE[0] // 2 + SCORE_SEPERATOR_DISTANCE
    surface.blit(FONT.render(right_text, False, WHITE), (right_score_x, score_y))


def main():
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(WINDOW_CAPTION)
    clock = pygame.time.Clock()

    # Paddles
    left_x = PADDLE_WALL_DISTANCE
    left_y = SCREEN_SIZE[1] // 2 - PADDLE_HEIGHT // 2
    right_x = SCREEN_SIZE[0] - PADDLE_WALL_DISTANCE
    right_y = SCREEN_SIZE[1] // 2 - PADDLE_HEIGHT // 2

    # Ball
    ball_x = int(round(SCREEN_SIZE[0] / 2 - BALL_WIDTH / 2))
    ball_y = int(round(SCREEN_SIZE[1] / 2 - BALL_WIDTH / 2))
    ball_speed_x = 8
    ball_speed_y = 8

    # Score
    left_score = 0
    right_score = 0

    running = True
    while running:
        # Draw field
        draw_field(screen)

        # Draw paddles
        draw_paddle(left_x, left_y, screen)
        draw_paddle(right_x, right_y, screen)

        # Draw ball
        draw_ball(ball_x, ball_y, screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Collision
        #print(f"l:{left_y}  r:{right_y}   x:{ball_x}  y:{ball_y}")
        ball_speed_x, ball_speed_y = handle_collision(ball_x, ball_y, ball_speed_x, ball_speed_y, left_y, left_x, right_y, right_x)

        # Out
        if ball_x < 0:
            ball_x = int(round(SCREEN_SIZE[0] / 2 - BALL_WIDTH / 2))
            ball_y = int(round(SCREEN_SIZE[1] / 2 - BALL_WIDTH / 2))
            ball_speed_x = 6
            ball_speed_y = 6
            right_score += 1
            pygame.time.wait(GAME_START_WAIT)
        if ball_x > (SCREEN_SIZE[0] - BALL_WIDTH):
            ball_x = int(round(SCREEN_SIZE[0] / 2 - BALL_WIDTH / 2))
            ball_y = int(round(SCREEN_SIZE[1] / 2 - BALL_WIDTH / 2))
            ball_speed_x = -6
            ball_speed_y = -6
            left_score += 1
            pygame.time.wait(GAME_START_WAIT)

        # Draw Score
        draw_score(left_score, right_score, screen)

        # Button input and movement
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_DOWN]:
            right_y += 10
        if pressed_keys[pygame.K_UP]:
            right_y -= 10
        if pressed_keys[pygame.K_s]:
            left_y += 10
        if pressed_keys[pygame.K_w]:
            left_y -= 10
        left_y = ball_y

        ball_y += ball_speed_y
        ball_x += ball_speed_x

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
