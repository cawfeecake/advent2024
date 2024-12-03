# Part 1

1. Extract valid data from `input.txt`: matches `mul(\d{1,3},\d{1,3})`

<details>
<summary><code>ggrep --version</code></summary>

`ggrep (GNU grep) 3.11 ...`
</details>

```zsh
ggrep -Eo 'mul\([1-9][0-9]{0,2},[1-9][0-9]{0,2}\)' input.txt > muls.txt
```

2. Format it for `awk` by removing `mul(`, `)`

```zsh
ggrep -o '[0-9]*,[0-9]*' muls.txt > muls_clean.txt
```

Run the program to multiply values

```zsh
awk -F, -f program_1.awk muls_clean.txt
```

# Part 2

1. Expand match criteria to extract control function calls. Then replicate previous formatting step to allow for control calls.

```zsh
ggrep -Eo '(mul\([1-9][0-9]{0,2},[1-9][0-9]{0,2}\)|do\(\)|don'"'"'t\(\))' input.txt > muls_and_controls.txt
ggrep -Eo '([0-9]*,[0-9]*|d.*)' muls_and_controls.txt > muls_and_controls_clean.txt
```

Run the program to multiply values (while ignoring others)

```zsh
awk -F, -f program_2.awk muls_and_controls_clean.txt
```
