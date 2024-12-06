```sh
python program.py input.txt --debug | tee /tmp/prog_out
grep INVALID /tmp/prog_out > /tmp/prog_out_invalid
# see all that failed due to single conflict
grep "{'[0-9]*'}" /tmp/prog_out_invalid
# ... for _n_ multiple conflicts
grep "{'[0-9]*', '[0-9]*', '[0-9]*'}" /tmp/prog_out_invalid
```
