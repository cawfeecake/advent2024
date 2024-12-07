import argparse

def non_empty_str(s: str) -> str:
    if not s:
        raise argparse.ArgumentTypeError("Can't be empty!")
    return s
