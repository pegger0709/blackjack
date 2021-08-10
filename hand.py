import random

class Card:
    def __init__(self, face_value=None):
        if face_value is None:
            self.face_value = random.choice(['A','2','3','4','5','6','7','8','9','T','T','T','T'])
        else:
            self.face_value = face_value
        if self.face_value in ['2','3','4','5','6','7','8','9']:
            self.numeric_value = int(self.face_value)
        elif self.face_value == 'T':
            self.numeric_value = 10
        elif self.face_value =='A':
            self.numeric_value = 11
        else:
            pass
            
    def isSoftAce(self):
        if self.face_value == 'A' and self.numeric_value == 11:
            return True
        else:
            return False

    def hardenAce(self):
        if self.isSoftAce():
            self.numeric_value = 1
        else:
            pass

class Hand:
    def __init__(self, cards=None):
        if cards is None:
            self.cards = [Card(), Card()]
        else:
            self.cards = cards
        if self.cards[0].face_value=='A' and self.isPair():
            self.cards[0].hardenAce()
        self.value = sum([card.numeric_value for card in self.cards])
        self.soft = self.isSoftHand()

    def isBlackjack(self):
        if len(self.cards) != 2:
            return False
        elif (self.cards[0].face_value == 'A' and self.cards[1].face_value == 'T'):
            return True
        elif (self.cards[0].face_value == 'T' and self.cards[1].face_value == 'A'):
            return True
        else:
            return False

    def isPair(self):
        if len(self.cards) != 2:
            return False
        else:
            return self.cards[0].face_value == self.cards[1].face_value
            
    def containsSoftAce(self):
        for card in self.cards:
            if card.isSoftAce():
                return True
                break
        else:
            return False
            
    def firstSoftAce(self):
        for card in self.cards:
            if card.isSoftAce():
                return card
                break
        else:
            return None
            
    def isSoftHand(self):
        for card in self.cards:
            if card.isSoftAce():
                return True
                break
        else:
            return False
            
    def isBust(self):
        return ~self.isSoftHand() and self.value > 21

    def addCard(self, card=None):
        if card is None:
            card = Card()
        self.cards.append(card)
        self.value += card.numeric_value
        if self.value > 21 and self.containsSoftAce():
            self.value -= 10
            self.firstSoftAce().hardenAce()
            self.soft = self.isSoftHand()
            
    def handToString(self):
        if self.isBust():
            return 'bust'
        elif self.isBlackjack():
            return 'blackjack'
        elif self.isPair():
            return 'pair of ' + self.cards[0].face_value
        elif self.isSoftHand():
            return 'soft ' + str(self.value)
        else:
            return 'hard ' + str(self.value)

    def __repr__(self):
        if self.isPair():
            repr = 'Pair of ' + self.cards[0].face_value + '\n'
        else:
            repr = 'Hand: ' + ' / '.join([card.face_value for card in self.cards]) + '\n'
        repr += 'Value: %s'%self.handToString()
        return repr
