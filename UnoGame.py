import tkinter
import random
import time
from typing import Union
EscapeCode = '\033'
Color = ['31','32','33','34']
Style = '1'
Powers = ['Reverse','Skip','+4Wild','Wild','+2']
COLORS = ['Red','Blue','Green','Yellow']
WildCardAmount = 4
DrawFourCardAmount = 4
ReverseCardAmount = 2
DrawTwoCardAmount = 2
SkipCardAmount = 2
NUMBERS = [1,2,3,4,5,6,7,8,9]
NumOfPlayers = 5
NumberOfCardsToStartWith = 7

class Card(object):
    def __init__(self,color,value,power,display):
        self.__value = value
        self.__color = color
        self.__power = power
        self.__display = display

    def __str__(self):
        if self.__color == 'Red':
            return f"{EscapeCode}[{Style};{Color[0]};48m{self.__color} {self.__display}"
        elif self.__color == 'Green':
            return f"{EscapeCode}[{Style};{Color[1]};48m{self.__color} {self.__display}"
        elif self.__color == 'Yellow':
            return f"{EscapeCode}[{Style};{Color[2]};48m{self.__color} {self.__display}"
        elif self.__color == 'Blue':
            return f"{EscapeCode}[{Style};{Color[3]};48m{self.__color} {self.__display}"
        else:
            return f"{self.__display}"
    def get_color(self):
        return self.__color

    def get_number(self):
        return self.__value

    def get_power(self):
        return self.__power

class ReverseCard(Card):
    def __init__(self,color,power):
        Card.__init__(self,color,12,power, u'\u27f2')
        self.__color = color
        self.__power = power

    def get_color(self):
        return self.__color

    def get_number(self):
        #Power Value of Card
        return 12

    def get_power(self):
        return self.__power


class SkipCard(Card):
    """
    Skips a player's turn
    """
    def __init__(self, color,power):
        Card.__init__(self,color,13,power,"\u2298")
        self.__color = color
        self.__power = power

    def get_color(self):
        return self.__color

    def get_number(self):
        #Power Value of Card
        return 14

    def get_power(self):
        return self.__power


class DrawFourWild(Card):
    """
    Draw Four Cards and Pick a Different Color
    """

    def __init__(self,power):
        Card.__init__(self,5,16,power, "Pick Color")
        self.__power = power

    def get_color(self):
        #Draw Fours dont have a number specified to them so we need to make a new color
        return 5

    def get_number(self):
        #Power Value of Card
        return 16

    def get_power(self):
        return self.__power

class ZeroCard(Card):
    """
    Just another Number Card
    """

    def __init__(self, color):
        Card.__init__(self,color,0,None,"0")
        self.__color = color

    def get_color(self):
        return self.__color

    def get_number(self):
        return 0


class WildCard(Card):
    """
    Pick a different Color
    """

    def __init__(self,power):
        Card.__init__(self,5,11,power,"Wild")
        self.__power = power
    def get_color(self):
        return 5

    def get_number(self):
        #Power Value of Card
        return 11

    def get_power(self):
        return self.__power


class DrawTwo(Card):
    """
    Draw Two
    """

    def __init__(self, color, power):
        Card.__init__(self, color,15,power,'+2')
        self.__color = color
        self.__power = power

    def get_color(self):
        #Power Value of Card
        return self.__color

    def get_number(self):
        return 15

    def get_power(self):
        return self.__power
