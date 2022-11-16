import random
import names
import numpy
from tkinter import *
from PIL import Image, ImageTk, ImageFont
import PIL.Image
import PIL.ImageTk

COLORS = ['♡', '♣', '♦', '♠']
VALUES = {
    '2': 15,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'V': 11,
    'D': 12,
    'R': 13,
    'A': 14
}


class Deck:
    """ Deck du jeu de société du Président. """
    def __init__(self):
        self.__cards: list = []
        """ Génération d'un deck de 52 cartes"""
        for (symbol, val) in VALUES.items():
            for color in COLORS:
                new_card = Card(symbol, color)
                self.__cards.append(new_card)

    def shuffle(self) -> None:
        """ Mélanger les cartes de mon deck. """
        random.shuffle(self.__cards)

    def pick_card(self):
        return self.cards.pop(0)

    def __str__(self) -> str:
        return str(self.__cards)

    @property
    def cards(self):
        return self.__cards


class Card:
    __symbol: str
    __value: int
    __color: str

    def __init__(self, symbol: str, color: str):
        """
            Card Constructor.
            attrs:
                symbol: One of the VALUES keys.
                color:  One of the  COLORS values.
        """

        self.__symbol = symbol
        self.__value = VALUES[symbol]
        self.__color = color

    def __lt__(self, other):
        return self.__value < other.value

    def __gt__(self, other):
        return self.__value > other.value

    def __eq__(self, other):
        return self.__value == other.value

    def __ne__(self, other):
        return self.__value != other.value

    @property
    def value(self):
        return self.__value

    @property
    def symbol(self):
        return self.__symbol

    def __repr__(self):
        return f"{self.__symbol} {self.__color}"


class Player:
    def __init__(self, player_name=None):
        self._name: str = player_name if player_name is not None else \
            names.get_first_name()
        self._hand: list = []

    def add_to_hand(self, card: Card):
        self._hand.append(card)
        self._hand.sort()

    def remove_from_hand(self, cards: list):
        for c in cards:
            self._hand.remove(c)

    @property
    def hand(self):
        return self._hand

    @property
    def name(self):
        return self._name

    def play(self, choice, nb_cards: int) -> list:
        symbol = choice
        choice_value = VALUES[choice]
        if int(choice_value) > self.hand[-1].value or choice_value == 15 :
            print('vous ne pouvez pas jouer')
            cards_played = []
        else:
            print(symbol)
            while self.has_symbol(symbol) == 0:
                print(VALUES[symbol])
                while symbol is None or VALUES[symbol] <= choice_value:
                    print('y')
                    symbol = choice
            cards_pla = [card for card in self._hand if card.symbol ==
                            symbol]
            cards_played = cards_pla[:int(nb_cards)]
            self.remove_from_hand(cards_played)
            print(f"You play {cards_played}")
        return cards_played

    def __repr__(self):
        return f"{self.name}\t: {self.hand}"

    def has_symbol(self, card_symbol) -> int:
        nb_cards = 0
        for card in self._hand:
            if card.symbol == card_symbol:
                nb_cards += 1
        return nb_cards


class AIPlayer(Player):
    def play(self, choice, nb_cards : int) -> list:
        choice_value = VALUES[choice]
        """
        Play a card correspondig to what has been played on the table.
        TODO: Implement an AI
        Args:
            choice: The minimum card value to play.
            nb_cards: The number of cards to play.

        Returns: An array of cards to play.

        """
        cards_played = []
        best_choice = None

        for index, card in enumerate(self.hand):
            if best_choice is None and VALUES[card.symbol] >= choice_value and \
                    self.has_symbol(card.symbol) >= \
                    nb_cards:
                cards_played = self._hand[index:index+nb_cards]
                self.remove_from_hand(cards_played)
                best_choice = card.symbol
        if choice_value == 15:
            cards_played = []
        if len(cards_played) == 0:
            print(f'{self.name} ne peut pas jouer')
        else:
            print(f"{self.name} plays \t {cards_played}")
        return cards_played


class PresidentGame:
    def __init__(self, nb_players: int = 4):
        self.__generate_players(nb_players)
        self.__generate_cards()
        self.round = 0

    def __generate_players(self, nb_players: int):
        self.__players = [Player()]
        for _ in range(nb_players-1):
            self.__players.append(AIPlayer())

    def __generate_cards(self):
        self.__deck = Deck()
        self.__deck.shuffle()

    def distribute_cards(self):
        giving_card_to_player = 0
        nb_players = len(self.__players)
        while len(self.__deck.cards) > 0:
            card = self.__deck.pick_card()
            self.__players[giving_card_to_player].add_to_hand(card)
            giving_card_to_player = (giving_card_to_player+1) % nb_players

    def announce_players(self):
        for i, player in enumerate(self.players):
            print(f'vous jouer contre {player.name} possedant {len(player.hand)} en main')


    @property
    def players(self):
        return self.__players

    @property
    def ai_players(self):
        return self.__players[1:]

    @property
    def main_player(self):
        """ Main player is player 0 """
        return self.__players[0]
