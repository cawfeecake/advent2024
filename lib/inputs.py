import argparse

from .grids import Grid

def non_empty_str(s: str) -> str:
    if not s:
        raise argparse.ArgumentTypeError("Can't be empty!")
    return s

def non_empty_upper_str(s: str) -> str:
    return non_empty_str(s).upper()

def non_empty_upper_grid(input_file: str) -> Grid:
    try:
        with open(input_file, "r") as file:
            def parse_input():
                for line in file:
                    row = line.strip()  # `.strip()` removes leading and trailing whitespace
                    if len(row) > 0:
                        yield row.upper()
            grid = Grid(parse_input)
            if grid.rows == 0:
                raise argparse.ArgumentTypeError(f"File \"{input_file}\" can't be empty!")
            return grid

    except FileNotFoundError:
        raise argparse.ArgumentTypeError(f"File \"{input_file}\" can't be read!")
