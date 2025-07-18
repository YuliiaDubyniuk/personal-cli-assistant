from datetime import datetime
from pathlib import Path
from contacts.contacts import ContactBook, Record, Phone, Name, Birthday
from decorators import input_error
from notes.notes import NoteBook
from rich.prompt import Prompt
import utilities
#from utilities import rich_console

#print = rich_console.print
from rich.console import Console

rich_console = Console()
print = rich_console.print

def add_contact(book: ContactBook, args: list):
    """create contact if not exist, add phone to the contact"""
    contact_name, phone = Name(args[0]), Phone(args[1])
    if contact_name.value in book.data:
        record = book.find(contact_name.value)
    else:
        record = Record(contact_name.value)
        book.add_record(record)
    record.add_phone(phone)


def add_contact_birthday(book: ContactBook, args: list):
    """create contact if not exist, add birthday to the contact"""
    contact_name, b_day = Name(args[0]), Birthday(args[1])
    if contact_name.value in book.data:
        record = book.find(contact_name.value)
    else:
        record = Record(contact_name.value)
        book.add_record(record)

    record.add_birthday(b_day)


def show_upcoming_birthdays(book: ContactBook, days: int = 7):
    """Return list of contacts that have birthday in the next 7 days."""
    if days is None:
        days = 7
    upcoming_birthdays = book.get_upcoming_birthdays(days)
    if not upcoming_birthdays:
        print(f"There are no birthdays in the next {days} days.")
    else:
        print(f"Here are the upcoming birthdays in the next {days} days:")
        for record in upcoming_birthdays:
            name = record.name.value
            dob = record.birthday.value.date()
            upcoming_bday = dob.replace(year=datetime.today().year)
            print(
                f"{name}'s birthday is {upcoming_bday.strftime('%d.%m.%Y')}")


def add_contact_address(book: ContactBook, args: list):
    """Add or update address for contact"""
    contact_name, address = args[0], " ".join(args[1:])
    if contact_name in book.data:
        record = book.find(contact_name)
        record.add_address(address)
    else:
        raise KeyError(f"Contact {contact_name} not found.")


def add_contact_email(book: ContactBook, args: list):
    """Add or update email for contact"""
    contact_name, email = args[0], args[1]
    if contact_name in book.data:
        record = book.find(contact_name)
        record.add_email(email)
    else:
        raise KeyError(f"Contact {contact_name} not found.")

def ask_yes_no(question):
    return Prompt.ask(f"[blue]{question} (y/n)[/blue]").strip().lower() == "y"


def confirm_existing_phone(record):
    while True:
        old_phone = Prompt.ask("[blue]Enter the old phone number[/blue]").strip()
        if any(p.value == old_phone for p in record.phones):
            return old_phone
        print(f"[bold red]{old_phone} not found. Try again.[/bold red]")


def update_contact(record, contact_name):
    while True:
        print(f"[bold blue]Current contact data:[/bold blue]\n{record}")
        field = Prompt.ask("[blue]What do you want to update? (phone/email/address/birthday or 'back' to cancel)[/blue]").strip().lower()
        if field == "back":
            print("[bold yellow]Update cancelled.[/bold yellow]")
            break

        field_updated = False

        match field:
            case "phone":
                old_phone = confirm_existing_phone(record)
                new_phone = Phone(Prompt.ask("[blue]Enter the new phone number[/blue]").strip())
                record.edit_phone(old_phone, new_phone)
                field_updated = True
            case "email":
                while True:
                    new_email = Prompt.ask("[blue]Enter the new email[/blue]").strip()
                    try:
                        record.add_email(new_email)
                        field_updated = True
                        break
                    except ValueError:
                        print("[bold red]Invalid email format. Try again.[/bold red]")
            case "address":
                new_address = Prompt.ask("[blue]Enter the new address[/blue]").strip()
                record.add_address(new_address)
                field_updated = True
            case "birthday":
                while True:
                    new_birthday_str = Prompt.ask("[blue]Enter the new birthday (DD.MM.YYYY)[/blue]").strip()
                    try:
                        new_birthday = Birthday(new_birthday_str)
                        record.add_birthday(new_birthday)
                        field_updated = True
                        break
                    except ValueError:
                        print("[bold red]Invalid birthday format. Expected DD.MM.YYYY. Try again.[/bold red]")
            case _:
                print("[bold red]Invalid field. Please choose phone, email, address, or birthday.[/bold red]")
    
        if field_updated and not ask_yes_no("Update another field?"):
            break

