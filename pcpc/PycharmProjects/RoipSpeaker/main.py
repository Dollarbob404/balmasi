import morse
import time


SLEEP_BETWEEN_WORDS = 3

def get_split(input_string):
    input_string.replace('\n', ' ')
    morse_list = input_string.split(" ")
    return morse_list

def play_morse_word(morse_word):
    for char in morse_word:
        morse.play_morse_letter(char)
    time.sleep(SLEEP_BETWEEN_WORDS)
    print()

def play_morse_list(morse_list):
    for morse_word in morse_list:
        play_morse_word(morse_word)


def main():
    text = input("Please enter a sentence in hebrew: ")
    word_list = get_split(text)
    play_morse_list(word_list)
    input("Press ENTER to close . . .")


if __name__ == "__main__":
    main()
