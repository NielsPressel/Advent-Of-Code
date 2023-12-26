import os
import math

def calculate_options(race: tuple[int, int]):
    count = 0

    for i in range(0, race[0]):
        distance = i * (race[0] - i)

        if distance > race[1]:
            count += 1
    
    return count

def find_boundary(race: tuple[int, int]):
    time_1 = race[0]/2 - math.sqrt(math.pow(race[0]/2, 2) - race[1])
    time_2 = race[0]/2 + math.sqrt(math.pow(race[0]/2, 2) - race[1])

    return time_1, time_2


input_text = []

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(f"{dir_path}/input.txt", "r") as f:
    input_text = f.readlines()

# First part
times = list(map(int, input_text[0].split(":")[1].split()))
distances = list(map(int, input_text[1].split(":")[1].split()))
races = list(zip(times, distances))


prod = 1
for race in races:
    prod *= calculate_options(race)

print(f"Answer first part: {prod}")

# Second part
race = (int("".join(map(str, times))), int("".join(map(str, distances))))

time_1, time_2 = find_boundary(race)
time_1, time_2 = math.ceil(time_1), math.floor(time_2)

print(f"Answer second part: {time_2 - time_1 + 1}")
