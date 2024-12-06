from typing import Callable, Generator, Optional

from .directions import Direction

class Grid:
    def __init__(self, row_generator: Callable[[], Generator[list[any], None, None]]):
        self.grid = []

        for row in row_generator():
            self.grid.append(row)

        self.rows = len(self.grid)

    def __str__(self):
        return f"Grid(rows={self.rows})"

    def __repr__(self):
        rows = []
        for y in range(self.rows):
            row = []
            for x in range(len(self.grid[y])):
                row.append(str(self.grid[y][x]))
            rows.append(f"[ {", ".join(row)} ]")
        return "\n".join(rows)

    def _is_in_bounds(self, x: int, y: int):
        return 0 <= y < self.rows and 0 <= x < len(self.grid[y])

    # usage note: doesn't work if the underlying rows don't support assignment
    def set_value(self, x: int, y: int, value: any) -> None:
        if self._is_in_bounds(x, y):
            self.grid[y][x] = value

    def _get_value(self, x: int, y: int) -> any:
        return self.grid[y][x]

    def get_value(self, x: int, y: int) -> Optional[any]:
        if self._is_in_bounds(x, y):
            return self._get_value(x, y)

    def get_points(self, start: (int, int), direction: Direction, length: int) -> (list[(int, int)], bool):
        x, y = start
        dx, dy = direction.value

        points = []
        fits = self._is_in_bounds(x, y)
        for _ in range(length):
            if not self._is_in_bounds(x, y):
                completed = False
                break
            points.append((x, y))
            x, y = x + dx, y + dy

        return points, fits

    def get_values(self, start: (int, int), direction: Direction, length: int) -> (list[any], bool):
        points, fits  = self.get_points(start, direction, length)
        return [self._get_value(x, y) for x, y in points], fits

    # usage note: this won't work if row of Grid are str (as they don't support assignment at an index)
    def mask(self, mask_generator: Callable[[], Generator[list[((int, int), any)], None, None]]) -> None:
        # this algo. works best if the size of `mask_generator` is less than or equal to the total size of `self.grid`
        for mask in mask_generator():
            point, value = mask
            x, y = point
            if self._is_in_bounds(x, y):
                self.set_value(x, y, value)

