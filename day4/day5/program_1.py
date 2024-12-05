import sys

input_file = sys.argv[1]
assert len(input_file) > 0, "Missing 1st argument: path to input file"
# assumes no need to trim whitespace, escape characters

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

def is_valid_update(update: list[int], must_come_before_map: dict[int, set[int]]) -> bool:
    seen = set()
    for n in update:
        if n in must_come_before_map:  # opt. could check if in `seen` if repeat numbers happen often
            must_come_before = must_come_before_map[n]
            if (conflicts := seen.intersection(must_come_before)):
                print(f"Conflict! {n} needed to come before one of these: {must_come_before}")
                return False
        seen.add(n)
    return True

valid, s = 0, 0
for update in updates_to_check:
    if is_valid_update(update, must_come_before_map):
        print(f"{update} is valid!")
        valid += 1
        s += int(update[len(update) // 2])
    else:
        print(f"{update} is NOT valid :(")

print(f"There are {valid} valid updates")
print(f"The middle value sum is: {s}")
