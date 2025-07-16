from pathlib import Path
from decorators import input_error
from notes.notes import NoteBook, Note
from contacts.contacts import ContactBook
import utilities


@input_error
def handle_note_commands(contactbook: ContactBook, notebook: NoteBook, command: str, args: list, filename: Path):
    """Command processor for handling notes"""
    match command:
        case "back":
            utilities.print_main_help_menu()
            return "back"
        case "exit":
            return utilities.exit_assistant(contactbook, notebook, filename)
        case "add-note":
            note = Note()
            notebook.add_note(note)
