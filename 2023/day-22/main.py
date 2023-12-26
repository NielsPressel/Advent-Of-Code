import os
import re
from typing import NamedTuple
from queue import PriorityQueue
from functools import cache


class Position(NamedTuple):
    x: int
    y: int
    z: int


class Position2D(NamedTuple):
    x: int
    y: int


class Brick(NamedTuple):
    start: Position
    end: Position


def parse(input_text: list[str]) -> list[Brick]:
    regex = r"(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)"
    pattern = re.compile(regex)

    result = []
    for line in input_text:
        match = pattern.match(line)
        result.append(Brick(Position(int(match.group(1)), int(match.group(2)), int(match.group(
            3))), Position(int(match.group(4)), int(match.group(5)), int(match.group(6)))))

    return result


def overlap(a: Brick, b: Brick) -> bool:
    for x in range(a.start.x, a.end.x + 1):
        if x in range(b.start.x, b.end.x + 1) and a.start.y in range(b.start.y, b.end.y + 1):
            return True

    for y in range(a.start.y, a.end.y + 1):
        if y in range(b.start.y, b.end.y + 1) and a.start.x in range(b.start.x, b.end.x + 1):
            return True

    return False


def settle(bs: list[Brick]) -> dict[int, Brick]:
    q: PriorityQueue[tuple[int, Brick]] = PriorityQueue()

    for b in bs:
        q.put((b.start.z, b))

    result: list[Brick] = []
    while not q.empty():
        _, item = q.get()

        min_diff = -1
        for b in result:
            if overlap(item, b):
                diff = item.start.z - b.end.z - 1

                if diff >= 0 and (min_diff == -1 or diff < min_diff):
                    min_diff = diff

        if min_diff != -1:
            new_start = Position(item.start.x, item.start.y,
                                 item.start.z - min_diff)
            new_end = Position(item.end.x, item.end.y, item.end.z - min_diff)
        else:
            diff = item.start.z - 1
            new_start = Position(item.start.x, item.start.y, 1)
            new_end = Position(item.end.x, item.end.y, item.end.z - diff)

        result.append(Brick(new_start, new_end))

    start: dict[int, list[Brick]] = dict()
    for r in result:
        if r.start.z not in start:
            start[r.start.z] = []
        start[r.start.z].append(r)

    end: dict[int, list[Brick]] = dict()
    for r in result:
        if r.end.z not in end:
            end[r.end.z] = []
        end[r.end.z].append(r)

    return result, start, end


def calculate_removal_count(l: list[Brick], start: dict[int, list[Brick]], end: dict[int, list[Brick]]):
    count = 0

    for b in l:
        supporting: list[Brick] = []
        for item in start.get(b.end.z + 1, []):
            if overlap(b, item):
                supporting.append(item)

        for s in supporting:
            for item in end.get(s.start.z - 1, []):
                if item != b and overlap(item, s):
                    break
            else:
                # No other supporting item found
                break
        else:
            # Found other supporting item for each
            count += 1

    return count


def calculate_fall_count(l: list[Brick], start: dict[int, list[Brick]], end: dict[int, list[Brick]]):
    @cache
    def disintegrate_layer(bricks: tuple[Brick]):
        falling: set[Brick] = set(bricks)
        res = 0

        supporting: set[Brick] = set()
        for b in bricks:
            for item in start.get(b.end.z + 1, []):
                if overlap(b, item) and item not in falling:
                    supporting.add(item)

        for s in supporting:
            for item in end.get(s.start.z - 1, []):
                if item not in falling and overlap(item, s):
                    break
            else:
                res += 1
                falling.add(s)

        if len(bricks) == len(falling):
            return res

        return res + disintegrate_layer(tuple(falling))

    result = 0
    for brick in l:
        result += disintegrate_layer((brick, ))

    return result


input_text = []

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(f"{dir_path}/input.txt", "r") as f:
    input_text = f.readlines()

input_text = list(map(lambda x: x.replace("\n", ""), input_text))
bricks = parse(input_text)
l, s, e = settle(bricks)

print(f"Answer first part: {calculate_removal_count(l, s, e)}")
print(f"Answer second part: {calculate_fall_count(l, s, e)}")
