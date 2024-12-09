import argparse

from lib.inputs import BASE_PARSER

def main():
    parser = argparse.ArgumentParser(
            parents=[BASE_PARSER],
            description="<TMP>")
    parser.add_argument("input_file")
    parser.add_argument("-e", "--extended", help="Do second part of the problem set", action="store_true")
    args = parser.parse_args()

    input_file = args.input_file
    #assert len(input_file) > 0, "Must provide filepath for input as the first argument"
    # TODO:
    # - how does `argparse` handle... whitespace? quotes? characters that are invalid for a file path?
    # - to be robust, should we attempt to open file and wrap in try block?

    # `part_1()` is when `assert not args.extended`
    # `part_2()` is when `assert args.extended`
    part_1(input_file, args.extended, args.debug)

def can_reach(goal: int, nums: list[int], extended: bool, debug: bool) -> bool:
    #assert len(nums) > 0
    active = [(nums[0], str(nums[0]), nums[1:])]
    while len(active) > 0:
        next_active = []
        for curr, curr_str, _nums in active:
            if len(_nums) == 0:
                if curr == goal:
                    if debug:
                        print(f"Can reach {goal} with {curr_str}!")
                    return True
            else:
                if curr <= goal:
                    if curr + _nums[0] <= goal:
                        next_active.append((curr + _nums[0], f"{curr_str} + {_nums[0]}", _nums[1:]))
                    if curr * _nums[0] <= goal:
                        next_active.append((curr * _nums[0], f"{curr_str} * {_nums[0]}", _nums[1:]))
                    if extended and int(f"{curr}{_nums[0]}") <= goal:
                        next_active.append((int(f"{curr}{_nums[0]}"), f"{curr_str} || {_nums[0]}", _nums[1:]))

        active = next_active
    if debug:
        print(f"No way to reach {goal} with: {nums}...")
    return False

def sum_reachable(goal: int, nums: list[int], extended: bool, debug: bool) -> int:
    if can_reach(goal, nums, extended, debug):
        return goal
    return 0

def part_1(input_file: str, extended: bool, debug: bool) -> None:
    _input = []
    # list[(int, list[int])]
    with open(input_file, "r") as file:
        for line in file:
            line = line.strip()  # `.strip()` removes leading and trailing whitespace
            if len(line) > 0:
                parts = line.split(":")
                goal = int(parts[0])
                nums = [int(n) for n in parts[1].strip().split(" ")]
                _input.append((goal, nums))
    assert len(_input) > 0, "Input file must not be empty!"

    func_args = [(goal, nums, extended, debug) for goal, nums in _input]

    from multiprocessing import Pool

    with Pool() as pool:
        results = pool.starmap(sum_reachable, func_args)
        count, s = len([i for i in results if i > 0]), sum(results)

    print(f"Was able to reach goal with {count} of the input rows for a sum of {s}")

if __name__ == "__main__":
    main()

