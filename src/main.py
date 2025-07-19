import argparse
from pathlib import Path
from contacts.contact_handler import handle_contact_commands
from contacts.contacts import ContactBook
from notes.notes import NoteBook
from notes.note_handler import handle_note_commands
import utilities
from rich.prompt import Prompt
from decorators import input_error


def main():
    """Handle contact book through CLI"""
    parser = argparse.ArgumentParser(description="Personal CLI Assistant")
    parser.add_argument(
        "-f", "--file",
        type=Path,
        help="Path to assistant data file",
        default=Path.home() / "assistant.pkl"
    )
    cli_args = parser.parse_args()

    # Load Assistant data from file or create new contacts/notes objects
    data = utilities.load_data(cli_args.file)
    contactbook = data.get("contacts", ContactBook())
    notebook = data.get("notes", NoteBook())

    # Welcome user and show main command menu
    utilities.rich_console.print(
        "[bold magenta]Welcome to the Assistant Bot![/bold magenta]")
    utilities.print_main_help_menu()

    while True:
        user_input = Prompt.ask(
            "[bold blue]MainMenu[/bold blue]")
        command, args = utilities.parse_input(user_input)

        result = handle_commands(
            contactbook, notebook, command, args, cli_args.file)
        if result == "exit":
            exit_assistant(contactbook, notebook, cli_args.file)
            break


@input_error
def handle_commands(contactbook: ContactBook, notebook: NoteBook, command: str, args: list, filename: Path):
    """Central command processor with error handling via a decorator."""
    match command:
        case "hello":
            print("How can I help you? You can type 'help' to see available commands.")
        case "help":
            utilities.print_main_help_menu()
        case "contacts":
            utilities.rich_console.print(
                "[blue]Type contact command or [bold orange1]help[/bold orange1] to see available commands.[/blue]")
            while True:
                user_input = Prompt.ask(
                    "[bold blue]ContactBook[/bold blue]")
                command, args = utilities.parse_input(user_input)
                result = handle_contact_commands(contactbook, command, args)
                if result == "back":
                    break
                elif result == "exit":
                    return "exit"
        case "notes":
            utilities.rich_console.print(
                "[blue]Type note command or [bold orange1]help[/bold orange1] to see available commands.[/blue]")
            while True:
                user_input = Prompt.ask(
                    "[bold blue]NoteBook[/bold blue]")
                command, args = utilities.parse_input(user_input)
                result = handle_note_commands(notebook, command, args)
                if result == "back":
                    break
                elif result == "exit":
                    return "exit"
        case "exit":
            return "exit"


def exit_assistant(contactbook: ContactBook, notebook: NoteBook, filename):
    # Save Assistant data to file and exit assistant
    backup_state = {
        "contacts": contactbook,
        "notes": notebook
    }
    utilities.save_data(backup_state, filename)
    utilities.rich_console.print("[bold magenta]Good bye![bold magenta]")
    return "exit"


if __name__ == "__main__":
    main()
