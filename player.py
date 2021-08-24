from basic_strategy import *
from hand import *

COUNT_BY_CARD = {'A':-1,'2':1,'3':1,'4':1,'5':1,'6':1,'7':0,'8':0,'9':0,'T':-1}

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
    count: int
        the running count in the player's head during card counting

    Methods
    -------
    finish(hand)
        puts the hand in the player's list once the player has finished modifying the hand
    playHand(playerHand, dealerUpCard, shoe, bet, useBasicStrategy)
        plays the dealt hand either on the fly or according to basic strategy
    addToBankroll(amount)
        adds a player's winnings to (or deducts losses from) the bankroll
    addToCount(count)
        adds to the rolling card count
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
        self.count = 0

    def __repr__(self):
        return 'Bankroll: %.1f dollars, count: %d' % (self.bankroll, self.count)

    def finish(self, hand, bet):
        """
        Stores the hand and bet in memory, no longer to be touched until it is time to settle accounts

        Parameters
        ----------
        hand: Hand object
        bet: float

        Returns
        -------
        None
        """
        self.hands.append(hand)
        self.bets.append(bet)

    def resetBoard(self):
        """
        Resets the board in preparation for the next round of play

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.hands = []
        self.bets = []

    def addToBankroll(self, amount=0):
        """
        Adjusts the bankroll following a win or loss

        Parameters
        ----------
        amount: float
            amount by which to adjust the bankroll (default 0)

        Returns
        -------
        None
        """
        self.bankroll += amount

    def playHand(self, playerHand, dealerUpCard, shoe, bet=0, useBasicStrategy=True, verbose=False):
        """
        Plays the hand either automatically using the basic strategy or based on user input.

        Parameters
        ----------
        playerHand: Hand object
            The two card hand the player holds. This is passed as a parameter to enable recalling the function after splitting a pair
        dealerUpCard: Card object
            The card the dealer is showing
        shoe: Shoe object
            The shoe from which to deal the subsequent cards in the hand
        bet: float
            The amount of money wagered on this hand
        useBasicStrategy: bool
            If True, play is done automatically according to basic strategy. If False, user will be asked which action to take at each decision point
        verbose: bool

        Returns
        -------
        None
        """
        if bet > self.bankroll: pass
        if verbose or not useBasicStrategy:
            print('Dealer up card: ' + dealerUpCard.face_value)
            print(playerHand)

        self.addToCount(COUNT_BY_CARD[playerHand.cards[0].face_value] + COUNT_BY_CARD[playerHand.cards[1].face_value])
        while True:
            if playerHand.isBust():
                self.finish(playerHand, bet)
                break
            if playerHand.isBlackjack():
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
                newCard = shoe.dealCard()
                playerHand.addCard(newCard)
                self.addToCount(COUNT_BY_CARD[newCard.face_value])
                if not useBasicStrategy: print(playerHand)
            elif choice=='d':
                newCard = shoe.dealCard()
                playerHand.addCard(newCard)
                self.addToCount(COUNT_BY_CARD[newCard.face_value])
                self.finish(playerHand, 2*bet)
                break
            elif choice=='p':
                if playerHand.isPair():
                    if verbose: print('split')
                    leftSplitCard = playerHand.cards[0]
                    leftSplitCard.softenAce()
                    leftSplitHand = Hand([leftSplitCard, shoe.dealCard()], is_original_hand=False)
                    self.playHand(leftSplitHand, dealerUpCard, shoe, bet, useBasicStrategy)
                    rightSplitCard = playerHand.cards[1]
                    rightSplitCard.softenAce()
                    rightSplitHand = Hand([rightSplitCard, shoe.dealCard()], is_original_hand=False)
                    self.playHand(rightSplitHand, dealerUpCard, shoe, bet, useBasicStrategy)
                    break
            else:
                pass

    def addToCount(self, number=0):
        self.count += number

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
        """
        Gives the dealer a given hand

        Parameters
        ----------
        hand: Hand object
            hand to give the dealer

        Returns
        -------
        None
        """
        if hand is None:
            self.hand = Hand()
        else:
            self.hand = hand

    def playHand(self, shoe):
        """
        Makes the dealer play the hand according to the rules (hits soft 17)

        Parameters
        ----------
        shoe: Shoe object
            the shoe from which to take the dealer's hand

        Returns
        -------
        None
        """
        finishedHand = False
        while not finishedHand:
            if self.hand.isBlackjack():
                finishedHand = True
            elif self.hand.isBust():
                finishedHand = True
            elif self.hand.value > 17:
                finishedHand = True
            elif self.hand.value == 17 and not self.hand.isSoftHand():
                self.hand.addCard(shoe.dealCard())
            else:
                self.hand.addCard(shoe.dealCard())

    def payoutToPlayer(self, playerHand, playerBet):
        """
        Determines how much a player wins or loses on a bet

        Parameters
        ----------
        playerHand: Hand object
        playerBet: float

        Returns:
        payout: float
        """
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
        """
        Settles accounts with the player and clears board for the next round of play

        Parameters
        ----------
        player: Player object

        Returns
        -------
        None
        """
        n_hands = len(player.hands)
        for i in range(n_hands):
            playerHand = player.hands[i]
            playerBet = player.bets[i]
            payout = self.payoutToPlayer(playerHand, playerBet)
            player.addToBankroll(payout)
        player.resetBoard()
        self.hand = None
