import argparse
from pathlib import Path
from contacts.contact_handler import handle_contacts_command
from contacts.contacts import ContactBook
import utilities
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

    book = ContactBook.load_data(cli_args.file)
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, *args = utilities.parse_input(user_input)

        result = handle_commands(book, command, args, cli_args.file)
        if result == "exit":
            break


@input_error
def handle_commands(book: ContactBook, command: str, args: list, filename: Path):
    """Central command processor with error handling via a decorator."""
    match command:
        case "hello":
            print("How can I help you?")
        case "help":
            pass
        case "contact":
            while True:
                user_input = input("Enter a command: ")
                command, *args = utilities.parse_input(user_input)
                result = handle_contacts_command(book, command, args, filename)
                if result == "back":
                    break
        case "note":
            pass
        case "exit" | "close":
            book.save_data(filename)
            print("Good bye!")
            return "exit"
        case _:
            print("Invalid command.")


if __name__ == "__main__":
    main()
