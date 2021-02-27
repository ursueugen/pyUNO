"""
"""

# from uno.UnoGame import UnoCard

class UnoPlayer:

    """

    Attributes:
        - name: str
    
    Methods:
        - receive_cards()

    """

    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return self.name
    
    def __str__(self):
        return self.name

    def take_card(self, card):  # TODO: typehint
        pass

    def decide_action(self):
        return None