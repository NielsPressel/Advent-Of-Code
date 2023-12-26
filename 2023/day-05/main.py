import os

class ConvertMapEntry:

    def __init__(self, source_start, dest_start, length) -> None:
        self.source_start = source_start
        self.dest_start = dest_start
        self.length = length
    
    def __repr__(self) -> str:
        return f"MapEntry [ Source Start: {self.source_start}, Destination Start: {self.dest_start}, Length: {self.length} ]"
    
    def __str__(self) -> str:
        return f"MapEntry [ Source Start: {self.source_start}, Destination Start: {self.dest_start}, Length: {self.length} ]"

class ConvertMap:
    
    @staticmethod
    def calculate_intersection(range_a: tuple[int, int], range_b: tuple[int, int]):
        if range_b[0] >= range_a[1] or range_a[0] >= range_b[1]:
            intersection = None
        else:
            intersection = (max(range_a[0], range_b[0]), min(range_a[1], range_b[1]))
        
        return intersection
    
    @staticmethod
    def calculate_diff(range_a: tuple[int, int], range_b: tuple[int, int]) -> list[tuple[int, int]]:
        result = []

        if range_a[0] < range_b[0]:
            result.append((range_a[0], range_b[0]))

        if range_a[1] > range_b[1]:
            result.append((range_b[1], range_a[1]))

        return result

    def __init__(self, values: list[ConvertMapEntry]) -> None:
        self.values = values

    def convert(self, seed: int):
        for value in self.values:
            if seed in range(value.source_start, value.source_start + value.length):
                return value.dest_start + (seed - value.source_start)
        
        return seed

    def convert_range(self, range_item: tuple[int, int]):
        if range_item[1] - range_item[0] <= 0:
            return []

        for value in self.values:
            value_end = value.source_start + value.length

            intersection = ConvertMap.calculate_intersection(range_item, (value.source_start, value_end))

            if intersection:
                diff = ConvertMap.calculate_diff(range_item, intersection)

                result = []
                result.append((value.dest_start + (intersection[0] - value.source_start), value.dest_start + (intersection[1] - value.source_start)))
                
                for item in diff:
                    result += self.convert_range(item)
                
                return result

        return [range_item]

    def convert_list(self, seeds: list[int]):
        return list(map(self.convert, seeds))
    
    def convert_range_list(self, seed_ranges: list[tuple[int, int]]):
        result = []

        for seed_range in seed_ranges:
            result += self.convert_range(seed_range)
        
        return result



def parse_map(input_text: list[str], index):
    entries = []

    for i in range(index, len(input_text)):
        line = input_text[i]
        if line.strip() == "":
            break

        numbers = list(map(int, line.split()))
        entries.append(ConvertMapEntry(numbers[1], numbers[0], numbers[2]))
    
    return i, ConvertMap(entries)

input_text = []

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(f"{dir_path}/input.txt", "r") as f:
    input_text = f.readlines()


seeds = list(map(int, input_text[0].split(":")[1].split()))
seed_ranges = [(seeds[i], seeds[i] + seeds[i + 1]) for i in range(0, len(seeds), 2)]

current_index = 3
while current_index < len(input_text):
    current_index, convert_map = parse_map(input_text, current_index)
    seeds = convert_map.convert_list(seeds)
    seed_ranges = convert_map.convert_range_list(seed_ranges)

    current_index += 2

print(f"Answer first part: {min(seeds)}")
print(f"Answer second part: {min(list(map(lambda x: x[0], seed_ranges)))}")
