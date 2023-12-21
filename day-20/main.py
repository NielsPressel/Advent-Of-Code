import os
import re
from dataclasses import dataclass
from queue import SimpleQueue
from math import lcm


@dataclass
class Pulse:
    start: str
    dest: str
    state: bool


class Module:

    def __init__(self, label: str, destinations: list[str]) -> None:
        self.label = label
        self.destinations = destinations

    def handle(self, pulse: Pulse) -> list[Pulse]:
        raise Exception()


class FlipFlop(Module):

    def __init__(self, label: str, destinations: list[str]) -> None:
        super().__init__(label, destinations)
        self.state = False

    def handle(self, pulse: Pulse) -> list[Pulse]:
        if pulse.state == True:
            return []

        self.state = not self.state

        result = []
        for d in self.destinations:
            result.append(Pulse(self.label, d, self.state))

        return result


class Conjunction(Module):

    def __init__(self, label: str, destinations: list[str], inputs: list[str]) -> None:
        super().__init__(label, destinations)
        self.state: dict[str, bool] = dict()

        for i in inputs:
            self.state[i] = False

    def handle(self, pulse: Pulse) -> list[Pulse]:
        self.state[pulse.start] = pulse.state

        msg = True
        if all(k for k in self.state.values()):
            msg = False

        result = []
        for d in self.destinations:
            result.append(Pulse(self.label, d, msg))

        return result


class Broadcast(Module):

    def __init__(self, label: str, destinations: list[str]) -> None:
        super().__init__(label, destinations)

    def handle(self, pulse: Pulse):
        result = []
        for d in self.destinations:
            result.append(Pulse(self.label, d, pulse.state))

        return result


def parse(input_text: list[str]) -> list[Module]:
    input_map: dict[str, list[str]] = dict()

    for line in input_text:
        regex = r"([%&]*)(\w+) -> (.*)"
        pattern = re.compile(regex)
        match = pattern.match(line)

        name = match.group(2)
        destinations = match.group(3).split(", ")

        for d in destinations:
            if not d in input_map:
                input_map[d] = []

            input_map[d].append(name)

    result: dict[str, Module] = dict()
    for line in input_text:
        regex = r"([%&]*)(\w+) -> (.*)"
        pattern = re.compile(regex)
        match = pattern.match(line)

        t = match.group(1)
        name = match.group(2)
        destinations = match.group(3).split(", ")

        if t == "%":
            result[name] = FlipFlop(name, destinations)
        elif t == "&":
            result[name] = Conjunction(name, destinations, input_map[name])
        else:
            result[name] = Broadcast(name, destinations)

    return input_map, result


def process_button_press(modules: dict[str, Module]) -> tuple[int, int]:
    q: SimpleQueue[Pulse] = SimpleQueue()
    q.put(Pulse("", "broadcaster", False))

    hp = 0
    lp = 1
    while not q.empty():
        item = q.get()

        if not item.dest in modules:
            continue

        result = modules[item.dest].handle(item)

        for r in result:
            q.put(r)

            if r.state == True:
                hp += 1
            else:
                lp += 1

    return hp, lp

def find_cycles(input_map: dict[str, list[str]], modules: dict[str, Module]):
    conj_inputs = input_map[input_map["rx"][0]]
    cycles_memory = dict()
    cycle = 1

    while len(conj_inputs) > len(cycles_memory):
        q: SimpleQueue[Pulse] = SimpleQueue()
        q.put(Pulse("", "broadcaster", False))

        while not q.empty():
            item = q.get()

            if not item.dest in modules:
                continue

            result = modules[item.dest].handle(item)

            if result and result[0].state:
                if item.dest in conj_inputs:
                    if item.dest not in cycles_memory:
                        cycles_memory[item.dest] = cycle

            for r in result:
                q.put(r)
        
        cycle += 1
    
    return lcm(*cycles_memory.values())


input_text = []

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(f"{dir_path}/input.txt", "r") as f:
    input_text = f.readlines()

input_text = list(map(lambda x: x.replace("\n", ""), input_text))

input_map, modules = parse(input_text)

hp = 0
lp = 0
for i in range(0, 1000):
    h, l = process_button_press(modules)
    hp += h
    lp += l

print(f"Answer first part: {hp * lp}")

input_map, modules = parse(input_text)
print(f"Answer second part: {find_cycles(input_map, modules)}")
