from basic_strategy import *
from hand import *


class Player:
    """
    class Player represents a blackjack player.
    
    Attributes
    ----------
    bankroll: float
        the amount of money the player has to play with
    hands: list of Hand objects
        the blackjack hands the player has. May be more than one if splitting pairs
    bets: list of floats
        the bets corresponding to the hands. They may not all be identical due to doubling down    
        
    Methods
    -------
    finish(hand)
        puts the hand in the player's list once the player has finished modifying the hand
    playHand(playerHand, dealerUpCard, bet, useBasicStrategy)
        plays the dealt hand either on the fly or according to basic strategy
    addToBankroll(amount)
        adds a player's winnings to (or deducts losses from) the bankroll
    resetBoard()
        gets rid of all hands and resets the board
    """
    def __init__(self, bankroll=0):
        """
        Parameters
        ----------
        bankroll: float
            the amount of money the player has to play with
        """
        self.bankroll = bankroll
        self.hands = []
        self.bets = []
        
    def __repr__(self):
        return 'Bankroll: %.1f dollars' % self.bankroll
    
    def finish(self, hand, bet):
        self.hands.append(hand)
        self.bets.append(bet)
    
    def resetBoard(self):
        self.hands = []
        self.bets = []
        
    def addToBankroll(self, amount=0):
        self.bankroll += amount
           
    def playHand(self, playerHand, dealerUpCard, bet=0, useBasicStrategy=True):
        """
        Plays the hand either automatically using the basic strategy or based on user input.
        
        Parameters
        ----------
        playerHand: Hand object
            The two card hand the player holds. This is passed as a parameter to enable recalling the function after splitting a pair
        dealerUpCard: Card object
            The card the dealer is showing
        bet: float
            The amount of money wagered on this hand
        useBasicStrategy: bool
            If True, play is done automatically according to basic strategy. If False, user will be asked which action to take at each decision point
            
        Returns
        -------
        None
        """
        if bet > self.bankroll: pass
        print('Dealer up card: ' + dealerUpCard.face_value)
        print(playerHand)
        if playerHand.isBlackjack():
            self.finish(playerHand, bet)
            pass
        while True:
            if playerHand.isBust():
                self.finish(playerHand, bet)
                break

            basicStrategyChoice = BASIC_STRATEGY.loc[playerHand.handToString(), dealerUpCard.face_value]
            if useBasicStrategy: 
                choice = basicStrategyChoice
            elif playerHand.isPair():
                choice = input('(h)it, (s)tand, (d)ouble down, s(p)lit pair? Basic strategy: %s\n' % basicStrategyChoice)
            else:
                choice = input('(h)it, (s)tand, (d)ouble down? Basic strategy: %s\n' % basicStrategyChoice)

            if choice=='s':
                self.finish(playerHand, bet)
                break
            elif choice=='h':
                playerHand.addCard()
                if not useBasicStrategy: print(playerHand)
            elif choice=='d':
                playerHand.addCard()
                self.finish(playerHand, 2*bet)
                break
            elif choice=='p':
                if playerHand.isPair():
                    print('split')
                    leftSplitHand = Hand([playerHand.cards[0], Card()], is_original_hand=False)
                    self.playHand(leftSplitHand, dealerUpCard, bet, useBasicStrategy)
                    rightSplitHand = Hand([playerHand.cards[1], Card()], is_original_hand=False)
                    self.playHand(rightSplitHand, dealerUpCard, bet, useBasicStrategy)
                    break
            else:
                pass
                
class Dealer:
    """
    class Dealer represents a blackjack dealer.
    
    Attributes
    ----------
    hand: Hand object
        the dealer's hand
        
    Methods
    -------
    dealHand(hand)
        starts the dealer off with a hand
    playHand()
        plays the dealer's hand according to the rules
    payoutToPlayer(self, playerHand, playerBet)
        how much should the dealer give to or take from the player
    settlePlayer(player)
        settles the accounts for all the player's hands and resets board for the next round
    """
    def __init__(self):
        self.hand = None
        
    def dealHand(self, hand=None):
        if hand is None:
            self.hand = Hand()
        else:
            self.hand = hand
            
    def playHand(self):
        finishedHand = False
        while not finishedHand:
            if self.hand.isBlackjack():
                finishedHand = True
            elif self.hand.isBust():
                finishedHand = True
            elif self.hand.value > 17:
                finishedHand = True
            elif self.hand.value == 17 and not dealerHand.isSoftHand():
                self.hand.addCard()
            else:
                self.hand.addCard()
                
    def payoutToPlayer(self, playerHand, playerBet):
        if playerHand.isBust(): return -playerBet
        else:
            if self.hand.isBust(): 
                return playerBet
            elif playerHand.isBlackjack() and not playerHand.is_original_hand: 
                return 1.5*playerBet
            elif playerHand.value > self.hand.value:
                return playerBet
            elif playerHand.value < self.hand.value:
                return -playerBet
            else:
                return 0
            
    def settlePlayer(self, player):
        n_hands = len(player.hands)
        for i in range(n_hands):
            playerHand = player.hands[i]
            playerBet = player.bets[i]
            payout = self.payoutToPlayer(playerHand, playerBet)
            player.addToBankroll(payout)
        player.resetBoard()

