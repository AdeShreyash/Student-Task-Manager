
import json
from pathlib import Path
from datetime import datetime

FILE_NAME = Path(__file__).with_name("tasks.json")


def load_tasks():
    if not FILE_NAME.exists():
        return []

    try:
        with FILE_NAME.open("r", encoding="utf-8") as file:
            saved_tasks = json.load(file)

        if isinstance(saved_tasks, list):
            return saved_tasks

        print("Saved file has an unexpected format.")

    except (json.JSONDecodeError, OSError) as error:
        print(f"Could not load saved tasks: {error}")

    return []


def save_tasks(tasks):
    try:
        with FILE_NAME.open("w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4)
    except OSError as error:
        print(f"Could not save tasks: {error}")


tasks = load_tasks()
next_id = max((task["id"] for task in tasks), default=0) + 1

while True:
    print("\n===== STUDENT TASK MANAGER =====")
    print("1. Add a task")
    print("2. View all tasks")
    print("3. Mark task as complete")
    print("4. Delete a task")
    print("5. Exit")
    print("6. Edit a task")

    choice = input("Enter your choice: ")

 
    if choice == "1":
        title = input("Enter task name: ").strip()

        if not title:
            print("Task name cannot be empty.")
            continue

        while True:
            due_date = input(
                "Enter due date (YYYY-MM-DD) or press Enter to skip: "
            ).strip()

            if not due_date:
                due_date = "Not set"
                break

            try:
                datetime.strptime(due_date, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date! Use YYYY-MM-DD format.")

        while True:
            priority = input(
                "Enter priority (High/Medium/Low): "
            ).strip().capitalize()

            if priority in ("High", "Medium", "Low"):
                break

            print("Please choose High, Medium or Low.")

        task = {
            "id": next_id,
            "title": title,
            "completed": False,
            "due_date": due_date,
            "priority": priority
        }

        tasks.append(task)
        save_tasks(tasks)

        print("Task added and saved successfully!")
        next_id += 1


    elif choice == "2":
        if not tasks:
            print("No tasks found.")
        else:
            print("\nYour Tasks:")

           
            for task in tasks:
                status = "Completed" if task["completed"] else "Pending"
                due_date = task.get("due_date", "Not set")
                priority = task.get("priority", "Medium")

                print(
                    f'{task["id"]}. {task["title"]} | '
                    f'{status} | Priority: {priority} | Due: {due_date}'
                )

    elif choice == "3":
        try:
            task_id = int(input("Enter task ID to complete: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        found = False

        for task in tasks:
            if task["id"] == task_id:
                task["completed"] = True
                found = True
                break

        if found:
            save_tasks(tasks)
            print("Task marked complete and saved!")
        else:
            print("Task ID not found.")

    elif choice == "4":
        try:
            task_id = int(input("Enter task ID to delete: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        old_count = len(tasks)
        tasks = [task for task in tasks if task["id"] != task_id]

        if len(tasks) < old_count:
            save_tasks(tasks)
            print("Task deleted and changes saved!")
        else:
            print("Task ID not found.")
            
    elif choice == "6":
        if not tasks:
            print("No tasks available to edit.")
            continue

        try:
            task_id = int(input("Enter the task ID to edit: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        selected_task = None

        for task in tasks:
            if task["id"] == task_id:
                selected_task = task
                break

        if selected_task is None:
            print("Task ID not found.")

        else:
            print("Press Enter to keep the existing value.")

            # Edit task name
            new_title = input(
                f'New task name ({selected_task["title"]}): '
            ).strip()

            if new_title:
                selected_task["title"] = new_title

            # Edit due date
            current_date = selected_task.get("due_date", "Not set")

            while True:
                new_date = input(
                    f"New due date ({current_date}) or NONE to clear: "
                ).strip()

                if not new_date:
                    break

                if new_date.lower() == "none":
                    selected_task["due_date"] = "Not set"
                    break

                try:
                    datetime.strptime(new_date, "%Y-%m-%d")
                    selected_task["due_date"] = new_date
                    break
                except ValueError:
                    print("Invalid date! Use YYYY-MM-DD.")

            # Edit priority
            current_priority = selected_task.get("priority", "Medium")

            while True:
                new_priority = input(
                    f"New priority (High/Medium/Low) ({current_priority}): "
                ).strip().capitalize()

                if not new_priority:
                    break

                if new_priority in ("High", "Medium", "Low"):
                    selected_task["priority"] = new_priority
                    break

                print("Choose High, Medium or Low.")

            save_tasks(tasks)
            print("Task updated and saved successfully!")


    elif choice == "5":
        print("Thank you for using Student Task Manager!")
        break

    else:
        print("Invalid choice. Please try again.")


