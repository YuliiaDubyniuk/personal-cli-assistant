import argparse
from pathlib import Path
from contacts.contact_handler import handle_contact_commands
from contacts.contacts import ContactBook
from notes.notes import NoteBook
from notes.note_handler import handle_note_commands
import src.utilities as utilities
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

    # Welcome user and show main available commands
    print("Welcome to the assistant bot!")
    utilities.print_main_help_menu()

    while True:
        user_input = input("Enter a command: ")
        command, *args = utilities.parse_input(user_input)

        result = handle_commands(
            contactbook, notebook, command, args, cli_args.file)
        if result == "exit":
            utilities.exit_assistant(contactbook, notebook, cli_args.file)
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
            print("Type 'help' to see available contact commands.")
            while True:
                user_input = input("ContactBook > ")
                command, *args = utilities.parse_input(user_input)
                result = handle_contact_commands(
                    contactbook, notebook, command, args, filename)
                if result == "back":
                    break
                elif result == "exit":
                    return "exit"
        case "notes":
            while True:
                utilities.print_notes_help_menu()
                user_input = input("Enter command to handle your NoteBook: ")
                command, *args = utilities.parse_input(user_input)
                result = handle_note_commands(
                    contactbook, notebook, command, args, filename)
                if result == "back":
                    break
                elif result == "exit":
                    return "exit"
        case "exit":
            return "exit"
        case _:
            print("Invalid command.")


if __name__ == "__main__":
    main()
