import random

def generate_bank():
    bank = CardStack()

    # Yellow numbers
    bank.add(Card("Y1", "Y", "1"), 2)
    #bank.add(Card("Y2+", "Y", "2+"), 2)
    bank.add(Card("Y3", "Y", "3"), 2)
    bank.add(Card("Y4", "Y", "4"), 2)
    bank.add(Card("Y5", "Y", "5"), 2)
    bank.add(Card("Y6", "Y", "6"), 2)
    bank.add(Card("Y7", "Y", "7"), 2)
    bank.add(Card("Y8", "Y", "8"), 2)
    bank.add(Card("Y9", "Y", "9"), 2)

    # Red cards
    bank.add(Card("R1", "R", "1"), 2)
    #bank.add(Card("R2+", "R", "2+"), 2)
    bank.add(Card("R3", "R", "3"), 2)
    bank.add(Card("R4", "R", "4"), 2)
    bank.add(Card("R5", "R", "5"), 2)
    bank.add(Card("R6", "R", "6"), 2)
    bank.add(Card("R7", "R", "7"), 2)
    bank.add(Card("R8", "R", "8"), 2)
    bank.add(Card("R9", "R", "9"), 2)

    # Green cards
    bank.add(Card("G1", "G", "1"), 2)
    #bank.add(Card("G2+", "G", "2+"), 2)
    bank.add(Card("G3", "G", "3"), 2)
    bank.add(Card("G4", "G", "4"), 2)
    bank.add(Card("G5", "G", "5"), 2)
    bank.add(Card("G6", "G", "6"), 2)
    bank.add(Card("G7", "G", "7"), 2)
    bank.add(Card("G8", "G", "8"), 2)
    bank.add(Card("G9", "G", "9"), 2)

    # Blue cards
    bank.add(Card("B1", "B", "1"), 2)
    #bank.add(Card("B2+", "B", "2+"), 2)
    bank.add(Card("B3", "B", "3"), 2)
    bank.add(Card("B4", "B", "4"), 2)
    bank.add(Card("B5", "B", "5"), 2)
    bank.add(Card("B6", "B", "6"), 2)
    bank.add(Card("B7", "B", "7"), 2)
    bank.add(Card("B8", "B", "8"), 2)
    bank.add(Card("B9", "B", "9"), 2)

    # STOP
    bank.add(Card("YStop", "Y", "Stop"), 2)
    bank.add(Card("BStop", "B", "Stop"), 2)
    bank.add(Card("GStop", "G", "Stop"), 2)
    bank.add(Card("RStop", "R", "Stop"), 2)

    # Change Direction
    bank.add(Card("YChngDir", "Y", "ChngDir"), 2)
    bank.add(Card("BChngDir", "B", "ChngDir"), 2)
    bank.add(Card("RChngDir", "R", "ChngDir"), 2)
    bank.add(Card("GChngDir", "G", "ChngDir"), 2)

    # Plus
    bank.add(Card("Y+", "Y", "+"), 2)
    bank.add(Card("B+", "B", "+"), 2)
    bank.add(Card("R+", "R", "+"), 2)
    bank.add(Card("G+", "G", "+"), 2)

    # TAKI
    #bank.add(Card("YTAKI", "Y", "TAKI"), 2)
    #bank.add(Card("BTAKI", "B", "TAKI"), 2)
    #bank.add(Card("RTAKI", "R", "TAKI"), 2)
    #bank.add(Card("GTAKI", "G", "TAKI"), 2)

    # Color Change
    bank.add(Card("ColrChng", None, "ColrChng"), 4)

    # Super TAKI
    #bank.add(Card("SuprTAKI", None, "SuprTAKI"), 2)

    # King
    bank.add(Card("King", None, "King"), 2)

    # Plus 3
    #bank.add(Card("3+", None, "3+"), 2)

    # Broken Plus 3
    #bank.add(Card("3-", None, "3-"), 2)

    # Crazy card (Removed)
    #bank.add(Card("Crazy", None, "Crazy"), 2)

    # Psychopath (Removed)
    #bank.add(Card("Psycho", None, "Psycho"), 2)

    # Super plus (Removed)
    #bank.add(Card("S+", None, "S+"), 2)

    bank.shuffle()
    return bank

def give_cards(bank, players):
    for player in players:
        for i in range(9):
            player.add_cards(bank.first())


