import os
import hashlib
from Common import *
from organizer import move_to_recycle_bin

def file_hash(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def run():
    clear_screen()
    header("Duplicate Finder")
    start = ask_folder(os.path.join(os.path.expanduser('~'), 'Downloads'))
    if not start:
        pause()
        return

    print(f"{White}Scanning...{Reset}")
    # Step 1: group by size (fast). Files with different sizes can't match.
    by_size = {}
    for root, dirs, names in os.walk(start):
        for name in names:
            path = os.path.join(root, name)
            try:
                size = os.path.getsize(path)
            except OSError:
                continue
            if size > 0:
                by_size.setdefault(size, []).append(path)

    # Step 2: only hash files that share a size (slow, so we do less of it)
    by_hash = {}
    for size, paths in by_size.items():
        if len(paths) < 2:
            continue
        for path in paths:
            try:
                by_hash.setdefault((size, file_hash(path)), []).append(path)
            except OSError:
                pass

    groups = [(size, paths) for (size, _), paths in by_hash.items() if len(paths) > 1]
    if not groups:
        print(f"{Green}No duplicates found!{Reset}")
        pause()
        return

    wasted = sum(size * (len(paths) - 1) for size, paths in groups)
    print(f"{Yellow}Found {len(groups)} sets of duplicates, wasting {format_size(wasted)}.{Reset}")

    for g, (size, paths) in enumerate(groups, start=1):
        print(f"\n{Yellow}Set {g}/{len(groups)} ({format_size(size)} each){Reset}")
        for i, path in enumerate(paths, start=1):
            print(f"{White}{i}. {path}{Reset}")
        choice = input(f"{Yellow}Keep which number? (Enter = skip, q = stop): {Reset}").strip().lower()
        if choice == 'q':
            break
        if choice.isdigit() and 1 <= int(choice) <= len(paths):
            keep = paths[int(choice) - 1]
            for path in paths:
                if path != keep:
                    try:
                        move_to_recycle_bin(path)
                        print(f"{Red}Recycled {path}{Reset}")
                    except OSError as error:
                        print(f"{Red}{error}{Reset}")
    pause()