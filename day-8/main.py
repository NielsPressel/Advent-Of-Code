import os
import re
from itertools import cycle
from math import lcm
from functools import reduce

class Node:

    @staticmethod
    def parse(line: str):
        r = r"([A-Z]+) = \(([A-Z]+), ([A-Z]+)\)"
        p = re.compile(r)
        m = p.match(line)

        return Node(m.group(1), m.group(2), m.group(3))

    def __init__(self, label: str, left: str, right: str) -> None:
        self.label = label
        self.left = left
        self.right = right
        
    def __repr__(self) -> str:
        return f"Node [ Label: {self.label}, Left: {self.left}, Right: {self.right} ]"

class Graph:

    @staticmethod
    def parse(lines: list[str]):
        result = {}

        for line in lines:
            node = Node.parse(line)

            result[node.label] = node
        
        return Graph(result)

    def __init__(self, nodes: dict[str, Node]) -> None:
        self.nodes = nodes

    def follow(self, start: Node, instructions: str, is_final) -> int:
        current_node = start
        count = 0

        for character in cycle(instructions):
            if character == 'L':
                current_node = self.nodes[current_node.left]
            elif character == 'R':
                current_node = self.nodes[current_node.right]
            else:
                continue

            count += 1

            if is_final(current_node.label):
                break
        
        return count

    def follow_instructions(self, instructions: str):
        start = self.nodes['AAA']
        
        return self.follow(start, instructions, lambda x: x == 'ZZZ')
    
    def follow_instructions_simul(self, instructions: str):
        start_nodes = [self.nodes[key] for key in self.nodes if key[-1] == 'A']
        counts = list(map(lambda x: self.follow(x, instructions, lambda x: x[-1] == 'Z'), start_nodes))
        
        return reduce(lcm, counts)


input_text = []

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(f"{dir_path}/input.txt", "r") as f:
    input_text = f.readlines()

instructions = input_text[0]

graph = Graph.parse(input_text[2:])
first_count = graph.follow_instructions(instructions)
second_count = graph.follow_instructions_simul(instructions)

print(f"Answer first part: {first_count}")
print(f"Answer second part: {second_count}")