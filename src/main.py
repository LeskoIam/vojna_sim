import random
from collections import Counter
from enum import Enum


class WarCardEnum(Enum):
    ACE = 14
    JACK = 11
    QUEEN = 12
    KING = 13
    JOKER = 15

    @classmethod
    def name_safe(cls, value):
        try:
            return cls(value).name
        except ValueError:
            return str(value)


class WarCard:
    def __init__(self, value: int, color: str | None = None):
        """Represents a playing card."""
        self.value = value
        self.color = color

    def __repr__(self):
        return f"Card(value={self.value}, color={self.color})"

    def __str__(self):
        return (
            f"{WarCardEnum.name_safe(self.value).capitalize()} of {self.color}"
            if self.color
            else WarCardEnum.name_safe(self.value).capitalize()
        )

    def __eq__(self, other):
        if not isinstance(other, WarCard):
            return NotImplemented
        return self.value == other.value

    def __ne__(self, other):
        if not isinstance(other, WarCard):
            return NotImplemented
        return not self.__eq__(other)

    def __gt__(self, other):
        if not isinstance(other, WarCard):
            return NotImplemented
        return self.value > other.value

    def __lt__(self, other):
        if not isinstance(other, WarCard):
            return NotImplemented
        return self.value < other.value

    def __ge__(self, other):
        if not isinstance(other, WarCard):
            return NotImplemented
        return self.value >= other.value

    def __le__(self, other):
        if not isinstance(other, WarCard):
            return NotImplemented
        return self.value <= other.value


class WarDeck:
    def __init__(self, deck: list[WarCard]):
        self.__cards = deck

    def __len__(self):
        return len(self.__cards)

    def shuffle(self):
        random.shuffle(self.__cards)

    def pop(self, _i) -> WarCard:
        return self.__cards.pop(_i)


class WarGame:
    def __init__(self, num_players: int):
        self.num_players = num_players
        self.war_deck: WarDeck | None = None
        self.player_hands: list[list[WarCard]] | None = None

        self.__game_over = False

    @property
    def game_over(self) -> bool:
        return self.__game_over

    def prepare_deck(self):
        colors = ["heart", "diamonds", "spades", "clubs"]
        deck = [WarCard(value, color) for value in range(2, 15) for color in colors]
        # Add two jokers
        deck.append(WarCard(WarCardEnum.JOKER.value))
        deck.append(WarCard(WarCardEnum.JOKER.value))
        self.war_deck = WarDeck(deck)
        self.war_deck.shuffle()

    def deal_cards(self, cards_per_deal: int = 1):
        if self.war_deck is None:
            raise ValueError("Deck has not been created.")
        player_hands = [[] for _ in range(self.num_players)]
        players = range(self.num_players)
        while len(self.war_deck) > 0:
            for player in players:
                if len(self.war_deck) == 0:
                    break
                [
                    player_hands[player].append(self.war_deck.pop(0))
                    for _ in range(cards_per_deal)
                    if len(self.war_deck) > 0
                ]
        print(len(self.war_deck))
        self.player_hands = player_hands

    def get_equal_cards(self, round_cards: list[WarCard]) -> list[WarCard]:
        value_counts = Counter(card.value for card in round_cards)
        equal_values = {value for value, count in value_counts.items() if count > 1}
        return [card for card in round_cards if card.value in equal_values]

    def war(self, round_cards: list[WarCard]):
        print(f"War starting with {round_cards}...")
        winner = random.choice(range(self.num_players))
        return round_cards, winner

    def play_tick(self):
        if self.player_hands is None:
            raise ValueError("No player hands available.")

        round_cards = []

        for i, player_hand in enumerate(self.player_hands):
            if len(player_hand) == 0:
                print(f"Player {i} has no cards left and is out of the game.")
                continue
            round_cards.append(player_hand.pop(0))
            print(f"Player {i} plays {round_cards[-1]}")

        max_card = max(round_cards, key=lambda card: card.value)

        war_happened = False
        # detect equal value cards
        round_values = [card.value for card in round_cards]
        if len(round_values) != len(set(round_values)):
            print("At least two players have equal cards in this round.")
            # if they are the biggest cards in round, trigger war
            equal_cards = self.get_equal_cards(round_cards)
            print(f"{len(equal_cards)} cards [{equal_cards}] equal in this round.")
            if any(card == max_card for card in equal_cards):
                print("Equal cards are the biggest in this round, triggering war...")
                round_cards, round_winner = self.war(round_cards)
                war_happened = True

        if not war_happened:
            round_winner = round_cards.index(max_card)
        self.player_hands[round_winner].extend(round_cards)

        print(
            f"Player {round_winner} wins the round with {max_card} and now has {len(self.player_hands[round_winner])} cards."
        )
        print(f"Max player hand sizes: {[len(h) for h in self.player_hands]}")
        if max([len(h) for h in self.player_hands]) == 54:
            print("Winnnnnnner")
            self.__game_over = True
        print()


if __name__ == "__main__":
    wg = WarGame(num_players=5)
    wg.prepare_deck()
    wg.deal_cards(1)

    print()
    for h in wg.player_hands:
        print(h)

    jh = 0
    while not wg.game_over:
        # while "pigs" != "fly":
        wg.play_tick()
        jh += 1
        print(jh)
