def check(grid: list[str], word: str, start: (int, int), update: (int, int)) -> bool:
    x_update, y_update = update
    assert not (x_update == 0 and y_update == 0), "at least 1 value of `update` must be non-zero"

    x, y = start
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

def check_around_in_direction(grid, prefix, suffix, start, direction):
    start_x, start_y = start
    direction_x, direction_y = direction
    if check(grid, prefix[::-1], (start_x + direction_x, start_y + direction_y), direction):
        return check(grid, suffix, (start_x - direction_x, start_y - direction_y), (direction_x * -1, direction_y * -1))
    return False

# Helpers: individual directions that make an "X" (if starting from center)
def check_left_and_up(grid, prefix, suffix, start):
    direction = (1, -1)
    return check_around_in_direction(grid, prefix, suffix, start, direction)

def check_right_and_up(grid, prefix, suffix, start):
    direction = (-1, -1)
    return check_around_in_direction(grid, prefix, suffix, start, direction)

def check_left_and_down(grid, prefix, suffix, start):
    direction = (1, 1)
    return check_around_in_direction(grid, prefix, suffix, start, direction)

def check_right_and_down(grid, prefix, suffix, start):
    direction = (-1, 1)
    return check_around_in_direction(grid, prefix, suffix, start, direction)

# Helpers: true if "word" is either forwards or backwards along a slash of "X"
def check_forward_slash(grid, prefix, suffix, start):
    return check_left_and_up(grid, prefix, suffix, start) \
        or check_right_and_down(grid, prefix, suffix, start)

def check_back_slash(grid, prefix, suffix, start):
    return check_right_and_up(grid, prefix, suffix, start) \
        or check_left_and_down(grid, prefix, suffix, start)

import sys

# TODO: formalize `assert` checks (i.e. program boundaries)

word = sys.argv[1]
# assumes no whitespace in `word`
assert len(word) > 0, "Must provide a word to search for as the first argument"
assert len(word) % 2 == 1, "Search word must be of an odd length to have a center"
word = word.lower()

input_file = sys.argv[2]
# assumes no whitespace in `input_file`
assert len(input_file) > 0, "Must provide a filepath for the input to search in as the second argument"

grid = []
with open(input_file, "r") as file:
    for line in file:
        row = line.strip() # `.strip()` removes leading and trailing whitespace
        if len(row) > 0:
            grid.append(row.lower())
assert len(grid) > 0, "Input file must not be empty"

prefix, center, suffix = word[:len(word) // 2], word[len(word) // 2], word[len(word) // 2 + 1:]
found = 0
# TODO: optimize to skip looking in first/last len() - 1 / 2 rows, columns
for i in range(len(grid)):
    row = grid[i]
    for j in range(len(row)):
        if row[j] == center:
            if check_forward_slash(grid, prefix, suffix, (j, i)) \
                    and check_back_slash(grid, prefix, suffix, (j, i)):
                print(f"Found match for {word} centered at ({j}, {i})") # DEBUG
                found += 1

print(f"Found {found} \"X\" of the word {word} in {input_file}")
