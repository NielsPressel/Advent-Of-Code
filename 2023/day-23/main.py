import os
from typing import NamedTuple
from queue import SimpleQueue
from dataclasses import dataclass
from copy import copy


class Position(NamedTuple):
    row: int
    col: int


@dataclass(frozen=True, order=True)
class State:
    steps: int
    pos: Position
    visited_tiles: set[Position]


@dataclass(frozen=True)
class StateP2:
    steps: int
    node: int
    visited: set[int]


def filter_n(pos: Position, grid: list[str]) -> bool:
    if pos.row not in range(len(grid)):
        return False

    if pos.col not in range(len(grid[pos.row])):
        return False

    if grid[pos.row][pos.col] == "#":
        return False

    return True


def get_neighbors(pos: Position, grid: list[str]) -> list[Position]:
    char = grid[pos.row][pos.col]

    if char == ".":
        neighbors = [Position(pos.row, pos.col - 1), Position(pos.row, pos.col + 1),
                     Position(pos.row - 1, pos.col), Position(pos.row + 1, pos.col)]

        return [n for n in neighbors if filter_n(n, grid)]

    if char == ">":
        n = Position(pos.row, pos.col + 1)

        if filter_n(n, grid):
            return [n]

        return []

    if char == "<":
        n = Position(pos.row, pos.col - 1)

        if filter_n(n, grid):
            return [n]

        return []

    if char == "v":
        n = Position(pos.row + 1, pos.col)

        if filter_n(n, grid):
            return [n]

        return []

    if char == "^":
        n = Position(pos.row - 1, pos.col)

        if filter_n(n, grid):
            return [n]

        return []

    raise Exception()


def get_neighbors_p2(pos: Position, grid: list[str]) -> list[Position]:
    neighbors = [Position(pos.row, pos.col - 1), Position(pos.row, pos.col + 1),
                 Position(pos.row - 1, pos.col), Position(pos.row + 1, pos.col)]

    return [n for n in neighbors if filter_n(n, grid)]


def calculate_longest_hike(start: Position, grid: list[str]):
    q: SimpleQueue[State] = SimpleQueue()
    q.put(State(0, start, set(start)))

    max_length = 0
    while not q.empty():
        item = q.get()

        if item.pos.row == len(grid) - 1:
            max_length = max(item.steps, max_length)

        for n in get_neighbors(item.pos, grid):
            if n not in item.visited_tiles:
                visited = copy(item.visited_tiles)
                visited.add(n)
                q.put(State(item.steps + 1, n, visited))

    return max_length


def create_pruned_graph(start: Position, grid: list[str]):
    junction_nodes = {
        Position(x, y)
        for x in range(len(grid))
        for y in range(len(grid[x]))
        if grid[x][y] != "#" and (len(get_neighbors_p2(Position(x, y), grid)) > 2 or x == 0 or x == len(grid) - 1)
    }

    nodes = {pos: i for i, pos in enumerate(junction_nodes)}
    adj_matrix = [[-1 for _ in nodes] for _ in nodes]

    visited = set()
    visited.add(start)

    q = SimpleQueue()
    q.put(start)

    def path_length(pos: Position, last: Position, grid: list[str]):
        visited.add(pos)

        if pos in nodes:
            return pos, 0

        for n in get_neighbors_p2(pos, grid):
            if n != last:
                p, l = path_length(n, pos, grid)
                return p, l + 1

    while not q.empty():
        item = q.get()

        for n in get_neighbors_p2(item, grid):
            if n not in visited:
                p, l = path_length(n, item, grid)
                adj_matrix[nodes[item]][nodes[p]] = l + 1
                adj_matrix[nodes[p]][nodes[item]] = l + 1
                q.put(p)

    return nodes, adj_matrix


def calculate_longest_path(start: int, end: int, adj_matrix: list[list[int]]):
    q: SimpleQueue[StateP2] = SimpleQueue()
    q.put(StateP2(0, start, {start}))

    max_length = 0
    while not q.empty():
        item = q.get()

        if item.node == end:
            max_length = max(item.steps, max_length)

        for node, length in enumerate(adj_matrix[item.node]):
            if node not in item.visited and length >= 0:
                visited = copy(item.visited)
                visited.add(node)
                q.put(StateP2(item.steps + length, node, visited))

    return max_length


input_text = []

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(f"{dir_path}/input.txt", "r") as f:
    input_text = f.readlines()

input_text = list(map(lambda x: x.replace("\n", ""), input_text))

print(f"Answer first part: {
      calculate_longest_hike(Position(0, 1), input_text)}")


nodes, adj_matrix = create_pruned_graph(Position(0, 1), input_text)
start = None
end = None
for pos, n in nodes.items():
    if pos.row == len(input_text) - 1:
        end = n
    if pos.row == 0:
        start = n

print(f"Answer second part: {calculate_longest_path(start, end, adj_matrix)}")
