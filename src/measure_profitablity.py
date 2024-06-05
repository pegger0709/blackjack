import numpy as np
import pandas as pd
import glob
import argparse
def buildArgsParser():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter,
        epilog="")
    p._optionals.title = "Generic options"
    p.add_argument('--bankroll', dest='initial_bankroll', type=int, default=1000, help="Initial bankroll of the player.")
    p.add_argument('--bet', dest='bet_per_hand', type=int, default=1, help="How much to bet on each hand.")
    return p

if __name__ == "__main__":
    parser = buildArgsParser()
    args = parser.parse_args()
    pnl_basicstrategy = pd.read_csv("data/MC_runs.csv").fillna(0) - args.initial_bankroll
    num_hands = pnl_basicstrategy.shape[0]
    total_number_of_runs = pnl_basicstrategy.shape[1]
    bankrupting_runs = (pnl_basicstrategy.iloc[-1] == -args.initial_bankroll).sum()
    profitable_runs = (pnl_basicstrategy.iloc[-1] >= 0.).sum()
    losing_runs = (np.logical_and(pnl_basicstrategy.iloc[-1] < 0., pnl_basicstrategy.iloc[-1] > -args.initial_bankroll)).sum()
    message = f"We ran {total_number_of_runs} runs of {num_hands} hands each, using the basic strategy. Of these runs, {bankrupting_runs} went bankrupt, {losing_runs} lost money, and {profitable_runs} were profitable.\nOn these runs, the average profit was {pnl_basicstrategy.iloc[-1].mean()/(num_hands*args.bet_per_hand)*100} percent of each hand; the maximal profit was {pnl_basicstrategy.iloc[-1].max()/(num_hands*args.bet_per_hand)*100} percent"
    print(message)
    for csv_filename in glob.glob("data/MC_runs_counting_cards*.csv"):
        count_factor = csv_filename[:-4].split('_')[-1]
        pnl_cardcount = pd.read_csv(csv_filename).fillna(0) - args.initial_bankroll
        num_hands = pnl_cardcount.shape[0]
        total_number_of_runs = pnl_cardcount.shape[1]
        bankrupting_runs = (pnl_cardcount.iloc[-1] == -args.initial_bankroll).sum()
        profitable_runs = (pnl_cardcount.iloc[-1] >= 0.).sum()
        losing_runs = (np.logical_and(pnl_cardcount.iloc[-1] < 0., pnl_cardcount.iloc[-1] > -args.initial_bankroll)).sum()
        message = f"We ran {total_number_of_runs} runs of {num_hands} hands each, increasing the bet by a factor of {count_factor} when the true count was higher than 1. Of these runs, {bankrupting_runs} went bankrupt, {losing_runs} lost money, and {profitable_runs} were profitable.\nOn these runs, the average profit was {pnl_cardcount.iloc[-1].mean()/(num_hands*args.bet_per_hand)*100} percent of each hand; the maximal profit was {pnl_cardcount.iloc[-1].max()/(num_hands*args.bet_per_hand)*100} percent"
        print(message)