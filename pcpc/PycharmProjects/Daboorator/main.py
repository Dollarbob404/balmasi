import time
import pygame
import random
import sys
from os import listdir
from os.path import isfile, join

WORKING_DIRECTORY = "\\".join(sys.argv[0].split("\\")[:-1]) + "\\"


pygame.init()
pygame.mixer.init()
pygame.display.set_icon(pygame.image.load("icon.png"))
pygame.display.set_caption("Daboorator")

WIDTH, HEIGHT = 320, 180
window = pygame.display.set_mode((WIDTH, HEIGHT))
SOUND_FOLDER_PATH = WORKING_DIRECTORY + "Sounds\\"
DABOOR_PNG_PATH = WORKING_DIRECTORY + "daboor.png"
DABOOR_CONF_PATH = WORKING_DIRECTORY + "Daboor.config"
font = pygame.font.SysFont('Arial', 50)  # Use Arial font with size 50

# Set up color
text_color = (255, 255, 255)  # White text color

bg = pygame.image.load(DABOOR_PNG_PATH)



def get_random_mp3_path():
    sound_paths = [f for f in listdir(SOUND_FOLDER_PATH) if isfile(join(SOUND_FOLDER_PATH, f))]
    sound_path = sound_paths[random.randint(0, len(sound_paths) - 1)]
    full_sound_path = SOUND_FOLDER_PATH + sound_path
    return full_sound_path


def play_daboor(mp3_path):
    daboor_sound = pygame.mixer.Sound(mp3_path)
    pygame.mixer.Sound.play(daboor_sound)

def load_config():
    with open(DABOOR_CONF_PATH, 'r') as config_file:
        min, max = config_file.read().split('\n')
    return int(min), int(max)

try:
    def main():
        min_time, max_time = load_config()
        running = True
        next_daboor = time.time()
        while running:
            window.blit(bg, (0, 0))
            window.blit(font.render(
                f"{int((next_daboor - time.time())) // 60 // 60}:{str(int((next_daboor - time.time())) // 60 % 60).zfill(2)}:{str(int((next_daboor - time.time())) % 60).zfill(2)}:{str(next_daboor - time.time()).split('.')[1][:2]}",
                True, text_color), (0, 130))  # Draw text at position (100, 100)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
            if time.time() > next_daboor:
                play_daboor(get_random_mp3_path())
                next_daboor = time.time() + random.randint(min_time * 60 * 60, max_time * 60 * 60)
        pygame.mixer.quit()
        pygame.quit()
except Exception as e:
    print(e)


if __name__ == "__main__":
    main()
