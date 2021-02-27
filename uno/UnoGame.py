"""
Classes:
    - UnoGame
"""

from itertools import product
from collections import deque
from random import shuffle
from dataclasses import dataclass, field
from typing import Tuple, List, Deque, Dict
import warnings

from uno.UnoPlayer import UnoPlayer

NUM_INIT_CARDS = 7
class UnoGame:
    """
    

    Attributes:
        - players: Tuple[UnoPlayer]
        - state: UnoGameState
    
    Methods:
        -

        static:
        - get_init_state() -> dict

    """

    def __init__(self, players: Tuple[UnoPlayer]):
        
        self.players = players
        self.scores = {}
        
        # Round attributes
        self._round = None
        self._deck = None
        self._player_cards = None
        self._turn = None

        self.init_round(round=1)

    def init_round(self, round: int):

        self._round = round
        self.scores[self._round] = {p: 0 for p in self.players}

        self._deck = make_uno_deck()
        shuffle(self._deck)
        
        self._player_cards = {p: [] for p in self.players}
        for p in self.players:
            for _ in range(NUM_INIT_CARDS):
                card = self._deck.pop()
                p.take_card(card)
                self._player_cards[p].append(card)

        # Make sure last card is not a WILD DRAW 4
        card_to_draw = self._deck[-1]
        while card_to_draw.name == 'WILD DRAW 4':
            shuffle(self._deck)
            card_to_draw = self._deck[-1]
        
        # Create discard deck and draw first card
        card = self._deck.popleft()
        self._discard_deck = deque()
        self._discard_deck.append(card)
        
        self._turn = self.players[0]

    def play_turn(self):
        
        active_player = self.get_active_player()
        action = active_player.decide_action()
        self.apply_action(active_player, action)

    def play_round(self):
        pass
        # while all(have_cards()):
            # self.play_turn()

    def run(self):
        pass
        # round = ?
        # while all(scores[]):
            # self.init_round(round)
            # self.play_round()
            # round += 1
    
    def apply_action(self, active_player, action):
        pass
        self._turn = self.get_next_player()

    def get_current_card(self):
        return self._discard_deck[-1]
    
    def get_active_player(self):
        return self._turn
    
    def get_next_player(self):
        active_idx = self.players.index(self.get_active_player())
        next_idx = (active_idx + 1) % len(self.players)
        return self.players[next_idx]


UNOCARD_COLORS = {'RED', 'BLUE', 'YELLOW', 'GREEN'}
UNOCARD_CATEGORIES = {'NUMBER', 'ACTION', 'WILD'}
UNOCARD_NUMBERS = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
UNOCARD_ACTIONS = {'REVERSE', 'SKIP', 'DRAW TWO'}
UNOCARD_WILDCARDS = {'WILD', 'WILD DRAW 4'}
UNOCARD_WILDCARD_COLOR = "BLACK"

@dataclass(frozen=True)
class UnoCard:
    name: str
    color: str
    
    def get_score(self):
        if self.name in UNOCARD_WILDCARDS:
            return 50
        elif self.name in UNOCARD_ACTIONS:
            return 20
        elif self.name in UNOCARD_NUMBERS:
            return int(self.name)
        else:
            raise Exception("Unkown card name")

def make_uno_deck() -> List[UnoCard]:
    deck = deque()
    for cat in UNOCARD_CATEGORIES:
        
        if cat == 'NUMBER':
            for num, col in product(UNOCARD_NUMBERS, UNOCARD_COLORS):
                if num == '0':
                    deck.append(UnoCard(num, col))
                elif num in UNOCARD_NUMBERS:
                    deck.append(UnoCard(num, col))
                    deck.append(UnoCard(num, col))
                else:
                    raise Exception('Unrecognized number card')
        
        if cat == 'ACTION':
            for action, col in product(UNOCARD_ACTIONS, UNOCARD_COLORS):
                deck.append(UnoCard(action, col))
                deck.append(UnoCard(action, col))
        
        if cat == 'WILD':
            for wild_card in UNOCARD_WILDCARDS:
                deck.append(UnoCard(wild_card, UNOCARD_WILDCARD_COLOR))
                deck.append(UnoCard(wild_card, UNOCARD_WILDCARD_COLOR))
                deck.append(UnoCard(wild_card, UNOCARD_WILDCARD_COLOR))
                deck.append(UnoCard(wild_card, UNOCARD_WILDCARD_COLOR))
    
    return deck


@dataclass
class UnoDeck:
    cards: Deque[UnoCard] = field(default_factory = make_uno_deck)
