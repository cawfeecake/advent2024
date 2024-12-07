import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("-e", "--extended", help="Do both parts of the problem set (defaults to doing just the first", action="store_true")
    parser.add_argument("-d", "--debug", help="Print debug statements", action="store_true")
    args = parser.parse_args()

    input_file = args.input_file
    #assert len(input_file) > 0, "Must provide filepath for input as the first argument"
    # TODO:
    # - how does `argparse` handle... whitespace? quotes? characters that are invalid for a file path?
    # - to be robust, should we attempt to open file and wrap in try block?

    struct = part_1(input_file, args.debug)
    if args.extended:
        part_2(struct, args.debug)

def can_reach(goal: int, nums: list[int], debug: bool) -> bool:
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

        active = next_active
    if debug:
        print(f"No way to reach {goal} with: {nums}...")
    return False

def part_1(input_file: str, debug: bool) -> any:
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

    count, s = 0, 0
    for goal, nums in _input:
        if can_reach(goal, nums, debug):
            count += 1
            s += goal
            
    print(f"Was able to reach goal with {count} of the input rows for a sum of {s}")
    return None

def part_2(struct: any, debug: bool) -> None:
    pass

if __name__ == "__main__":
    main()

