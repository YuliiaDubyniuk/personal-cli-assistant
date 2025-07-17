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
    table = create_help_table()
    table.title = "[bold blue]Main Commands[/bold blue]"
    
    table.add_row("contacts", "Manage your contacts")
    table.add_row("notes", "Manage your notes")
    table.add_row("help", "Show this help menu")
    table.add_row("exit", "Exit the assistant")

    rich_console.print(table)


def print_contacts_help_menu():
    table = create_help_table()
    table.title = "[bold blue]Contact Commands[/bold blue]"

    table.add_row("add <name> <phone>", "Add a new contact or phone to existing")
    table.add_row("add-birthday <name> <DD.MM.YYYY>", "Add or overwrite birthday")
    table.add_row("add-address <name> <address>", "Add or overwrite address")
    table.add_row("add-email <name> <email>", "Add or overwrite email")
    table.add_row("update <name>", "Interactive edit (phone, email, address, birthday)")
    table.add_row("remove <name>", "Remove phone/email/address/birthday or entire contact")
    table.add_row("show <name>", "Print full contact info")
    table.add_row("show-birthday <name>", "Show contact's birthday")
    table.add_row("birthdays [days]", "Show birthdays in the next N days (default is 7)")
    table.add_row("all", "Show all contacts")
    table.add_row("help", "Show this contact command list again")
    table.add_row("back", "Return to the main menu")
    table.add_row("exit", "Save and exit assistant")

    rich_console.print(table)


def print_notes_help_menu():
    table = create_help_table()
    table.title = "[bold blue]Note Commands[/bold blue]"

    table.add_row("add", "Add a new note")
    table.add_row("update", "Update an existing note")
    table.add_row("delete", "Delete a note")
    table.add_row("all", "Show all notes")
    table.add_row("help", "Show this note command list again")
    table.add_row("back", "Return to the main menu")
    table.add_row("exit", "Save and exit assistant")

    rich_console.print(table)


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
