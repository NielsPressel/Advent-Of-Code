import os
import re

class Lens:

    def __init__(self, label: str, fl: int) -> None:
        self.label = label
        self.fl = fl


def hash_str(item: str):
    current_value = 0

    for c in item:
        current_value += ord(c)
        current_value = (current_value * 17) % 256
    
    return current_value

def perform_operation(item: str, hash_map: dict[int, list[Lens]]):
    if "=" in item:
        r = r"([a-z]+)=(\d)"
        p = re.compile(r)
        m = p.match(item)
        label = m.group(1)
        fl = int(m.group(2))
        h = hash_str(label)

        if not h in hash_map:
            hash_map[h] = []

        for index, value in enumerate(hash_map[h]):
            if value.label == label:
                hash_map[h][index] = Lens(label, fl)
                break
        else:
            hash_map[h].append(Lens(label, fl))

    elif "-" in item:
        r = r"([a-z]+)-"
        p = re.compile(r)
        m = p.match(item)
        label = m.group(1)
        h = hash_str(label)

        if not h in hash_map:
            hash_map[h] = []
        
        for index, value in enumerate(hash_map[h]):
            if value.label == label:
                break
        else:
            return
        
        del hash_map[h][index]

input_text = []

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(f"{dir_path}/input.txt", "r") as f:
    input_text = f.readlines()

input_text = list(map(lambda x: x.replace("\n", ""), input_text))

items = input_text[0].split(",")

first_sum = 0
hash_map: dict[int, list[Lens]] = dict()
for item in items:
    first_sum += hash_str(item)
    perform_operation(item , hash_map)

second_sum = 0
for key in hash_map:
    for index, value in enumerate(hash_map[key]):
        second_sum += (key + 1) * (index + 1) * value.fl

print(f"Answer first part: {first_sum}")
print(f"Answer second part: {second_sum}")