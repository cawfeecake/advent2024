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

def strip_leading_zeros(s: str) -> str:
    result = s.lstrip("0")
    if len(result) > 0:
        return result
    return "0"

def get_next(stone: str) -> list[str]:
    if stone == "0":
        return ["1"]
    elif len(stone) % 2 == 0:
        left = stone[:len(stone) // 2]
        right = strip_leading_zeros(stone[len(stone) // 2:])
        return [left, right]
    else:
        # [THIS IS AN OLD...] NOTE: `st` from walrus above is in scope here
        return [f"{int(stone) * 2024}"]

def solver(input_file: str, blinks: int, extended: bool, debug: bool):
    stones = [n for n in load_str_from_file(input_file).split(" ")]
    if debug:
        print(f"Starting stone configuration {len(stones)}:")
        print(stones)

    if extended:
        # order of stones isn't preserved, but that isn't significant to get an answer

        stone_counter = {st: 1 for st in stones}
        for i in range(blinks):
            next_stone_counter = {}
            for st, count in stone_counter.items():
                next_stones = get_next(st)
                for next_st in next_stones:
                    if next_st in next_stone_counter:
                        next_stone_counter[next_st] = next_stone_counter[next_st] + count
                    else:
                        next_stone_counter[next_st] = count
            stone_counter = next_stone_counter

            if debug:
                print(f"[Blink {i + 1}] Number of stones: {sum([count for _, count in stone_counter.items()])}", end="")
                print(f"; Number of unique stones: {len(stone_counter)}", end="")
                print(f"; '0' count: {stone_counter['0'] if '0' in stone_counter else 0}", end="")
                print(f"; '1' count: {stone_counter['1'] if '1' in stone_counter else 0}")

        count = sum([count for _, count in stone_counter.items()])
    else:
        for i in range(blinks):
            next_stones = []
            for st in stones:
                next_stones.extend(get_next(st))
            stones = next_stones

            if debug:
                print(f"[Blink {i + 1}] Stones:")
                print(stones)

        count = len(stones)
    
    print(f"Total number of stones after {blinks} blinks: {count}")

if __name__ == "__main__":
    main()
