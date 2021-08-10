import pandas as pd
from hand import *

BASIC_STRATEGY = pd.DataFrame(
    index = ['hard %d'%n for n in range(5,21+1)] + ['soft %d'%n for n in range(13,21+1)] + ['pair of %d'%n for n in range(2,9+1)] + ['pair of T','pair of A'],
    columns = ['2','3','4','5','6','7','8','9','T','A'],
    data=[
    ['h','h','h','h','h','h','h','h','h','h'],#hard 5
    ['h','h','h','h','h','h','h','h','h','h'],#hard 6
    ['h','h','h','h','h','h','h','h','h','h'],#hard 7
    ['h','h','h','h','h','h','h','h','h','h'],#hard 8
    ['h','d','d','d','d','h','h','h','h','h'],#hard 9
    ['d','d','d','d','d','d','d','d','h','h'],#hard 10
    ['d','d','d','d','d','d','d','d','d','h'],#hard 11
    ['h','h','s','s','s','h','h','h','h','h'],#hard 12
    ['s','s','s','s','s','h','h','h','h','h'],#hard 13
    ['s','s','s','s','s','h','h','h','h','h'],#hard 14
    ['s','s','s','s','s','h','h','h','h','h'],#hard 15
    ['s','s','s','s','s','h','h','h','h','h'],#hard 16
    ['s','s','s','s','s','s','s','s','s','s'],#hard 17
    ['s','s','s','s','s','s','s','s','s','s'],#hard 18
    ['s','s','s','s','s','s','s','s','s','s'],#hard 19
    ['s','s','s','s','s','s','s','s','s','s'],#hard 20
    ['s','s','s','s','s','s','s','s','s','s'],#hard 21
    ['h','h','h','d','d','h','h','h','h','h'],#soft 13
    ['h','h','h','d','d','h','h','h','h','h'],#soft 14
    ['h','h','d','d','d','h','h','h','h','h'],#soft 15
    ['h','h','d','d','d','h','h','h','h','h'],#soft 16
    ['h','d','d','d','d','h','h','h','h','h'],#soft 17
    ['s','d','d','d','d','s','s','h','h','h'],#soft 18
    ['s','s','s','s','s','s','s','s','s','s'],#soft 19
    ['s','s','s','s','s','s','s','s','s','s'],#soft 20
    ['s','s','s','s','s','s','s','s','s','s'],#soft 21
    ['p','p','p','p','p','p','h','h','h','h'],#pair of 2
    ['p','p','p','p','p','p','h','h','h','h'],#pair of 3
    ['h','h','h','p','p','h','h','h','h','h'],#pair of 4
    ['d','d','d','d','d','d','d','d','h','h'],#pair of 5
    ['p','p','p','p','p','h','h','h','h','h'],#pair of 6
    ['p','p','p','p','p','p','h','h','h','h'],#pair of 7
    ['p','p','p','p','p','p','p','p','h','h'],#pair of 8
    ['p','p','p','p','p','s','p','p','s','s'],#pair of 9
    ['s','s','s','s','s','s','s','s','s','s'],#pair of T
    ['p','p','p','p','p','p','p','p','p','p'],#pair of A
    ]
).replace({'p':'h'}) #todo: deal with splitting pairs

class Player:
    def __init__(self, bankroll=0):
        self.bankroll = bankroll
        self.hand = None
        self.bet = None
        
    def __repr__(self):
        return 'Bankroll: %.1f dollars' % self.bankroll
        
    def dealHand(self, hand=None):
        if hand is None: 
            hand = Hand()
        self.hand = hand
    
    def playHand(self, bet=0, verbose=False):
        if bet > self.bankroll: pass
        else:
            dealerHand = Hand()
            if verbose: print('Dealer up card: ' + dealerHand.cards[0].face_value)
            self.dealHand()
            if verbose: print(self.hand)
            playerFinished = False
            if self.hand.isBlackjack():
                playerFinished = True
            while (not playerFinished) and (not self.hand.isBust()):
                choice = BASIC_STRATEGY.loc[self.hand.handToString(), dealerHand.cards[0].face_value]             
                if choice=='h':
                    self.hand.addCard()
                    if verbose: print(self.hand)
                elif choice=='s':
                    playerFinished = True
                elif choice=='p':
                    #todo
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
            
