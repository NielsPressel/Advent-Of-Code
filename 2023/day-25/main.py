import os
import re
import random
import networkx as nx


def parse(input_text: list[str]) -> dict[str, list[str]]:
    regex = r"([a-z]+): (.*)"
    pattern = re.compile(regex)

    graph = nx.Graph()

    for line in input_text:
        match = pattern.match(line)
        label = match.group(1)
        connections = match.group(2).split()

        for c in connections:
            graph.add_edge(label, c, capacity=1)

    return graph


input_text = []

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(f"{dir_path}/input.txt", "r") as f:
    input_text = f.readlines()

input_text = list(map(lambda x: x.replace("\n", ""), input_text))

graph = parse(input_text)
nodes = graph.nodes

value = -1

while value != 3:
    test = random.sample(sorted(nodes), 2)
    value, partition = nx.minimum_cut(graph, test[0], test[1])

print(f"Answer first part: {len(partition[0]) * len(partition[1])}")
