import random
import time


class Card:
    types = ["Guard", "Priest", "Baron", "Handmaid", "Prince", "King", "Countess", "Princess"]

    def __init__(self, type=0):
        self.type = type

    def __str__(self):
        return self.types[self.type]

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.type == other.type
        return False


class Deck:
    def __init__(self):
        num = [5, 2, 2, 2, 2, 1, 1, 1]
        self.cards = []
        for i in range(len(num)):
            for j in range(num[i]):
                self.cards.append(Card(i))

    def __str__(self):
        seen = []
        for i in range(len(self.cards)):
            seen.append(str(self.cards[i]))
        return str(seen)

    def shuffle(self):
        rng = random.Random()
        num_cards = len(self.cards)
        for i in range(num_cards):
            j = rng.randrange(i, num_cards)
            (self.cards[i], self.cards[j]) = (self.cards[j], self.cards[i])

    def pop(self):
        if not self.is_empty():
            return self.cards.pop(0)
        else:
            return None

    def is_empty(self):
        return len(self.cards) == 0


class Hand(Deck):
    def __init__(self, name=""):
        self.cards = []
        self.name = name

    def add(self, card):
        self.cards.append(card)

    def remove(self, card):
        self.cards.remove(card)

    def is_empty(self):
        return len(self.cards) == 0

    def __str__(self):
        s = self.name
        if self.is_empty():
            s += " has no cards \n"
        else:
            s += " has: " + Deck.__str__(self)
        return s


def newline():
    print("\n")


