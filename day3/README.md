# Part 1

First, extract all `mul(\d{1,3},\d{1,3})` from `input.txt`:

```zsh
ggrep --version
# output: ggrep (GNU grep) 3.11 ...
ggrep -Eo 'mul\([1-9][0-9]{0,2},[1-9][0-9]{0,2}\)' input.txt > muls.txt
ggrep -o '[0-9]*,[0-9]*' muls.txt > muls_clean.txt
awk -F, -f program_1.awk muls_clean.txt
```

# Part 2

...
