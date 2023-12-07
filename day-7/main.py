import os
import functools
from collections import Counter

@functools.total_ordering
class Card:

    @staticmethod
    def parse(char: str, part_2: bool):
        if char.isdigit():
            return Card(int(char))
        elif char == 'T':
            return Card(10)
        elif char == 'J':
            return Card(1) if part_2 else Card(11)
        elif char == 'Q':
            return Card(12)
        elif char == 'K':
            return Card(13)
        elif char == 'A':
            return Card(14)
        
        raise Exception()

    def __init__(self, number: int) -> None:
        self.number = number 
    
    def __eq__(self, other) -> bool:
        return self.number == other.number
    
    def __lt__(self, other) -> bool:
        return self.number < other.number
    
    def __hash__(self) -> int:
        return self.number
    
    def __repr__(self) -> str:
        return str(self.number)

@functools.total_ordering
class Hand:

    def __init__(self, cards: list[Card], bid: int, part_2: bool) -> None:
        self.cards = cards
        self.bid = bid
        self.part_2 = part_2

    def __eq__(self, other) -> bool:
        for a, b in zip(self.cards, other.cards):
            if a != b:
                return False
        
        return True
    
    def __lt__(self, other) -> bool:
        if self.part_2:
            rank_a = self.calculate_rank_joker()
            rank_b = other.calculate_rank_joker()
        else:
            rank_a = self.calculate_rank()
            rank_b = other.calculate_rank()

        if rank_a != rank_b:
            return rank_a < rank_b
        
        for a, b in zip(self.cards, other.cards):
            if a != b:
                return a < b
        
        return False
    
    def __repr__(self) -> str:
        return f"Hand [ Cards: {self.cards}, Bid: {self.bid} ]"
    
    @staticmethod
    def parse(line: str, part_2: bool):
        cards, bid = line.split()

        res = []
        for char in cards:
            res.append(Card.parse(char, part_2))
        
        return Hand(res, int(bid), part_2)
    
    def calculate_rank(self):
        counts = Counter(self.cards)
        mc = counts.most_common()

        if mc[0][1] == 5:
            return 6
        
        if mc[0][1] == 4:
            return 5
        
        if mc[0][1] == 3 and mc[1][1] == 2:
            return 4
        
        if mc[0][1] == 3:
            return 3
        
        if mc[0][1] == 2 and mc[1][1] == 2:
            return 2
        
        if mc[0][1] == 2:
            return 1
        
        return 0
    
    def calculate_rank_joker(self):
        counts = Counter(self.cards)
        mc = counts.most_common()
        jc = counts[Card(1)]

        if mc[0][1] == 5:
            return 6
        
        if mc[0][1] == 4:
            if jc == 0:
                return 5
            else:
                return 6
        
        if mc[0][1] == 3 and mc[1][1] == 2:
            if jc == 0:
                return 4
            else:
                return 6
        
        if mc[0][1] == 3:
            if jc == 0:
                return 3
            else:
                return 5
        
        if mc[0][1] == 2 and mc[1][1] == 2:
            if jc == 0:
                return 2
            elif jc == 1:
                return 4
            else:
                return 5

        
        if mc[0][1] == 2:
            if jc == 0:
                return 1
            else:
                return 3
        
        if jc > 0:
            return 1

        return 0


input_text = []

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(f"{dir_path}/input.txt", "r") as f:
    input_text = f.readlines()


# First part
first_hands = []
for line in input_text:
    first_hands.append(Hand.parse(line, False))



first_sum = 0
first_hands.sort()
for index, hand in enumerate(first_hands):
    first_sum += (index + 1) * hand.bid

print(f"Answer first part: {first_sum}")

# Second part
second_hands = []
for line in input_text:
    second_hands.append(Hand.parse(line, True))

second_sum = 0
second_hands.sort()
for index, hand in enumerate(second_hands):
    second_sum += (index + 1) * hand.bid

print(f"Answer second part: {second_sum}")
