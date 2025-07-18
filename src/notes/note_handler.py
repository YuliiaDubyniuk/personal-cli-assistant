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
                "Enter tag(s) separated by [bold orange1]';'[/bold orange1] "
                "(press [bold orange1]Enter[/bold orange1] to skip)", Tag)
            text = utilities.get_validated_input("Enter text", Text)
            note = Note(title, text, tags)
            notebook.add_note(note)
        case "update":
            result = handle_update_note(notebook, command)
            if result == "exit":
                return "exit"
        case "remove":
            result = handle_delete_note(notebook, command)
            if result == "exit":
                return "exit"
        case "find":
            if not args:
                utilities.rich_console.print(
                    "[bold red]Search phrase is required.[/bold red]")
                return
            matches = notebook.find_by_keyword(args)
            if matches:
                utilities.show_notes_list(matches, f"Matched notes")
            else:
                utilities.rich_console.print(
                    "[bold red]No matched note found.[/bold red]")
                return
        case "sort":
            sorted_notes = notebook.sort_notes_by_tags()
            utilities.show_notes_list(sorted_notes, "Sorted Notes")
        case "all":
            utilities.show_notes_list(notebook.notes, "All Notes")


def handle_delete_note(notebook: NoteBook, cmd: str):
    """Handles deleting a note by user selection."""
    if not notebook.notes:
        utilities.rich_console.print(
            "[bold red]No notes to delete.[/bold red]")
        return

    selection = utilities.select_note(notebook, cmd)

    match selection:
        case "exit":
            return "exit"
        case None:
            return
        case note:
            cont = Prompt.ask(
                f"[blue]Are you sure you want to remove '{note.title.value}'? ([bold orange1]y[/bold orange1]/[bold orange1]n[/bold orange1])[/blue]").strip().lower()
            if cont != "y":
                utilities.rich_console.print(
                    f"[bold red]Removing cancelled.[/bold red]"
                )
                return
            notebook.notes.remove(note)
            utilities.rich_console.print(
                f"[bold green]Note '{note.title.value}' successfully deleted.[/bold green]"
            )


def handle_update_note(notebook: NoteBook, cmd):
    """Handles updating a note parts (title, text, or tags)."""
    if not notebook.notes:
        utilities.rich_console.print(
            "[bold red]No notes to update.[/bold red]")
        return
    # Is Note object or command to cancel updating
    selection = utilities.select_note(notebook, cmd)

    if selection == "exit":
        return "exit"
    if selection is None:
        return

    note_to_update = selection

    while True:
        sub_command = Prompt.ask(
            "[blue]What do you want to update? ([bold orange1]title[/bold orange1]/[bold orange1]tag[/bold orange1]/[bold orange1]text[/bold orange1] or [bold orange1]back[/bold orange1] to cancel)[/blue]").strip().lower()
        match sub_command:
            case "title":
                new_title = utilities.get_validated_input(
                    "Enter new title", Title)
                note_to_update.title = new_title
                utilities.rich_console.print(
                    "[bold green]Title successfully updated![/bold green]")
                note_to_update.date = note_to_update.set_date()
            case "text":
                new_text = utilities.get_validated_input(
                    "Enter new text", Text)
                note_to_update.text = new_text
                utilities.rich_console.print(
                    "[bold green]Text successfully updated![/bold green]")
            case "tag":
                if not note_to_update.tags:
                    utilities.rich_console.print(
                        f"[bold red]No tags to update.[/bold red]")
                    note_to_update.tags = utilities.get_validated_input(
                        "Enter new tag to add", Tag)
                    continue
                tags = utilities.get_validated_input(
                    "Enter tags separated by [bold orange1];[/bold orange1] (<old-tag> ; <new-tag>)", Tag)
                if not tags or len(tags) != 2:
                    utilities.rich_console.print(
                        "[bold red]Please enter exactly 2 tags: old; new.[/bold red]")
                    continue
                prev_tag = tags[0].value.lower()
                if not any(t.value.lower() == prev_tag for t in note_to_update.tags):
                    utilities.rich_console.print(
                        f"[bold red]Note does not have '{prev_tag}' tag.[/bold red]")
                    continue
                new_tag = tags[1]
                # update note tags by replacing old one with new
                note_to_update.tags = [new_tag if t.value.lower() ==
                                       prev_tag else t for t in note_to_update.tags]
                utilities.rich_console.print(
                    "[bold green]Tags successfully updated![/bold green]")
            case "back":
                break
            case "exit":
                return "exit"
            case _:
                utilities.rich_console.print(
                    "[bold red]Invalid command.[/bold red]")
                continue

        cont = Prompt.ask(
            "[blue]Update another field? ([bold orange1]y[/bold orange1]/[bold orange1]n[/bold orange1])[/blue]").strip().lower()
        if cont != "y":
            break
