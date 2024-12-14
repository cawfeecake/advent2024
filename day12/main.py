import argparse

from lib.directions import Direction
from lib.inputs import BASE_PARSER
from lib.inputs import load_grid_from_file

def main():
    parser = argparse.ArgumentParser(
            parents=[BASE_PARSER],
            description="X")
    parser.add_argument("input_file", help="Path to a file that Y.")
    parser.add_argument("-e", "--extended", help="Do second part of the problem set", action="store_true")
    args = parser.parse_args()

    input_file = args.input_file
    #assert len(input_file) > 0, "Must provide filepath for input as the first argument"
    # TODO:
    # - how does `argparse` handle... whitespace? quotes? characters that are invalid for a file path?
    # - to be robust, should we attempt to open file and wrap in try block?

    solver(input_file, args.extended, args.debug)

def get_bulk_perimeter(perimeter_plots: list[((int, int), Direction)], debug: bool) -> int:
    if debug:
        print(f"perimeter_plots: {[(e[0], e[1].name) for e in perimeter_plots]}")

    perimeter = 0
    for d in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
        plots_with_fence_in_direction = [e[0] for e in perimeter_plots if e[1] == d]
        if d in [Direction.UP, Direction.DOWN]:
            plots_with_fence_in_direction.sort(key=lambda e: (e[1], e[0]))  # keeps locations on same Y together
        else:  # d in [Direction.LEFT, Direction.RIGHT]:
            plots_with_fence_in_direction.sort(key=lambda e: (e[0], e[1]))  # keeps locations on same X together

        if debug:
            print(f"[{d.name}] {[e for e in plots_with_fence_in_direction]}")

        curr_x, curr_y = plots_with_fence_in_direction.pop(0)
        curr_perimeter = 1
        for next_x, next_y in plots_with_fence_in_direction:
            if d in [Direction.UP, Direction.DOWN]:
                if next_y != curr_y or next_x != curr_x + 1:
                    # only add if point isn't on same row (`next_y == curr_y`) or isn't only 1 away on X-axis
                    curr_perimeter += 1
                    if debug:
                        print(f"[{d.name}] Was at {(curr_x, curr_y)}, checked that {(next_x, next_y)} was not adjacent")
            else:  # d in [Direction.LEFT, Direction.RIGHT]:
                if next_x != curr_x or next_y != curr_y + 1:
                    # only add if point isn't on same column (`next_x == curr_x`) or isn't only 1 away on Y-axis
                    curr_perimeter += 1
                    if debug:
                        print(f"[{d.name}] Was at {(curr_x, curr_y)}, checked that {(next_x, next_y)} was not adjacent")

            curr_x, curr_y = next_x, next_y

        if debug:
            print(f"Added {curr_perimeter} from {d.name}")

        perimeter += curr_perimeter

    return perimeter

def solver(input_file: str, extended: bool, debug: bool):
    map_grid = load_grid_from_file(input_file)

    def collect_plants(pt: (int, int), plant: str, plants: dict[(int, int), str]) -> dict[(int, int), str]:
        plants[pt] = plant
        return plants
    all_plants = map_grid.reduce(collect_plants, {})

    unvisited_plots = set(all_plants.keys())  # for O(1) remove; `set()` will not reduce size of list from `.keys()`

    if debug:
        print(f"Starting unvisited count ({len(unvisited_plots)}): {unvisited_plots}")

    all_plots = []
    while len(unvisited_plots) > 0:
        plant_start_x, plant_start_y = unvisited_plots.pop()
        plant = map_grid.get_value(plant_start_x, plant_start_y)
        if debug:
            print(f"Working on {plant}'s plot...")

        plots_to_check = [(plant_start_x, plant_start_y)]
        curr_area = 0
        if extended:
            perimeter_plots = []
        else:
            curr_perimeter = 0
        while len(plots_to_check) > 0:
            curr = plots_to_check.pop()
            curr_area += 1
            for d in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
                next_plot, exists = map_grid.get_points(curr, d, 2)
                if exists:
                    next_plot = next_plot[-1]  # unwrap by getting last element
                    next_x, next_y = next_plot
                    if (next_plot_plant := map_grid.get_value(next_x, next_y)) == plant and next_plot in unvisited_plots:
                        plots_to_check.append(next_plot)
                        unvisited_plots.remove(next_plot)
                    elif next_plot_plant != plant:  # at an edge of a different plot
                        if debug:
                            print(f"[{plant}] At edge of another plot map!", end="")
                            print(f" Due {d.name} from {curr} there is {next_plot_plant}", end="")

                        if extended:
                            perimeter_plots.append((curr, d))
                            if debug:
                                print(f"; added plot to set of perimeter plots, and now have {len(perimeter_plots)}")
                        else:
                            curr_perimeter += 1
                            if debug:
                                print(f"; now perimiter of {curr_perimeter}")

                else:  # at an edge of the map
                    if debug:
                        print(f"[{plant}] At edge of map!", end="")
                        print(f" Due {d.name} from {curr}", end="")

                    if extended:
                        perimeter_plots.append((curr, d))
                        if debug:
                            print(f"; added plot to set of perimeter plots, and now have {len(perimeter_plots)}")
                    else:
                        curr_perimeter += 1
                        if debug:
                            print(f"; now perimiter of {curr_perimeter}")

        if extended:
            # transform `perimeter_plots` list into `curr_perimeter` equiv.
            curr_perimeter = get_bulk_perimeter(perimeter_plots, debug)

        all_plots.append((plant, (plant_start_x, plant_start_y), curr_area, curr_perimeter))

    if debug:
        print(f"All plots: {all_plots}")

    total_price = sum([a * p for (_, _, a, p) in all_plots])

    print(f"Total price: {total_price}")

if __name__ == "__main__":
    main()
