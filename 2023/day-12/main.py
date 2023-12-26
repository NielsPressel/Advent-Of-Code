import os
import functools

class Row:

    @staticmethod
    def parse(line: str):
        first, second = line.split()
        numbers = list(map(int, second.split(",")))

        return Row(first, numbers)

    def __init__(self, pattern: str, limitations: list[int]) -> None:
        self.pattern = pattern
        self.limitations = limitations
    
    @functools.cache
    @staticmethod
    def count_options(rem_pattern: str, rem_length: int, rem_splits: tuple):
        if len(rem_splits) == 0:
            if all(c == "." or c == "?" for c in rem_pattern):
                return 1
            return 0
        
        first = rem_splits[0]
        rest = rem_splits[1:]
        back = sum(rest) + len(rest)

        count = 0
        for front in range(rem_length - back - first + 1):
            candidate = '.' * front + '#' * first + '.'

            if all(c0 == c1 or c0 == "?" for c0, c1 in zip(rem_pattern, candidate)):
                rest_pattern = rem_pattern[len(candidate):]
                count += Row.count_options(rest_pattern, rem_length - front - first - 1, rest)
        
        return count
    
    def part1(self):
        return Row.count_options(self.pattern, len(self.pattern), tuple(self.limitations))

    def part2(self):
        return Row.count_options("?".join([self.pattern for _ in range(0, 5)]), len(self.pattern) * 5 + 4, tuple(self.limitations * 5))


input_text = []

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(f"{dir_path}/input.txt", "r") as f:
    input_text = f.readlines()

input_text = list(map(lambda x: x.replace("\n", ""), input_text))

first_sum = 0
second_sum = 0
for line in input_text:
    r = Row.parse(line)
    first_sum += r.part1()
    second_sum += r.part2()

print(f"Answer first part: {first_sum}")
print(f"Answer second part: {second_sum}")