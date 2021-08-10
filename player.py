from basic_strategy import *
from hand import *


class Player:
    """
    class Player represents a blackjack player.
    
    Attributes
    ----------
    bankroll: float
        the amount of money the player has to play with
    bet: float
        the amount of money the player wagers on the current hand
    hand: Hand object
        the blackjack hand the player has been dealt
        
    Methods
    -------
    dealHand(hand)
        deals out a blackjack hand to the player
    playHand(bet, use_basic_strategy, verbose)
        plays the dealt hand either on the fly or according to the predetermined basic strategy
    """
    def __init__(self, bankroll=0):
        """
        Parameters
        ----------
        bankroll: float
            the amount of money the player has to play with
        """
        self.bankroll = bankroll
        self.hand = None
        self.bet = None
        
    def __repr__(self):
        return 'Bankroll: %.1f dollars' % self.bankroll
        
    def dealHand(self, hand=None):
        """
        Provides the player with an initial hand
        
        Parameters
        ----------
        hand: Hand object
            The blackjack hand to be dealt (default None). If None, then a random hand is dealt.
            
        Returns
        -------
        None
        """
        if hand is None: 
            hand = Hand()
        self.hand = hand
    
    def playHand(self, bet=0, use_basic_strategy=True, verbose=False):
        """
        Plays the hand either automatically using the basic strategy or based on user input.
        
        Parameters
        ----------
        bet: float
            The amount of money wagered on this hand
        use_basic_strategy: bool
            If True, play is done automatically according to basic strategy. If False, user will be asked which action to take at each decision point
        verbose: bool
            If True, print detailed information about the hand's outcome to the console. Otherwise, print only the bare necessities
            
        Returns
        -------
        None
        """
        if bet > self.bankroll: pass
        else:
            dealerHand = Hand()
            if not use_basic_strategy: print('Dealer up card: ' + dealerHand.cards[0].face_value)
            self.dealHand()
            if not use_basic_strategy: print(self.hand)
            playerFinished = False
            if self.hand.isBlackjack():
                playerFinished = True
            while (not playerFinished) and (not self.hand.isBust()):
                if use_basic_strategy: 
                    choice = BASIC_STRATEGY.loc[self.hand.handToString(), dealerHand.cards[0].face_value]
                elif self.hand.isPair():
                    choice = input('(h)it, (s)tand, (d)ouble down, s(p)lit pair?')         
                else:
                    choice = input('(h)it, (s)tand, (d)ouble down?')
                if choice=='h':
                    self.hand.addCard()
                    if not use_basic_strategy: print(self.hand)
                elif choice=='s':
                    playerFinished = True
                elif choice=='p':
                    if self.hand.isPair():
                        #todo
                        pass
                    else:
                        pass
                elif choice=='d':
                    bet *= 2
                    self.hand.addCard()
                    if verbose: print(self.hand)
                    playerFinished = True
                else:
                    pass
            
            if self.hand.isBust():
                self.bankroll -= bet
            elif self.hand.isBlackjack():
                self.bankroll += 1.5*bet
            else:
                while True:
                    if dealerHand.value < 17: 
                        dealerHand.addCard()
                    else:
                        break
                if dealerHand.isBust():
                    if verbose: print('Player has %d, dealer busts' % self.hand.value)
                    self.bankroll += bet
                elif self.hand.value > dealerHand.value:
                    if verbose: print('Player has %d, dealer has %d, player wins' % (self.hand.value, dealerHand.value))
                    self.bankroll += bet
                elif self.hand.value < dealerHand.value:
                    if verbose: print('Player has %d, dealer has %d, dealer wins' % (self.hand.value, dealerHand.value))
                    self.bankroll -= bet
                else:
                    if verbose: print('Player has %d, dealer has %d, tie' % (self.hand.value, dealerHand.value))        
            if verbose: print(self)
            
