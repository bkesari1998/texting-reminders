from task import Task

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
