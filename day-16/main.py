from dataclasses import dataclass
import os


@dataclass(eq=True, frozen=True)
class State:
    row: int
    col: int
    direction: tuple[int, int]


def filter_state(state: State, grid: list[str], visited_pos: set[State]):
    if state in visited_pos:
        return False
    
    if state.row < 0 or state.col < 0:
        return False
    
    if state.row >= len(grid):
        return False
    
    if state.col >= len(grid[state.row]):
        return False
    
    return True

def step_beam(pos: State, grid: list[str], visited_pos: set[State]) -> list[State]:
    current_char = grid[pos.row][pos.col]
    result = []

    if current_char == ".":
        result.append(State(pos.row + pos.direction[0], pos.col + pos.direction[1], pos.direction))
    elif current_char == "/":
        new_direction = (pos.direction[1] * -1, pos.direction[0] * -1)
        result.append(State(pos.row + new_direction[0], pos.col + new_direction[1], new_direction))
    elif current_char == "\\":
        new_direction = (pos.direction[1], pos.direction[0])
        result.append(State(pos.row + new_direction[0], pos.col + new_direction[1], new_direction))
    elif current_char == "-":
        if pos.direction[0] == 0:
            result.append(State(pos.row + pos.direction[0], pos.col + pos.direction[1], pos.direction))
        else:
            result.append(State(pos.row, pos.col - 1, (0, -1)))
            result.append(State(pos.row, pos.col + 1, (0,  1)))
    elif current_char == "|":
        if pos.direction[1] == 0:
            result.append(State(pos.row + pos.direction[0], pos.col + pos.direction[1], pos.direction))
        else:
            result.append(State(pos.row - 1, pos.col, (-1, 0)))
            result.append(State(pos.row + 1, pos.col, ( 1, 0)))
    
    result = list(filter(lambda x: filter_state(x, grid, visited_pos), result))

    for res in result:
        visited_pos.add(res)
    
    return result

def step_list(states: list[State], grid: list[str], visited_pos = set[State]) -> list[State]:
    result = []

    for state in states:
        result += step_beam(state, grid, visited_pos)
    
    return result

def calc_number_of_energized_tiles(start: State, grid: list[str]):
    current_list = [start]
    visited: set[State] = { start }

    while len(current_list) > 0:
        current_list = step_list(current_list, grid, visited)

    return len(set(map(lambda x: (x.row, x.col), visited)))

def find_max(grid: list[str]):
    current_max = 0

    for i in range(0, len(grid)):
        current_max = max(current_max, calc_number_of_energized_tiles(State(i, 0, (0, 1)), grid))
        current_max = max(current_max, calc_number_of_energized_tiles(State(i, len(grid[i]) - 1, (0, -1)), grid))
    
    for i in range(0, len(grid[0])):
        current_max = max(current_max, calc_number_of_energized_tiles(State(0, i, (1, 0)), grid))
        current_max = max(current_max, calc_number_of_energized_tiles(State(len(grid) - 1, i, (-1, 0)), grid))
    
    return current_max


input_text = []

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(f"{dir_path}/input.txt", "r") as f:
    input_text = f.readlines()

input_text = list(map(lambda x: x.replace("\n", ""), input_text))

print(f"Answer first part: {calc_number_of_energized_tiles(State(0, 0, (0, 1)), input_text)}")
print(f"Answer second part: {find_max(input_text)}")
