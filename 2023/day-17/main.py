import os
import math
from typing import NamedTuple
from enum import IntEnum
from queue import PriorityQueue


class Direction(IntEnum):
    up = 1
    right = 2
    down = 3
    left = 4


class Node(NamedTuple):
    row: int
    col: int
    direction: Direction
    same_direction_count: int


def filter_node(node: Node, grid: list[str]) -> bool:
    if not node.row in range(0, len(grid)):
        return False

    if not node.col in range(0, len(grid[0])):
        return False

    if node.same_direction_count > 3:
        return False

    return True


def filter_node_p2(node: Node, pred: Node, grid: list[str]) -> bool:
    if not node.row in range(0, len(grid)):
        return False

    if not node.col in range(0, len(grid[0])):
        return False

    if node.direction != pred.direction:
        if pred.same_direction_count < 4:
            return False

    if node.same_direction_count > 10:
        return False

    return True


def find_neighbors(node: Node, grid: list[str], part2: bool) -> list[Node]:
    result = []

    if node.direction == Direction.left:
        result.append(Node(node.row, node.col - 1, node.direction,
                      node.same_direction_count + 1))
        result.append(Node(node.row - 1, node.col, Direction.up, 1))
        result.append(Node(node.row + 1, node.col, Direction.down, 1))
    elif node.direction == Direction.right:
        result.append(Node(node.row, node.col + 1, node.direction,
                      node.same_direction_count + 1))
        result.append(Node(node.row - 1, node.col, Direction.up, 1))
        result.append(Node(node.row + 1, node.col, Direction.down, 1))
    elif node.direction == Direction.up:
        result.append(Node(node.row - 1, node.col, node.direction,
                      node.same_direction_count + 1))
        result.append(Node(node.row, node.col - 1, Direction.left, 1))
        result.append(Node(node.row, node.col + 1, Direction.right, 1))
    elif node.direction == Direction.down:
        result.append(Node(node.row + 1, node.col, node.direction,
                      node.same_direction_count + 1))
        result.append(Node(node.row, node.col - 1, Direction.left, 1))
        result.append(Node(node.row, node.col + 1, Direction.right, 1))

    if part2:
        return [x for x in result if filter_node_p2(x, node, grid)]

    return [x for x in result if filter_node(x, grid)]


def dijkstra(grid: list[str], part2: bool) -> int:
    heat_loss: dict[Node, int] = {}
    pred: dict[Node, Node] = {}
    queue = PriorityQueue()

    heat_loss[Node(0, 0, Direction.right, 0)] = 0
    heat_loss[Node(0, 0, Direction.down, 0)] = 0
    pred[Node(0, 0, Direction.right, 0)] = None
    pred[Node(0, 0, Direction.down, 0)] = None
    queue.put((0, Node(0, 0, Direction.right, 0)))
    queue.put((0, Node(0, 0, Direction.down, 0)))

    visited: set[Node] = set()

    while not queue.empty():
        while not queue.empty():
            _, u = queue.get()

            if u not in visited:
                break
        else:
            break

        visited.add(u)

        for n in find_neighbors(u, grid, part2):
            if n in visited:
                continue

            current_cost = heat_loss.get(n, math.inf)
            alternative = heat_loss[u] + int(grid[n.row][n.col])
            if alternative < current_cost:
                queue.put((alternative, n))
                heat_loss[n] = alternative
                pred[n] = u

    row = len(grid) - 1
    col = len(grid[row]) - 1

    if part2:
        return min(heat_loss.get(Node(row, col, direction, count), math.inf) for direction in Direction for count in range(4, 11))

    return min(heat_loss.get(Node(row, col, direction, count), math.inf) for direction in Direction for count in range(1, 4))


input_text = []

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(f"{dir_path}/input.txt", "r") as f:
    input_text = f.readlines()

input_text = list(map(lambda x: x.replace("\n", ""), input_text))

print(f"Answer first part: {dijkstra(input_text, False)}")
print(f"Answer second part: {dijkstra(input_text, True)}")