class Card:
    def __init__(self, name, color, symbol):
        self.name = name
        self.color = color
        self.symbol = symbol

    def placeable(self, bank):
        top_card = bank.look_card(-1)
        if top_card.color == self.color or top_card.symbol == self.symbol:
            return True
        if top_card.name in ["King"]:
            return True
        if self.name in ["King", "3+", "3-", "SuprTAKI", "ColrChng"]:
            self.color = top_card.color
            return True
        return False

    def __str__(self):
        return self.name

class CardStack:
    def __init__(self):
        self.cards = []

    def draw(self, index):
        if len(self.cards) == 0:
            return None
        card = self.cards.pop(index)
        return card

    def first(self):
        if len(self.cards) == 0:
            return None
        card = self.cards.pop(0)
        return card

    def shuffle(self):
        random.shuffle(self.cards)

    def add(self, card, count=1):
        for i in range(count):
            self.cards.append(Card(card.name, card.color, card.symbol))

    def number_of_cards(self):
        return len(self.cards)

    def look_card(self, i):
        if len(self.cards) == 0:
            return None
        card_copy = Card(self.cards[i].name, self.cards[i].color, self.cards[i].symbol)
        return card_copy

    def draw_specific(self, card_name):
        for i, card in enumerate(self.cards):
            if card.name == card_name:
                return self.draw(i)
        return None


    def __str__(self):
        out = ""
        for card in self.cards:
            out += card.__str__() + ", "
        return out[:-2]

class Player:
    def __init__(self, name, is_player=False):
        self.cards = CardStack()
        self.name = name
        self.is_player = is_player

    def add_cards(self, card):
        self.cards.add(card)

    def play(self, bank):
        is_valid = False
        while not is_valid:
            is_valid = True
            print(f"Top card: {bank.look_card(-1)} Color: {bank.look_card(-1).color}")
            print(f"Your cards: {self.cards}")
            card_name = input("Select card: ")
            if card_name == "draw":
                return None
            card = self.cards.draw_specific(card_name)

            # later add rules that block playing when effect blocked (2+)

            if card is None:
                is_valid = False
            elif not card.placeable(bank):
                is_valid = False
                self.cards.add(card)

        if card_name == "ColrChng":
            colors = ['Y', 'R', 'B', 'G']
            if not self.is_player:
                card.color = colors[random.randint(0, len(colors) - 1)]
            else:
                color = input("Please select new color: ")
                if color not in colors:
                    color = colors[random.randint(0, len(colors) - 1)]
                    print(f"We selected the color {color} for you since you can't type")
                card.color = color
        return card


class Bank:
    def __init__(self):
        self.bank = generate_bank()
        self.bank.shuffle()
        self.discard_pile = CardStack()

    def first(self):
        if self.bank.number_of_cards() == 0:
            while self.discard_pile.number_of_cards() > 8:
                self.bank.add(self.discard_pile.first())
            self.bank.shuffle()
        card = self.bank.first()
        return card

    def discard(self, card):
        self.discard_pile.add(card)

    def look_card(self, i):
        if self.discard_pile.number_of_cards() == 0:
            return None
        card_copy = Card(
            self.discard_pile.look_card(i).name,
            self.discard_pile.look_card(i).color,
            self.discard_pile.look_card(i).symbol
        )
        return card_copy





def main():
    #bank = generate_bank()
    #used_cards = CardStack()
    bank = Bank()

    player = Player("Player", is_player=True)
    cpu1 = Player("CPU1", is_player=True)
    #cpu2 = Player("CPU2")
    #cpu3 = Player("CPU3")

    players = [player, cpu1]
    give_cards(bank, players)

    while bank.look_card(-1) is None or not bank.look_card(-1).symbol.isnumeric():
        bank.discard(bank.first())

    game_over = False
    current_player_index = 0
    play_direction = 1

    while not game_over:
        current_player = players[current_player_index]
        turn_over = False
        while not turn_over:
            played_card = current_player.play(bank)
            turn_over = True
            if played_card is None:
                current_player.add_cards(bank.first())
                break
            bank.discard(played_card)
            if played_card.symbol == "ChngDir":
                play_direction = -play_direction
            elif played_card.symbol == "Stop":
                current_player_index += play_direction
            elif played_card.symbol == "+" or played_card.symbol == "King":
                turn_over = False

            if current_player.cards.number_of_cards() == 0:
                game_over = True


        # move to next player
        current_player_index += play_direction
        if current_player_index < 0:
            current_player_index += len(players)
        if current_player_index == len(players):
            current_player_index = 0



if __name__ == "__main__":
    main()