from collections import deque
import random
import unittest
from uno.UnoGame import UnoGame, UnoCard, UnoDeck, make_uno_deck
from uno.UnoPlayer import UnoPlayer

class Test_UnoGame(unittest.TestCase):
    
    def setUp(self):
        
        self.players = tuple([
            UnoPlayer(str(i)) for i in range(5)
        ])

        self.game = UnoGame(self.players)

    
    def test_init_round(self):
        game = UnoGame(self.players)
        ROUND = 1
        WILD_DRAW_4 = 'WILD_DRAW_4'
        assert all(
            game.players[i] == self.players[i]
            for i in range(len(self.players))
        )
        assert game._round == ROUND
        assert len(game._deck) == (108 - 1 - 7*len(self.players))
        assert game._turn == self.players[0]
        assert game.scores == {ROUND: {p: 0 for p in self.players}}
        assert all([
            len(cards) == 7 and isinstance(cards[0], UnoCard)
            for player, cards in game._player_cards.items()
        ])
        assert isinstance(game._discard_deck, deque)
        assert len(game._discard_deck) == 1
        assert game._discard_deck[-1].name != WILD_DRAW_4
    
    def test_play_turn(self):
        nturns = 5
        for _ in range(nturns):
            self.game.play_turn()
        assert self.game._turn == self.game.players[0]




class Test_UnoCards(unittest.TestCase):

    def setUp(self):
        self.NUM_UNOCARDS = 108

        self.test_cards_values = {
            UnoCard('5', 'RED'): 5,
            UnoCard('WILD', 'BLACK'): 50,
            UnoCard('DRAW TWO', 'BLUE'): 20
        }

    def test_unocard(self):
        card = UnoCard('5', 'RED')
    
    def test_uno_deck(self):
        deck = make_uno_deck()
        assert len(deck) == self.NUM_UNOCARDS
        deck = UnoDeck()
        assert len(deck.cards) == self.NUM_UNOCARDS
        random.shuffle(deck.cards)

    def test_values(self):
        assert all(
            [
                test_val == card.get_score()
                for card, test_val in self.test_cards_values.items()
            ]
        )