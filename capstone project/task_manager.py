# ===== Importing external modules ===========
from datetime import datetime
import os
'''This is the section where you will import modules'''

# ==== Login Section ====
# TODO: Implement the following functionality


# Add a user as a admin
def reg_user(current_user, credentials):
    if current_user != "admin":
        print("Only Admin Access")
        return

    new_username = input("Enter new user: ")
    if not new_username:
        print("Username cannot be empty")
        return
    if new_username in credentials:
        print("username already taken")
        return

    new_password = input("Please enter a password: ")
    confirm_password = input("Confirm password: ")
    if new_password != confirm_password:
        print("Passwords dont match")
        return

    with open("user.txt", "a") as user_file:
        user_file.write(f"{new_username}, {new_password}\n")

    credentials[new_username] = new_password
    print("New user registered")

def add_task(credentials, task_file_path="task.txt"):
    user_assigned = input("who is assigned to this task").strip()
    if user_assigned not in credentials:
        print("User not found")
        return

    title = input("What is title for the task: ")
    description = input("What is description for task: ")
    due_date = input("When is this due: ").strip()

    assigned_date = datetime.today().strftime("%d %b %Y")

    with open (task_file_path, "a") as task_file:
        task_file.write(f"{user_assigned}, {title}, {description}, {assigned_date}, {due_date}, No\n")

    print("Task added!")


def view_all(task_file_path="task.txt"):
    try:
        with open(task_file_path, "r") as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("not tasks found")
        return

    if not lines:
        print("no tasks to show")
        return

    for line in lines:
        parts = line.split(", ")
        if len(parts) < 6:
            print("skipping malformed task line", line)
            continue
        assigned_user, task_title, task_description, assigned_date, due_date, completed = parts[:6]
        print("--------------")
        print(assigned_user)
        print(f"Task:\t {task_title}")
        print(f"Date assigned:\t {assigned_date}")
        print(f"Due date:\t {due_date}")
        print(f"Task complete?\t {completed}")
        print(f"Task description:\n {task_description}")
        print()


def calculate_task_statistics(task_file_path="task.txt"):
    total_tasks = 0
    completed_tasks = 0
    uncompleted_tasks = 0
    overdue_tasks = 0

    try:
        with open(task_file_path, "r") as task_file:
            for line in task_file:
                line = line.strip()
                if not line:
                    continue

                parts = line.split(", ")
                if len(parts) < 6:
                    continue

                total_tasks += 1
                completed = parts[5]
                due_date_str = parts[4]

                if completed.lower() == "yes":
                    completed_tasks += 1
                else:
                    uncompleted_tasks += 1

                    try:
                        due_date = datetime.strptime(due_date_str, "%d %b %Y")
                        today = datetime.today()
                        if due_date < today:
                            overdue_tasks += 1
                    except ValueError:
                        pass
    except FileNotFoundError:
        return None

    if total_tasks > 0:
        incomplete_percentage = (uncompleted_tasks / total_tasks) * 100
        overdue_percentage = (overdue_tasks / total_tasks) * 100
    else:
        incomplete_percentage = 0
        overdue_percentage = 0

    return {
        "total": total_tasks,
        "completed": completed_tasks,
        "uncompleted": uncompleted_tasks,
        "overdue": overdue_tasks,
        "incomplete_percentage": incomplete_percentage,
        "overdue_percentage": overdue_percentage
    }

def generate_task_overview(task_file_path="task.txt", report_file="task_overview.txt"):

    stats = calculate_task_statistics(task_file_path)

    if stats is None:
        print("no tasks file found")
        return

    try:
        with open(report_file, "w") as report:
            report.write("="*60 + "\n")
            report.write("TASK OVERVIEW REPORT\n")
            report.write("="*60 + "\n\n")

            report.write(f"Total Number of Tasks: {stats['total']}\n")
            report.write(f"Total completed Tasks: {stats['completed']}\n")
            report.write(f"Total Uncompleted Tasks: {stats['uncompleted']}\n")
            report.write(f"Total Overdue Tasks: {stats['overdue']}\n\n")

            report.write(f"Percentage Incomplete: {stats['incomplete_percentage']:.2f}%\n")
            report.write(f"Percentage Overdue: {stats['overdue_percentage']:.2f}%\n")

            report.write("\n" + "="*60 + "\n")

            print(f"Task overview report generated: {report_file}")

    except IOError:
        print("Error creating report file")



