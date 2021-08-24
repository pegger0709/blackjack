from player import *
import matplotlib.pyplot as plt

def runSimulation(initial_bankroll, bet_per_hand, n_decks, shoe_shuffle, n_runs, n_hands_per_run, count_cards=False):
    dealer = Dealer()
    df = pd.DataFrame(index=range(n_hands_per_run), columns=['run_%d'%j for j in range(n_runs)])
    useBasicStrategy = True
    for j in range(n_runs):
        shoe = Shoe(n_decks, shoe_shuffle)
        player = Player(initial_bankroll)
        for i in range(n_hands_per_run):
            if player.bankroll > bet_per_hand:
                bet = 5*bet_per_hand if count_cards and player.count > 10 else bet_per_hand
                dealerUpCard = shoe.dealCard()
                playerHand = shoe.dealHand()
                player.playHand(playerHand, dealerUpCard, shoe, bet, useBasicStrategy)
                dealer.dealHand(Hand([dealerUpCard, shoe.dealCard()]))
                dealer.playHand(shoe)
                for card in dealer.hand.cards: player.addToCount(COUNT_BY_CARD[card.face_value])
                dealer.settlePlayer(player)
                df.loc[i,'run_%d'%j] = player.bankroll
                if shoe.timeToShuffle(): shoe.shuffleShoe()
            else:
                color = 'red'
                break
        else:
            color = 'yellow'
        if df.loc[n_hands_per_run-1,'run_%d'%j] >= initial_bankroll: color = 'green'

        plt.plot(df.loc[:,'run_%d'%j], alpha=0.05, c=color)

    filename = 'MC_runs_counting_cards' if count_cards else 'MC_runs'
    df.to_csv(filename+'.csv', index=False)
    plt.axhline(initial_bankroll, c='k', linestyle='--')
    plt.xlim([0, n_hands_per_run])
    plt.ylim(bottom=0)
    plt.ylabel('bankroll')
    plt.xlabel('number of hands played at $%d per hand' % bet_per_hand)
    plt.savefig(filename+'.png')

if __name__ == '__main__':
    initial_bankroll = int(input('Please enter initial bankroll in dollars: '))
    bet_per_hand = int(input('Please enter the amount to bet per hand: '))
    n_decks = int(input('Please enter the number of decks in the shoe: '))
    shoe_shuffle = int(input('Please enter the number of cards to leave undealt in the shoe: '))
    n_runs = int(input('Please enter the number of Monte Carlo runs: '))
    n_hands_per_run = int(input('Please enter the maximum number of hands you want to play: '))
    count_cards = input('Press C if you want to count cards and adjust bets: ')=='C'
    runSimulation(initial_bankroll, bet_per_hand, n_decks, shoe_shuffle, n_runs, n_hands_per_run, count_cards)
