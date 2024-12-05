import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input_file")
parser.add_argument("-e", "--extend", help="Do extended problem set", action="store_true")
parser.add_argument("-d", "--debug", help="Print DEBUG messages", action="store_true")
args = parser.parse_args()

_as_debug = args.debug
_do_extended = args.extend

input_file = args.input_file
#assert len(input_file) > 0, "Missing 1st argument: path to input file"
## assumes no need to trim whitespace, escape characters

must_come_before_map = {}
# {int -> set()}
# associates set of nums that key would need to ensure comes
# before (i.e. these nums can't appear before key)
updates_to_check = []
# list[list[int]]

with open(input_file, "r") as file:
    parsing_first_section = True
    for line in file:
        clean_line = line.strip()  # `.strip()` removes leading and trailing whitespace
        if clean_line == "":
            # finished parsing first section; moving to 2nd section...
            parsing_first_section = False
            continue

        if parsing_first_section:
            superior, inferior = clean_line.split("|")
            if superior in must_come_before_map:
                must_come_before_map[superior].add(inferior)
            else:
                new_set = set()
                new_set.add(inferior)
                must_come_before_map[superior] = new_set
        else:
            updates_to_check.append(clean_line.split(","))

assert len(updates_to_check) > 0, "Input file must contain updates to check"

def is_valid_update(update: list[int], must_come_before_map: dict[int, set[int]]) -> tuple[bool, tuple[int, set[int]]]:
    seen = set()
    for i, n in enumerate(update):
        if n in must_come_before_map:  # opt. could check if in `seen` if repeat numbers happen often
            must_come_before = must_come_before_map[n]
            if (conflicts := seen.intersection(must_come_before)):
                if _as_debug:
                    print(f"Update {update} is INVALID due to {n} (at {i}) coming after: {conflicts}")
                return False, (i, conflicts)
        seen.add(n)
    if _as_debug:
        print(f"Update {update} is valid!")
    return True, ()

valid, s = 0, 0
invalid_updates = []
for update in updates_to_check:
    is_valid, conflict = is_valid_update(update, must_come_before_map)
    if is_valid:
        valid += 1
        s += int(update[len(update) // 2])
    else:
        invalid_updates.append((update, conflict))

if _as_debug:
    print("Rules:")
    rules = 0
    for superior, inferiors in must_come_before_map.items():
        print(f"{superior} must come before: {sorted(inferiors)}")
        rules += len(inferiors)
    print(f"Total rules: {rules}")
    print(f"Number of \"n\" with rules: {len(must_come_before_map)}")
print(f"Valid updates: {valid} of {len(updates_to_check)} total")
print(f"Sum of middle value of each valid update: {s}")

if _do_extended:
    def attempt_fix_update(update: list[int], conflict: tuple[int, set[int]]) -> None:
        i_to_move, comes_before = conflict
        #assert(0 < i_to_move < len(update))
        insert_at = 0
        while insert_at < i_to_move:
            if update[insert_at] in comes_before:
                to_move = update[i_to_move]
                update.insert(insert_at, to_move)
                update.pop(i_to_move + 1)
                return
            insert_at += 1
        # should not happen b/c the assumption is that there is an element that exists in `update`
        # at an index of 0 up until `i_to_move` that will insert the element at `i_to_move` before
        raise Exception("Was not able to modify the update at all.") 
    
    invalid_s = 0
    for update, conflict in invalid_updates:
        is_valid = False
        while not is_valid:  # TODO: could there be input that makes this an infinite loop?
            attempt_fix_update(update, conflict)
            is_valid, conflict = is_valid_update(update, must_come_before_map)
    
        invalid_s += int(update[len(update) // 2])
    
    print(f"Sum of middle value of each fixed invalid update: {invalid_s}")
