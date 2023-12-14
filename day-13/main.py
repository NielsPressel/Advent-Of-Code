import os

def compare_rows(first_ind: int, second_ind: int, pattern: list[str]) -> bool:
        return all(c1 == c2 for c1, c2 in zip(pattern[first_ind], pattern[second_ind]))
    
def compare_columns(first_ind: int, second_ind: int, pattern: list[str]) -> bool:
    return all(line[first_ind] == line[second_ind] for line in pattern)

def check_ref_row_line(index: int, pattern: list[str]):
    i = 0
    while index - i - 1 >= 0 and index + i < len(pattern):
        if not compare_rows(index - i - 1, index + i, pattern):
            return False
        
        i += 1
    
    return True

def check_ref_col_line(index: int, pattern: list[str]):
    i = 0
    while index - i - 1 >= 0 and index + i < len(pattern[0]):
        if not compare_columns(index - i - 1, index + i, pattern):
            return False
        
        i += 1
    
    return True

def find_reflections(pattern: list[str]) -> list[int]:
    results = []

    for index in range(1, len(pattern)):
        if check_ref_row_line(index, pattern):
            results.append(100 * index)
    for index in range(1, len(pattern[0])):
        if check_ref_col_line(index, pattern):
            results.append(index)

    return results

def iterate_pattern(pattern):
    result = find_reflections(pattern)[0]

    for row_ind, line in enumerate(pattern):
        for col_ind, char in enumerate(line):
            if char == ".":
                pattern[row_ind] = pattern[row_ind][:col_ind] + "#" + pattern[row_ind][col_ind + 1:]
                results_smudge = find_reflections(pattern)

                for r in results_smudge:
                    if r != result:
                        return r
                
                pattern[row_ind] = pattern[row_ind][:col_ind] + "." + pattern[row_ind][col_ind + 1:]
            elif char == "#":
                pattern[row_ind] = pattern[row_ind][:col_ind] + "." + pattern[row_ind][col_ind + 1:]
                results_smudge = find_reflections(pattern)

                for r in results_smudge:
                    if r != result:
                        return r
                
                pattern[row_ind] = pattern[row_ind][:col_ind] + "#" + pattern[row_ind][col_ind + 1:]
    
    raise Exception()


input_text = []

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(f"{dir_path}/input.txt", "r") as f:
    input_text = f.readlines()

input_text = list(map(lambda x: x.replace("\n", ""), input_text))

first_sum = 0
second_sum = 0
current_block = []
for line in input_text:
    if line.strip() == "":
        first_sum += find_reflections(current_block)[0]
        second_sum += iterate_pattern(current_block)

        current_block = []
    else:
        current_block.append(line)

first_sum += find_reflections(current_block)[0]
second_sum += iterate_pattern(current_block)

print(f"Answer first part: {first_sum}")
print(f"Answer second part: {second_sum}")