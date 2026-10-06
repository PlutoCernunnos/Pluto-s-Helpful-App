import os
import shutil
import string
from Common import *

def get_drives():
    return [f"{letter}:\\" for letter in string.ascii_uppercase
            if os.path.exists(f"{letter}:\\")]

def run():
    clear_screen()
    header("Disk Space")
    bar_width = 30
    for drive in get_drives():
        try:
            usage = shutil.disk_usage(drive)
        except OSError:
            continue  # empty card reader, disconnected drive, etc.
        percent = usage.used / usage.total * 100
        filled = int(percent / 100 * bar_width)
        color = Green if percent < 70 else Yellow if percent < 90 else Red
        bar = '█' * filled + '░' * (bar_width - filled)
        print(f"{White}{drive} {color}{bar}{Reset} {percent:.0f}%  "
              f"{White}{format_size(usage.free)} free of {format_size(usage.total)}{Reset}")
    pause()