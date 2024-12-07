import argparse

from lib.directions import Direction
from lib.grids import Grid
from lib.inputs import non_empty_str

def main():
    parser = argparse.ArgumentParser(
            description="Reports the number of times the given word is found in the input.")
    parser.add_argument("target_word", type=non_empty_str, help="The word to search for")
    # TODO look into argparse.FileType
    parser.add_argument("word_search_file", help="Path to the file containing the word search")
    parser.add_argument("-d", "--debug", help="Print debug statements", action="store_true")
    args = parser.parse_args()

    # Program flags
    debug = args.debug

    # Program inputs
    word = args.target_word.upper()

    input_file = args.word_search_file
    try:
        with open(input_file, "r") as file:
            def parse_input():
                for line in file:
                    row = line.strip()  # `.strip()` removes leading and trailing whitespace
                    if len(row) > 0:
                        yield row.upper()
            ws = Grid(parse_input)
    except FileNotFoundError:
        parser.error(f"Input file ({input_file}) doesn't exist!")

    if ws.rows == 0:
        parser.error(f"Input file ({input_file}) is empty!")

    word_start = word[0]
    found, found_mask = 0, []
    for y in range(ws.rows):
        for x in range(ws.cols(y)):
            if ws.get_value(x, y) == word_start:
                start = (x, y)
                for d in Direction:  # looks for `target_word` emanating in every direction (8)
                    values, is_all_in_bounds = ws.get_values(start, d, len(word))
                    if is_all_in_bounds and "".join(values) == word:
                        if debug:
                            points, _ = ws.get_points(start, d, len(word))
                            found_mask.extend([((x, y), ws.get_value(x, y)) for x, y in points])
                            print(f"[DEBUG] Match for \"{word}\" starting from {start} and going {d.name}!")
                        found += 1

    if debug:
        def dot_grid(n: int):
            def f():
                for i in range(n):
                    yield "." * n
            return f
        dots = Grid(dot_grid(ws.rows))

        def mask_func():
            for mask in found_mask:
                yield mask

        dots_masked = dots.mask(mask_func)
        print(dots_masked)

    print(f"In {input_file} \"{word}\" is found {found} times.")

if __name__ == "__main__":
    main()