def calculate_user_statistics(task_file_path="task.txt", users_file="user.txt"):
    user_stats = {}

    #load users
    try:
        with open(users_file, "r") as user_file:
            for line in user_file:
                line = line.strip()
                if not line:
                    continue
                username, _ = line.split(", ")
                user_stats[username] = {
                    "total": 0,
                    "completed": 0,
                    "uncompleted": 0,
                    "overdue": 0
                }
    except FileNotFoundError:
        return {}

    #count tasks for each user
    try:
        with open(task_file_path, "r") as task_file:
            for line in task_file:
                line = line.strip()
                if not line:
                    continue

                parts = line.split(", ")
                if len(parts) < 6:
                    continue

                assigned_user = parts[0]
                completed = parts[5]

                if assigned_user not in user_stats:
                    continue

                user_stats[assigned_user]["total"] += 1

                if completed.lower() == "yes":
                    user_stats[assigned_user]["completed"] += 1
                else:
                    user_stats[assigned_user]["uncompleted"] += 1
                    due_date_str = parts[4]
                    try:
                        due_date = datetime.strptime(due_date_str, "%d %b %Y")
                        today = datetime.today()
                        if due_date < today:
                            user_stats[assigned_user]["overdue"] += 1
                    except ValueError:
                     pass
    except FileNotFoundError:
        return {}

    return user_stats

def generate_user_overview(task_file_path="task.txt", users_file="user.txt", report_file="user_overview.txt"):
    user_stats = calculate_user_statistics(task_file_path, users_file)

    if not user_stats:
        print("No user statistics available")
        return

    total_users = len(user_stats)
    total_tasks = sum(stats['total'] for stats in user_stats.values())

    try:
        with open(report_file, "w") as report:
            report.write("+" * 60 + "\n")
            report.write("USER OVERVIEW REPORT\n")
            report.write("=" * 60 + "\n\n")

            report.write(f"Total Number of users: {total_users}\n")
            report.write(f"Total number of Tasks: {total_tasks}\n\n")

            for username, stats in user_stats.items():
                report.write(f"Username: {username}\n")
                report.write(f"Total Tasks Assigned: {stats['total']}\n")
             

                if total_tasks > 0:
                    pct_of_total = (stats['total'] / total_tasks) * 100
                else:
                    pct_of_total = 0

                report.write(f"percentage of Total Tasks: {pct_of_total :.2f}%\n")

                if stats['total'] > 0:
                    pct_completed = (stats['completed'] / stats['total']) * 100
                    pct_uncompleted = (stats['uncompleted'] / stats['total']) * 100
                    pct_overdue = (stats['overdue'] / stats['total']) * 100
                else:
                    pct_completed = 0
                    pct_uncompleted = 0
                    pct_overdue = 0

                report.write(f"Percentage of Tasks Completed: {pct_completed:.2f}%\n")
                report.write(f"Percentage of Tasks Pending: {pct_uncompleted:.2f}%\n")
                report.write(f"Percentage of Tasks Overdue: {pct_overdue:.2f}%\n\n")

            report.write("+" * 60 + "\n")

        print(f"user overview report generared: {report_file}")

    except IOError:
        print("Error creating user overview report")

def display_statistics():
    files_to_check = ["task_overview.txt", "user_overview.txt"]

    for file_name in files_to_check:
        if not os.path.exists(file_name):
            generate_user_overview()
            generate_task_overview()
            break

    for file_name in files_to_check:
        print(f"\n--- {file_name} ---")
        try:
            with open(file_name, "r") as file:
                for line in file:
                    print(line.strip())
        except FileNotFoundError:
            print(f"{file_name} not found")


def view_my_tasks(username, task_file_path="task.txt"):

    my_tasks = []

    try:
        with open(task_file_path, "r") as task_file:
            for line in task_file:
                line = line.strip()
                if not line:
                    continue

                parts = line.split(", ")
                if len(parts) < 6:
                    continue

                assigned_user = parts[0]

                if assigned_user == username:
                    my_tasks.append(parts)

    except FileNotFoundError:
        print("No tasks file found")
        return

    if not my_tasks:
        print("You have no tasks assigned to you")
        return

    print(f"You have {len(my_tasks)} task(s)")

    for i, task in enumerate(my_tasks, 1):
        task_title = task[1]
        due_date = task[4]
        completed = task[5]
        print(f"{i}, {task_title} (Due: {due_date}) - {completed}")

    print()

    while True:
        try:
            selection = input(f"select a task (1-{len(my_tasks)}) or -1 to return to menu").strip()
            task_num = int(selection)

            if task_num == -1:
                return


            if task_num < 1 or task > len(my_tasks):
                print(f"Invalid selection. Please enter a number between 1 and {len(my_tasks)}), or -1 to return.")
                continue

            break

        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

    selected_task = my_tasks[task_num - 1]

    assigned_user = selected_task[0]
    task_title = selected_task[1]
    task_description = selected_task[2]
    assigned_date = selected_task[3]
    due_date = selected_task[4]
    completed = selected_task[5]

    print("\n" + "="*50)
    print("TASK DETAILS")
    print("="*50)
    print(f"Assigned to: {assigned_user}")
    print(f"Title: {task_title}")
    print(f"Description: {task_description}")
    print(f"Date Assigned: {assigned_date}")
    print(f"Due Date: {due_date}")
    print(f"Completed: {completed}")
    print("="*50 + "\n")

    while True:
        task_action = input("\nWhat would you like to do?\nm - mark task as complete\ne -Edit task\nb - Back to task list\n: ").lower().strip()

        if task_action == 'b':
            return

        elif task_action == 'm':

            if completed.lower() == "yes":
                print("This task is already marked as complete.")
            else:
                selected_task[5] = "Yes"
                completed = "Yes"
                print("Task marked as complete!")

        elif task_action == 'e':
            if completed.lower() =="yes":
                print("Cannot edit a completed task.")
            else:
                edit_task(selected_task, my_tasks, task_file_path)
                return
        else:
            print("Invalid input. Please enter 'm', 'e', or 'b'.")

        if task_action == 'm':
            continue_action = input("\nWould you like to do anything else? (y/n): ")
            if continue_action != 'y':
                save_tasks(my_tasks, task_file_path)
                return


