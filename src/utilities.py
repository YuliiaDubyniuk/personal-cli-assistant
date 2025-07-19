from rich.table import Table
from pathlib import Path
import pickle
from notes.notes import NoteBook, Tag, Note
from rich.console import Console
from rich.prompt import Prompt
from rich.padding import Padding
from rapidfuzz import process


VALID_COMMANDS = [
    "add", "add-birthday", "add-address", "add-email", "phone", "sort",
    "update", "remove", "show", "show-birthday", "birthdays", "find",
    "all", "help", "exit", "back", "contacts", "notes", "title", "text",
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
        show_header=False,
        show_edge=False,
        show_lines=True,
        row_styles=["none"],
        border_style="blue"
    )

    table.add_column("Command", style="bold orange1",
                     justify="left", no_wrap=True)
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

    match_result = process.extractOne(
        user_cmd, VALID_COMMANDS, score_cutoff=60)

    if match_result:
        match, score = match_result[:2]
        confirm = Prompt.ask(
            f"[blue]Did you mean [bold orange1]{match}[/bold orange1]? ([bold orange1]y[/bold orange1]/[bold orange1]n[/bold orange1])[blue]").strip().lower()
        if confirm == 'y':
            return match, args
        else:
            rich_console.print("[bold red]Command cancelled.[/bold red]")
            return None, []
    else:
        rich_console.print(
            "[bold red]Unknown command. Type [bold orange1]help[/bold orange1] to see available commands[/bold red].")
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


# def exit_assistant(contactbook: ContactBook, notebook: NoteBook, filename):
#     # Save Assistant data to file and exit assistant
#     backup_state = {
#         "contacts": contactbook,
#         "notes": notebook
#     }
#     save_data(backup_state, filename)
#     rich_console.print("[bold magenta]Good bye![bold magenta]")
#     return "exit"


def print_main_help_menu():
    table = create_help_table()
    table.title = "[bold blue]Main Commands[/bold blue]"

    table.add_row("contacts", "Manage your contacts")
    table.add_row("notes", "Manage your notes")
    table.add_row("help", "Show this help menu")
    table.add_row("exit", "Exit the assistant")

    rich_console.print(Padding(table, (0, 0, 1, 0)))


def print_contacts_help_menu():
    table = create_help_table()
    table.title = "[bold blue]Contact Commands[/bold blue]"

    table.add_row("add <name> <phone>",
                  "Add a new contact or phone to existing")
    table.add_row("add-birthday <name> <DD.MM.YYYY>",
                  "Add or overwrite birthday")
    table.add_row("add-address <name> <address>", "Add or overwrite address")
    table.add_row("add-email <name> <email>", "Add or overwrite email")
    table.add_row("update <name>",
                  "Interactive edit (phone, email, address, birthday)")
    table.add_row("remove <name>",
                  "Remove phone/email/address/birthday or entire contact")
    table.add_row("show <name>", "Print full contact info")
    table.add_row("show-birthday <name>", "Show contact's birthday")
    table.add_row("birthdays [days]",
                  "Show birthdays in the next N days (default is 7)")
    table.add_row("all", "Show all contacts")
    table.add_row("help", "Show this contact command list again")
    table.add_row("back", "Return to the main menu")
    table.add_row("exit", "Save and exit assistant")

    rich_console.print(Padding(table, (0, 0, 1, 0)))


def print_notes_help_menu():
    table = create_help_table()
    table.title = "[bold blue]Note Commands[/bold blue]"

    table.add_row("add", "Add a new note")
    table.add_row("update", "Update an existing note")
    table.add_row("remove", "Delete a note")
    table.add_row("find <search phrase>", "Find note(s) by search phrase")
    table.add_row("sort", "Sort all notes by tags")
    table.add_row("all", "Show all notes")
    table.add_row("help", "Show this note command list again")
    table.add_row("back", "Return to the main menu")
    table.add_row("exit", "Save and exit assistant")

    rich_console.print(Padding(table, (0, 0, 1, 0)))


def get_validated_input(prompt_text: str, field_class):
    """
    Prompt user for input with Rich styling and validate using the given Field subclass.
    Repeats until valid input is entered.
    """
    while True:
        try:
            user_input = Prompt.ask(
                f"[blue]{prompt_text}[/blue]")
            stripped = user_input.strip()

            if field_class == Tag:
                # allow user to skip providing tags
                if not stripped:
                    return []
                raw_tags = stripped.split(';')
                return [Tag(t.strip()) for t in raw_tags]

            return field_class(user_input)
        except ValueError as e:
            rich_console.print(f"[bold red]{e}[/bold red]")


def get_valid_id(value: str, max_id: int) -> int:
    """
    Prompt user for a valid numeric ID within the given range.
    Retries until valid input is entered.
    """
    try:
        id_num = int(value)
        if 1 <= id_num <= max_id:
            return id_num
        else:
            rich_console.print(
                f"[bold red]ID must be between 1 and {max_id}.[/bold red]")
            return None
    except ValueError:
        rich_console.print(
            f"[bold red]Please enter a number from 1 to {max_id}.[/bold red]")
        return None


def ask_for_id(max_id: int, cmd: str) -> int | None | str:
    """Prompt user for ID or allow 'back'/'exit'."""
    while True:
        input_val = Prompt.ask(
            f"[blue]Enter [bold orange1]ID[/bold orange1] to {cmd} note "
            "(type [bold orange1]back[/bold orange1] to cancel)[/blue]"
        ).strip().lower()

        if input_val == "exit":
            return "exit"
        if input_val == "back":
            return None

        note_id = get_valid_id(input_val, max_id)
        if note_id is not None:
            return note_id


def select_note(notebook: NoteBook, cmd: str) -> Note | None | str:
    """Show notes, ask user for ID to perform action (update/delete), return the selected note."""
    show_notes_list(notebook.notes, "All Notes")
    note_id = ask_for_id(len(notebook.notes), cmd)

    if note_id == "exit":
        return "exit"
    if note_id is None:
        return None

    return notebook.notes[note_id - 1]


def show_notes_list(notes: list[Note], title: str):
    """Display a list of notes in a Rich table with given title."""
    table = create_table(title)
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

    rich_console.print(table)


def show_contacts_list(disp_data, title: str):
    table = create_table(title)
    table.add_column("Name")
    table.add_column("Phones")
    table.add_column("Email")
    table.add_column("Address")
    table.add_column("Birthday")

    if isinstance(disp_data, dict):
        records = list(disp_data.values())
    elif isinstance(disp_data, list):
        records = disp_data
    else:
        records = [disp_data]

    for contact in records:
        table.add_row(
            contact.name.value,
            '; '.join(p.value for p in contact.phones),
            contact.email.value if contact.email else "",
            contact.address.value if contact.address else "",
            contact.birthday.value.strftime(
                "%d.%m.%Y") if contact.birthday else ""
        )

    rich_console.print(table)
