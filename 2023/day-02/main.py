import re

class Round:
    def __init__(self, red: int, green: int, blue: int) -> None:
        self.red = red
        self.green = green
        self.blue = blue

    @staticmethod
    def parse(line: str):
        result_parts = line.split(",")

        red = 0
        green = 0
        blue = 0

        for part in result_parts:
            number = int(re.findall(r"\d+", part)[0])

            if part.find("red") > -1:
                red = number
            elif part.find("green") > -1:
                green = number
            elif part.find("blue") > -1:
                blue = number

        return Round(red, green, blue)
    
    def is_possible(self):
        return self.red <= 12 and self.green <= 13 and self.blue <= 14


class Game:

    def __init__(self, id: str, results: list[Round]) -> None:
        self.id = id
        self.results = results

    @staticmethod
    def parse(line: str):
        id_split = line.split(":")
        id = int(re.findall(r"\d+", id_split[0])[0])

        result = []
        for round in id_split[1].split(";"):
            result.append(Round.parse(round))
        
        return Game(id, result)
    
    def is_possible(self):
        for round in self.results:
            if not round.is_possible():
                return False
        
        return True
    
    def set_power_minimal(self):
        red_max = 0
        green_max = 0
        blue_max = 0

        for round in self.results:
            red_max = max(round.red, red_max)
            green_max = max(round.green, green_max)
            blue_max = max(round.blue, blue_max)
        
        return red_max * green_max * blue_max


input_text = []
with open("input.txt", "r") as f:
    input_text = f.readlines()

first_sum = 0
second_sum = 0
for line in input_text:
    game = Game.parse(line)

    if game.is_possible():
        first_sum += game.id
    
    second_sum += game.set_power_minimal()

print(f"Answer first part: {first_sum}")
print(f"Answer second part: {second_sum}")
