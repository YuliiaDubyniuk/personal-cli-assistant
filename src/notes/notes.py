from datetime import datetime
# from rich.console import Console
from contacts.contacts import Field
import utils

# rich_console = Console()


class Title(Field):
    def __init__(self, value: str):
        if not value.strip():
            raise ValueError("Title cannot be empty!")
        if len(value) > 50:
            raise ValueError("Title cannot exceed 50 characters!")
        super().__init__(value)


class Text(Field):
    def __init__(self, value: str):
        if not value.strip():
            raise ValueError("Text cannot be empty!")
        if len(value) < 10:
            raise ValueError("Text must be at least 10 characters!")
        super().__init__(value)


class Note:
    """Represents a single note and provides methods to manage its data"""

    def __init__(self, title: Title, text: Text):
        self.title = title
        self.date = datetime.today().strftime("%d %B %Y")
        self.text = text

    def __str__(self):
        # Create the table for a single note
        table = utils.create_table(title="Note Details")
        table.add_column("Field", no_wrap=True)
        table.add_column("Value")

        table.add_row("Title", self.title.value)
        table.add_row("Date", self.date)
        table.add_row("Text", self.text.value)

        with utils.rich_console.capture() as capture:
            utils.rich_console.print(table)
        return capture.get()


class NoteBook:
    """Manages a collection of notes"""

    def __init__(self):
        self.notes: list[Note] = []

    def add_note(self, note: Note):
        self.notes.append(note)
        utils.rich_console.print(
            f"[bold green]Note '{note.title}' added successfully.[/bold green]")

    def show_all_notes(self):
        if not self.notes:
            utils.rich_console.print("[bold red]No notes found.[/bold red]")
            return

        table = utils.create_table("All Notes")
        table.add_column("ID", justify="center", no_wrap=True)
        table.add_column("Title", justify="left", no_wrap=True)
        table.add_column("Date", justify="center", no_wrap=True)
        table.add_column("Text", justify="left")

        for i, note in enumerate(self.notes, start=1):
            formatted_text = note.text.value.replace(", ", "\n")
            table.add_row(
                str(i),
                note.title.value,
                note.date,
                formatted_text
            )

        utils.rich_console.print(table)

    def delete_by_id(self, note_id: int):
        removed_note = self.notes.pop(note_id - 1)
        utils.rich_console.print(
            f"[bold green]Note '{removed_note.title}' deleted successfully.[/bold green]")

    def find_note_by_id(self):
        note_id = utils.get_valid_id(
            "Provide ID of the note you want to update", len(self.notes))
        return self.notes[note_id - 1]
