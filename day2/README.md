# Part 1

## `input.txt` Notes

1. No line has less than 5 values

   <details>
   <summary>Verifying regex...</summary>

   `^\d\+ \d\+ \d\+ \d\+ \d\+$` resulted in first match after iterating thru lesser amounts of `\d\+`
   </details>


```zsh
awk -f program_1.awk input.txt
```

# Part 2

```zsh
awk -f program_2.awk input.txt
# for debug output:
awk -f program_2_debug.awk input.txt
```

## `awk` Learnings

Variables are global, so make sure variable names don't clash if doing for loops in function and outer scopes.
