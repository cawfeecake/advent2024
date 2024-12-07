import argparse

from lib.grids import Grid
from lib.directions import Direction

GUARD_REPRESENTATIONS = {
    "<": Direction.LEFT,
    "^": Direction.UP,
    ">": Direction.RIGHT,
    "v": Direction.DOWN,
}

GUARD_DIRECTIONS = {
    Direction.LEFT: "<",
    Direction.UP: "^",
    Direction.RIGHT: ">",
    Direction.DOWN: "v",
}

GUARD_TURNS = {
    Direction.LEFT: Direction.UP,
    Direction.UP: Direction.RIGHT,
    Direction.DOWN: Direction.LEFT,
    Direction.RIGHT: Direction.DOWN,
}

def get_traveled(_map: Grid, guard_start: (int, int), guard_heading: Direction, debug: bool) -> (dict[(int, int), list[Direction]], bool):
    guard_at = guard_start
    traveled = {}
    while True:
        if debug:
            print(f"Guard is at {guard_at} and heading: {guard_heading}")
            # TODO:
            # - print out _map each time masked with `traveled` (create function)
            # - (opt) have it "locked" behind 2nd level of debug
            #print(masked_map)

        if guard_at in traveled:
            traveled[guard_at].append(guard_heading)
        else:
            traveled[guard_at] = [guard_heading]

        # determine next space guard will go (i.e. look ahead)...
        next_points, next_point_in_bounds = _map.get_points(guard_at, guard_heading, 2)
        if not next_point_in_bounds:
            if debug:
                print("Guard has gone off the map!")
            return traveled, False

        next_point = next_points[-1]
        next_x, next_y = next_point

        # take action if we need to turn...
        if _map.get_value(next_x, next_y) == "#":
            guard_heading = GUARD_TURNS[guard_heading]
            if debug:
                print(f"Guard has turned and is heading: {guard_heading}")

            next_points, next_point_in_bounds = _map.get_points(guard_at, guard_heading, 2)
            if not next_point_in_bounds:
                if debug:
                    print("Guard has turned off the map!")
                return traveled, False

            next_point = next_points[-1]
            next_x, next_y = next_point

            # ... possible we hit a wall again, so will now be clear going opposite direction from where we are at now...
            if _map.get_value(next_x, next_y) == "#":
                guard_heading = GUARD_TURNS[guard_heading]
                if debug:
                    print(f"Guard has hit a wall a second time, and will now head: {guard_heading}")
            else:
                guard_at = next_point
        else:
            guard_at = next_point

        if guard_at in traveled:
            traveled_directions = traveled[guard_at]
            if debug:
                print(f"Guard has been here before traveling the direction(s): {traveled_directions}")

            if guard_heading in traveled_directions:
                if debug:
                    print(f"Guard has completed a loop!")
                return traveled, True

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

    _map, guard_start, guard_starting_heading, first_traveled_path = part_1(input_file, args.debug)
    if args.extended:
        points_to_check = list(first_traveled_path.keys())
        points_to_check.remove(guard_start)
        part_2(_map, guard_start, guard_starting_heading, points_to_check, args.debug)

def part_1(input_file: str, debug: bool) -> (Grid, (int, int), Direction, dict[(int, int), list[Direction]]):
    def open_and_parse_input():
        with open(input_file, "r") as file:
            for line in file:
                row = line.strip()  # `.strip()` removes leading and trailing whitespace
                if len(row) > 0:
                    yield row.lower()
    _map = Grid(open_and_parse_input)
    assert _map.rows > 0, "Input file must not be empty!"
    if debug:
        print(_map)

    guard_start, guard_heading = (-1, -1), (0, 0)  # both (first) invalid states for types
    is_valid_map = False
    for y in range(_map.rows):
        for x in range(_map.cols(y)):
            c = _map.get_value(x, y)
            if (c in GUARD_REPRESENTATIONS.keys()):
                guard_start = (x, y)
                guard_heading = GUARD_REPRESENTATIONS[c]
                is_valid_map = True
                break
    assert is_valid_map, "No \"guard\" ('v', '>', '<', or '^') character found on map!"

    traveled, is_loop = get_traveled(_map, guard_start, guard_heading, debug)
    # `traveled` is `dict[(int, int), list[Direction]]`
    # represents: which points were visted, and which direction the guard was going at the time

    if debug:
        def mask_func():
            for s in traveled.keys():
                yield s, "X"

        masked_map = _map.mask(mask_func)
        print(masked_map)

    is_loop_str = ""
    if is_loop:
        is_loop_str = "(looping) "
    print(f"Guard travels {len(traveled)} spaces {is_loop_str}on map in {input_file}")

    return _map, guard_start, guard_heading, traveled

def determine_loop(mask_point: (int, int), _map: Grid, guard_start: (int, int), guard_heading: Direction, debug: bool) -> bool:
    def mask_func():
        yield mask_point, "#"

    map_with_ob = _map.mask(mask_func)

    _, is_loop = get_traveled(map_with_ob, guard_start, guard_heading, debug)

    if debug and is_loop:
        print(f"Created new loop by adding obstacle ('#') at {mask_point}!")

    return is_loop

def part_2(_map: Grid, guard_start: (int, int), guard_heading: Direction, points_to_check: list[(int, int)], debug: bool) -> None:
    func_args = [(pt, _map, guard_start, guard_heading, debug) for pt in points_to_check]

    from multiprocessing import Pool

    with Pool() as pool:
        results = pool.starmap(determine_loop, func_args)
        new_loops = sum(results)

    print(f"Guard can be made to loop in {new_loops} cases")

if __name__ == "__main__":
    main()

