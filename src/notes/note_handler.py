from pathlib import Path
from rich.prompt import Prompt
from decorators import input_error
from notes.notes import NoteBook, Note, Title, Text, Tag
from contacts.contacts import ContactBook
import utilities


@input_error
def handle_note_commands(notebook: NoteBook, command: str, args: list):
    """Command processor for handling notes"""
    match command:
        case "help":
            utilities.print_notes_help_menu()
        case "back":
            return "back"
        case "exit":
            return "exit"
        case "add":
            title = utilities.get_validated_input("Enter title", Title)
            tags = utilities.get_validated_input(
                "Enter tag(s) separated by [bold orange1]';'[/bold orange1] (or press Enter to skip)", Tag)
            text = utilities.get_validated_input("Enter text", Text)
            note = Note(title, text, tags)
            notebook.add_note(note)
        case "update":
            result = handle_update_note(notebook)
            # if result == "back":
            #     return
            if result == "exit":
                return "exit"
        case "delete":
            if not notebook.notes:
                utilities.rich_console.print(
                    "[bold red]No notes to delete.[/bold red]")
                return
            show_notes_list(notebook.notes, "All Notes")
            id_to_delete = utilities.get_valid_id(
                "Enter the note [bold orange1]ID[/bold orange1] to delete (press [bold orange1]Enter[/bold orange1] to cancel)", len(notebook.notes))
            if id_to_delete == 0:
                return
            notebook.delete_by_id(id_to_delete)
        case "find":
            if not args:
                utilities.rich_console.print(
                    "[bold red]Search phrase is required.[/bold red]")
                return
            matches = notebook.find_by_keyword(args)
            if matches:
                show_notes_list(matches, f"Matched notes")
            else:
                utilities.rich_console.print(
                    "[bold red]No matched note found.[/bold red]")
                return
        case "all":
            show_notes_list(notebook.notes, "All Notes")


def handle_update_note(notebook: NoteBook):
    if not notebook.notes:
        utilities.rich_console.print(
            "[bold red]No notes to update![/bold red]")
        return

    show_notes_list(notebook.notes, "All Notes")
    note_id = utilities.get_valid_id(
        "Enter the note [bold orange1]ID[/bold orange1] to update (press [bold orange1]Enter[/bold orange1] to cancel)", len(notebook.notes))
    if note_id == 0:
        return
    note_to_update = notebook.notes[note_id - 1]

    while True:
        sub_command = Prompt.ask(
            "[blue]What do you want to update? ([bold orange1]title[/bold orange1]/[bold orange1]tag[/bold orange1]/[bold orange1]text[/bold orange1] or [bold orange1]back[/bold orange1] to cancel)[/blue]").strip().lower()
        match sub_command:
            case "title":
                new_title = utilities.get_validated_input(
                    "Provide new title", Title)
                note_to_update.title = new_title
                utilities.rich_console.print(
                    "[bold green]Title updated successfully![/bold green]")
                note_to_update.date = note_to_update.set_date()
                return
            case "text":
                new_text = utilities.get_validated_input(
                    "Provide new text", Text)
                note_to_update.text = new_text
                utilities.rich_console.print(
                    "[bold green]Text updated successfully![/bold green]")
                return
            case "tag":
                if not note_to_update.tags:
                    utilities.rich_console.print(
                        f"[bold red]No tags to update![/bold red]")
                    note_to_update.tags = utilities.get_validated_input(
                        "Enter new tag to add", Tag)
                    return
                tags = utilities.get_validated_input(
                    "Enter tags separated by ';' (<old-tag> ; <new-tag>)", Tag)
                if not tags or len(tags) != 2:
                    utilities.rich_console.print(
                        "[bold red]Please enter exactly 2 tags: old and new![/bold red]")
                    continue
                prev_tag = tags[0].value.lower()
                if not any(t.value.lower() == prev_tag for t in note_to_update.tags):
                    utilities.rich_console.print(
                        f"[bold red]Note does not have {prev_tag} tag![/bold red]")
                    continue
                new_tag = tags[1]
                # update note tags by replacing old one with new
                note_to_update.tags = [new_tag if t.value.lower() ==
                                       prev_tag else t for t in note_to_update.tags]
                return
            case "back":
                break
            case "exit":
                return "exit"
            case _:
                utilities.rich_console.print(
                    "[bold red]Invalid command. Use [orange1]'title'[/orange1], [orange1]'text'[/orange1], [orange1]'back'[/orange1] or [orange1]'exit'[/orange1].[/bold red]")


def show_notes_list(notes: list[Note], title: str):
    """Display a list of notes in a Rich table with given title."""
    if not notes:
        utilities.rich_console.print("[bold red]No notes found.[/bold red]")
        return

    table = utilities.create_table(title)
    table.add_column("ID", justify="center", no_wrap=True)
    table.add_column("Title", justify="left", no_wrap=True)
    table.add_column("Created/Updated", justify="center", no_wrap=True)
    table.add_column("Tags", justify="left")
    table.add_column("Text", justify="left")

    for i, note in enumerate(notes, start=1):
        formatted_text = note.text.value.replace(", ", "\n")
        table.add_row(
            str(i),
            note.title.value,
            note.date,
            ", ".join(t.value for t in note.tags),
            formatted_text
        )

    utilities.rich_console.print(table)
