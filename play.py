import argparse
import sys
from player import *

def buildArgsParser():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter,
        epilog="")
    p._optionals.title = "Generic options"
    p.add_argument('--bankroll', dest='initial_bankroll', type=int, default=1000, help="Initial bankroll of the player.")
    p.add_argument('--decks', dest='n_decks', type=int, default=-1, help="How many decks to put in the shoe.")
    p.add_argument('--shuffle', dest='shoe_shuffle', type=int, default=100, help="How many cards to leave undealt in the shoe.")
    return p

if __name__ == "__main__":
    parser = buildArgsParser()
    args = parser.parse_args()
    player = Player(args.initial_bankroll)
    shoe = Shoe(args.n_decks, args.shoe_shuffle)
    dealer = Dealer()
    useBasicStrategy = False
    verbose = True
    outputFile = sys.stdout
    while player.bankroll > 0:
        print(shoe)
        print(player)
        true_count = player.running_count * 52 / shoe.numberOfCards()
        bet = int(input("Please enter the bet: "))
        dealerUpCard = shoe.dealCard()
        playerHand = shoe.dealHand()
        player.playHand(playerHand, dealerUpCard, shoe, bet, useBasicStrategy, verbose, outputFile)
        dealer.dealHand(Hand([dealerUpCard, shoe.dealCard()]))
        dealer.playHand(shoe, verbose, outputFile)
        for hand in player.hands+[dealer.hand]:
            for card in hand.cards: player.addToCount(COUNT_BY_CARD[card.face_value])
        dealer.settlePlayer(player, verbose, outputFile)

