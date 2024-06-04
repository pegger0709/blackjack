from player import *
from plot import *
import argparse

def buildArgsParser():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter,
        epilog="")
    p._optionals.title = "Generic options"
    p.add_argument('--bankroll', dest='initial_bankroll', type=int, default=1000, help="Initial bankroll of the player.")
    p.add_argument('--bet', dest='bet_per_hand', type=int, default=1, help="How much to bet on each hand.")
    p.add_argument('--decks', dest='n_decks', type=int, default=6, help="How many decks to put in the shoe.")
    p.add_argument('--shuffle', dest='shoe_shuffle', type=int, default=100, help="How many cards to leave undealt in the shoe.")
    p.add_argument('--runs', dest='n_runs', type=int, default=1000, help="How many Monte Carlo runs to perform.")
    p.add_argument('--hands', dest='n_hands_per_run', type=int, default=100000, help="Maximum number of hands to play per Monte Carlo run.")
    p.add_argument('--count', action='store_true', dest='count_cards', default=False, help='If set, increase bet when count favors the player.')
    p.add_argument('--verbose', action='store_true', dest='verbose', default=False, help='If set, record certain hands.')
    return p

def runSimulation():
    parser = buildArgsParser()
    args = parser.parse_args()
    dealer = Dealer()
    df = pd.DataFrame(index=range(args.n_hands_per_run), columns=['run_%d'%j for j in range(args.n_runs)])
    useBasicStrategy = True
    for j in range(args.n_runs):
        shoe = Shoe(args.n_decks, args.shoe_shuffle)
        player = Player(args.initial_bankroll)
        for i in range(args.n_hands_per_run):
            verbose = (j % 1000 == 0) and (i % 10000 == 0) and args.verbose
            outputFile = open(f"hands{'_count_cards' if args.count_cards else ''}/run_{j}/hand_{i}.txt", "a") if verbose else None
            trueCount = 52.0 * player.running_count / shoe.numberOfCards()
            if player.bankroll > args.bet_per_hand:
                if args.count_cards and trueCount > 1:
                    bet = 5*args.bet_per_hand
                elif args.count_cards and trueCount < -1:
                    bet = 0
                else:
                    bet = args.bet_per_hand
                if verbose: 
                    outputFile.write(f'{player}, true count {52.0 * player.running_count / shoe.numberOfCards()}\n')
                dealerUpCard = shoe.dealCard()
                playerHand = shoe.dealHand()
                player.playHand(playerHand, dealerUpCard, shoe, bet, useBasicStrategy, verbose, outputFile)
                dealer.dealHand(Hand([dealerUpCard, shoe.dealCard()]))
                dealer.playHand(shoe, verbose, outputFile)
                for hand in player.hands+[dealer.hand]:
                    for card in hand.cards: player.addToCount(COUNT_BY_CARD[card.face_value])
                dealer.settlePlayer(player, verbose, outputFile)
                if verbose: 
                    outputFile.write(f'{player}, true count {52.0 * player.running_count / shoe.numberOfCards()}\n')
                    outputFile.close()
                df.loc[i,'run_%d'%j] = player.bankroll
                if shoe.timeToShuffle(): 
                    shoe.shuffleShoe()
                    player.resetCount()
            else:
                break

    filename = 'MC_runs_counting_cards' if args.count_cards else 'MC_runs'
    df.to_csv(filename+'.csv', index=False)
    plot(df.fillna(0), args.initial_bankroll, args.bet_per_hand, args.n_hands_per_run)
    plt.savefig(filename+'.png')
    plt.close()
    
if __name__ == '__main__':
    runSimulation()
