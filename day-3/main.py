import re
import os 

dir_path = os.path.dirname(os.path.realpath(__file__))

input_text = []

with open(f"{dir_path}/input.txt", "r") as f:
    input_text = f.readlines()

symbol_grid = [[False for _ in input_text[0]] for _ in input_text]

def is_match_adjacent(row: int, start: int, end: int):
    for row_index in range(max(0, row - 1), min(len(symbol_grid), row + 2)):
        for col_index in range(max(0, start - 1), min(len(symbol_grid[0]), end + 1)):
            if symbol_grid[row_index][col_index]:
                return True
    
    return False

def find_adjacent_numbers(row: int, col: int):
    col_range = range(max(0, col - 1), min(len(symbol_grid), col + 2))
    numbers = []

    for row_index in range(max(0, row - 1), min(len(symbol_grid), row + 2)):
        for match in re.finditer(r"\d+", input_text[row_index]):
            if match.start() in col_range or match.end() - 1 in col_range:
                numbers.append(int(input_text[row_index][match.start():match.end()]))
    
    return numbers

for row, line in enumerate(input_text):
    for column, character in enumerate(line):
        if character != "." and not character.isdigit() and not character.isspace():
            symbol_grid[row][column] = True
        

first_sum = 0
for row, line in enumerate(input_text):
    for match in re.finditer(r"\d+", line):
        if is_match_adjacent(row, match.start(), match.end()):
            adj_number = int(line[match.start():match.end()])
            first_sum += adj_number


print(f"Answer first part: {first_sum}")

second_sum = 0
for row, line in enumerate(input_text):
    for column, character in enumerate(line):
        if character == '*':
            numbers = find_adjacent_numbers(row, column)

            if len(numbers) == 2:
                second_sum += numbers[0] * numbers[1]

print(f"Answer second part: {second_sum}")