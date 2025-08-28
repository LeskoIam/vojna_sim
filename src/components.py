import random
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


class CurrentRoundCards:
    def __init__(self, number_of_players):
        self.cards: dict[int, WarCard | None] = {k: None for k in range(number_of_players)}

    def add(self, new_card: WarCard, played_by: int):
        self.cards[played_by] = new_card

    def player_card(self, player: int) -> WarCard:
        return self.cards[player]

    @property
    def max(self):
        max_card = max(self.values)
        return max_card

    @property
    def values(self) -> list:
        return list(self.cards.values())

    def index(self, card: WarCard) -> int:
        return self.cards.index(card)

    def __iter__(self):
        return iter(self.cards)

    def __repr__(self):
        return f"{self.__class__.__name__}(cards={self.cards})"