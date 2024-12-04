def check(grid: list[str], word: str, start: tuple[int, int], update: tuple[int, int]) -> bool:
    x, y = start
    assert x >= 0 and y >= 0, "`start` position must be non-negative"
    x_update, y_update = update
    assert not (x_update == 0 and y_update == 0), "at least 1 value of `update` must be non-zero"

    word_i = 0
    while (
            y < len(grid) and x < len(grid[y]) # TODO: test if this conditional holds up for a non-square `grid`
            and x >= 0 and y >=0 # note: prevents word from matching around across left-side/bottom-side
        ): 
        if grid[y][x] != word[word_i]:
            return False

        # update position in `word`, and see if we've seen it all...
        word_i += 1
        if word_i == len(word):
            #print(f"Found match for {word} starting at {start} and going {update}") # DEBUG
            return True

        # update where to check next...
        x, y = x + x_update, y + y_update

    return False

# Helpers for: cardinal directions
def check_left(grid, word, start):
    return check(grid, word, start, (1, 0))

def check_right(grid, word, start):
    return check(grid, word, start, (-1, 0))

def check_up(grid, word, start):
    return check(grid, word, start, (0, -1))

def check_down(grid, word, start):
    return check(grid, word, start, (0, 1))

# Helpers for: diagnol directions
def check_left_and_up(grid, word, start):
    return check(grid, word, start, (1, -1))

def check_right_and_up(grid, word, start):
    return check(grid, word, start, (-1, -1))

def check_left_and_down(grid, word, start):
    return check(grid, word, start, (1, 1))

def check_right_and_down(grid, word, start):
    return check(grid, word, start, (-1, 1))

import sys

word = sys.argv[1]
assert len(word) > 0, "Must provide word to search for as the first argument"
word = word.lower()

input_file = sys.argv[2]
assert len(input_file) > 0, "Must provide input's filepath as the second argument"

grid = []
with open(input_file, "r") as file:
    for line in file:
        row = line.strip() # `.strip()` removes leading and trailing whitespace
        if len(row) > 0:
            grid.append(row.lower())
assert len(grid) > 0, "Input file must not be empty"

word_start = word[0]
found = 0
for i in range(len(grid)):
    row = grid[i]
    for j in range(len(row)):
        if row[j] == word_start:
            bs = [
                check_left(grid, word, (j, i)),
                check_right(grid, word, (j, i)),
                check_up(grid, word, (j, i)),
                check_down(grid, word, (j, i)),
                check_left_and_up(grid, word, (j, i)),
                check_right_and_up(grid, word, (j, i)),
                check_left_and_down(grid, word, (j, i)),
                check_right_and_down(grid, word, (j, i))
            ]
            for b in bs:
                if b:
                    found += 1

print(f"Found {found} instances of {word} in {input_file}")