class Deck:
    """
    A Deck represents the table's deck of cards, which is used to create
    a Hand (colleciton of cards).
    """
    def __init__(self):
        self.__cards = self.__load_deck()

    def __shuffle(self, deck):
        random.shuffle(deck)

    def __load_deck(self):
        """
        Creates a deck of 102 cards. Consists of 4 suits, each of which
        contain, 1-10, Eight Skips, Eight Reverses, Eight Draw 2s, Four Draw 4s, and  Four Wild Cards.
        """
        ###################################################################
        DeckOfCards = []
        for c in COLORS:
            ZCard = ZeroCard(c)
            DeckOfCards.append(ZCard)
            for i in range(2):
                for n in NUMBERS:
                    NumCard = Card(c,n,None,n)
                    DeckOfCards.append(NumCard)
            for r in range(ReverseCardAmount):
                RevCard = ReverseCard(c,Powers[0])
                DeckOfCards.append (RevCard)
            for dt in range(DrawTwoCardAmount):
                DT = DrawTwo(c,Powers[4])
                DeckOfCards.append(DT)
            for s in range(SkipCardAmount):
                Skip = SkipCard(c,Powers[1])
                DeckOfCards.append(Skip)
        """
        for df in range(DrawFourCardAmount):
            DF = DrawFourWild(Powers[2])
            DeckOfCards.append(DF)
        for w in range(WildCardAmount):
            W = WildCard(Powers[3])
            DeckOfCards.append(W)
        """
        self.__shuffle(DeckOfCards)
        """
        for i in range(len(DeckOfCards)):
            print(DeckOfCards[i])
        print(len(DeckOfCards))
        """
        return DeckOfCards
        ###################################################################
    def deal_card(self):
        """
        Removes a Card from the Deck and returns it so that it can
        enter play. If the deck is empty, deal_card() should create a
        new deck, shuffle it, and deal a card.
        """
        ###################################################################
        try:
            DealtCard = self.__cards.pop()
        except IndexError:
            self.__cards = self.__load_deck()
            DealtCard = self.__cards.pop()
        return DealtCard
        ###################################################################
    def readd_card(self,card):
        """
        Readds a Card to the Deck. If the deck is empty, deal_card() should create a
        new deck, shuffle it, and deal a card.
        """
        ###################################################################
        self.__cards.append(card)
        ###################################################################
deck = Deck()
class Hand(object):
    def __init__(self):
        self.__cards = []
        self.___Discard = ()


class Discard(object):
    """
    This class handles all the discard pile stuff such as:
    Getting the Top Card, Top Number, Top Color, Top Power
    """
    def __init__(self):
        self.Pile = []
        self.Color = []
        self.Deck = Deck()
        self.DrawFirstCard()

    def DrawFirstCard(self):
        """
        Draws the first card starting the game
        """
        FirstCard = self.Deck.deal_card()
        self.Pile.append(FirstCard)
        if self.GetPower() != None:
            self.DrawFirstCard()
        else:
            self.GetColor()

    def GetColor(self):
        """
        Returns the top card's color
        """
        Amount = len(self.Pile)
        Color = self.Pile[Amount-1].get_color()
        self.Color.append(Color)
        return self.Color[len(self.Color)-1]

    def GetPower(self):
        """
        Returns the top card's power
        """
        Amount = len(self.Pile)
        Power = self.Pile[Amount-1].get_power()
        return Power

    def GetNumber(self):
        """
        Returns the top card's number
        """
        Amount = len(self.Pile)
        Number = self.Pile[Amount-1].get_number()
        return Number

    def GetCard(self):
        """
        Returns the current top card's display
        """
        Amount = len(self.Pile)
        return self.Pile[Amount-1]

    def SetColor(self,color):
        self.Color.append(color)
