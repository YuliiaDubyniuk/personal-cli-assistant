from rich.table import Table
from pathlib import Path
import pickle
from contacts.contacts import ContactBook
from notes.notes import NoteBook
from rich.console import Console
from rich.prompt import Prompt
from rapidfuzz import process



VALID_COMMANDS = [
    "add", "add-birthday", "add-address", "add-email", "phone",
    "update", "remove", "show", "show-birthday", "birthdays",
    "all", "help", "exit", "back", "contacts", "notes", "title", "text", "delete"
]



rich_console = Console()


def create_table(title: str = None) -> Table:
    """Creates a Rich table with consistent styling for reuse."""
    table = Table(
        title=f"[bold blue]{title}[/bold blue]",
        show_lines=True,
        border_style="blue",
        header_style="bold orange1",
    )
    return table


def create_help_table() -> Table:
    """
    Creates a reusable Rich table for commands without header and borders,
    with blue row separators.
    """
    table = Table(
        show_header=False,       # No header
        show_edge=False,         # No outer borders
        show_lines=True,         # Blue separators between rows
        row_styles=["none"],     # No alternating colors
        border_style="blue"      # Color of row separators
    )

    table.add_column("Command", style="bold orange1",
                     justify="center", no_wrap=True)
    table.add_column("Action", justify="left")

    return table


def parse_input(user_input: str) -> tuple[str | None, list[str]]:
    user_input = user_input.strip()

    if not user_input:
        return None, []

    words = user_input.split()
    user_cmd = words[0].lower()
    args = words[1:]

    if user_cmd in VALID_COMMANDS:
        return user_cmd, args

    match_result = process.extractOne(user_cmd, VALID_COMMANDS, score_cutoff=60)

    if match_result:
        match, score = match_result[:2]
        confirm = input(f"Did you mean '{match}'? (y/n): ").strip().lower()
        if confirm == 'y':
            return match, args
        else:
            print("Command cancelled.")
            return None, []
    else:
        print("Unknown command.")
        return None, []


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


def get_validated_input(prompt_text: str, field_class):
    """
    Prompt user for input with Rich styling and validate using the given Field subclass.
    Repeats until valid input is entered.
    """
    while True:
        try:
            user_input = Prompt.ask(f"[blue]{prompt_text}[/blue]")
            return field_class(user_input)
        except ValueError as e:
            rich_console.print(f"[bold red]{e}[/bold red]")


def get_valid_id(prompt_text: str, max_id: int) -> int:
    """
    Prompt user for a valid numeric ID within the given range.
    Retries until valid input is entered.
    """
    while True:
        try:
            value = int(Prompt.ask(f"[blue]{prompt_text}[/blue]"))
            if 1 <= value <= max_id:
                return value
            rich_console.print(
                f"[bold red]ID must be between 1 and {max_id}.[/bold red]")
        except ValueError:
            rich_console.print(
                "[bold red]Please enter a valid number.[/bold red]")
