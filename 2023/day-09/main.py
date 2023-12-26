import os

def calculate_diff_seq(sequence: list[int]) -> list[int]:
    diff_sequence = []

    for i in range(1, len(sequence)):
        diff_sequence.append(sequence[i] - sequence[i - 1])
    
    return diff_sequence

def extrapolate(sequence: list[int]) -> int:
    if not any(sequence):
        return 0
    
    diff_sequence = calculate_diff_seq(sequence)
    return diff_sequence[-1] + extrapolate(diff_sequence)

def extrapolate_back(sequence: list[int]) -> int:
    if not any(sequence):
        return 0
    
    diff_sequence = calculate_diff_seq(sequence)
    return diff_sequence[0] - extrapolate_back(diff_sequence)

    
input_text = []

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(f"{dir_path}/input.txt", "r") as f:
    input_text = f.readlines()

# First part
first_sum = 0
for line in input_text:
    numbers = list(map(int, line.split()))
    first_sum += numbers[-1] + extrapolate(numbers)

print(f"Answer first part: {first_sum}")

# Second part
second_sum = 0
for line in input_text:
    numbers = list(map(int, line.split()))
    second_sum += numbers[0] - extrapolate_back(numbers)

print(f"Answer second part: {second_sum}")