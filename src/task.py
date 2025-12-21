class Task:

    MAX_LEN = 255

    def __init__(self, description: str, unique_id: int = None):
        """Initializes a Task."""
        self.description = description
        self.unique_id = unique_id

    @property
    def description(self) -> str:
        """Gets the description of the Task."""
        return self._description

    @description.setter
    def description(self, description: str):
        """Sets the description of the Task. If the description is over 255
        characters or the string is empty, raises a ValueError."""

        if len(description) == 0:
            raise ValueError("Provided description is empty")
        
        if len(description) > Task.MAX_LEN:
            raise ValueError("Provided description is longer than " + MAX_LEN + " characters.")

        self._description = description

