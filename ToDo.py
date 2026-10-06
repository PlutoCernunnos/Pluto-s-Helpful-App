import os
import json
from Common import *

todo_file = 'todo.json'

def load_tasks():
    if os.path.exists(todo_file):
        with open(todo_file, 'r') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(todo_file, 'w') as f:
        json.dump(tasks, f, indent=2)

def show_tasks(tasks):
    if not tasks:
        print(f"{White}No tasks yet.{Reset}")
    for i, task in enumerate(tasks, start=1):
        mark = f"{Green}[x]" if task['done'] else f"{White}[ ]"
        print(f"{mark} {i}. {task['text']}{Reset}")

def pick_task(tasks, prompt):
    choice = input(f"{White}{prompt}{Reset}").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(tasks):
        return int(choice) - 1
    print(f"{Red}Not a valid task number.{Reset}")
    pause()
    return None

def run():
    tasks = load_tasks()
    while True:
        clear_screen()
        header("To-Do List")
        show_tasks(tasks)
        print(f"\n{White}1. Add  2. Check/uncheck  3. Delete  4. Clear finished  5. Back{Reset}")
        choice = input(f"{Yellow}Choose: {Reset}")

        if choice == '1':
            text = input(f"{White}Task: {Reset}").strip()
            if text:
                tasks.append({"text": text, "done": False})
                save_tasks(tasks)
        elif choice == '2':
            i = pick_task(tasks, "Which number? ")
            if i is not None:
                tasks[i]['done'] = not tasks[i]['done']
                save_tasks(tasks)
        elif choice == '3':
            i = pick_task(tasks, "Delete which number? ")
            if i is not None:
                tasks.pop(i)
                save_tasks(tasks)
        elif choice == '4':
            tasks = [t for t in tasks if not t['done']]
            save_tasks(tasks)
        elif choice == '5':
            break