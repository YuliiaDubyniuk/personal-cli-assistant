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
    print(
        "\nAvailable contact commands:\n"
        "  • add <name> <phone>               — add a new contact or phone to existing\n"
        "  • add-birthday <name> <DD.MM.YYYY> — quick add or overwrite birthday\n"
        "  • add-address <name> <address>     — quick add or overwrite address\n"
        "  • add-email <name> <email>         — quick add or overwrite email\n"
        "  • update <name>                    — interactive edit (phone, email, address, birthday)\n"
        "  • remove <name>                    — remove phone/email/address/birthday or entire contact\n"
        "  • phone <name>                     — show contact's phone numbers\n"
        "  • show-birthday <name>             — show contact's birthday\n"
        "  • birthdays [days]                 — show birthdays in the next N days (default is 7)\n"
        "  • all                              — show all contacts\n"
        "  • help                             — show this contact command list again\n"
        "  • back                             — return to the main menu\n"
        "  • exit                             — save and exit assistant\n"
    )


def print_notes_help_menu():
    pass