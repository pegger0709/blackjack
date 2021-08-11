import pandas as pd

"""
The basic strategy is a strategy prescribing an exact action for every possible scenario in blackjack. It is widely considered the best strategy not requiring the player to 'count cards', i.e. keep track of cards which have come out of the pack.
"""

BASIC_STRATEGY = pd.DataFrame(
    index = ['hard %d'%n for n in range(5,21+1)] + ['soft %d'%n for n in range(13,21+1)] + ['pair of %d'%n for n in range(2,9+1)] + ['pair of T','pair of A'],
    columns = ['2','3','4','5','6','7','8','9','T','A'],
    data=[
    ['h','h','h','h','h','h','h','h','h','h'],#hard 5
    ['h','h','h','h','h','h','h','h','h','h'],#hard 6
    ['h','h','h','h','h','h','h','h','h','h'],#hard 7
    ['h','h','h','h','h','h','h','h','h','h'],#hard 8
    ['h','d','d','d','d','h','h','h','h','h'],#hard 9
    ['d','d','d','d','d','d','d','d','h','h'],#hard 10
    ['d','d','d','d','d','d','d','d','d','h'],#hard 11
    ['h','h','s','s','s','h','h','h','h','h'],#hard 12
    ['s','s','s','s','s','h','h','h','h','h'],#hard 13
    ['s','s','s','s','s','h','h','h','h','h'],#hard 14
    ['s','s','s','s','s','h','h','h','h','h'],#hard 15
    ['s','s','s','s','s','h','h','h','h','h'],#hard 16
    ['s','s','s','s','s','s','s','s','s','s'],#hard 17
    ['s','s','s','s','s','s','s','s','s','s'],#hard 18
    ['s','s','s','s','s','s','s','s','s','s'],#hard 19
    ['s','s','s','s','s','s','s','s','s','s'],#hard 20
    ['s','s','s','s','s','s','s','s','s','s'],#hard 21
    ['h','h','h','d','d','h','h','h','h','h'],#soft 13
    ['h','h','h','d','d','h','h','h','h','h'],#soft 14
    ['h','h','d','d','d','h','h','h','h','h'],#soft 15
    ['h','h','d','d','d','h','h','h','h','h'],#soft 16
    ['h','d','d','d','d','h','h','h','h','h'],#soft 17
    ['s','d','d','d','d','s','s','h','h','h'],#soft 18
    ['s','s','s','s','s','s','s','s','s','s'],#soft 19
    ['s','s','s','s','s','s','s','s','s','s'],#soft 20
    ['s','s','s','s','s','s','s','s','s','s'],#soft 21
    ['p','p','p','p','p','p','h','h','h','h'],#pair of 2
    ['p','p','p','p','p','p','h','h','h','h'],#pair of 3
    ['h','h','h','p','p','h','h','h','h','h'],#pair of 4
    ['d','d','d','d','d','d','d','d','h','h'],#pair of 5
    ['p','p','p','p','p','h','h','h','h','h'],#pair of 6
    ['p','p','p','p','p','p','h','h','h','h'],#pair of 7
    ['p','p','p','p','p','p','p','p','h','h'],#pair of 8
    ['p','p','p','p','p','s','p','p','s','s'],#pair of 9
    ['s','s','s','s','s','s','s','s','s','s'],#pair of T
    ['p','p','p','p','p','p','p','p','p','p'],#pair of A
    ]
)

