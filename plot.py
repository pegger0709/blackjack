import matplotlib.pyplot as plt
import pandas as pd

def plot(df, bankroll, bet, n_hands_per_run):
    winning_runs = 0
    losing_runs = 0
    bankrupting_runs = 0
    for j, col in enumerate(df.columns):
        if df.iloc[-1,j] == 0:
            bankrupting_runs += 1
            color = 'red'
        elif df.iloc[-1,j] > bankroll:
            winning_runs += 1
            color = 'green'
        else:
            losing_runs += 1
            color = 'yellow'
        plt.plot(df.loc[:,col], c=color, alpha=0.05)
    plt.axhline(bankroll, c='k', linestyle='--')
    plt.xlim([0, n_hands_per_run])
    plt.ylim(bottom=0)
    plt.ylabel('bankroll')
    plt.xlabel(f'number of hands played at ${bet} per hand')
    plt.title(f'{winning_runs+losing_runs+bankrupting_runs} runs: {winning_runs} winning, {losing_runs} losing, {bankrupting_runs} bankrupting')
