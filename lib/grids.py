from typing import Callable, Generator, Optional, Type

from .directions import Direction

class Grid:
    def __init__(self, row_generator: Callable[[], Generator[list[any], None, None]]):
        self.grid = []

        for row in row_generator():
            self.grid.append(row)

        self.rows = len(self.grid)

    # care: will error if `assert y >= self.rows`
    def cols(self, y: int) -> int:
        return len(self.grid[y])

    # care: will error if `assert y >= self.rows` or `assert x >= self.grid[y]
    def get_value(self, x: int, y: int) -> any:
        return self.grid[y][x]

    def __str__(self):
        rows = []
        for y in range(self.rows):
            row = []
            for x in range(self.cols(y)):
                row.append(str(self.get_value(x, y)))
            rows.append("".join(row))
        return "\n".join(rows)

    # care: will error if the rows of `self.grid` don't support assignment (e.g. if they are strings)
    # care: will error if `assert y >= self.rows` or `assert x >= self.grid[y]
    def set_value(self, x: int, y: int, value: any) -> None:
        self.grid[y][x] = value

    def is_in_bounds(self, x: int, y: int) -> bool:
        return 0 <= y < self.rows and 0 <= x < self.cols(y)

    def get_points(self, start: (int, int), direction: Direction, length: int) -> (list[(int, int)], bool):
        x, y = start
        dx, dy = direction.value

        points = []
        for i in range(length):
            if not self.is_in_bounds(x, y):
                break
            points.append((x, y))
            x, y = x + dx, y + dy

        return points, len(points) == length

    def get_values(self, start: (int, int), direction: Direction, length: int) -> (list[any], bool):
        points, fits  = self.get_points(start, direction, length)
        return [self.get_value(x, y) for x, y in points], fits

    def mask(self, masks: Callable[[], Generator[list[((int, int), any)], None, None]]) -> "Grid":
        def copy_grid():
            for y in range(self.rows):
                row = []
                for x in range(self.cols(y)):
                    row.append(self.get_value(x, y))
                yield row
        masked_copy = Grid(copy_grid)

        # note: algo. works best if the size of result from `for ... in masks()` is less than or near in size to `self.grid`
        for masked_point in masks():
            point, mask = masked_point
            x, y = point
            masked_copy.set_value(x, y, mask)

        return masked_copy

