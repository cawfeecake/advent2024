import argparse

from .grids import Grid

BASE_PARSER = argparse.ArgumentParser(add_help=False)
BASE_PARSER.add_argument("-d", "--debug", help="Print debug statements", action="store_true")

def non_empty_str(s: str) -> str:
    if not s:
        raise argparse.ArgumentTypeError("Can't be empty!")
    return s

def upper_str(s: str) -> str:
    return s.upper()

def odd_length_str(s: str) -> str:
    if len(s) % 2 == 0:
        raise argparse.ArgumentTypeError("Can't be of even length!")
    return s

# Format is 1 character in file -> 1 space in grid
# Each row of the file starts at the 0 for the x-coord.
def load_grid_from_file(input_file: str) -> Grid:
    with open(input_file, "r") as file:
        def parse_file():
            for line in file:
                row = line.strip()  # `.strip()` removes leading and trailing whitespace
                if len(row) > 0:  # ignore blank lines
                    yield row
        grid = Grid(parse_file)
    return grid

def non_empty_upper_grid(input_file: str) -> Grid:
    try:
        with open(input_file, "r") as file:
            def parse_file():
                for line in file:
                    row = line.strip()  # `.strip()` removes leading and trailing whitespace
                    if len(row) > 0:  # ignore blank lines
                        yield row.upper()
            grid = Grid(parse_file)
            if grid.rows == 0:
                raise argparse.ArgumentTypeError(f"File \"{input_file}\" can't be empty!")
            return grid

    except FileNotFoundError:
        raise argparse.ArgumentTypeError(f"File \"{input_file}\" can't be read!")
