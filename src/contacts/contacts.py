from collections import UserDict
from datetime import datetime
import re
from models import Field
from rich.console import Console

rich_console = Console()
print = rich_console.print


class Name(Field):
    """Represents a name field which requires a minimum length validation."""

    def __init__(self, value: str):
        if len(value.strip()) < 3:
            raise ValueError("Name must have at least 3 characters.")
        super().__init__(value.capitalize())


class Phone(Field):
    """Represents a phone field which requires the value to be numeric and at least 10 digits long."""

    def __init__(self, value: str):
        if not value.isdigit() or len(value.strip()) < 10:
            raise ValueError("Phone must be 10 digits or more.")
        super().__init__(value)


class Birthday(Field):
    """Field that stores and validates a birthday date in the format DD.MM.YYYY"""

    def __init__(self, value: str):
        try:
            parsed_date = datetime.strptime(value, "%d.%m.%Y")
            super().__init__(parsed_date)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Address(Field):
    """Field that stores and validates address."""

    def __init__(self, value: str):
        if len(value.strip()) < 5:
            raise ValueError("Address must contain at least 5 characters.")
        super().__init__(value.strip())


class Email(Field):
    """Field that stores and validates an email address."""

    def __init__(self, value: str):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, value.strip()):
            raise ValueError("Invalid email format")
        super().__init__(value.strip())


class Record:
    """Represents a single contact record in the contacts book and provides methods to manage its details"""

    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.address = None
        self.email = None

    def is_empty(self) -> bool:
        """Check if record has no data except name."""
        return not (self.phones or self.birthday or self.address or self.email)

    def add_phone(self, phone: str):
        self.phones.append(phone)

    def remove_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValueError(f"Contact {self.name} doesn't have phone '{phone}'")

    def edit_phone(self, old_phone: str, new_phone: Phone):
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = new_phone
                print(
                    f"[bold green]{self.name}'s phone '{old_phone}' has been successfully updated to '{new_phone.value}'.[/bold green]")
                return
        raise ValueError(
            f"Contact {self.name} doesn't have phone '{old_phone}'")

    def add_birthday(self, b_day_date: Birthday):
        self.birthday = b_day_date

    def add_address(self, address: str):
        self.address = Address(address)
        print(
            f"[bold green]Address for {self.name.value} has been added.[/bold green]")

    def add_email(self, email: str):
        self.email = Email(email)
        print(
            f"[bold green]Email for {self.name.value} has been added.[/bold green]")


class ContactBook(UserDict):
    """A contact management class that stores, retrieves, updates, and deletes contact records"""

    def add_contact(self, name: str, phone: str):
        """Add a new contact or add phone to existing contact."""
        contact_name = Name(name)
        phone_obj = Phone(phone)

        if contact_name.value in self.data:
            record = self.find(contact_name.value)
        else:
            record = Record(contact_name.value)
            self.data[contact_name.value] = record

        record.add_phone(phone_obj)

    def find(self, search_name: str):
        if search_name in self.data:
            return self.data[search_name]
        else:
            raise KeyError()

    def delete(self, search_name: str):
        if search_name in self.data:
            del self.data[search_name]
        else:
            raise KeyError()

    def get_upcoming_birthdays(self, days: int = 7):
        """
        Return a list of contacts with birthdays in the next 7 days
        """
        current_date = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if not record.birthday:
                continue
            dob = record.birthday.value.date()
            current_birthday = dob.replace(year=current_date.year)

            if current_birthday < current_date:
                current_birthday = dob.replace(year=current_date + 1)

            days_to_birthday = (current_birthday - current_date).days

            if 0 < days_to_birthday <= days:
                upcoming_birthdays.append(record)

        return upcoming_birthdays
