import os
import sys

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

def main():
    # TODO use day5 parsing strategy
    input_file = sys.argv[1]
    assert len(input_file) > 0, "Must provide input's filepath as the first argument"

    _as_debug = False
    try:
        _as_debug = os.environ["DEBUG"] == "1"
    except:
        pass

    def open_and_parse_input():
        with open(input_file, "r") as file:
            for line in file:
                row = line.strip()  # `.strip()` removes leading and trailing whitespace
                if len(row) > 0:
                    yield row.lower()
    _map = Grid(open_and_parse_input)
    assert _map.rows > 0, "Input file must not be empty"
    if _as_debug:
        print(_map)

    guard_at, guard_travel_dir = (-1, -1), (0, 0)  # both (first) invalid states for types
    guard_on_map = False
    for y in range(_map.rows):
        row = _map.grid[y]
        for x in range(len(row)):
            c = _map.get_value(x, y)
            if (c in GUARD_REPRESENTATIONS.keys()):
                guard_at = (x, y)
                guard_travel_dir = GUARD_REPRESENTATIONS[c]
                guard_on_map = True
                break
    assert guard_on_map, "No \"guard\" ('v', '>', '<', or '^') found within input file"

    # spaces_traveled needs to be a map of points to directions traveling so we can tell when to stop
    # and then to get all points traveled, it's `keys()`
    spaces_traveled = {}
    while True:
        if _as_debug:
            print(f"Guard is at {guard_at} and heading: {guard_travel_dir}")
            # TODO:
            # - print out _map each time masked with `spaces_traveled` (create function)
            # - (opt) have it "locked" behind 2nd level of debug
            #print(masked_map)

        if guard_at in spaces_traveled:
            spaces_traveled[guard_at].append(guard_travel_dir)
        else:
            spaces_traveled[guard_at] = [guard_travel_dir]

        # determine next space for guard by looking ahead...
        up_ahead_pts, guard_on_map = _map.get_points(guard_at, guard_travel_dir, 2)
        if not guard_on_map:
            if _as_debug:
                print("Guard has gone off the map!")
            break

        up_ahead = up_ahead_pts[-1]
        up_ahead_x, up_ahead_y = up_ahead

        # take action if we need to turn...
        if _map.get_value(up_ahead_x, up_ahead_y) == "#":
            guard_travel_dir = GUARD_TURNS[guard_travel_dir]
            if _as_debug:
                print(f"Guard has turned and is heading: {guard_travel_dir}")

            up_ahead_pts, guard_on_map = _map.get_points(guard_at, guard_travel_dir, 2)
            if not guard_on_map:
                if _as_debug:
                    print("Guard has turned off the map!")
                break

            up_ahead = up_ahead_pts[-1]
            up_ahead_x, up_ahead_y = up_ahead

            # ... possible we hit a wall again, so will now be clear going opposite direction from where we are at now...
            if _map.get_value(up_ahead_x, up_ahead_y) == "#":
                guard_travel_dir = GUARD_TURNS[guard_travel_dir]
                if _as_debug:
                    print(f"Guard has hit a wall a second time, and will now head: {guard_travel_dir}")
            else:
                guard_at = up_ahead
        else:
            guard_at = up_ahead

        if guard_at in spaces_traveled:
            traveled_directions = spaces_traveled[guard_at]
            if _as_debug:
                print(f"Guard has been here before traveling the direction(s): {traveled_directions}")
            if guard_travel_dir in traveled_directions:
                if _as_debug:
                    print(f"Guard has completed a loop!")
                break

    if _as_debug:
        def _mask_func():
            for s in spaces_traveled.keys():
                yield s, "X"

        masked_map = _map.mask(_mask_func)
        print(masked_map)

    print(f"Guard travels {len(spaces_traveled)} spaces on map in {input_file}")

if __name__ == "__main__":
    main()

