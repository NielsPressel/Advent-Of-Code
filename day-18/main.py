import os
import re
import sys
from dataclasses import dataclass
from enum import IntEnum
from typing import NamedTuple


class Direction(IntEnum):
    up = 1
    right = 2
    down = 3
    left = 4


@dataclass(eq=True, frozen=True)
class Command:
    direction: Direction
    steps: int


class Position(NamedTuple):
    row: int
    col: int


def parse_direction_p1(direction: str):
    if direction == "R":
        return Direction.right

    if direction == "L":
        return Direction.left

    if direction == "U":
        return Direction.up

    if direction == "D":
        return Direction.down

    raise Exception("Invalid direction character")


def parse_direction_p2(direction: str):
    if direction == "0":
        return Direction.right

    if direction == "1":
        return Direction.down

    if direction == "2":
        return Direction.left

    if direction == "3":
        return Direction.up

    raise Exception("Invalid direction character")


def parse_p1(input_text: list[str]) -> list[Command]:
    regex = r"([A-Z]) (\d+) \((#[a-f0-9]+)\)"
    p = re.compile(regex)

    result = []
    for line in input_text:
        m = p.match(line)
        result.append(Command(parse_direction_p1(m.group(1)), int(m.group(2))))

    return result


def parse_p2(input_text: list[str]):
    regex = r"[A-Z] \d+ \(#([a-f0-9]+)\)"
    p = re.compile(regex)

    result = []
    for line in input_text:
        m = p.match(line)
        result.append(Command(parse_direction_p2(
            m.group(1)[-1]), int(m.group(1)[:-1], base=16)))

    return result


def shoelace(commands: list[Command]):
    current_pos = Position(0, 0)

    area = 0
    for command in commands:
        if command.direction == Direction.left:
            next_pos = Position(
                current_pos.row, current_pos.col - command.steps)
        elif command.direction == Direction.right:
            next_pos = Position(
                current_pos.row, current_pos.col + command.steps)
        elif command.direction == Direction.up:
            next_pos = Position(
                current_pos.row - command.steps, current_pos.col)
        elif command.direction == Direction.down:
            next_pos = Position(
                current_pos.row + command.steps, current_pos.col)

        area -= current_pos.row * next_pos.col - current_pos.col * next_pos.row
        area += command.steps
        current_pos = next_pos

    return area // 2 + 1


input_text = []

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(f"{dir_path}/input.txt", "r") as f:
    input_text = f.readlines()

input_text = list(map(lambda x: x.replace("\n", ""), input_text))

commands_p1 = parse_p1(input_text)
commands_p2 = parse_p2(input_text)

print(f"Answer first part: {shoelace(commands_p1)}")
print(f"Answer second part: {shoelace(commands_p2)}")
