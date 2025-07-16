from datetime import datetime


class Field:
    """Base class to represent a note field with a value."""

    def __init__(self, field_name: str):
        self.name: str = field_name
        self.value: str = self.set_value()

    def __str__(self) -> str:
        return self.value

    def set_value(self) -> str:
        while True:
            val = input(f"Provide {self.name}: ").strip()
            if val:
                return val
            print(f"{self.name.capitalize()} field cannot be empty!")


class Note:
    """Represents a single note and provides methods to manage its data"""

    def __init__(self):
        self.title = Field("title").value
        self.date = datetime.today().date()
        self.text = Field("text").value

    def __str__(self):
        pass


class NoteBook:
    """Manages a collection of notes"""

    def __init__(self):
        self.notes: list[Note] = []

    def add_note(self, note: Note):
        self.notes.append(note)
        print(f"Note '{note.title}' added successfully.")
