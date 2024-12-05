from enum import Enum

class Direction(Enum):
    LEFT = (1, 0)
    RIGHT = (-1, 0)
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT_AND_UP = (1, -1)
    LEFT_AND_DOWN = (1, 1)
    RIGHT_AND_UP = (-1, -1)
    RIGHT_AND_DOWN = (-1, 1)

def check(grid: list[str], word: str, start: tuple[int, int], update: Direction) -> bool:
    x, y = start
    assert x >= 0 and y >= 0, "`start` position must be non-negative"
    x_update, y_update = update.value

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
            return True

        # update where to check next...
        x, y = x + x_update, y + y_update

    return False

def get_locations(grid: list[any], start: tuple[int, int], length: int, direction: Direction) -> list[tuple[int, int]], bool:
    locations = []

    x, y = start
    x_update, y_update = update.value
    i = 0
    while (
            y < len(grid) and x < len(grid[y])
            and x >= 0 and y >= 0
        ):
        locations.append((x, y))

        i += 1
        if i == length:
            return locations, True

        x, y = x + x_update, y + y_update

    return locations, False

import sys
import os

word = sys.argv[1]
assert len(word) > 0, "Must provide word to search for as the first argument"
word = word.lower()

input_file = sys.argv[2]
assert len(input_file) > 0, "Must provide input's filepath as the second argument"

_as_debug = False
try:
    _as_debug = os.environ["DEBUG"] == "1"
except:
    pass

grid = []
with open(input_file, "r") as file:
    for line in file:
        row = line.strip() # `.strip()` removes leading and trailing whitespace
        if len(row) > 0:
            grid.append(row.lower())
assert len(grid) > 0, "Input file must not be empty"

word_start = word[0]
found = 0
if as_debug:
    found_set = set()
for i in range(len(grid)):
    row = grid[i]
    for j in range(len(row)):
        if row[j] == word_start:
            start = (j, i)
            ds = [
                Direction.LEFT,
                Direction.RIGHT,
                Direction.UP,
                Direction.DOWN,
                Direction.LEFT_AND_UP,
                Direction.LEFT_AND_DOWN,
                Direction.RIGHT_AND_UP,
                Direction.RIGHT_AND_DOWN
            ]
            for d in ds:
                if check(grid, word, start, d):
                    if _as_debug:
                        print(f"Found match for {word} starting at {start} due: {d.name}")
                    found += 1

print(f"Found {found} instances of {word} in {input_file}")
