# Run

```zsh
PYTHONPATH=.. python -m main --debug input.txt
python -m day7.main --debug day7/input.txt
```

# Results

## Before parallel

```zsh
$ time PYTHONPATH=.. python -m main input.txt -e
Was able to reach goal with 636 of the input rows for a sum of 105517128211543
PYTHONPATH=.. python3 -m main input.txt -e  7.31s user 0.31s system 99% cpu 7.637 total
```

## After parallel

```zsh
```
