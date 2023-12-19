import os
import re
from dataclasses import dataclass
from enum import Enum


class Attribute(Enum):
    x = "x"
    m = "m"
    a = "a"
    s = "s"

    @staticmethod
    def from_str(string: str):
        if string == "x":
            return Attribute.x

        if string == "m":
            return Attribute.m

        if string == "a":
            return Attribute.a

        if string == "s":
            return Attribute.s

        raise Exception()


class Operator(Enum):
    lt = "<"
    gt = ">"

    @staticmethod
    def from_str(string: str):
        if string == "<":
            return Operator.lt

        if string == ">":
            return Operator.gt

        raise Exception()


@dataclass
class Rule:
    attribute: Attribute
    operator: Operator
    value: int
    next_chain: str


@dataclass
class MachinePart:
    x: int
    m: int
    a: int
    s: int


@dataclass
class Range:
    lower: int
    upper: int


@dataclass
class PartRange:
    x: Range
    m: Range
    a: Range
    s: Range


def parse_rules(rules: str) -> list[Rule]:
    parts = rules.split(",")
    regex = r"([xmas])([<>])(\d+):(\w+)"
    pattern = re.compile(regex)

    result = []
    for part in parts:
        match = pattern.match(part)

        if match:
            attr = Attribute.from_str(match.group(1))
            operator = Operator.from_str(match.group(2))
            value = int(match.group(3))
            next_chain = match.group(4)

            result.append(Rule(attr, operator, value, next_chain))
        else:
            result.append(Rule(None, None, None, part))

    return result


def parse_chain(line: str):
    regex = r"([a-z]+){(.*)}"
    pattern = re.compile(regex)
    match = pattern.match(line)

    wf_name = match.group(1)
    wf_rules = match.group(2)

    return wf_name, parse_rules(wf_rules)


def parse_part(line: str) -> MachinePart:
    regex = r"{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}"
    pattern = re.compile(regex)
    match = pattern.match(line)

    return MachinePart(int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4)))


def compare(attr_value: int, rule: Rule):
    if rule.operator == Operator.lt:
        if attr_value < rule.value:
            return True

        return False

    if rule.operator == Operator.gt:
        if attr_value > rule.value:
            return True

    return False


def process_part(part: MachinePart, wf: str, wfs: dict[str, list[Rule]]):
    if wf == "A":
        return True

    if wf == "R":
        return False

    for rule in wfs[wf]:
        if not rule.attribute:
            return process_part(part, rule.next_chain, wfs)

        if rule.attribute == Attribute.a:
            if compare(part.a, rule):
                return process_part(part, rule.next_chain, wfs)
        elif rule.attribute == Attribute.m:
            if compare(part.m, rule):
                return process_part(part, rule.next_chain, wfs)
        elif rule.attribute == Attribute.s:
            if compare(part.s, rule):
                return process_part(part, rule.next_chain, wfs)
        elif rule.attribute == Attribute.x:
            if compare(part.x, rule):
                return process_part(part, rule.next_chain, wfs)

    raise Exception()


def check_range(part_range: PartRange) -> bool:
    if part_range.a.lower >= part_range.a.upper:
        return False

    if part_range.x.lower >= part_range.x.upper:
        return False

    if part_range.s.lower >= part_range.s.upper:
        return False

    if part_range.m.lower >= part_range.m.upper:
        return False

    return True


def build_range(old_range: Range, new_range: Range) -> Range:
    if old_range.lower != new_range.lower:
        return Range(old_range.lower, new_range.lower + 1)
    
    if old_range.upper != new_range.upper:
        return Range(new_range.upper - 1, old_range.upper)
    
    raise Exception()


def build_part_range(old_range: PartRange, new_range: PartRange) -> PartRange:
    if old_range.a != new_range.a:
        return PartRange(old_range.x, old_range.m, build_range(old_range.a, new_range.a), old_range.s)

    if old_range.x != new_range.x:
        return PartRange(build_range(old_range.x, new_range.x), old_range.m, old_range.a, old_range.s)

    if old_range.m != new_range.m:
        return PartRange(old_range.x, build_range(old_range.m, new_range.m), old_range.a, old_range.s)

    if old_range.s != new_range.s:
        return PartRange(old_range.x, old_range.m, old_range.a, build_range(old_range.s, new_range.s))

    raise Exception()


