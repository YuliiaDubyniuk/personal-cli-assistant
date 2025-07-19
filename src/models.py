class Field:
    """Base class to represent a generic field with a value."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
