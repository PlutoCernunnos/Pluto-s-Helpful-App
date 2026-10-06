import secrets
import string
from Common import *

def run():
    while True:
        clear_screen()
        header("Password Generator")
        length = input(f"{White}Length (Enter for 16, q to go back): {Reset}").strip().lower()
        if length == 'q':
            break
        if length == '':
            length = '16'
        if not length.isdigit() or not 4 <= int(length) <= 128:
            print(f"{Red}Pick a number from 4 to 128.{Reset}")
            pause()
            continue

        use_symbols = input(f"{White}Include symbols? (y/n): {Reset}").lower() != 'n'
        chars = string.ascii_letters + string.digits
        if use_symbols:
            chars += "!@#$%^&*-_=+?"

        print(f"\n{Yellow}Here are 5 options:{Reset}")
        for _ in range(5):
            password = ''.join(secrets.choice(chars) for _ in range(int(length)))
            print(f"{Green}{password}{Reset}")
        pause()