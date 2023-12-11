import os
import itertools

def create_map(grid: list[str], increase: int):
    result: dict()

    col_indices = []
    row_indices = []

    current = 0
    for col_index in range(0, len(grid[0])):
        found_galaxy = False
        for row_index in range(0, len(grid)):
            if grid[row_index][col_index] == "#":
                found_galaxy = True
        
        col_indices.append(current)
        if found_galaxy:
            current += 1
        else:
            current += increase
    
    current = 0
    for row in grid:
        row_indices.append(current)
        if "#" in row:
            current += 1
        else:
            current += increase
    
    result = dict()

    current_id = 0
    for row_index, row in enumerate(grid):
        for col_index, item in enumerate(row):
            if item == "#":
                result[current_id] = (row_indices[row_index], col_indices[col_index])
                current_id += 1
    
    return result



def manhattan_dist(g1: tuple[int, int], g2: tuple[int, int]):
    return abs(g2[0] - g1[0]) + abs(g2[1] - g1[1])

input_text = []

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(f"{dir_path}/input.txt", "r") as f:
    input_text = f.readlines()

input_text = list(map(lambda x: x.replace("\n", ""), input_text))


# First part
m1 = create_map(input_text, 2)

first_sum = 0
for a, b in itertools.combinations(m1.keys(), 2):
    first_sum += manhattan_dist(m1[a], m1[b])

print(f"Answer first part: {first_sum}")

# Second part
m2 = create_map(input_text, 1_000_000)

second_sum = 0
for a, b in itertools.combinations(m2.keys(), 2):
    second_sum += manhattan_dist(m2[a], m2[b])

print(f"Answer first part: {second_sum}")
