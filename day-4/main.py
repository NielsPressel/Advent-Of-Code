input_text = []

with open("input.txt", "r") as f:
    input_text = f.readlines()

first_sum = 0
d = {index: 1 for index, _ in enumerate(input_text)}
for index, line in enumerate(input_text):
    _, content = line.split(":")
    winning_numbers_str, elve_numbers_str = content.split("|")

    winning_numbers = list(map(int, winning_numbers_str.split()))
    elve_numbers = list(map(int, elve_numbers_str.split()))

    matches = 0
    for num in elve_numbers:
        if num in winning_numbers:
            matches += 1
    
    if matches > 0:
        first_sum += pow(2, matches - 1)

    for i in range(index + 1, index + matches + 1):
        d[i] += d[index]

print(f"Answer first part: {first_sum}")
print(f"Answer second part: {sum(d.values())}")
