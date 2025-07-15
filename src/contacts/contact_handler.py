from datetime import datetime
from pathlib import Path
from contacts.contacts import ContactBook, Record, Phone, Name, Birthday
from decorators import input_error


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


def show_upcoming_birthdays(book: ContactBook):
    """Return list of contacts that have birthday in the next 7 days."""
    upcoming_birthdays = book.get_upcoming_birthdays()
    if not upcoming_birthdays:
        print("There are no birthdays in the next 7 days.")
    else:
        print("Here are the upcoming birthdays in the next 7 days:")
        for record in upcoming_birthdays:
            name = record.name.value
            dob = record.birthday.value.date()
            upcoming_bday = dob.replace(year=datetime.today().year)
            print(
                f"{name}'s birthday is {upcoming_bday.strftime('%d.%m.%Y')}")


@input_error
def handle_contacts_command(book: ContactBook, command: str, args: list, filename: Path):
    """Central command processor with error handling via a decorator."""
    match command:
        case "back":
            print("What do you want to work with? contact | note")
            return "back"
        case "add":
            add_contact(book, args)
        case "change":
            # update phone for provided name to the new one
            contact_name, old_phone, new_phone = args[0], args[1], Phone(
                args[2])
            if contact_name in book.data:
                record = book.find(contact_name)
                record.edit_phone(old_phone, new_phone)
            else:
                raise KeyError()
        case "remove":
            # remove contact phone (if phone is provided) or delete contact by name
            contact_name = args[0]
            if contact_name in book.data:
                if len(args) > 1:
                    phone = args[1]
                    record = book.find(contact_name)
                    record.remove_phone(phone)
                else:
                    book.delete(contact_name)
            else:
                raise KeyError()
        case "phone":
            # print contact's data for provided name if record exists
            contact_name = args[0]
            record = book.find(contact_name)
            if record:
                print(
                    f"{contact_name}'s phones: {', '.join(str(phone) for phone in record.phones)}")

        case "all":
            # return all records in the address book
            if book.data:
                for record in book.data.values():
                    print(record)
            else:
                print("There are no records in your address book. Start adding.")
        case "add-birthday":
            add_contact_birthday(book, args)
        case "show-birthday":
            contact_name = args[0]
            record = book.find(contact_name)
            birthday = record.birthday
            print(
                f"{contact_name}'s birthday is {birthday}" if birthday else f"{contact_name}'s birthday is not set.")

        case "birthdays":
            show_upcoming_birthdays(book)
        case _:
            print("Invalid command.")
