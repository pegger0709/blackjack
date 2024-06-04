import numpy as np
import pandas as pd

initial_bankroll = float(input("What was the initial bankroll? "))
df_basicstrategy = pd.read_csv("MC_runs.csv").fillna(0)
total_number_of_runs = df_basicstrategy.shape[1]
bankrupting_runs = (df_basicstrategy.iloc[-1] == 0).sum()
profitable_runs = (df_basicstrategy.iloc[-1] >= initial_bankroll).sum()
losing_runs = (np.logical_and(df_basicstrategy.iloc[-1] < initial_bankroll, df_basicstrategy.iloc[-1] > 0)).sum()
message = f"We ran {total_number_of_runs} runs using the basic strategy. Of these, {bankrupting_runs} went bankrupt, {losing_runs} lost money, and {profitable_runs} were profitable.\nThe runs made an average profit of {df_basicstrategy.iloc[-1].mean()-initial_bankroll} and a maximal profit of {df_basicstrategy.iloc[-1].max()-initial_bankroll}"
print(message)
df_cardcount = pd.read_csv("MC_runs_counting_cards.csv").fillna(0)
total_number_of_runs = df_cardcount.shape[1]
bankrupting_runs = (df_cardcount.iloc[-1] == 0).sum()
profitable_runs = (df_cardcount.iloc[-1] >= initial_bankroll).sum()
losing_runs = (np.logical_and(df_cardcount.iloc[-1] < initial_bankroll, df_cardcount.iloc[-1] > 0)).sum()
message = f"We ran {total_number_of_runs} runs using the basic strategy. Of these, {bankrupting_runs} went bankrupt, {losing_runs} lost money, and {profitable_runs} were profitable.\nThe runs made an average profit of {df_cardcount.iloc[-1].mean()-initial_bankroll} and a maximal profit of {df_cardcount.iloc[-1].max()-initial_bankroll}"
print(message)