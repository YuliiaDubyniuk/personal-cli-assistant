from pathlib import Path
import pickle
from contacts.contacts import ContactBook
from notes.notes import NoteBook


def parse_input(user_input: str) -> tuple[str]:
    """Get command from user input and parse it"""
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def load_data(filename=Path):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}


def save_data(data: dict, filename=Path):
    with open(filename, "wb") as f:
        pickle.dump(data, f)


def exit_assistant(contactbook: ContactBook, notebook: NoteBook, filename):
    # Save Assistant data to file and exit assistant
    backup_state = {
        "contacts": contactbook,
        "notes": notebook
    }
    save_data(backup_state, filename)
    print("Good bye!")
    return "exit"


def print_main_help_menu():
    print(
        "\nChoose one of available commands\n"
        "  • contacts  — manage your contacts\n"
        "  • notes     — manage your notes\n"
        "  • help     — show this help menu\n"
        "  • exit     — exit the assistant\n"
    )


def print_contacts_help_menu():
    pass


def print_notes_help_menu():
    pass