def calculate_variations(part_range: PartRange, wf: str, wfs: dict[str, list[Rule]]):
    if not check_range(part_range):
        return 0

    if wf == "A":
        return (part_range.a.upper - part_range.a.lower - 1) * (part_range.m.upper - part_range.m.lower - 1) * (part_range.x.upper - part_range.x.lower - 1) * (part_range.s.upper - part_range.s.lower - 1)

    if wf == "R":
        return 0

    var_sum = 0
    for rule in wfs[wf]:
        if not rule.operator:
            return var_sum + calculate_variations(part_range,
                                                  rule.next_chain, wfs)

        if rule.operator == Operator.lt:
            if rule.attribute == Attribute.a:
                new_range = PartRange(part_range.x, part_range.m, Range(
                    part_range.a.lower, min(part_range.a.upper, rule.value)), part_range.s)
                var_sum += calculate_variations(new_range,
                                                rule.next_chain, wfs)

            elif rule.attribute == Attribute.m:
                new_range = PartRange(part_range.x, Range(part_range.m.lower, min(
                    part_range.m.upper, rule.value)), part_range.a, part_range.s)
                var_sum += calculate_variations(new_range,
                                                rule.next_chain, wfs)

            elif rule.attribute == Attribute.s:
                new_range = PartRange(part_range.x, part_range.m, part_range.a, Range(
                    part_range.s.lower, min(part_range.s.upper, rule.value)))
                var_sum += calculate_variations(new_range,
                                                rule.next_chain, wfs)

            elif rule.attribute == Attribute.x:
                new_range = PartRange(Range(part_range.x.lower, min(
                    part_range.x.upper, rule.value)), part_range.m, part_range.a, part_range.s)
                var_sum += calculate_variations(new_range,
                                                rule.next_chain, wfs)

        elif rule.operator == Operator.gt:
            if rule.attribute == Attribute.a:
                new_range = PartRange(part_range.x, part_range.m, Range(
                    max(part_range.a.lower, rule.value), part_range.a.upper), part_range.s)
                var_sum += calculate_variations(new_range,
                                                rule.next_chain, wfs)

            elif rule.attribute == Attribute.m:
                new_range = PartRange(part_range.x, Range(max(
                    part_range.m.lower, rule.value), part_range.m.upper), part_range.a, part_range.s)
                var_sum += calculate_variations(new_range,
                                                rule.next_chain, wfs)

            elif rule.attribute == Attribute.s:
                new_range = PartRange(part_range.x, part_range.m, part_range.a, Range(
                    max(part_range.s.lower, rule.value), part_range.s.upper))
                var_sum += calculate_variations(new_range,
                                                rule.next_chain, wfs)

            elif rule.attribute == Attribute.x:
                new_range = PartRange(Range(max(part_range.x.lower, rule.value),
                                      part_range.x.upper), part_range.m, part_range.a, part_range.s)
                var_sum += calculate_variations(new_range,
                                                rule.next_chain, wfs)

        part_range = build_part_range(part_range, new_range)

    return var_sum


input_text = []

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(f"{dir_path}/input.txt", "r") as f:
    input_text = f.readlines()

input_text = list(map(lambda x: x.replace("\n", ""), input_text))

wfs: dict[str, list[Rule]] = dict()
index = 0
while input_text[index]:
    key, value = parse_chain(input_text[index])
    wfs[key] = value
    index += 1

parts: list[MachinePart] = []
index += 1
while index < len(input_text):
    parts.append(parse_part(input_text[index]))
    index += 1

# First part
first_sum = 0
for part in parts:
    if process_part(part, "in", wfs):
        first_sum += part.x + part.s + part.m + part.a

print(f"Answer first part: {first_sum}")

# Second part
print(f"Answer second part: {calculate_variations(PartRange(Range(0, 4001), Range(
    0, 4001), Range(0, 4001), Range(0, 4001)), "in", wfs)}")
