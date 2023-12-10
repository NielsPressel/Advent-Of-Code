import os
import sys

class Grid:

    def __init__(self, grid: list[str]) -> None:
        self.grid = grid
        self.loop = [[0] * len(line) for line in grid]

    def find_start(self):
        for r_index, row in enumerate(self.grid):
            for c_index, item in enumerate(row):
                if item == "S":
                    return r_index, c_index
        
        raise Exception()

    def find_adjacent(self, current: tuple[int, int], last: tuple[int, int], grid):
        item = grid[current[0]][current[1]]

        if item == "|":
            return current[0] - (last[0] - current[0]), current[1]
        
        if item == '-':
            return current[0], current[1] - (last[1] - current[1])
        
        if item == "F":
            if current[0] < last[0]:
                return current[0], current[1] + 1
            else:
                return current[0] + 1, current[1]
        
        if item == "J":
            if current[0] > last[0]:
                return current[0], current[1] - 1
            else:
                return current[0] - 1, current[1]
        
        if item == "7":
            if current[0] < last[0]:
                return current[0], current[1] - 1
            else:
                return current[0] + 1, current[1]
        
        if item == "L":
            if current[0] > last[0]:
                return current[0], current[1] + 1
            else:
                return current[0] - 1, current[1]
            
        if item == "S":
            top = self.grid[current[0] - 1][current[1]]

            if top == "F" or top == "|" or top == "7":
                return current[0] - 1, current[1]
            
            right = self.grid[current[0]][current[1] + 1]

            if right == "J" or right == "7" or right == "-":
                return current[0], current[1] + 1
            
            bottom = self.grid[current[0] - 1][current[1]]

            if bottom == "L" or bottom == "J" or bottom == "|":
                return current[0] + 1, current[1]
            
            left = self.grid[current[0]][current[1] - 1]

            if left == "F" or left == "L" or left == "-":
                return current[0], current[1] - 1
            
        raise Exception()
    
    def calculate_loop_length(self):
        start = self.find_start()
        last = start
        current = self.find_adjacent(start, None, self.grid)
        count = 1

        self.loop[current[0]][current[1]] = 1

        while current != start:
            tmp = self.find_adjacent(current, last, self.grid)

            last = current
            current = tmp
            self.loop[current[0]][current[1]] = 1

            count += 1
        
        return count
    
    def find_root_outside(self, grid: list[list[int]]):
        for i in range(0, len(grid)):
            if grid[i][0] == 0:
                return i, 0
            
            if grid[i][len(grid[0]) - 1] == 0:
                return i, len(grid[0]) - 1
        
        for i in range(0, len(grid[0]) - 1):
            if grid[0][i] == 0:
                return 0, i
            
            if grid[len(grid) - 1][i] == 0:
                return len(grid) - 1, i
    
    def fill_neighbors(self, pos: tuple[int], grid: list[list[int]]):
        neighbors = [(max(0, pos[0] - 1), pos[1]), (min(len(grid) - 1, pos[0] + 1), pos[1]), (pos[0], max(0, pos[1] - 1)), (pos[0], min(len(grid[0]) - 1, pos[1] + 1))]

        for n in neighbors:
            if grid[n[0]][n[1]] == 0:
                grid[n[0]][n[1]] = 2
                self.fill_neighbors(n, grid)
    
    def dfs(self, grid):
        root = self.find_root_outside(grid)
        self.fill_neighbors(root, grid)
    
    def calculate_contained_points(self):
        expanded_grid: list[list[str]] = []
        for i in range(0, 3 * len(self.grid)):
            expanded_grid.append([])
            for j in range(0, 3 * len(self.grid[0])):
                expanded_grid[i].append(".")


        for row_ind, row in enumerate(self.grid):
            for col_ind, item in enumerate(row):
                if item == '|':
                    expanded_grid[3 * row_ind + 0][3 * col_ind + 1] = '|'
                    expanded_grid[3 * row_ind + 1][3 * col_ind + 1] = '|'
                    expanded_grid[3 * row_ind + 2][3 * col_ind + 1] = '|'
                elif item == '-':
                    expanded_grid[3 * row_ind + 1][3 * col_ind + 0] = '-'
                    expanded_grid[3 * row_ind + 1][3 * col_ind + 1] = '-'
                    expanded_grid[3 * row_ind + 1][3 * col_ind + 2] = '-'
                elif item == 'F':
                    expanded_grid[3 * row_ind + 1][3 * col_ind + 1] = 'F'
                    expanded_grid[3 * row_ind + 2][3 * col_ind + 1] = '|'
                    expanded_grid[3 * row_ind + 1][3 * col_ind + 2] = '-'
                elif item == '7':
                    expanded_grid[3 * row_ind + 1][3 * col_ind + 1] = '7'
                    expanded_grid[3 * row_ind + 2][3 * col_ind + 1] = '|'
                    expanded_grid[3 * row_ind + 1][3 * col_ind + 0] = '-'
                elif item == 'J':
                    expanded_grid[3 * row_ind + 1][3 * col_ind + 1] = 'J'
                    expanded_grid[3 * row_ind + 0][3 * col_ind + 1] = '|'
                    expanded_grid[3 * row_ind + 1][3 * col_ind + 0] = '-'
                elif item == 'L':
                    expanded_grid[3 * row_ind + 1][3 * col_ind + 1] = 'L'
                    expanded_grid[3 * row_ind + 0][3 * col_ind + 1] = '|'
                    expanded_grid[3 * row_ind + 1][3 * col_ind + 2] = '-'
                elif item == 'S':
                    expanded_grid[3 * row_ind + 1][3 * col_ind + 1] = 'S'
                    expanded_grid[3 * row_ind + 0][3 * col_ind + 1] = '|'
                    expanded_grid[3 * row_ind + 2][3 * col_ind + 1] = '|'
                    expanded_grid[3 * row_ind + 1][3 * col_ind + 0] = '-'
                    expanded_grid[3 * row_ind + 1][3 * col_ind + 2] = '-'
        
        start = self.find_start()
        last = (start[0] * 3 + 1, start[1] * 3 + 1)

        current = self.find_adjacent(start, None, self.grid)
        diff = (current[0] - start[0], current[1] - start[1])
        current = (last[0] + diff[0], last[1] + diff[1])
        start = last

        loop_grid = []
        for row in expanded_grid:
            new_row = []
            
            for item in row:
                new_row.append(0)
            
            loop_grid.append(new_row)

        loop_grid[current[0]][current[1]] = 1

        while current != start:
            tmp = self.find_adjacent(current, last, expanded_grid)

            last = current
            current = tmp

            loop_grid[current[0]][current[1]] = 1
        
        self.dfs(loop_grid)

        count = 0
        for row_ind, row in enumerate(loop_grid):
            for col_ind, item in enumerate(row):
                if item == 0:
                    orig_item = self.loop[row_ind // 3][col_ind // 3]

                    if orig_item != 1:
                        count += 1
        
        return count // 9


sys.setrecursionlimit(100000)

input_text = []

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(f"{dir_path}/input.txt", "r") as f:
    input_text = f.readlines()

input_text = list(map(lambda x: x.replace("\n", ""), input_text))

grid = Grid(input_text)
print(f"Answer first part: {grid.calculate_loop_length() // 2}")
print(f"Answer second part: {grid.calculate_contained_points()}")
