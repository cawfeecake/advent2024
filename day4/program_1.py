import os
import sys

from lib.grids import Grid
from lib.directions import Direction

def main():
    word = sys.argv[1]
    assert len(word) > 0, "Must provide word to search for as the first argument"
    word = word.upper()

    input_file = sys.argv[2]
    assert len(input_file) > 0, "Must provide input's filepath as the second argument"

    _as_debug = False
    try:
        _as_debug = os.environ["DEBUG"] == "1"
    except:
        pass

    def open_and_parse_input():
        with open(input_file, "r") as file:
            for line in file:
                row = line.strip()  # `.strip()` removes leading and trailing whitespace
                if len(row) > 0:
                    yield row.upper()

    ws = Grid(open_and_parse_input)
    assert ws.rows > 0, "Input file must not be empty"

    word_start = word[0]
    found, found_mask = 0, []
    for i in range(ws.rows):
        row = ws.grid[i]
        for j in range(len(row)):
            if row[j] == word_start:
                start = (j, i)
                for d in Direction:  # iterates thru all 8 directions
                    values, fits = ws.get_values(start, d, len(word))
                    if fits and word == "".join(values):
                        if _as_debug:
                            points, _ = ws.get_points(start, d, len(word))
                            found_mask.extend([((x, y), ws.get_value(x, y)) for x, y in points])
                            print(f"Found match for {word} starting at {start} due: {d.name}")
                        found += 1

    if _as_debug:
        def _dot_grid(n: int):
            def f():
                for i in range(n):
                    yield list("." * n)
            return f
        dots = Grid(_dot_grid(ws.rows))

        def _mask_func():
            for mask in found_mask:
                yield mask

        dots.mask(_mask_func)
        print(dots.__repr__())

    print(f"Found {found} instances of {word} in {input_file}")

if __name__ == "__main__":
    main()

