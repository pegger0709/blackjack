import random

class Card:
    """
    class Card represents a single card in blackjack. Numbered cards are worth their face value. Face cards are worth 10 points. An ace is initially worth 11 points, though this value can be reduced to 1 point if necessary to prevent the total hand value from going over 21. An ace worth 11 points is called soft as its value can decrease, while an ace worth 1 point is called hard.
    
    Attributes
    ----------
    face_value: str
        the value printed on the card. Note that we lump together all 10's and face cards as 'T'
    numeric_value: int
        the point value of the card per the rules of blackjack
        
    Methods
    -------
    isSoftAce()
        determines whether a card is both an ace and worth 11 points
    hardenAce()
        turns an ace worth 11 points into an ace worth 1 point
    """
    def __init__(self, face_value=None):
        """
        Parameters
        ----------
        face_value: str
            assigns the given face value to the card. If None, assigns a random value. (default None)
        """
        if face_value is None:
            self.face_value = random.choice(['A','2','3','4','5','6','7','8','9','T','T','T','T'])
        else:
            self.face_value = face_value
        if self.face_value in ['2','3','4','5','6','7','8','9']:
            self.numeric_value = int(self.face_value)
        elif self.face_value == 'T':
            self.numeric_value = 10
        elif self.face_value =='A':
            self.numeric_value = 11
        else:
            pass
            
    def __repr__(self):
        return self.face_value
            
    def isSoftAce(self):
        """
        Determines whether a card is both an ace and worth 11 points
        
        Parameters
        ----------
        None
        
        Returns
        -------
        isSoftAce: bool
            If True, the card is an ace worth 11 points
            If False, the card is either not an ace, or an ace worth 1 point
            
        """
        if self.face_value == 'A' and self.numeric_value == 11:
            return True
        else:
            return False

    def hardenAce(self):
        """
        Turns a soft ace (11 points) into a hard ace (1 point)
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        if self.isSoftAce():
            self.numeric_value = 1
        else:
            pass

class Hand:
    """
    class Hand represents a blackjack hand, which always starts with two cards, but may expand to three or more cards. A hand has a point value, the goal of blackjack is to get as close as possible to 21 without going over (busting). A hand consisting of an ace and ten is called a blackjack and pays 3 to 2.
    
    Attributes
    ----------
    cards: list of Card objects
        the cards that make up the hand
    value: int
        the point value of the hand
        
    Methods
    -------
    isBlackjack()
        determines whether a 2-card hand is a blackjack
    isPair()
        determines whether a 2-card hand is a pair
    isSoftHand()
        determines whether a hand contains a soft ace
    firstSoftAce()
        returns the first soft ace in a hand if applicable
    isBust()
        determines whether the hand has busted, i.e. gone over 21 points with no soft aces
    addCard(card)
        adds a card into the hand
    handToString()
        string describing the hand in blackjack terms e.g. 'pair of 3' or 'hard 13' or 'soft 15'
    """
    def __init__(self, cards=None, is_original_hand=True):
        """
        Parameters
        ----------
        cards: list of Card objects (default None)
            If None, then two cards are drawn at random.
        is_original_hand: bool
            indicates whether the hand was the first dealt, or was subsequent to splitting a pair (default True)
        """
        self.is_original_hand = is_original_hand
        if cards is None:
            self.cards = [Card(), Card()]
        else:
            self.cards = cards
        if self.cards[0].face_value=='A' and self.isPair():
            self.cards[0].hardenAce()
        self.value = sum([card.numeric_value for card in self.cards])
        self.soft = self.isSoftHand()

    def isBlackjack(self):
        """
        Determines whether a 2-card hand is a blackjack
        
        Parameters
        ----------
        None
        
        Returns
        -------
        isBlackjack: bool
            True if the hand is a 2-card blackjack (one ace and one ten)
            False otherwise
        """
        if len(self.cards) != 2:
            return False
        elif (self.cards[0].face_value == 'A' and self.cards[1].face_value == 'T'):
            return True
        elif (self.cards[0].face_value == 'T' and self.cards[1].face_value == 'A'):
            return True
        else:
            return False

    def isPair(self):
        """
        Determines whether a 2-card hand is a pair
        
        Parameters
        ----------
        None
        
        Returns
        -------
        isPair: bool
            True if the hand is a 2-card pair
            False otherwise
        """
        if len(self.cards) != 2:
            return False
        else:
            return self.cards[0].face_value == self.cards[1].face_value
            
    def isSoftHand(self):
        """
        Determines whether a hand contains a soft ace
        
        Parameters
        ----------
        None
        
        Returns
        -------
        isSoftHand: bool
            True if the hand contains a soft ace
            False otherwise
        """
        for card in self.cards:
            if card.isSoftAce():
                return True
                break
        else:
            return False
            
    def firstSoftAce(self):
        """
        Returns the first soft ace in a hand if applicable
        
        Parameters
        ----------
        None
        
        Returns
        -------
        firstSoftAce: Card object or None
            The first Card object corresponding to a soft ace, or None if the hand contains no soft ace.
        """
        for card in self.cards:
            if card.isSoftAce():
                return card
                break
        else:
            return None
            
    def isBust(self):
        """
        Determines whether the hand has busted, i.e. gone over 21 points with no soft aces
        
        Parameters
        ----------
        None
        
        Returns
        -------
        isBust: bool
            True if the hand has busted, i.e. has a value over 21 even after all aces have become hard.
            False otherwise
        """
        return ~self.isSoftHand() and self.value > 21

    def addCard(self, card=None):
        """
        Adds a card into the hand. In the event that the hand contains a soft ace and the new card causes the value of the hand to exceed 21, the ace is hardened and the value of the hand adjusted accordingly.
        
        Parameters
        ----------
        card: Card object
        
        Returns
        -------
        None
        """
        if card is None:
            card = Card()
        self.cards.append(card)
        self.value += card.numeric_value
        if self.value > 21 and self.isSoftHand():
            self.value -= 10
            self.firstSoftAce().hardenAce()
            self.soft = self.isSoftHand()
            
    def handToString(self):
        """
        Describes the hand in blackjack terminology. For instance, the hand [A, 3] is called a 'soft 14', while the hand [A, 3, 8] is called a 'hard 12'.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        handToString: str
            string describing the hand in blackjack terms
        """
        if self.isBust():
            return 'bust'
        elif self.isBlackjack():
            return 'blackjack'
        elif self.isPair():
            return 'pair of ' + self.cards[0].face_value
        elif self.isSoftHand():
            return 'soft ' + str(self.value)
        else:
            return 'hard ' + str(self.value)

    def __repr__(self):
        repr = 'original' if self.is_original_hand else 'secondary'
        return repr + ' ' + self.handToString()
