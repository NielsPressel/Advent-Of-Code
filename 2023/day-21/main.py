import os
import numpy as np
from typing import NamedTuple
from functools import cache


class Position(NamedTuple):
    row: int
    col: int


@cache
def find_neighbors(current: Position, grid: tuple[str]) -> list[Position]:
    neighbors = [Position(current.row, current.col + 1), Position(current.row, current.col - 1),
                 Position(current.row + 1, current.col), Position(current.row - 1, current.col)]

    return [n for n in neighbors if grid[n.row % len(grid)][n.col % len(grid[0])] != "#"]


def get_tiles_count(start: Position, steps: int, grid: tuple[str]) -> int:
    current_positions = {start}
    next_positions = set()

    for _ in range(steps):
        for item in current_positions:
            for n in find_neighbors(item, grid):
                next_positions.add(n)

        current_positions = next_positions
        next_positions = set()

    return len(current_positions)


def interpolate_tiles_count(start: Position, grid: tuple[str]) -> int:
    n = 202300
    a0 = get_tiles_count(start, 65, grid)
    a1 = get_tiles_count(start, 65 + 131, grid)
    a2 = get_tiles_count(start, 65 + 2 * 131, grid)

    vandermonde = np.matrix([[0, 0, 1], [1, 1, 1], [4, 2, 1]])
    b = np.array([a0, a1, a2])
    x = np.linalg.solve(vandermonde, b).astype(np.int64)

    return x[0] * n * n + x[1] * n + x[2]


input_text = []

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(f"{dir_path}/input.txt", "r") as f:
    input_text = f.readlines()

input_text = tuple(map(lambda x: x.replace("\n", ""), input_text))


s = Position(len(input_text) // 2, len(input_text[0]) // 2)
print(f"Answer first part: {get_tiles_count(s, 64, input_text)}")
print(f"Answer second part: {interpolate_tiles_count(s, input_text)}")
