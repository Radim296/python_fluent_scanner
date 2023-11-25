import enum


# The `FluentPlaceableTypes` class is an enumeration that represents different types of placeable
# objects.
class FluentPlaceableTypes(enum.Enum):
    VARIABLE: str = "VARIABLE"
    SELECT_EXPRESSION: str = "SELECT_EXPRESSION"
