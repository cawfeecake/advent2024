# Part 1

First, extract all `mul(\d{1,3},\d{1,3})` from `input.txt`, and then format it for `awk`

<details>
<summary>`ggrep --version`</summary>

`ggrep (GNU grep) 3.11 ...`
</details>

```zsh
ggrep --version
ggrep -Eo 'mul\([1-9][0-9]{0,2},[1-9][0-9]{0,2}\)' input.txt > muls.txt
ggrep -o '[0-9]*,[0-9]*' muls.txt > muls_clean.txt

awk -F, -f program_1.awk muls_clean.txt
```

# Part 2

Expand extraction to include control functions, and then use the order of their appearance to control flags in `awk`

```zsh
ggrep -Eo '(mul\([1-9][0-9]{0,2},[1-9][0-9]{0,2}\)|do\(\)|don'"'"'t\(\))' input.txt > muls_and_control.txt
ggrep -Eo '([0-9]*,[0-9]*|d.*)' muls_and_control.txt > muls_and_control_clean.txt

awk -F, -f program_2.awk muls_and_control_clean.txt
```