def remove_contact_field(contactbook, record, contact_name):
    while True:
        print(f"[bold blue]Current contact data:[/bold blue]\n{record}")
        field = Prompt.ask("[blue]What do you want to remove? (phone/email/address/birthday/contact or 'back' to cancel)[/blue]").strip().lower()
        if field == "back":
            print("[bold yellow]Remove cancelled.[/bold yellow]")
            break

        field_removed = False

        match field:
            case "phone":
                    phone_to_remove = Prompt.ask("[blue]Enter the phone number to remove[/blue]").strip()
                    if phone_to_remove in [p.value for p in record.phones]:
                        record.remove_phone(phone_to_remove)
                        field_removed = True
                    else:
                        print(f"[bold red]{phone_to_remove} not found.[/bold red]")
            case "email":
                if record.email:
                    record.email = None
                    print(f"[bold green]Email removed for {contact_name}.[/bold green]")
                else:
                    print(f"[bold yellow]No email set for {contact_name}.[/bold yellow]")
                field_removed = True
            case "address":
                if record.address:
                    record.address = None
                    print(f"[bold green]Address removed for {contact_name}.[/bold green]")
                else:
                    print(f"[bold yellow]No address set for {contact_name}.[/bold yellow]")
                field_removed = True
            case "birthday":
                if record.birthday:
                    record.birthday = None
                    print(f"[bold green]Birthday removed for {contact_name}.[/bold green]")
                else:
                    print(f"[bold yellow]No birthday set for {contact_name}.[/bold yellow]")
                field_removed = True
            case "contact":
                print(f"[bold red]Full record:\n{record}[/bold red]")
                if ask_yes_no(f"Are you sure you want to delete {contact_name}?"):
                    contactbook.delete(contact_name)
                    print(f"[bold green]{contact_name} has been deleted.[/bold green]")
                else:
                    print("[bold yellow]Deletion cancelled.[/bold yellow]")
                break
            case _:
                print("[bold red]Unknown field. Try again.[/bold red]")

        if field_removed and not ask_yes_no("Remove another field?"):
            break


@input_error
def handle_contact_commands(contactbook: ContactBook, command: str, args: list):
    """Central command processor with error handling via a decorator."""
    match command:
        case "back":
            return "back"
        case "help":
            utilities.print_contacts_help_menu()
        case "exit":
            return "exit"
        case "add":
            add_contact(contactbook, args)
        case "add-birthday":
            add_contact_birthday(contactbook, args)
        case "add-address":
            add_contact_address(contactbook, args)
        case "add-email":
            add_contact_email(contactbook, args)

        case "update":
            # update contact phone, email, address, birthday
            contact_name = args[0]
            if contact_name not in contactbook.data:
                raise KeyError(f"Contact {contact_name} not found.")
            record = contactbook.find(contact_name)
            update_contact(record, contact_name)       

        case "remove":
            # remove contact phone (if phone is provided), email, address, birthday or delete contact by name
            contact_name = args[0]
            if contact_name not in contactbook.data:
                raise KeyError(f"Contact {contact_name} not found.")
            record = contactbook.find(contact_name)
            remove_contact_field(contactbook, record, contact_name)    

        case "show":
            # print full contact info
            if not args:
                raise ValueError(
                    "Contact name is required for 'show' command.")
            contact_name = args[0]
            record = contactbook.find(contact_name)
            print(record)

        case "all":
            # return all records in the address book
            if contactbook.data:
                for record in contactbook.data.values():
                    print(record)
            else:
                print("[bold red]There are no records in your address book. Start adding.[/bold red]")

        case "show-birthday":
            contact_name = args[0]
            record = contactbook.find(contact_name)
            birthday = record.birthday
            print(
                f"{contact_name}'s birthday is {birthday}" if birthday else f"{contact_name}'s birthday is not set.")

        case "birthdays":
            days = int(args[0]) if args else None
            show_upcoming_birthdays(contactbook, days)
        case _:
            print("[bold red]Invalid command.[/bold red]")
