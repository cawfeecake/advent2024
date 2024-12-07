import argparse

from lib.directions import Direction
from lib.grids import Grid, dot_copy, points_mask
from lib.inputs import BASE_PARSER
from lib.inputs import non_empty_upper_grid
from lib.inputs import non_empty_str, odd_length_str, upper_str

def _get_slash_points(grid: Grid, start: (int, int), slash: (Direction, Direction), length: str) -> (list[(int, int)], bool):
    leading_direction, tailing_direction = slash
    lead, is_in_bounds = grid.get_points(start, leading_direction, length)
    if not is_in_bounds:
        return [], False
    lead = lead[1:]
    lead = list(reversed(lead))

    tail, is_in_bounds = grid.get_points(start, tailing_direction, length)
    if not is_in_bounds:
        return [], False

    return lead + tail, True

_forward_slash = (Direction.RIGHT_AND_UP, Direction.LEFT_AND_DOWN)
_back_slash = (Direction.RIGHT_AND_DOWN, Direction.LEFT_AND_UP)

def get_x_points(grid: Grid, start: (int, int), length: int) -> (list[(int, int)], bool):
    both, is_in_bounds = _get_slash_points(grid, start, _forward_slash, length)
    _both, _is_in_bounds = _get_slash_points(grid, start, _back_slash, length)
    both += _both
    is_in_bounds &= _is_in_bounds
    return both, is_in_bounds

def _match_slash(grid: Grid, start: (int, int), slash: (Direction, Direction), target_word: str) -> bool:
    points, is_in_bounds = _get_slash_points(grid, start, slash, len(target_word) // 2 + 1)
    if not is_in_bounds:
        return False

    word = "".join([grid.get_value(x, y) for x, y in points])
    reversed_word = word[::-1]

    return target_word == word or target_word == reversed_word

def match_forward_slash(grid: Grid, start: (int, int), target_word: str) -> bool:
    return _match_slash(grid, start, _forward_slash, target_word)

def match_back_slash(grid: Grid, start: (int, int), target_word: str) -> bool:
    return _match_slash(grid, start, _back_slash, target_word)

def main():
    def input_target_word_type(s: str) -> str:
        s = non_empty_str(s)
        s = odd_length_str(s)
        return upper_str(s)

    parser = argparse.ArgumentParser(
            parents=[BASE_PARSER],
            description="Reports the number of times the given word is found in the input word search when shaped as an \"X\".")

    parser.add_argument("target_word", type=input_target_word_type, help="The word to search for (must be of an odd length)")
    # TODO describe `word_search_file` expected format
    parser.add_argument("word_search_file", type=non_empty_upper_grid, help="Path to a file containing a word search")
    args = parser.parse_args()

    # Program flags
    debug = args.debug

    # Program inputs
    target = args.target_word
    word_grid = args.word_search_file

    #prefix, center, suffix = st[:len(st) // 2], st[len(st) // 2], st[len(st) // 2 + 1:]  # for odd length `st`
    center_letter = target[len(target) // 2]
    found_xs = []
    # TODO optimize to skip looking in first/last len() - 1 / 2 rows, columns
    for y in range(word_grid.rows):
        for x in range(word_grid.cols(y)):
            if word_grid.get_value(x, y) == center_letter:
                if match_forward_slash(word_grid, (x, y), target) \
                        and match_back_slash(word_grid, (x, y), target):
                    if debug:
                        print(f"Found match for \"{target}\" centered at {(x, y)}!")
                    found_xs.append((x, y))

    if debug:
        dots = Grid(dot_copy(word_grid))

        all_points = []
        for x in found_xs:
            x_points, _ = get_x_points(word_grid, x, len(target) // 2 + 1)
            all_points.extend(x_points)

        masked_dots = dots.mask(points_mask(word_grid, all_points))
        print(masked_dots)

    print(f"\"{target}\" can be found {len(found_xs)} time{"" if len(found_xs) == 1 else "s"} in the shape of an \"X\".")

if __name__ == "__main__":
    main()
