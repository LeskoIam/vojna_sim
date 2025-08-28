from vojna_sim.components import WarCardEnum, WarDeck, CurrentRoundCards, WarCard


def test_war_card():
    card = WarCard(14, "hearts")
    assert str(card) == "Ace of hearts"
    assert repr(card) == "Card(value=14, color=hearts)"
    assert card == WarCard(14, "spades")
    assert card > WarCard(13, "clubs")
    assert card < WarCard(15, "diamonds")


def test_war_card_enum():
    assert WarCardEnum.name_safe(14) == "ACE"
    assert WarCardEnum.name_safe(10) == "10"
    assert WarCardEnum.name_safe(15) == "JOKER"


def test_war_deck():
    cards = [WarCard(14, "hearts"), WarCard(13, "spades")]
    deck = WarDeck(cards)
    assert len(deck) == 2
    deck.shuffle()
    assert len(deck) == 2
    popped_card = deck.pop(0)
    assert isinstance(popped_card, WarCard)
    assert len(deck) == 1


def test_current_round_cards():
    round_cards = CurrentRoundCards(3)
    card1 = WarCard(14, "hearts")
    card2 = WarCard(13, "spades")
    round_cards.add(card1, 0)
    round_cards.add(card2, 1)
    assert round_cards.player_card(0) == card1
    assert round_cards.player_card(1) == card2
    assert round_cards.max == card1
    assert round_cards.values == [card1, card2, None]
    assert list(iter(round_cards)) == [0, 1, 2]
    assert repr(round_cards) == "CurrentRoundCards(cards={0: Card(value=14, color=hearts), 1: Card(value=13, color=spades), 2: None})"