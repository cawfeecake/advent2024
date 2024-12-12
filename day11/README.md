# Run

```zsh
PYTHONPATH=.. python -m main --debug input.txt
python -m day11.main --debug day11/input.txt
```

# Results

When executing the program without `-e`, it replicates the problem's conditions and brute forces the answer.
This works well when you want to output the actual list of stone, and it easily handles at least 50 iterations.

When executing the program with `-e`, it exploits a fact within the problem that none of the stones have an affect on other stones
during iterations, and as a result our answer will be independent of any ordering.
Therefore, we can treat all stones of the same value as the same, and use a map counter to easily get our final answer for 75
iterations.

<details>
<summary>It can even handle 1000 iteration easily!:</summary>

```zsh
time PYTHONPATH=.. python -m main input.txt 1000 -e
Number of stones: 195600701690076850506000341546007405317984064264180150537846487742106157720613395733924680344941675297722819823169120518420204713984264303445633744692064448821639245739172704861933334
PYTHONPATH=.. python3 -m main input.txt 1000 -e  2.44s user 0.03s system 95% cpu 2.574 total
```

# Old

<details>
<summary>There were some testing results I got when still trying to use the brute force solution for part 2:</summary>

Wasn't able to do 75 iterations with first impl. since it hangs.

## First attempt with keeping stones as `int`

```zsh
time PYTHONPATH=.. python -m main input.txt 35
Number of stones: 12833134
PYTHONPATH=.. python3 -m main input.txt 35  10.26s user 0.52s system 95% cpu 11.281 total
```

Multiprocess:

```zsh
time PYTHONPATH=.. python -m main input.txt -e 35
Number of stones: 12833134
PYTHONPATH=.. python3 -m main input.txt -e 35  9.63s user 0.49s system 95% cpu 10.627 total
```

## After keeping stones as `str`

```zsh
time PYTHONPATH=.. python -m main input.txt 35
Number of stones: 12833134
PYTHONPATH=.. python3 -m main input.txt 35  9.51s user 0.91s system 92% cpu 11.302 total

Multiprocess:

```zsh
time PYTHONPATH=.. python -m main input.txt -e 35
Number of stones: 12833134
PYTHONPATH=.. python3 -m main input.txt -e 35  20.17s user 1.94s system 371% cpu 5.954 total
```
</details>