#class Powers:
ReturnValue = 10
class AI(object):
    def __init__(self):
        self.__hand = Hand()
        self.__discard = Discard()
        self.__Holding = []
        self.__Colors = []
        self.__Numbers = []
        self.__Powers = []
        self.__ColorCount = []
        self.__NumberCount = []
        self.__PowerCount = []
        self.__NumberList = []
        self.__WildCards = 0
        self.__DrawFours = 0
        self.__DrawTwos = 0
        self.__Skips = 0
        self.__Reverses = 0
        self.__Zeros = 0
        self.__Ones = 0
        self.__Twos = 0
        self.__Threes = 0
        self.__Fours = 0
        self.__Fives = 0
        self.__Sixes = 0
        self.__Sevens = 0
        self.__Eights = 0
        self.__Nines = 0
        self.__Reds = 0
        self.__Blues = 0
        self.__Greens = 0
        self.__Yellows = 0
    def GetHand(self):
        return self.__Holding

    def AddCard(self,card):
        self.__Holding.append(card)
        Amount = len(self.__Holding)
        self.__Colors.append(self.__Holding[Amount-1].get_color())
        self.__Powers.append(self.__Holding[Amount-1].get_power())
        self.__Numbers.append(self.__Holding[Amount-1].get_number())
        self.__WildCards = 0
        self.__DrawFours = 0
        self.__DrawTwos = 0
        self.__Skips = 0
        self.__Reverses = 0
        self.__Zeros = 0
        self.__Ones = 0
        self.__Twos = 0
        self.__Threes = 0
        self.__Fours = 0
        self.__Fives = 0
        self.__Sixes = 0
        self.__Sevens = 0
        self.__Eights = 0
        self.__Nines = 0
        self.__Reds = 0
        self.__Blues = 0
        self.__Greens = 0
        self.__Yellows = 0
        self.__PowerRedCount = 0
        self.__PowerBlueCount = 0
        self.__PowerGreenCount = 0
        self.__PowerYellowCount = 0
        self.__PowerColorCount = []
        self.CountLists()

    def PrintValues(self):
        return self.__Colors, self.__Powers, self.__Numbers, self.__ColorCount, self.__NumberCount, self.__PowerCount,self.__Holding

    def RemoveCardFromHand(self,card):
        for i in self.__Holding:
            if i.get_color() == card.get_color() and i.get_number() == card.get_number() and i.get_power() == card.get_power():
                self.__Holding.remove(i)
                self.CountLists()
                return card
            else:
                pass

    def CountLists(self):
        self.__ColorCount = []
        self.__NumberCount = []
        self.__PowerCount = []
        self.__PowerColorCount = []
        self.__PowerBlueCount = 0
        self.__PowerGreenCount = 0
        self.__PowerYellowCount = 0
        self.__PowerRedCount = 0
        for i in ['Red', 'Yellow','Green','Blue',5]:
            ColorCount = self.__Colors.count(i)
            if i == 'Red':
                self.__Reds = ColorCount
                for i in self.__Holding:
                    cp = i.get_power()
                    if cp == "Reverse" or cp == "Skip" or cp == "+2" and i.get_color() == "Red":
                        self.__PowerRedCount + 1
                    else:
                        pass
            elif i == 'Yellow':
                self.__Yellows = ColorCount
                for i in self.__Holding:
                    cp = i.get_power()
                    if cp == "Reverse" or cp == "Skip" or cp == "+2" and i.get_color() == "Yellow":
                        self.__PowerYellowCount + 1
                    else:
                        pass
            elif i == 'Green':
                self.__Greens = ColorCount
                for i in self.__Holding:
                    cp = i.get_power()
                    if cp == "Reverse" or cp == "Skip" or cp == "+2" and i.get_color() == "Green":
                        self.__PowerGreenCount + 1
                    else:
                        pass
            elif i == 'Blue':
                self.__Blues = ColorCount
                for i in self.__Holding:
                    cp = i.get_power()
                    if cp == "Reverse" or cp == "Skip" or cp == "+2" and i.get_color() == "Blue":
                        self.__PowerBlueCount + 1
                    else:
                        pass
            self.__ColorCount.append(ColorCount)
            self.__PowerColorCount = [self.__PowerRedCount,self.__PowerYellowCount,self.__PowerGreenCount,self.__PowerBlueCount]
        for i in range(16):
            NumberCount = self.__Numbers.count(i)
            if i == 0:
                self.__Zeros = NumberCount
            elif i == 1:
                self.__Ones = NumberCount
            elif i == 2:
                self.__Twos = NumberCount
            elif i == 3:
                self.__Threes = NumberCount
            elif i == 4:
                self.__Fours = NumberCount
            elif i == 5:
                self.__Fives = NumberCount
            elif i == 6:
                self.__Sixes = NumberCount
            elif i == 7:
                self.__Sevens = NumberCount
            elif i == 8:
                self._Eights = NumberCount
            elif i == 9:
                self.__Nines = NumberCount
            else:
                pass
            self.__NumberCount.append(NumberCount)
        for i in Powers:
            PowerCount = self.__Powers.count(i)
            #Powers = ['Reverse', 'Skip', '+4Wild', 'Wild', '+2']
            if i == 'Reverse':
                self.__Reverses = PowerCount
            elif i == 'Skip':
                self.__Skips = PowerCount
            elif i == '+4Wild':
                self.__DrawFours = PowerCount
            elif i == 'Wild':
                self.__WildCards = PowerCount
            elif i == '+2':
                self.__DrawTwos = PowerCount
            else:
                pass
            self.__PowerCount.append(PowerCount)
            self.__NumberList = [self.__Zeros, self.__Ones, self.__Twos, self.__Threes, self.__Fours, self.__Fives,
                                 self.__Sixes, self.__Sevens, self.__Eights, self.__Nines, 0, self.__WildCards, self.__Reverses,
                                 0, self.__Skips, self.__DrawTwos,self.__DrawFours]


    def Play_Card(self):
        Color = self.__discard.GetColor()
        Number = self.__discard.GetNumber()

        if self.__DrawFours != 0 or self.__WildCards:
            for i in range(len(self.__Holding)):
                card = self.__Holding[i]
                cardpower = self.__Holding[i].get_power()
                if cardpower == '+4Wild':
                    RC = self.RemoveCardFromHand(card)
                    return RC
                elif cardpower == 'Wild':
                    RC = self.RemoveCardFromHand(card)
                    return RC
                else:
                    pass
        num = 0
        #for i in ['Red', 'Yellow', 'Green', 'Blue']:
        if Color == "Red":
            ColorVal = self.__PowerColorCount[0]
            ColorVal2 = self.__ColorCount[0]
        elif Color == "Yellow":
            ColorVal = self.__PowerColorCount[1]
            ColorVal2 = self.__ColorCount[1]
        elif Color == "Green":
            ColorVal = self.__PowerColorCount[2]
            ColorVal2 = self.__ColorCount[2]
        elif Color == "Blue":
            ColorVal = self.__PowerColorCount[3]
            ColorVal2 = self.__ColorCount[3]
        for i in range(len(self.__Holding)):
            if self.__DrawTwos != 0 or self.__Reverses != 0 or self.__Skips != 0 and ColorVal != 0:
                card = self.__Holding[i]
                cardpower = card.get_power()
                if cardpower == '+2' and Color == card.get_color():
                    RC = self.RemoveCardFromHand(card)
                    return RC
                elif cardpower == 'Skip' and Color == card.get_color():
                    RC = self.RemoveCardFromHand(card)
                    return RC
                elif cardpower == 'Reverse' and Color == card.get_color():
                    RC = self.RemoveCardFromHand(card)
                    return RC
                else:
                    pass
        if self.__NumberList[Number] != 0 and self.__NumberList[Number] > ColorVal2:
            for i in range(len(self.__Holding)):
                card = self.__Holding[i]
                if card.get_number == self.__NumberList[Number]:
                    RC = self.RemoveCardFromHand(card)
                    return RC
                else:
                    pass
        elif Color in self.__Colors:
            for i in range(len(self.__Holding)):
                card = self.__Holding[i]
                if card.get_color() == Color:
                    RC = self.RemoveCardFromHand(card)
                    return RC
        else:
            print("Must draw a card")
            return "Draw"
        num = num + 1











"""
class Dealer(object):
    def __init__(self)
class Game(object):
    def __init__(self):
"""
dk = Deck()
DC = Discard()
"""
print(DC.GetColor())
print(DC.GetPower())
print(DC.GetNumber())
"""
print(DC.GetCard())
ai = AI()
card = dk.deal_card()
ai.AddCard(card)
card = dk.deal_card()
ai.AddCard(card)
card = dk.deal_card()
ai.AddCard(card)
card = dk.deal_card()
ai.AddCard(card)
card = dk.deal_card()
ai.AddCard(card)
card = dk.deal_card()
ai.AddCard(card)
card = dk.deal_card()
ai.AddCard(card)
t,u,v,w,x,y,z = ai.PrintValues()
for i in z:
    print(i)
Array1 = []
Array2 = []
"""
print(u)
print(v)
print(w)
print(x)
print(y)
print(z)
"""

C = ai.Play_Card()
print(f"{C}")
C = ai.Play_Card()
print(f"{C}")
C = ai.Play_Card()
print(f"{C}")
C = ai.Play_Card()
print(f"{C}")
C = ai.Play_Card()
print(f"{C}")
#abcdefghijklmnopqrstuvwxyz
