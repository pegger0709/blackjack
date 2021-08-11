from player import *
import matplotlib.pyplot as plt

def runSimulation(initial_bankroll, bet_per_hand, n_runs, n_hands_per_run):
    dealer = Dealer()
    df = pd.DataFrame(index=range(n_hands_per_run), columns=['run_%d'%j for j in range(n_runs)])
    useBasicStrategy = True
    for j in range(n_runs):
        player = Player(initial_bankroll)
        for i in range(n_hands_per_run):
            if player.bankroll > bet_per_hand:
                dealerUpCard = Card()
                playerHand = Hand()
                player.playHand(playerHand, dealerUpCard, bet_per_hand, useBasicStrategy)
                dealer.dealHand(Hand([dealerUpCard, Card()]))
                dealer.playHand()
                dealer.settlePlayer(player)
                df.loc[i,'run_%d'%j] = player.bankroll
            else:
                color = 'red'
                break
        else:
            color = 'yellow'
        if df.loc[n_hands_per_run-1,'run_%d'%j] >= initial_bankroll: color = 'green'

        plt.plot(df.loc[:,'run_%d'%j], alpha=0.05, c=color)

    df.to_csv('MC_runs.csv', index=False)
    plt.axhline(initial_bankroll, c='k', linestyle='--')
    plt.xlim([0, n_hands_per_run])
    plt.ylim(bottom=0)
    plt.ylabel('bankroll')
    plt.xlabel('number of hands played at $%d per hand' % bet_per_hand) 
    plt.savefig('MC_runs.png')

if __name__ == '__main__':
    initial_bankroll = int(input('Please enter initial bankroll in dollars: '))
    bet_per_hand = int(input('Please enter the amount to bet per hand: '))
    n_runs = int(input('Please enter the number of Monte Carlo runs: '))
    n_hands_per_run = int(input('Please enter the maximum number of hands you want to play: '))
    runSimulation(initial_bankroll, bet_per_hand, n_runs, n_hands_per_run)


