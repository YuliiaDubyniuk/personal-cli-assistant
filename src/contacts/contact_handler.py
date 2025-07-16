from datetime import datetime
from pathlib import Path
from contacts.contacts import ContactBook, Record, Phone, Name, Birthday
from decorators import input_error
import utilities
from notes.notes import NoteBook


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
        print(f"Address added/updated for {contact_name}.")
    else:
        raise KeyError(f"Contact {contact_name} not found.")
    
def add_contact_email(book: ContactBook, args: list):
    """Add or update email for contact"""
    contact_name, email = args[0], args[1]
    if contact_name in book.data:
        record = book.find(contact_name)
        record.add_email(email)
        print(f"Email added/updated for {contact_name}.")
    else:
        raise KeyError(f"Contact {contact_name} not found.")

@input_error
def handle_contact_commands(contactbook: ContactBook, notebook: NoteBook, command: str, args: list, filename: Path):
    """Central command processor with error handling via a decorator."""
    match command:
        case "back":
            return "back"
        case "help":
            utilities.print_contacts_help_menu()
        case "exit":
            return utilities.exit_assistant(contactbook, notebook, filename)
        case "add":
            add_contact(contactbook, args)
        case "add-birthday":
            add_contact_birthday(contactbook, args)
        case "add-address":
            add_contact_address(contactbook, args)
        case "add-email":
            add_contact_email(contactbook, args)

        case "update":
            # update phone for provided name to the new one
            contact_name = args[0]

            if contact_name not in contactbook.data:
                raise KeyError(f"Contact {contact_name} not found.")

            record = contactbook.find(contact_name)

            while True:
                field = input("What do you want to update? (phone/email/address/birthday or 'back' to cancel): ").strip().lower()

                match field:
                    case "phone":
                        old_phone = input("Enter the old phone number: ").strip()
                        new_phone = Phone(input("Enter the new phone number: ").strip())
                        record.edit_phone(old_phone, new_phone)
                        break
                    case "email":
                        new_email = input("Enter the new email: ").strip()
                        record.edit_email(new_email)
                        break
                    case "address":
                        new_address = input("Enter the new address: ").strip()
                        record.edit_address(new_address)
                        break
                    case "birthday":
                        new_birthday = Birthday(input("Enter the new birthday (DD.MM.YYYY): ").strip())
                        record.add_birthday(new_birthday)
                        break
                    case "back":
                        print("Update cancelled.")
                        break
                    case _:
                        print("Unknown field. Try again.")

        case "remove":
            # remove contact phone (if phone is provided) or delete contact by name
            contact_name = args[0]

            if contact_name not in contactbook.data:
                raise KeyError(f"Contact {contact_name} not found.")

            record = contactbook.find(contact_name)

            while True:
                field = input("What do you want to remove? (phone/email/address/birthday/contact or 'back' to cancel): ").strip().lower()

                match field:
                    case "phone":
                        phone = input("Enter the phone number to remove: ").strip()
                        record.remove_phone(phone)
                        break
                    case "email":
                        if record.email:
                            record.email = None
                            print(f"Email removed for {contact_name}.")
                        else:
                            print(f"No email set for {contact_name}.")
                        break
                    case "address":
                        if record.address:
                            record.address = None
                            print(f"Address removed for {contact_name}.")
                        else:
                            print(f"No address set for {contact_name}.")
                        break
                    case "birthday":
                        if record.birthday:
                            record.birthday = None
                            print(f"Birthday removed for {contact_name}.")
                        else:
                            print(f"No birthday set for {contact_name}.")
                        break
                    case "contact":
                        print(f"Full record:\n{record}")
                        confirm = input(f"Are you sure you want to delete {contact_name}? (yes/no): ").strip().lower()
                        if confirm == "yes":
                            contactbook.delete(contact_name)
                        else:
                            print("Deletion cancelled.")
                        break
                    case "back":
                        print("Remove cancelled.")
                        break
                    case _:
                        print("Unknown field. Try again.")
            
        case "phone":
            # print contact's data for provided name if record exists
            contact_name = args[0]
            record = contactbook.find(contact_name)
            if record:
                print(
                    f"{contact_name}'s phones: {', '.join(str(phone) for phone in record.phones)}")
                
        case "all":
            # return all records in the address book
            if contactbook.data:
                for record in contactbook.data.values():
                    print(record)
            else:
                print("There are no records in your address book. Start adding.")

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
            print("Invalid command.")
