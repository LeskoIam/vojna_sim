import random
from collections import Counter

from src.components import WarCard, WarCardEnum, WarDeck, CurrentRoundCards


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

    # def get_equal_cards(self, round_cards: CurrentRoundCards) -> list[WarCard]:
    #     value_counts = Counter(round_cards.values)
    #     equal_values = {value for value, count in value_counts.items() if count > 1}
    #     return [card for card in round_cards if card.value in equal_values]
    #
    # def war(self, round_cards: list[WarCard]):
    #     print(f"War starting with {round_cards}...")
    #     winner = random.choice(range(self.num_players))
    #     return round_cards, winner
    #
    # def is_war(self, round_cards: CurrentRoundCards):
    #     max_card = round_cards.max
    #     # detect equal value cards
    #     round_values = round_cards.values
    #     if len(round_values) != len(set(round_values)):
    #         print("At least two players have equal cards in this round.")
    #         # if they are the biggest cards in round, trigger war
    #         equal_cards = self.get_equal_cards(round_cards)
    #         print(f"{len(equal_cards)} cards [{equal_cards}] equal in this round.")
    #         if any(card == max_card for card in equal_cards):
    #             print("Equal cards are the biggest in this round, triggering war...")
    #             return True
    #     return False

#     def play_tick(self):
#         if self.player_hands is None:
#             raise ValueError("No player hands available.")
#
#         current_round_cards = CurrentRoundCards(self.num_players)
#
#         for i, player_hand in enumerate(self.player_hands):
#             if len(player_hand) == 0:
#                 print(f"Player {i} has no cards left and is out of the game.")
#                 continue
#             current_round_cards.add(player_hand.pop(0))
#             print(f"Player {i} plays {current_round_cards.player_card(i)}")
#
#         max_card = current_round_cards.max
#         war_happened = False
#         if self.is_war(current_round_cards):
#             war_happened = True
#             current_round_cards, round_winner = self.war(current_round_cards)
#
#         if not war_happened:
#             round_winner = current_round_cards.index(max_card)
#         self.player_hands[round_winner].extend(current_round_cards)
#
#         print(
#             f"Player {round_winner} wins the round with {max_card} and now has {len(self.player_hands[round_winner])} cards."
#         )
#         print(f"Max player hand sizes: {[len(h) for h in self.player_hands]}")
#         if max([len(h) for h in self.player_hands]) == 54:
#             print("Winnnnnnner")
#             self.__game_over = True
#         print()
#
#
# if __name__ == "__main__":
#     wg = WarGame(num_players=5)
#     wg.prepare_deck()
#     wg.deal_cards(1)
#
#     print()
#     for h in wg.player_hands:
#         print(h)
#
#     jh = 0
#     while not wg.game_over:
#         # while "pigs" != "fly":
#         wg.play_tick()
#         jh += 1
#         print(jh)