def edit_task(selected_task, my_tasks, task_file_path):
    print("\nWhat would you like to edit?")
    print("u - Edit assigned user")
    print("d - Edit due date")
    print("b - back")

    edit_choice = input(": ").lower().strip()

    if edit_choice == 'u':
        new_user = input("Enter new username: ").strip()
        if not new_user:
            print("Username cannot be empty")
            return
        selected_task[0] = new_user
        print("User updated")

    elif edit_choice == 'd':
        new_due_date = input("Enter new due date: ")
        if not new_due_date:
            print("Due date cannot be empty")
            return
        selected_task[4] = new_due_date
        print("Due date updated!")

    elif edit_choice == "b":
        return

    else:
        print("Invalid input")
        return

def save_tasks(my_tasks, task_file_path):

    try:
        with open(task_file_path, "w") as task_file:
            for task in my_tasks:
                task_line = ", ".join(task)
                task_file.write(task_line + "\n")
        print("Changes saved!")
    except IOError:
        print("Error saving tasks")

credentials = {}
with open("user.txt", "r") as user_file:
    for line in user_file:
        line = line.strip()
        if not line:
            continue # skip empty lines
        username, password = line.split(", ")
        credentials[username] = password

while True:
    username = input("Enter username: ")
    if username not in credentials:
        print("Invalid username, please try again.")
        continue

    password = input("Enter password: ")
    if password != credentials[username]:
        print("Invalid password, please try again.")
        continue

    print("Login successful!")
    break



while True:
    # Present the menu to the user and
    # make sure that the user input is converted to lower case.
    if username == "admin":
        menu = input(
        '''Select one of the following options:
    r - register a user
    a - add task
    va - view all tasks
    vm - view my tasks
    e - exit
    vc - view completed tasks
    del - delete tasks
    ds - display statistics
    gr - generate reports
    : '''
    ).lower()
    else:
        menu = input('''Select one of the following options:
    a - add task
    va - view all tasks
    vm - view my tasks
    e - exit
    : ''').lower()

        # This code block will add a new user to the user.txt file

    if menu == 'r':
       reg_user(username, credentials)


        # '''This code block will allow a user to add a new task to task.txt file


    elif menu == 'a':
        add_task(credentials)
      
        
    elif menu == 'va':
       view_all()
      
    elif menu == 'vm':
        view_my_tasks(username)

    elif menu =='gr':
        generate_task_overview()
        generate_user_overview()

    elif menu == 'ds':
        display_statistics()

    elif menu == "vc":
        if username != "admin":
            print("only admin has acces")
            continue
        with open("task.txt", "r") as task_file:
            found = False
            for line in task_file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(", ")
                assigned_user = parts[0]
                task_title = parts[1]
                task_description = parts[2]
                assigned_date = parts[3]
                due_date = parts[4]
                completed = parts[5]
                if completed.lower() == "yes":
                    found = True
                    print("----------------------")
                    print(f"{assigned_user}")
                    print(f"Task:\t {task_title}")
                    print(f"Date assigned:\t {assigned_date} ")
                    print(f"Due date:\t {due_date}")
                    print(f"Task comeplete?\f {completed}")
                    print(f"Task description:\n {task_description}")
                    print()
                if not found:
                    print("No completed tasks to show")
    elif menu == "del":
        if username != "admin":
            print("Admin only access")
            continue
        task_to_delete = input("Enter the title of the task you want to delete: ")
        with open("task.txt", "r") as task_file:
            tasks = [line for line in task_file if line.strip()]

        new_tasks = []
        deleted = False
        for line in tasks:
            parts = line.strip().split(", ")
            task_title = parts[1]
            if task_title.lower() == task_to_delete.lower():
                deleted = True
                continue
            new_tasks.append(line)

        if deleted:
            with open("task.txt", "w") as task_file:
                for task_line in new_tasks:
                    task_file.write(task_line + "\n")
                    print("Task deleted")
        else:
            print("Task not found.")

        

                    



        '''This code block will read the task from task.txt file and
         print to the console in the format of Output 2 presented in the PDF
         You can do it in this way:
            - Read a line from the file
            - Split the line where there is comma and space.
            - Check if the username of the person logged in is the same as the 
              username you have read from the file.
            - If they are the same you print the task in the format of Output 2
              shown in the PDF '''
        pass  # Remove this once you implement the functionality

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have entered an invalid input. Please try again")