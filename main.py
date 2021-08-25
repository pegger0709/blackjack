from player import *
import argparse
import matplotlib.pyplot as plt

def buildArgsParser():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter,
        epilog="")
    p._optionals.title = "Generic options"
    p.add_argument('--bankroll', dest='initial_bankroll', type=int, default=100, help="Initial bankroll of the player.")
    p.add_argument('--bet', dest='bet_per_hand', type=int, default=10, help="How much to bet on each hand.")
    p.add_argument('--decks', dest='n_decks', type=int, default=6, help="How many decks to put in the shoe.")
    p.add_argument('--shuffle', dest='shoe_shuffle', type=int, default=100, help="How many cards to leave undealt in the shoe.")
    p.add_argument('--runs', dest='n_runs', type=int, default=1000, help="How many Monte Carlo runs to perform.")
    p.add_argument('--hands', dest='n_hands_per_run', type=int, default=500, help="Maximum number of hands to play per Monte Carlo run.")
    p.add_argument('--count', action='store_true', dest='count_cards', default=False, help='If set, increase bet when count favors the player.')
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
            true_count = 52.0 * player.running_count / shoe.numberOfCards()
            if player.bankroll > args.bet_per_hand:
                if args.count_cards and true_count > 1:
                    bet = 5*args.bet_per_hand
                elif args.count_cards and true_count < -1:
                    bet = 0
                else:
                    bet = args.bet_per_hand
                dealerUpCard = shoe.dealCard()
                playerHand = shoe.dealHand()
                player.playHand(playerHand, dealerUpCard, shoe, bet, useBasicStrategy)
                dealer.dealHand(Hand([dealerUpCard, shoe.dealCard()]))
                dealer.playHand(shoe)
                for card in dealer.hand.cards: player.addToCount(COUNT_BY_CARD[card.face_value])
                dealer.settlePlayer(player)
                df.loc[i,'run_%d'%j] = player.bankroll
                if shoe.timeToShuffle(): 
                    shoe.shuffleShoe()
                    player.resetCount()
            else:
                color = 'red'
                break
        else:
            color = 'yellow'
        if df.loc[args.n_hands_per_run-1,'run_%d'%j] >= args.initial_bankroll: color = 'green'

        plt.plot(df.loc[:,'run_%d'%j], alpha=0.05, c=color)

    filename = 'MC_runs_counting_cards' if args.count_cards else 'MC_runs'
    df.to_csv(filename+'.csv', index=False)
    plt.axhline(args.initial_bankroll, c='k', linestyle='--')
    plt.xlim([0, args.n_hands_per_run])
    plt.ylim(bottom=0, top=10*args.initial_bankroll)
    plt.ylabel('bankroll')
    plt.xlabel('number of hands played at $%d per hand' % args.bet_per_hand)
    plt.savefig(filename+'.png')

if __name__ == '__main__':
    runSimulation()