def romantic_writing():
    types = ["Guard", "Priest", "Baron", "Handmaid", "Prince", "King", "Countess", "Princess"]
    moves = [
        "Player may choose another player and name a card other than the Guard. If the chosen player's hand contains the same card as named, that player is eliminated from the round",
        "Player may privately see another player's hand",
        "Player may choose another player and privately compare hands. The player with the lower-value card is eliminated from the round.",
        "Player cannot be affected by any other player's cards until their next turn",
        "Player may choose any player (including themselves) to discard their hand and draw a new one",
        "Player may trade hands with another player",
        "Does nothing when played, but if the player has this card and either the King or the Prince in their hand, this card must be played immediately",
        "If the player plays or discards this card for any reason, they are eliminated from the round"
    ]
    players = []
    hands = []
    played = ["null", "null", "null"]

    deck = Deck()
    deck.shuffle()

    num_players = int(input("How many people (or machines) are playing? "))
    for i in range(num_players):
        players.append(input("Enter name: "))

    for player in players:
        hand = Hand(player)
        hand.add(deck.pop())
        hands.append(hand)

    i = 0
    while len(deck.cards) > 0:
        gamer = hands[i]
        card = deck.pop()
        print(f"It's {gamer.name}'s turn! {gamer.name} pulled: {card}")
        gamer.add(card)
        print(gamer)
        newline()
        for card in gamer.cards:
            print(f"{card} means: {moves[types.index(str(card))]}")
        newline()
        if str(card) == "Countess" and (str(gamer.cards[0]) == "Prince" or str(gamer.cards[0]) == "King"):
            print(f"{gamer.name} has successfully played Countess")
            gamer.remove(card)
        else:
            while True:
                card_played = input(f"What card would {gamer.name} like to play? ")
                found_card = False
                for card in gamer.cards:
                    if str(card) == card_played:
                        print(f"{gamer.name} has successfully played {card_played}")
                        gamer.remove(card)
                        print(gamer)
                        found_card = True
                        played[i] = card_played
                        break
                if found_card:
                    break
                else:
                    print("Invalid move! Try playing a card from your hand!")

            if played[i] == "Guard":
                while True:
                    not_handmaid = False
                    copy = players.copy()
                    copy.remove(gamer.name)

                    if len(copy) == 0:
                        print("No valid targets remaining.")
                        break

                    targeted = input(f"Who's card would you like to name? Possible targets are: {copy} \n")
                    num = (players.index(targeted))

                    if played[num] != "Handmaid":
                        not_handmaid = True
                    else:
                        print(f"{targeted} is protected by Handmaid! Choose another target")
                        copy.remove(targeted)

                        if len(copy) == 0:
                            print("No more valid targets left. Skipping the turn.")
                            break
                        continue

                    if not_handmaid:
                        guess = input(
                            "What card do you think they have? (Priest, Baron, Handmaid, Prince, King, Countess, Princess): ")
                        guessed = hands[num]
                        if guess == str(guessed.cards[0]):
                            print(f"Good choice! {guessed.name} was in possession of {guess}. They have been eliminated.")
                            hands.remove(guessed)
                            players.remove(targeted)
                            if num < i:
                                i -= 1
                        else:
                            print(f"{guessed.name} did not have {guess}. They are safe.")
                        break



            elif played[i] == "Priest":
                while True:
                    not_handmaid = False
                    copy = players.copy()
                    copy.remove(gamer.name)

                    if len(copy) == 0:
                        print("No valid targets remaining.")
                        break

                    targeted = input(f"Who's card would you like to see? Possible targets are: {copy} \n")
                    num = (players.index(targeted))

                    if played[num] != "Handmaid":
                        not_handmaid = True

                    else:
                        print(f"{targeted} is protected by Handmaid! Choose another target")
                        copy.remove(targeted)
                        if len(copy) == 0:
                            print("No more valid targets left. Skipping the turn.")
                            break
                        continue

                    seen = hands[num]
                    if not_handmaid:
                        print(f"{seen.name} is in possession of: {seen.cards[0]}")
                        break


            elif played[i] == "Baron":
                while True:
                    copy = players.copy()
                    copy.remove(gamer.name)

                    if len(copy) == 0:
                        print("No valid targets remaining.")
                        break

                    targeted = input(f"Who's card would you like to compare with? Possible targets are: {copy} \n")
                    num = players.index(targeted)

                    if played[num] == "Handmaid":
                        print(f"{targeted} is protected by Handmaid! Choose another target.")
                        copy.remove(targeted)

                        if len(copy) == 0:
                            print("No more valid targets left. Skipping the turn.")
                            break
                        continue

                    enemy = hands[num]
                    current_card = gamer.cards[0].type
                    enemy_card = enemy.cards[0].type

                    if current_card > enemy_card:
                        print(f"Good choice! {targeted} had a: {enemy.cards[0]}. They have been eliminated.")
                        hands.remove(enemy)
                        players.remove(targeted)
                        if num < i:
                            i -= 1
                    elif current_card == enemy_card:
                        print(f"Lukewarm choice. {targeted} had the same card as you: {enemy.cards[0]}. Nothing happens.")
                    else:
                        print(f"Terrible choice! {targeted} had a: {enemy.cards[0]}. You have been eliminated.")
                        hands.remove(gamer)
                        players.remove(gamer.name)
                        if num < i:
                            i -= 1
                    break



            elif played[i] == "Handmaid":
                print(f"{players[i]} is now protected by the Handmaid! You're safe!")


            elif played[i] == "Prince":
                while True:
                    not_handmaid = False
                    copy = players.copy()
                    if len(copy) == 0:
                        print("No valid targets remaining.")
                        break

                    targeted = input(f"Who's card would you like to discard? Possible targets are: {players} \n")
                    num = (players.index(targeted))

                    if played[num] != "Handmaid":
                        not_handmaid = True
                        if str(hands[num].cards[0]) == "Princess":
                            print(f"{targeted} was forced to discard Princess! They have been eliminated")
                            hands.remove(hands[num])
                            players.remove(str(hands[num].name))

                            if num < i:
                                i -= 1
                            break

                        else:
                            old_card = hands[num].pop()
                            new_card = deck.pop()
                            hands[num].add(new_card)

                            if str(gamer.name) == targeted:
                                print(f"{targeted} discarded {old_card} and drew {new_card}")
                            else:
                                print(f"{targeted} discarded {old_card}")
                            break

                    else:
                        print(f"{targeted} is protected by Handmaid! Choose another target")
                        copy.remove(targeted)

                        if len(copy) == 0:
                            print("No more valid targets left. Skipping the turn.")
                            break
                        continue



            elif played[i] == "King":
                while True:
                    copy = players.copy()
                    copy.remove(gamer.name)

                    if len(copy) == 0:
                        print("No valid targets remaining.")
                        break

                    targeted = input(f"Who's card would you like to trade with? Possible targets are: {copy} \n")
                    num = (players.index(targeted))

                    if played[num] != "Handmaid":
                        not_handmaid = True
                        gamer.cards, hands[num].cards = hands[num].cards, gamer.cards
                        print(f"You now have {gamer.cards[0]}. {targeted} now has {hands[num].cards[0]}")
                        break

                    else:
                        print(f"{targeted} is protected by Handmaid! Choose another target")
                        copy.remove(targeted)

                        if len(copy) == 0:
                            print("No more valid targets left. Skipping the turn.")
                            break

                        continue


            elif played[i] == "Countess":
                print(f"{players[i]} has played Countess")

        if len(hands) == 1:
            print(f"{hands[0].name} has won the game! Congrats!")
            break
        i = (i + 1) % len(players)


romantic_writing()


