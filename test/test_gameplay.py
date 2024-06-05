import os
import sys

# Assuming that the code is in test's __init__.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))

from hand import *

def test_always_passes():
    assert True

def test_deal_cards():
    shoe = Shoe(n_decks=8)
    assert (shoe.cards["A"] == 8*4) and (shoe.cards["T"] == 8*16)
    assert (sum(shoe.cards.values()) == 8*52) and (shoe.numberOfCards() == 8*52)
    card = shoe.dealCard("A")
    assert (sum(shoe.cards.values()) == 8*52-1) and (shoe.numberOfCards() == 8*52-1)
    assert (shoe.cards["A"] == 8*4-1) and (shoe.cards["T"] == 8*16)
    shoe.dealHand()
    assert (sum(shoe.cards.values()) == 8*52-3) and (shoe.numberOfCards() == 8*52-3)

def test_deal_pair_of_aces():
    shoe = Shoe()
    hand = shoe.dealHand(["A", "A"])
    assert hand.isSoftHand()
    assert hand.isPair()
    assert hand.is_original_hand
    assert not hand.cards[0].isSoftAce()
    assert hand.cards[1].isSoftAce()
    assert hand.value == 12
    hand.addCard(shoe.dealCard("T"))
    assert not hand.cards[0].isSoftAce()
    assert not hand.cards[1].isSoftAce()
    assert hand.value == 12
    assert not hand.isSoftHand()
    assert not hand.isPair()