import argparse

from lib.inputs import BASE_PARSER
from lib.inputs import load_str_from_file

def main():
    parser = argparse.ArgumentParser(
            parents=[BASE_PARSER],
            description="See how many stones exist after blinking at them a given amount of time.")
    parser.add_argument("input_file", help="Path to a file that has the initial state of the stones.")
    parser.add_argument("blinks", type=int, help="The number of times you'll blink at the stones.")
    parser.add_argument("-e", "--extended", help="Do second part of the problem set", action="store_true")
    args = parser.parse_args()

    input_file = args.input_file
    #assert len(input_file) > 0, "Must provide filepath for input as the first argument"
    # TODO:
    # - how does `argparse` handle... whitespace? quotes? characters that are invalid for a file path?
    # - to be robust, should we attempt to open file and wrap in try block?

    blinks = args.blinks

    solver(input_file, blinks, args.extended, args.debug)

def get_next(stone: int) -> list[int]:
    if stone == 0:
        return [1]
    elif len((st := str(stone))) % 2 == 0:
        if len(st) >= 4300:
            print(st)
        left = st[:len(st) // 2]
        right = st[len(st) // 2:]
        return [int(left), int(right)]
    else:
        # note: `st` from walrus is in scope in this block
        return [stone * 2024]

def solver(input_file: str, blinks: int, extended: bool, debug: bool):
    stones = [int(n) for n in load_str_from_file(input_file).split(" ")]
    if debug:
        print(f"Initial stones: {stones}")

    for i in range(blinks):
        next_stones = []
        for st in stones:
            next_stones.extend(get_next(st))
        stones = next_stones

        if debug:
            print(f"Stones after {i + 1} blinks:")
            print(stones)

    print(f"Number of stones: {len(stones)}")

if __name__ == "__main__":
    main()
