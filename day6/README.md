# Run

```zsh
PYTHONPATH=.. python -m main --debug input.txt
python -m day6.main --debug day6/input.txt
```

# Results

```zsh
$ time PYTHONPATH=.. python -m main input.txt
Guard travels 5409 spaces on map in input.txt
PYTHONPATH=.. python3 -m main input.txt  0.04s user 0.02s system 65% cpu 0.091 total
$ time PYTHONPATH=.. python -m main input.txt -e
Guard travels 5409 spaces on map in input.txt
Guard can be made to loop in 2022 cases
PYTHONPATH=.. python3 -m main input.txt -e  32.38s user 0.11s system 99% cpu 32.563 total
```
