import time
from morse_dict import *
from playsound3 import playsound


LONG_ROIP_PATH = "Sounds\\ROIP_long.wav"
SHORT_ROIP_PATH = "Sounds\\ROIP_short.wav"
TIME_BETWEEN_LETTERS = 1

def play_morse_symbol(symbol):
    if symbol == "_":
        playsound(LONG_ROIP_PATH)
    elif symbol == ".":
        playsound(SHORT_ROIP_PATH)

def play_morse_letter(char):
    if char not in MORSE_DICT.keys():
        print(f"Char {char} not in dict")
        return
    morse = MORSE_DICT[char]
    print(morse)
    for symbol in morse:
        play_morse_symbol(symbol)
    time.sleep(TIME_BETWEEN_LETTERS)
