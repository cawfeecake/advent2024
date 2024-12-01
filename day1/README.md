# Part 1

First, sanitize and sort the input:

```zsh
cat input.txt | tr -s ' ' | tr ' ' ',' > input.csv
cat input.csv | cut -f 1 -d',' | sort > input_left_sorted.txt
cat input.csv | cut -f 2 -d',' | sort > input_right_sorted.txt
paste -d ',' input_left_sorted.txt input_right_sorted.txt > input_sorted.csv
```

Then run the program:

```zsh
awk -F , -f program_1.awk input_sorted.csv
```

# Part 2

Create set from right column, and then iterate over left column to find the sum:

```zsh
awk -F , -f program_2.awk input.csv input.csv
```
