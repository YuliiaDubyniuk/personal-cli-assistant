from datetime import datetime
from models import Field
import utilities


class Title(Field):
    def __init__(self, value: str):
        if not value.strip():
            raise ValueError("Title cannot be empty!")
        if len(value) > 50:
            raise ValueError("Title cannot exceed 50 characters!")
        super().__init__(value)


class Text(Field):
    def __init__(self, value: str):
        if not value.strip():
            raise ValueError("Text cannot be empty!")
        if len(value) < 10:
            raise ValueError("Text must be at least 10 characters!")
        super().__init__(value)


class Tag(Field):
    def __init__(self, value: str):
        if len(value) < 3:
            raise ValueError("Tag must be at least 3 characters!")
        super().__init__(value)


class Note:
    """Represents a single note and provides methods to manage its data"""

    def __init__(self, title: Title, text: Text, tags: list[Tag] = []):
        self.title = title
        self.date: str = self.set_date()
        self.text = text
        self.tags = tags

    def set_date(self) -> str:
        return datetime.today().strftime("%d %B %Y")


class NoteBook:
    """Manages a collection of notes"""

    def __init__(self):
        self.notes: list[Note] = []

    def add_note(self, note: Note):
        self.notes.append(note)

    def find_by_keyword(self, keywords: list[str]) -> list[Note]:
        """Search notes by one or more keywords in title or tags. Returns list of matched notes."""
        norm_keys = [k.strip().lower() for k in keywords if k and k.strip()]

        matches = []
        note_checked = set()

        for idx, note in enumerate(self.notes):
            title = note.title.value.lower()
            tags = [t.value.lower() for t in note.tags]

            # check for full match of the keyword with any note tag or for partial match with title
            for key in norm_keys:
                title_match = key in title
                tag_match = any(key == tag or key in tag for tag in tags)

                if title_match or tag_match:
                    # stop at first match, no need to check remaining keywords
                    if idx not in note_checked:
                        matches.append(note)
                        note_checked.add(idx)
                    break

        return matches

    def sort_notes_by_tags(self) -> list[Note]:
        """
        Return notes sorted alphabetically by the first tag in each note's tag list.
        Notes without tags appear last. Case-insensitive.
        """
        tagged_notes: list[Note] = []
        untagged_notes: list[Note] = []

        for note in self.notes:
            if note.tags:
                tagged_notes.append(note)
            else:
                untagged_notes.append(note)

        # Sort tagged notes by the first tag value (case-insensitive)
        tagged_notes.sort(key=lambda n: n.tags[0].value.lower())

        return tagged_notes + untagged_notes
