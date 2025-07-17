from pathlib import Path
from rich.prompt import Prompt
# from rich.console import Console
from decorators import input_error
from notes.notes import NoteBook, Note, Title, Text
from contacts.contacts import ContactBook
import utilities

# rich_console = Console()


@input_error
def handle_note_commands(contactbook: ContactBook, notebook: NoteBook, command: str, args: list, filename: Path):
    """Command processor for handling notes"""
    match command:
        case "back":
            utilities.print_main_help_menu()
            return "back"
        case "exit":
            return "exit"
        case "add":
            title = utilities.get_validated_input("Provide title: ", Title)
            text = utilities.get_validated_input("Provide text: ", Text)
            note = Note(title, text)
            notebook.add_note(note)
        case "update":
            result = handle_update_note(notebook)
            if result == "back":
                return
            elif result == "exit":
                return "exit"
        case "delete":
            if not notebook.notes:
                utilities.rich_console.print(
                    "[bold red]No notes to delete.[/bold red]")
                return
            notebook.show_all_notes()
            id_to_delete = utilities.get_valid_id(
                "Provide ID of the note you want to delete", len(notebook.notes))
            notebook.delete_by_id(id_to_delete)
        case "all":
            notebook.show_all_notes()


def handle_update_note(notebook: NoteBook):
    if not notebook.notes:
        utilities.rich_console.print(
            "[bold red]No notes to update.[/bold red]")
        return

    notebook.show_all_notes()
    note_id = utilities.get_valid_id(
        "Provide ID of the note you want to update", len(notebook.notes))
    note_to_update = notebook.notes[note_id - 1]

    show_update_commands()

    while True:
        sub_command = Prompt.ask(
            "[blue]Enter sub-command[/blue]").strip().lower()
        match sub_command:
            case "title":
                new_title = utilities.get_validated_input(
                    "Provide new title: ", Title)
                note_to_update.title = new_title
                utilities.rich_console.print(
                    "[bold green]Title updated successfully![/bold green]")
                return "back"
            case "text":
                new_text = utilities.get_validated_input(
                    "Provide new text: ", Text)
                note_to_update.text = new_text
                utilities.rich_console.print(
                    "[bold green]Text updated successfully![/bold green]")
                return "back"
            case "back":
                return "back"
            case "exit":
                return "exit"
            case _:
                utilities.rich_console.print(
                    "[bold red]Invalid sub-command. Use 'title', 'text', or 'back'.[/bold red]")


def show_update_commands():
    table = utilities.create_help_table()
    table.add_row("title", "Update the note title")
    table.add_row("text", "Update the note text")
    table.add_row("back", "Cancel and return to the previous menu")
    utilities.rich_console.print(table)
