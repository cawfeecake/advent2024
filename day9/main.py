import argparse

from bisect import bisect_left, insort_left

from lib.inputs import BASE_PARSER
from lib.inputs import load_str_from_file

def parse_simple_disk(disk_str: str) -> list[int]:
    is_file, next_file_id, disk = True, 0, []
    for c in disk_str:
        file_id = -1  # repr. no file
        if is_file:
            file_id = next_file_id
            next_file_id += 1
        disk.extend([file_id] * int(c))
        is_file = not is_file
    return disk

# modifies `disk`
def full_compact(disk: list[int]) -> None:
    front_ptr, end_ptr = 0, len(disk) - 1
    while end_ptr > front_ptr:
        if disk[front_ptr] >= 0:
            front_ptr += 1
        elif disk[end_ptr] < 0:
            end_ptr -= 1
        else:
            disk[front_ptr] = disk[end_ptr]
            disk[end_ptr] = -1
            front_ptr, end_ptr = front_ptr + 1, end_ptr - 1

def full_compact_disk_checksum(disk: list[int]) -> int:
    i, s = 0, 0
    while disk[i] >= 0:
        i, s = i + 1, s + disk[i] * i
    return s

type DiskUsedSpace = list[(int, int, int)]
# a list of: files, in order, formatted as (id, start, len)

type DiskFreeSpace = dict[int, list[int]]
# a map of: sizes of free blocks -> a list of indices of where a free block of that capacity exists (ascending)

def parse_complex_disk(disk_str: str) -> (DiskUsedSpace, DiskFreeSpace):
    used_space, free_space = [], {}

    is_file = True
    next_file_id = 0
    disk_i = 0
    for c in disk_str:
        block_len = int(c)
        if is_file:
            used_space.append((next_file_id, disk_i, block_len))
            next_file_id += 1
        elif block_len > 0:
            if block_len in free_space:
                free_space[block_len].append(disk_i)
            else:
                free_space[block_len] = [disk_i]

        disk_i += block_len
        is_file = not is_file

    return (used_space, free_space)

# modifies `used_space`, `free_space`; will make `used_space` no longer "in order" from left to right
def file_safe_compact(used_space: DiskUsedSpace, free_space: DiskFreeSpace) -> None:
    # TODO examine all but first file block b/c to get a better conditional there needs to be a better handling object(s)
    for i in reversed(range(1, len(used_space))):
        move_id, move_start, move_len = used_space[i]
        #print(f"{used_space[i]}")

        # look at the available `free_space` lengths and locations to see if `used_space[i]` can be moved to the left
        available_lens = sorted([l for l in free_space.keys() if l >= move_len])
        if (available_lens_i := bisect_left(available_lens, move_len)) < len(available_lens):
            available_free_spaces = []
            for l in available_lens[available_lens_i:]:
                if bisect_left(free_space[l], move_start) > 0:
                    available_free_spaces.append((free_space[l][0], l))

            if len(available_free_spaces) > 0:
                # sort by indices to get the available space most to the left
                chosen_i, chosen_len = sorted(available_free_spaces)[0]

                # next, update the used block in `used_space` to reflect it being moved (to the start of the free block)
                used_space[i] = (move_id, chosen_i, move_len)

                # finally, update `free_space` to remove filled block...
                chosen_free_space_len_indices = free_space[chosen_len]
                if len(chosen_free_space_len_indices) > 1:
                    chosen_free_space_len_indices.pop(0)  # if able to add to a capacity, we added to most left index
                else:
                    del free_space[chosen_len]

                # ... then add any remaining portion of the free block back
                remaining_len = chosen_len - move_len
                if remaining_len > 0:
                    remaining_i = chosen_i + move_len
                    if remaining_len in free_space:
                        insort_left(free_space[remaining_len], remaining_i)
                    else:
                        free_space[remaining_len] = [remaining_i]

def file_safe_disk_checksum(disk: DiskUsedSpace) -> int:
    s = 0
    for file_block in disk:
        file_id, file_start, file_len = file_block
        s += file_id * sum(range(file_start, file_start + file_len))
    return s

def main():
    parser = argparse.ArgumentParser(
            parents=[BASE_PARSER],
            description="")
    parser.add_argument("input_file", help="Path to a file that ...")
    parser.add_argument("-e", "--extended", help="Do second part of the problem set", action="store_true")
    args = parser.parse_args()

    input_file = args.input_file
    #assert len(input_file) > 0, "Must provide filepath for input as the first argument"
    # TODO:
    # - how does `argparse` handle... whitespace? quotes? characters that are invalid for a file path?
    # - to be robust, should we attempt to open file and wrap in try block?

    solver(input_file, args.extended, args.debug)

def solver(input_file: str, extended: bool, debug: bool):
    input_str = load_str_from_file(input_file)

    if extended:
        disk_used, disk_free = parse_complex_disk(input_str)
        if debug:
            print("Complex disk before compact:")
            print(f"Used: {disk_used[:min(100, len(disk_used))]}")
            print(f"Free: {'{'}{', '.join([f'{l}: {ls[:min(100, len(ls))]}' for l, ls in disk_free.items()])}{'}'}")

        file_safe_compact(disk_used, disk_free)
        if debug:
            print("Complex disk after compact:")
            print(f"Used: {disk_used[:min(100, len(disk_used))]}")
            print(f"Free: {'{'}{', '.join([f'{l}: {ls[:min(100, len(ls))]}' for l, ls in disk_free.items()])}{'}'}")

        s = file_safe_disk_checksum(disk_used)
    else:
        disk = parse_simple_disk(input_str)
        if debug:
            print(f"Size of disk: {len(disk)}")
            print("Disk before compact:")
            print(f"Head: {disk[:min(100, (len(disk) + 1) // 2)]}")
            print(f"Tail: {disk[-(min(100, len(disk) // 2)):]}")

        full_compact(disk)
        if debug:
            print(f"Disk after compact:")
            print(f"Head: {disk[:min(100, (len(disk) + 1) // 2)]}")
            print(f"Tail: {disk[-(min(100, len(disk) // 2)):]}")

        s = full_compact_disk_checksum(disk)

    print(f"Disk checksum: {s}")

if __name__ == "__main__":
    main()
