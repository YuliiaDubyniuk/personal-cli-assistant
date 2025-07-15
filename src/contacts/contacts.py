import pickle
from pathlib import Path
from collections import UserDict
from datetime import datetime


class Field:
    """Base class to represent a generic field with a value."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Represents a name field which requires a minimum length validation."""

    def __init__(self, value: str):
        if len(value.strip()) < 3:
            raise ValueError("Name must have at least 3 characters.")
        super().__init__(value)


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


class Record:
    """Represents a single contact record in the contacts book and provides methods to manage its details"""

    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        birthday_str = f"contact birthday: {self.birthday}" if self.birthday else "contact birthday: Not set"
        phones_str = '; '.join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, {birthday_str}, phones: {phones_str}"

    def add_phone(self, phone: str):
        self.phones.append(phone)
        print(f"Phone {phone} has been added.")

    def remove_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                print(f"Phone {phone} has been successfully removed.")
                return
        raise ValueError(f"Contact {self.name} doesn't have phone {phone}")

    def edit_phone(self, old_phone: str, new_phone: Phone):
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = new_phone
                print(
                    f"{self.name}'s phone {old_phone} has been successfully updated to {new_phone.value}.")
                return
        raise ValueError(f"Contact {self.name} doesn't have phone {old_phone}")

    def find_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                print(f"{self.name}: {phone}")
                return phone
        raise ValueError(f"Contact {self.name} doesn't have phone {phone}")

    def add_birthday(self, b_day_date: Birthday):
        self.birthday = b_day_date
        print(f"{self.name.value}'s birthday has been added.")


class ContactBook(UserDict):
    """A contact management class that stores, retrieves, updates, and deletes contact records"""

    def save_data(self, filename=Path):
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load_data(cls, filename=Path):
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return cls()

    def add_record(self, record: Record):
        self.data[record.name.value] = record
        print(
            f"Record for {record.name.value} has been successfully created.")

    def find(self, search_name: str):
        if search_name in self.data:
            return self.data[search_name]
        else:
            raise KeyError()

    def delete(self, search_name: str):
        if search_name in self.data:
            del self.data[search_name]
            print(f"Contact {search_name} has been deleted.")
        else:
            raise KeyError()

    def get_upcoming_birthdays(self):
        """
        Return a list of contacts with birthdays in the next 7 days
        """
        current_date = datetime.today().date()
        current_year = current_date.year

        next_week_birthdays = []

        for record in self.data.values():
            if not record.birthday:
                continue
            dob = record.birthday.value.date()
            current_birthday = dob.replace(year=current_year)

            if current_birthday > current_date:
                days_to_birthday = (current_birthday - current_date).days
                if days_to_birthday <= 7:
                    # user has a birthday in the next 7 days
                    next_week_birthdays.append(record)

        return next_week_birthdays
