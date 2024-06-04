# Blackjack
To clone this repo, open a terminal and run

```
git clone https://github.com/pegger0709/blackjack.git
```

## What this repo contains
If you want to play the game of blackjack as if you were in a casino, run

```
python .\play.py \
--bankroll <initial_bankroll_of_player> \
--decks <number_of_decks_in_shoe> \
--shuffle <number_of_cards_to_leave_in_shoe>
```

If you want to run a Monte Carlo simulation of blackjack, run

```
python .\simulate.py \
--bankroll <initial_bankroll_of_player> \
--decks <number_of_decks_in_shoe> \
--shuffle <number_of_cards_to_leave_in_shoe> \
--bet <amount_to_bet_on_each_hand> \
--runs <number_of_Monte_Carlo_runs_to_perform> \
--hands <maximum_number_of_hands_to_play_per_Monte_Carlo run> 
```
If you want to increase bets when the count is favorable, include the flag `--count` at the end.

If you want to compare the basic strategy runs with the card counting runs, run
```
python .\measure_profitability.py \
--bankroll <initial_bankroll_of_player> \
--bet <amount_to_bet_on_each_hand>
```
and enter whatever was the initial bankroll when prompted.

## A refresher course on the game
If you are here, chances are you know how to play the casino card game of blackjack. Nonetheless, it's worth taking some time for a refresher course on the basic rules and gameplay. You can find more resources online. Keep in mind there are minor variations and you should check the particulars of a casino near you; **I cannot bear responsibility for any gambling losses on your part**.

Cards 2 thru 10 have a corresponding point value. Face cards (Jack, Queen, King) are worth 10 points, and thus we don't distinguish between 10, J, Q and K, simply labeling them all as T for ten. Ace can be worth 1 or 11; an Ace worth 11 is called "soft" because it has the flexibility to be reduced in value to 1, while an Ace worth 1 is called "hard" as it has lost that flexibility.

The game pits player against dealer, with the winner being the party to get more points, without exceeding 21 (referred to as "going bust"). Importantly, the player goes first and if the player busts, then the dealer wins by default; this is the source of the house's edge. The best outcome for the player is to receive blackjack, a hand consisting of a ten and an ace; if the player gets blackjack and the dealer doesn't, the player wins a 3 to 2 payout on the bet.

The cards will be dealt from a shoe containing a few (usually 6 or 8) standard decks all shuffled together. The dealer will keep dealing until the number of cards left in the shoe reaches a certain minimum, at which point all the cards will be shuffled and re-entered into the shoe.

The game begins with the player choosing an amount to bet on a particular round, then receiving two cards, while the dealer receives one card (the "up card") which the player sees. The player must then decide to hit (take another card), stand (take no more cards), or double down (double the bet, take one more card, then forfeit the right to take another card). If the player receives a pair, there is a further option to split the pair (turn each card in the pair into the first card of a new hand with the same bet, then play each hand separately).

After the player has finished playing, with all derivative hands either having a point value or having gone bust, the dealer completes the up card into a hand, then continuing to take cards until either reaching 17 points (dealer may or may not hit soft 17) or going bust. The rules allow no flexibility on the part of the dealer.

If the dealer busts, all the player's non-busted bets are paid out. If the dealer does not bust, then the payout goes to whichever of dealer or player has more points (ties result in no win or loss).

### Basic strategy
One way to minimize the casino's edge in blackjack is by using the basic strategy, a predetermined set of actions to take in any of the possible situations encountered in play. Players using the basic strategy can reduce the house edge to less than 1%, and the strategy is easy to memorize, or to print on a business card to read off during play.

### Card counting
While the basic strategy can minimize the casino edge for an unskilled player, other strategies usable by skilled players can eliminate it altogether, and even give the player an edge.

It is easy to see that when a shoe has an abundance of small cards, this favors the dealer: it is easier to keep dealing to 17 without busting. Conversely, an abundance of tens and aces favors the player, as doubling down is more likely to pay off, and the likelihood of hitting blackjack increases. Blackjack is unlike most casino games in that the number of large and small cards fluctuates as play progresses; a card that has been dealt cannot be dealt again until the shoe is shuffled.

"Card counting" is simply the practice of keeping a running tally of large and small cards as they come out of the shoe: if an abundance of small cards has come out, that leaves an abundance of large cards still in, which, as we have seen, favors the player. The speed of gameplay makes this difficult, but achievable with enough practice. While all casinos frown upon it, in some jurisdictions (including the gambling-heavy US states of Nevada and New Jersey, outside of sovereign Indian reservations), it is not considered cheating. You should check the laws of a casino near you; **I cannot bear responsibility for any legal consequences on your part**.

As the mathematician Edward O. Thorp has found, the casino's edge can be reversed by players who skillfully use card counting, for instance increasing the bet when the count favors the player, a technique used by groups like the MIT Blackjack Team.