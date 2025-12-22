from task import Task
from db import TaskDatabase

if __name__ == '__main__':
    task_0 = Task("pick up dry cleaning")
    task_1 = Task("brush my teeth", 10)

    # Failure expected
    try:
        task_2 = Task("X" * 256)
    except:
        print("Unable to create task 2")

    # Failure expected
    try:
        task_3 = Task("")
    except:
        print("Unable to create task 3")

    # Create database
    db = TaskDatabase("tasks.db")
    db.connect()
    db.create_tasks_table()
    db.add_task(task_0)
    db.add_task(Task("finish coding this app"))

    tasks = db.get_tasks()
    task = db.get_task(1)

    print(tasks)
    print(task)

    db.disconnect()

