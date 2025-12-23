import sqlite3
from task import Task

class TaskDatabase:
    TASK_TABLE_NAME = "tasks"
    
    def __init__(self, path: str):
        self.path = path
        
    def connect(self):
        self._conn = sqlite3.connect(self.path, check_same_thread=False)
        self._cursor = self._conn.cursor()

    def disconnect(self):
        self._conn.close()

    def create_tasks_table(self):
        self._cursor.execute(f"""
            SELECT name FROM sqlite_master WHERE type='table' AND name='{self.TASK_TABLE_NAME}'""")
        
        result = self._cursor.fetchall()
        if len(result) > 0:
            return
        
        self._cursor.execute(f"""
            CREATE TABLE {self.TASK_TABLE_NAME}(description TEXT)""")

    def add_task(self, task: Task):
        self._cursor.execute(f"""
            INSERT INTO {self.TASK_TABLE_NAME} VALUES('{task.description}')""")

        self._conn.commit()

    def get_tasks(self) -> list[Task]:
        self._cursor.execute(f"""
            SELECT rowid, description FROM {self.TASK_TABLE_NAME}""")

        tasks = []
        result = self._cursor.fetchall()
        for row_id, description in result:
            tasks.append(Task(description, row_id))

        return tasks

    def get_task(self, row_id: int) -> Task:
        self._cursor.execute(f"""
            SELECT rowid, description FROM {self.TASK_TABLE_NAME} WHERE rowid == {row_id}""")

        result = self._cursor.fetchall()
        row_id, description = result[0]

        return Task(description, row_id)

if __name__ == '__main__':
    db = TaskDatabase("tasks.db")
    
    db.connect()
    db.create_tasks_table()
    tasks = db.get_tasks()
    for task in tasks:
        print(task)
    db.disconnect()

