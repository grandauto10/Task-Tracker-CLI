import sys
import json
import os
from datetime import datetime

TASKS_FILE = "task.json"


# -------------------------------
#     Utility Functions
# -------------------------------

def load_tasks():
    """load tasks from JSON; create file if missing."""
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "w") as f:
            json.dump([], f)
        return []

    with open(TASKS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDEcodeError:
            return []


def save_tasks(tasks):
    """save tasks to JSON file."""
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


def generate_task_id(tasks):
    """Generate a unique task ID."""
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


# ---------------------------------
#  Task Actions
# ---------------------------------

def add_task(description):
    tasks = load_tasks()
    new_task = {
        "id": generate_task_id(tasks),
        "description": description,
        "status": "todo",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added (ID: {new_task['id']})")


def list_tasks(filter_status=None):
    tasks = load_tasks()

    if filter_status:
        tasks = [t for t in tasks if t["status"] == filter_status]

    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        print(f"[{task['id']}] {task['description']} - {task['status']} (Created {task['created_at']})")


def update_task(task_id, new_description):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_description
            save_tasks(tasks)
            print("Task updated.")
            return

    print("Task not found.")


def delete_tasks(task_id):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]

    if len(new_tasks) == len(tasks):
        print("Task not found.")
        return

    save_tasks(new_tasks)
    print("Task deleted.")


def mark_status(task_id, status):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            save_tasks(tasks)
            print(f"Task marked as {status}.")
            return

    print("Task not found.")


# ---------------------------------
#   CLI Command Handler
# ---------------------------------

def print_usage():
    print("\nUsage:")
    print(" python task.py add \"task description\"")
    print(" python task.py list")
    print(" python task.py list-done")
    print(" python task.py list-todo")
    print(" python task.py list-in-progress")
    print(" python task.py update <id> \"new description\"")
    print(" python task.py delete <id>")
    print(" python task.py mark-done <id>")
    print(" python task.py mark-progress <id>")
    print()

def main():
    if len(sys.argv) < 2:
        print("Error: Missing command.")
        print_usage()
        return

    action = sys.argv[1]

    if action == "add":
        if len(sys.argv) < 3:
            print("Error: Missing task description.")
            return
        description = sys.argv[2]
        add_task(description)

    elif action == "list":
        list_tasks()

    elif action == "list-done":
        list_tasks("done")

    elif action == "list-todo":
        list_tasks("todo")

    elif action == "list-in-progress":
        list_tasks("in-progress")

    elif action == "update":
        if len(sys.argv) < 4:
            print("Error: Provide ID and new description.")
            return
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("Error: Task ID must be a number.")
            return


        new_description = sys.argv[3]
        update_task(task_id, new_description)

    elif action == "delete":
        if len(sys.argv) < 3:
            print("Error: Provide ID to delete.")
            return
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("Error: Task ID must be a number.")
            return
        delete_tasks(task_id)


    elif action == "mark-done":
        try:
            task_id = int(sys.argv[2])
        except:
            print("Error: Provide a valid numeric ID.")
            return
        mark_status(task_id, "done")

    elif action == "mark-progress":
        try:
            task_id = int(sys.argv[2])
        except:
            print("Error: Provide a valid numeric ID.")
            return
        mark_status(task_id, "in-progress")

    else:
        print("Unknown command")
        print_usage()



if __name__ == "__main__":
    main()
