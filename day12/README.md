# Run

```zsh
PYTHONPATH=.. python -m main --debug input.txt
python -m day12.main --debug day12/input.txt
```

# Notes

## Part 1

Each plot only needs to be visited once to record the area and to determine if there are any fences to be put up
around it. When each plot is visited, each of the 4 directions around it are check to determine if the adjacent plot is:
- the same plant
- a different plant
- the edge of the grid

A unit of fence is recorded for the last 2 cases. In the 1st case, that plot is visited next after recording that the
current one has been visited. This continues until all connecting plots of the same plant have been visited. After that,
a random, unvisited plot is chosen and the process repeated.

## Part 2

We do the same thing as above, but instead of counting the fences needed, we record the location of each plot that
will need a fence. After we have completed the above process, we will iterate through each group of plots and check
each row and column 1 at a time to see how many contiguous plots in that row or column require a fence on the same side
of the plot. Each unbroken sequence of plots is counted as a single face for that group.
