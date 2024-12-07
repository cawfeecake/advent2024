# Running the Python

## When in the root directory

```zsh
python -m dayN.main --debug dayN/input.txt arg2 arg3
```

## When in `/dayN`

```zsh
PYTHONPATH=.. python -m main --debug input.txt arg2 arg3
```

# Downloading the input

Need to go to the dev tools on browser and find the `"session"` cookie; copy value to env var: `SESSION="$(pbpaste)"`

```zsh
year="$(date +%Y)"; day="$(date +%-d)"
curl "https://adventofcode.com/$year/day/$day/input" --cookie "session=$SESSION" \
    --create-dirs -o "~/personal/advent${year}/day${day}/input.txt"
```

How can I automate for the month of Dec. downloading input, directions, test answers? Can I upload, too?

How can I program. get `"session"` cookie? Is it long-lived? Do I interact with browser?

# My Dev Notes

- `awk` would be good to know more of to bring more programming to cmdline

- Have used ChatGPT (typically GPT-4o) for help. Such as:
  - Filling out the initial methods for `grids.py` (have since refactored a lot)
  - Prototyping using "new" strategy, framework, library (e.g. adopting `argparse`)

- How do I keep contents of each (Python) file in `/dayN` consistent (across them all)?

- Need to create a test suite for all, subset of days that runs and confirms expected (from webpage, my own) output from solution code
