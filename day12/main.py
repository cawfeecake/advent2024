import argparse

from collections import Counter

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

def solver(input_file: str, extended: bool, debug: bool):
    map_grid = load_grid_from_file(input_file)

    #if extended:
    #    pass

    def collect_plants(pt: (int, int), plant: str, plants: dict[(int, int), str]) -> dict[(int, int), str]:
        plants[pt] = plant
        return plants
    all_plants = map_grid.reduce(collect_plants, {})

    plant_counts = Counter([pl for _, pl in all_plants.items()])

    if debug:
        print(f"All plants in input ({len(plant_counts)}): {plant_counts}")

    unvisited_plots = set(all_plants.keys()) # for O(1) remove; `set()` will not reduce size of list from `.keys()`

    if debug:
        print(f"Starting unvisited count ({len(unvisited_plots)}): {unvisited_plots}")

    all_plots = []
    while len(unvisited_plots) > 0:
        plant_start_x, plant_start_y = unvisited_plots.pop()
        plant = map_grid.get_value(plant_start_x, plant_start_y)
        if debug:
            print(f"Working on {plant}'s plot...")

        plots_to_check = [(plant_start_x, plant_start_y)]
        curr_area, curr_perim = 0, 0
        while len(plots_to_check) > 0:
            curr_x, curr_y = plots_to_check.pop()
            curr_area += 1
            for d in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
                next_plot, exists = map_grid.get_points((curr_x, curr_y), d, 2)
                if exists:
                    next_plot = next_plot[-1]  # unwrap from `(curr_x, curr_y)`
                    next_x, next_y = next_plot
                    if (next_plot_plant := map_grid.get_value(next_x, next_y)) == plant and next_plot in unvisited_plots:
                        plots_to_check.append(next_plot)
                        unvisited_plots.remove(next_plot)
                    elif next_plot_plant != plant:  # at an edge of a different plot
                        curr_perim += 1
                        if debug:
                            print(f"[{plant}] At edge of another plot map!", end="")
                            print(f"(Due {d.name} from {(curr_x, curr_y)} there is {next_plot_plant}); now {curr_perim}")
                else:  # at an edge of the map
                    curr_perim += 1
                    if debug:
                        print(f"[{plant}] At edge of map!", end="")
                        print(f"(Due {d.name} from {(curr_x, curr_y)}); now {curr_perim}")

        all_plots.append((plant, (plant_start_x, plant_start_y), curr_area, curr_perim))

    if debug:
        print(f"All plots: {all_plots}")

    total_price = sum([a * p for (_, _, a, p) in all_plots])

    print(f"Total price: {total_price}")

if __name__ == "__main__":
    main()
