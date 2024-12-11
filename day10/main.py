import argparse

from lib.directions import Direction
from lib.grids import Grid
from lib.inputs import BASE_PARSER
from lib.inputs import load_grid_from_file

def main():
    parser = argparse.ArgumentParser(
            parents=[BASE_PARSER],
            description="Count the sum of the number of peaks the trailheads can reach on the given map.")
    parser.add_argument("input_file", help="Path to a file that ...")
    parser.add_argument("-e", "--extended", help="Do second part of the problem set", action="store_true")
    args = parser.parse_args()

    input_file = args.input_file
    #assert len(input_file) > 0, "Must provide filepath for input as the first argument"
    # TODO:
    # - how does `argparse` handle... whitespace? quotes? characters that are invalid for a file path?
    # - to be robust, should we attempt to open file and wrap in try block?

    solver(input_file, args.extended, args.debug)

def get_trailheads(grid: Grid):
    trailheads = []

    def _reduce(pt: (int, int), value: str, acc: set[(int, int)]):
        if value == "0":
            acc.add(pt)
        return acc

    return grid.reduce(_reduce, set())

def get_peak_paths(grid: Grid, trailhead: (int, int), debug: bool):
    possible_paths = [[(0, trailhead)]]  # list[list[(int, (int, int))]]
    paths = []

    while len(possible_paths) > 0:
        if debug:
            print(f"Current paths being considered ({len(possible_paths)}): {possible_paths}")
        path = possible_paths.pop()
        curr_elevation, curr_pt = path[-1]
        if curr_elevation == 9:  # at peak
            paths.append(path)
        else:
            for d in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
                adjacent, is_in_bounds = grid.get_points(curr_pt, d, 2)
                if is_in_bounds:
                    next_pt = adjacent[-1]
                    next_x, next_y = next_pt
                    if int(grid.get_value(next_x, next_y)) == (next_elevation := curr_elevation + 1):
                        path_copy = list(path)
                        path_copy.append((next_elevation, next_pt))
                        possible_paths.append(path_copy)

    return paths

def solver(input_file: str, extended: bool, debug: bool):
    input_grid = load_grid_from_file(input_file)

    trailheads = get_trailheads(input_grid)
    if debug:
        print(f"Number of trailheads: {len(trailheads)}")
        print(f"Trailheads: {trailheads}")

    total_value = 0
    if extended:
        value_str = "Ratings"
    else:
        value_str = "Score"
    for t in trailheads:
        peak_paths = get_peak_paths(input_grid, t, debug)
        if debug:
            print(f"[{t}]:\n    {peak_paths}")

        if extended:
            value = len(peak_paths)
        else:
            value = len(set([p[-1] for p in peak_paths]))
        if debug:
            print(f"{value_str} for {t}: {value}")
        total_value += value

    print(f"Total {value_str.lower()} for the map: {total_value}")

if __name__ == "__main__":
    main()
