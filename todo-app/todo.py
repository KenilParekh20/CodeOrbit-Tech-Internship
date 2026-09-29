"""
Beginner-Friendly Command-Line To-Do List Application
------------------------------------------------------
A clean, modular Python script that helps you manage daily tasks.
Features:
- Add tasks, view tasks, remove tasks, and exit
- Automatic loading and saving from 'tasks.txt'
- Numbered display format
- Robust error handling (invalid numbers, empty list checks)
"""

import os

# Name of the file used to store tasks across sessions
DATA_FILE = "tasks.txt"


# ==========================================
# 1. File Handling Functions
# ==========================================

def load_tasks(filename=DATA_FILE):
    """
    Reads tasks from a text file into a Python list.
    If the file does not exist, returns an empty list.
    """
    tasks = []
    # Check if the file exists before trying to open it
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    # Strip newline characters and whitespace
                    clean_task = line.strip()
                    if clean_task:  # Only add non-empty lines
                        tasks.append(clean_task)
            print(f"[Info] Loaded {len(tasks)} task(s) from '{filename}'.")
        except Exception as e:
            print(f"[Warning] Could not load tasks from file: {e}")
    else:
        print(f"[Info] No existing '{filename}' found. Starting with a fresh list.")
    
    return tasks


def save_tasks(tasks, filename=DATA_FILE):
    """
    Writes all current tasks from the list into the text file.
    Each task is written on a new line.
    """
    try:
        with open(filename, "w", encoding="utf-8") as file:
            for task in tasks:
                file.write(f"{task}\n")
        print(f"[Success] Saved {len(tasks)} task(s) to '{filename}'.")
    except Exception as e:
        print(f"[Error] Failed to save tasks: {e}")


# ==========================================
# 2. Task Management Functions
# ==========================================

def view_tasks(tasks):
    """
    Displays the tasks in a numbered, easy-to-read list.
    Handles the case when the list is empty.
    """
    print("\n" + "=" * 40)
    print("             YOUR TO-DO LIST            ")
    print("=" * 40)

    if not tasks:
        print("  (Your to-do list is currently empty!)")
    else:
        # Enumerate gives both the 1-based index and the task string
        for index, task in enumerate(tasks, start=1):
            print(f"  {index}. {task}")

    print("=" * 40)


def add_task(tasks):
    """
    Prompts the user for a new task title and adds it to the list.
    Validates that the task is not empty.
    """
    new_task = input("\nEnter the new task description: ").strip()

    # Input validation: check for blank input
    if not new_task:
        print("  [!] Task description cannot be empty.")
        return

    tasks.append(new_task)
    print(f"  [✓] Added: \"{new_task}\"")


def remove_task(tasks):
    """
    Prompts the user for the task number to remove.
    Handles non-numeric input and out-of-bounds numbers using try/except.
    """
    # Guard clause: check if there's anything to remove
    if not tasks:
        print("\n  [!] The list is empty. Nothing to remove.")
        return

    # First show current tasks so the user knows the numbers
    view_tasks(tasks)

    user_input = input("\nEnter the task number to remove (or 'c' to cancel): ").strip()
    if user_input.lower() in ("c", "cancel"):
        print("  [Action cancelled]")
        return

    # Error handling for user input
    try:
        task_num = int(user_input)

        # Validate that the number is within 1 to len(tasks)
        if 1 <= task_num <= len(tasks):
            # Convert 1-based index to 0-based list index
            removed = tasks.pop(task_num - 1)
            print(f"  [✓] Successfully removed: \"{removed}\"")
        else:
            print(f"  [!] Invalid number: Please choose a number between 1 and {len(tasks)}.")

    except ValueError:
        # Handles cases where user enters letters or symbols
        print("  [!] Invalid input: Please enter a valid whole number.")


# ==========================================
# 3. Main Application Menu Loop
# ==========================================

def main():
    """
    Main driver function:
    - Loads tasks on startup
    - Displays interactive menu
    - Processes choices
    - Automatically saves tasks on exit
    """
    print("\n" + "*" * 45)
    print("      WELCOME TO PYTHON TO-DO LIST APP       ")
    print("*" * 45)

    # Load tasks from file at startup
    tasks = load_tasks()

    while True:
        print("\n-------- MAIN MENU --------")
        print("1. View Tasks")
        print("2. Add a Task")
        print("3. Remove a Task")
        print("4. Save & Exit")
        print("---------------------------")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            view_tasks(tasks)

        elif choice == "2":
            add_task(tasks)
            # Auto-save after adding
            save_tasks(tasks)

        elif choice == "3":
            remove_task(tasks)
            # Auto-save after removing
            save_tasks(tasks)

        elif choice == "4" or choice.lower() in ("exit", "quit", "q"):
            # Ensure latest tasks are saved before quitting
            save_tasks(tasks)
            print("\nThank you for using the To-Do List App. Goodbye!\n")
            break

        else:
            print("  [!] Invalid choice: Please enter a number from 1 to 4.")


if __name__ == "__main__":
    main()
