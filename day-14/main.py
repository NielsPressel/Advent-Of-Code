import os
import functools

def tilt_north(pattern: list[list[str]]):
    for col_ind in range(len(pattern[0])):
        last_blocked = 0

        for row_ind in range(len(pattern)):
            if pattern[row_ind][col_ind] == "O":
                if last_blocked != row_ind:
                    pattern[last_blocked][col_ind] = "O"
                    pattern[row_ind][col_ind] = "."
                last_blocked += 1
            elif pattern[row_ind][col_ind] == "#":
                last_blocked = row_ind + 1
    
    return pattern

def tilt_south(pattern: list[list[str]]):
    for col_ind in range(len(pattern[0])):
        last_blocked = len(pattern) - 1

        for row_ind in range(len(pattern) - 1, -1, -1):
            if pattern[row_ind][col_ind] == "O":
                if last_blocked != row_ind:
                    pattern[last_blocked][col_ind] = "O"
                    pattern[row_ind][col_ind] = "."
                last_blocked -= 1
            elif pattern[row_ind][col_ind] == "#":
                last_blocked = row_ind - 1
    
    return pattern

def tilt_west(pattern: list[list[str]]):
    for row_ind in range(len(pattern)):
        last_blocked = 0

        for col_ind in range(len(pattern[row_ind])):
            if pattern[row_ind][col_ind] == "O":
                if last_blocked != col_ind:
                    pattern[row_ind][last_blocked] = "O"
                    pattern[row_ind][col_ind] = "."
                last_blocked += 1
            elif pattern[row_ind][col_ind] == "#":
                last_blocked = col_ind + 1
    
    return pattern
    

def tilt_east(pattern: list[list[str]]):
    for row_ind in range(len(pattern)):
        last_blocked = len(pattern[row_ind]) - 1

        for col_ind in range(len(pattern[row_ind]) - 1, -1, -1):
            if pattern[row_ind][col_ind] == "O":
                if last_blocked != col_ind:
                    pattern[row_ind][last_blocked] = "O"
                    pattern[row_ind][col_ind] = "."
                last_blocked -= 1
            elif pattern[row_ind][col_ind] == "#":
                last_blocked = col_ind - 1
    
    return pattern

@functools.cache
def cycle(pattern: tuple[tuple[str]]):
    pattern = list(map(lambda x: list(x), pattern))

    pattern = tilt_north(pattern)
    pattern = tilt_west(pattern)
    pattern = tilt_south(pattern)
    pattern = tilt_east(pattern)

    pattern = tuple(map(lambda x: tuple(x), pattern))

    return pattern

def calculate_load(pattern: list[list[str]]):
    length = len(pattern)
    
    result = 0
    for index, row in enumerate(pattern):
        result += row.count("O") * (length - index)
    
    return result


input_text = []

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(f"{dir_path}/input.txt", "r") as f:
    input_text = f.readlines()

# First part
pattern = tuple(map(lambda x: list(x.replace("\n", "")), input_text))
pattern = tilt_north(pattern)

print(f"Answer first part: {calculate_load(pattern)}")

# Second part
pattern = tuple(map(lambda x: tuple(x.replace("\n", "")), input_text))

d = dict()
for i in range(1_000_000_000):
    pattern = cycle(pattern)

    if pattern in d:
        repeat_length = i - d[pattern]
        remaining = 1_000_000_000 - i - 1
        remaining_after_cycle = remaining % repeat_length

        for j in range(remaining_after_cycle):
            pattern = cycle(pattern)

        break

    d[pattern] = i

print(f"Answer second part: {calculate_load(pattern)}")
