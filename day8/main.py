import argparse
from itertools import combinations

from lib.grids import Grid
from lib.inputs import BASE_PARSER
from lib.inputs import load_grid_from_file

def main():
    parser = argparse.ArgumentParser(
            parents=[BASE_PARSER],
            description="Print the number of \"antinodes\" being produced on the input map")
    parser.add_argument("input_file", help="Path to a file that maps out the antenna")
    parser.add_argument("-e", "--extended", help="Do both parts of the problem set (defaults to doing just the first", action="store_true")
    args = parser.parse_args()

    input_file = args.input_file
    #assert len(input_file) > 0, "Must provide filepath for input as the first argument"
    # TODO:
    # - how does `argparse` handle... whitespace? quotes? characters that are invalid for a file path?
    # - to be robust, should we attempt to open file and wrap in try block?

    solver(input_file, args.extended, args.debug)

# TODO move to own class, make Movement module for this and Direction, other methods for moving in 2D space
type Point = type[tuple[int, int]]
# TODO move to `lib/grids.py`
type GridItemLocations = dict[str, list[Point]]

def get_antenna(pt: (int, int), value: str, acc: GridItemLocations) -> GridItemLocations:
    if value != ".":
        if value in acc:
            others = acc[value]
            others.append(pt)
        else:
            acc[value] = [pt]
    return acc

def get_antinodes(grid: Grid, allAntennas: GridItemLocations) -> set[Point]:
    nodes = set()
    for _, locations in allAntennas.items():
        for pair in combinations(locations, 2):
            # first, find delta between pair...
            a, b = pair
            a_x, a_y = a
            b_x, b_y = b
            d_x, d_y = b_x - a_x, b_y - a_y
            # next, test the first possible antinode location which is a _negative_ delta behind `a`...
            first_x, first_y = a_x - d_x, a_y - d_y
            if grid.is_in_bounds(first_x, first_y):
                nodes.add((first_x, first_y))
            # and then test the second antinode which is a delta ahead of `b`...
            second_x, second_y = b_x + d_x, b_y + d_y
            if grid.is_in_bounds(second_x, second_y):
                nodes.add((second_x, second_y))

    return nodes

def get_antinodes_resonant(grid: Grid, allAntennas: GridItemLocations) -> set[Point]:
    nodes = set()
    for _, locations in allAntennas.items():
        for pair in combinations(locations, 2):
            # first, find delta between pair...
            a, b = pair
            a_x, a_y = a
            b_x, b_y = b
            d_x, d_y = b_x - a_x, b_y - a_y
            # next, get each antinode a delta ahead of `a`...
            test_x, test_y = a_x + d_x, a_y + d_y
            while grid.is_in_bounds(test_x, test_y):
                nodes.add((test_x, test_y))
                test_x, test_y = test_x + d_x, test_y + d_y
            # then, do the same going a _negative_ delta ahead of `b`...
            test_x, test_y = b_x - d_x, b_y - d_y
            while grid.is_in_bounds(test_x, test_y):
                nodes.add((test_x, test_y))
                test_x, test_y = test_x - d_x, test_y - d_y

    return nodes

def solver(input_file: str, extended: bool, debug: bool):
    grid = load_grid_from_file(input_file)
    if debug:
        print(grid)

    antenna = grid.reduce(get_antenna, {})
    if debug:
        print(f"Unique antennas ({len(antenna)}):\n{list(antenna.keys())}")
        print("Antenna locations:", "\n".join([f"- '{a}' ({len(ls)}): {ls}" for a, ls in antenna.items()]), sep="\n")

    if extended:
        nodes = get_antinodes_resonant(grid, antenna)
    else:
        nodes = get_antinodes(grid, antenna)
    if debug:
        print("All \"antinodes\":", list(nodes))

    print(f"Number of \"antinodes\": {len(nodes)}")

if __name__ == "__main__":
    main()
