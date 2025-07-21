from enum import Enum


class MainCommands(Enum):
    CONTACTS = "contacts"
    NOTES = "notes"
    HELP = "help"
    EXIT = "exit"


class ContactCommands(Enum):
    ADD = "add"
    ADD_BIRTHDAY = "add-birthday"
    ADD_ADDRESS = "add-address"
    ADD_EMAIL = "add-email"
    UPDATE = "update"
    REMOVE = "remove"
    SHOW = "show"
    SHOW_BIRTHDAY = "show-birthday"
    BIRTHDAYS = "birthdays"
    FIND = "find"
    ALL = "all"
    HELP = "help"
    BACK = "back"
    EXIT = "exit"


class NoteCommands(Enum):
    ADD = "add"
    UPDATE = "update"
    REMOVE = "remove"
    SHOW = "show"
    FIND = "find"
    SORT = "sort"
    ALL = "all"
    HELP = "help"
    BACK = "back"
    EXIT = "exit"
