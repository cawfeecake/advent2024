import argparse

from lib.directions import Direction
from lib.grids import Grid, dot_copy, lines_mask
from lib.inputs import non_empty_upper_grid, non_empty_upper_str
from lib.strs import is_palindrome

def main():
    parser = argparse.ArgumentParser(
            description="Reports the number of times the given word is found in the input word search.")
    parser.add_argument("target_word", type=non_empty_upper_str, help="The word to search for")
    # TODO describe `word_search` expected format
    parser.add_argument("word_search_file", type=non_empty_upper_grid, help="Path to a file containing a word search")
    parser.add_argument("-d", "--debug", help="Print debug statements", action="store_true")
    args = parser.parse_args()

    # Program flags
    debug = args.debug

    # Program inputs
    target = args.target_word
    word_grid = args.word_search_file

    target_start = target[0]
    target_is_palindrome = is_palindrome(target)
    found_words = set()
    for y in range(word_grid.rows):
        for x in range(word_grid.cols(y)):
            if word_grid.get_value(x, y) == target_start:
                start = (x, y)
                if len(target) > 1:
                    directions_to_check = [d for d in Direction]  # looks for `target` emanating in all (8) directions
                    if target_is_palindrome:
                        #                                              v dx > 1, i.e. a Direction that goes right
                        directions_to_check = [d for d in Direction if d.value[0] > 0 or d == Direction.UP]

                    for d in directions_to_check:
                        values, is_all_in_bounds = word_grid.get_values(start, d, len(target))
                        if is_all_in_bounds and "".join(values) == target:
                            if debug:
                                print(f"[DEBUG] Match for \"{target}\" starting from {start} and going {d.name}!")
                            found_words.add((start, d, len(target)))
                else:
                    if debug:
                        print(f"[DEBUG] Match for \"{target}\" at {start}!")
                    found_words.add((start, None, 1))

    if debug:
        dots = Grid(dot_copy(word_grid))
        masked_dots = dots.mask(lines_mask(word_grid, found_words))
        print(masked_dots)

    print(f"\"{target}\" can be found {len(found_words)} time{"" if len(found_words) == 1 else "s"}.")

if __name__ == "__main__":
    main()
