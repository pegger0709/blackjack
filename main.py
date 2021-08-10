from player import *
import matplotlib.pyplot as plt

def runSimulation(initial_bankroll, bet_per_hand, n_runs, n_hands_per_run):
    df = pd.DataFrame(index=range(n_hands_per_run), columns=range(n_runs))

    for j in range(n_runs):
        player = Player(initial_bankroll)
        for i in range(n_hands_per_run):
            if player.bankroll >= bet_per_hand:
                player.playHand(bet_per_hand)
                df.loc[i,j] = player.bankroll
            else:
                color = 'red'
                break
        else:
            color = 'yellow'
        if df.loc[n_hands_per_run-1,j] >= initial_bankroll: color = 'green'

        plt.plot(df.loc[:,j], alpha=0.1, c=color)

    df.to_csv('MC_runs.csv')
    plt.axhline(initial_bankroll, c='k', linestyle='--')
    plt.ylim(bottom=0)
    plt.ylabel('bankroll')
    plt.xlabel('number of hands played at $%d per hand' % bet_per_hand) 
    plt.show()

if __name__ == '__main__':
    initial_bankroll = int(input('Please enter initial bankroll in dollars: '))
    bet_per_hand = int(input('Please enter the amount to bet per hand: '))
    n_runs = int(input('Please enter the number of Monte Carlo runs: '))
    n_hands_per_run = int(input('Please enter the maximum number of hands you want to play: '))
    runSimulation(initial_bankroll, bet_per_hand, n_runs, n_hands_per_run)


