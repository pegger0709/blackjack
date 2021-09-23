from player import *
player = Player(1000)
shoe = Shoe(6, 100)
dealer = Dealer()
verbose = True
useBasicStrategy = True

true_count = player.running_count * 52 / shoe.numberOfCards()
bet = 2 if true_count > 1 else 1
dealerUpCard = shoe.dealCard('9')
playerHand = Hand([shoe.dealCard('8'),shoe.dealCard('8')])
player.playHand(playerHand, dealerUpCard, shoe, bet, useBasicStrategy, verbose)
dealer.dealHand(Hand([dealerUpCard, shoe.dealCard()]))
dealer.playHand(shoe, verbose)
for hand in player.hands+[dealer.hand]:
    for card in hand.cards: player.addToCount(COUNT_BY_CARD[card.face_value])

dealer.settlePlayer(player, verbose)
player

