input_text = []

with open('input.txt', 'r') as f:
    input_text = f.readlines()

# First part
sum = 0
for line in input_text:
    digits = ''
    for character in line:
        if character.isdigit():
            digits += character

    number = int(digits[0] + digits[-1])
    sum += number

print(f"Answer first part: {sum}")

# Second part
digit_strings = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

def check_startswith(sub_str: str, options: list[str]):
    for index, opt in enumerate(options):
        if sub_str.startswith(opt):
            return index
    
    return -1

sum = 0
for line in input_text:
    digits = ''

    for index, character in enumerate(line):
        match_index = check_startswith(line[index:], digit_strings)

        if match_index > -1:
            digits += f"{match_index + 1}"
        else:
            if character.isdigit():
                digits += character
    
    number = int(digits[0] + digits[-1])
    sum += number

print(f"Answer second part: {sum}")
