# Running the Python

## When in the root directory

```zsh
python -m dayN.main --debug dayN/input.txt arg2 arg3
```

## When in `/dayN`

```zsh
PYTHONPATH=.. python -m main --debug input.txt arg2 arg3
```

# My Dev Notes

- `awk` would be good to know more of to bring more programming to cmdline

- Been using ChatGPT (typically GPT-4o) to create bare bones of some files, like `grids.py` (but refactored a lot)
  - Prototyped `argparse` adoption

- How do I keep each `/dayN` consistent?
