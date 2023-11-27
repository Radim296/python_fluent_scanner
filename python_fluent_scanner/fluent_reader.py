from fluent.syntax import parse
from fluent.syntax import ast
from fluent.syntax.errors import ParseError
from typing import Dict

from termcolor import cprint, colored
from python_fluent_scanner.types.enums import FluentPlaceableTypes
from python_fluent_scanner.types.models import (
    ScannerConfig,
    FluentDictionary,
    FluentMessage,
    FluentPlaceable,
)

class FluentReader:
    def __is_comment(self, entry: ast.Entry) -> bool:
        """
        The function checks if an entry is a comment in an abstract syntax tree.

        :param entry: The `entry` parameter is of type `ast.Entry`
        :type entry: ast.Entry
        :return: a boolean value.
        """
        return isinstance(
            entry,
            (
                ast.BaseComment,
                ast.ResourceComment,
                ast.GroupComment,
                ast.Comment,
            ),
        )

    def __get_entry_placeables(self, entry: ast.Entry) -> Dict[str, FluentPlaceable]:
        """
        The function `__get_entry_placeables` extracts placeables from an AST entry object in a Fluent file
        and returns them as a list of strings.
        """

        placeables: Dict[str, FluentPlaceable] = {}

        for value in entry.value.elements:
            if isinstance(value, ast.Placeable):
                if isinstance(value.expression, ast.SelectExpression):
                    placeables[value.expression.selector.id.name] = FluentPlaceable(
                        placeable_type=FluentPlaceableTypes.SELECT_EXPRESSION,
                    )
                elif isinstance(value.expression, ast.VariableReference):
                    placeables[value.expression.id.name] = FluentPlaceable(
                        placeable_type=FluentPlaceableTypes.VARIABLE,
                    )
                else:
                    raise ValueError("Unknown placeable type")

        return placeables

    def parse_by_file(self, path: str, language_code: str) -> FluentDictionary:
        """
        The `parse_by_file` function takes a file path and a language code as input, reads the file, parses
        its contents using the Fluent library, and returns a FluentDictionary object containing the parsed
        messages from the file.
        """

        with open(path, "r", encoding="utf-8") as file:
            try:
                resource = parse(file.read())
            except ParseError:
                cprint(f"An error occurred while parsing {language_code} from {path}")

        messages: Dict[str, FluentMessage] = {}

        for entry in resource.body:
            if isinstance(entry, ast.Message):
                if messages.get(entry.id.name):
                    print(colored(f"DICT({language_code}):"), f"Found duplicate for {entry.id.name}")

                messages[entry.id.name] = FluentMessage(
                    placeables=self.__get_entry_placeables(entry=entry),
                )

        return FluentDictionary(
            language_code=language_code, path=path, messages=messages
        )

    def parse_by_config(self, config: ScannerConfig) -> Dict[str, FluentDictionary]:
        """
        The `parse_by_config` function parses multiple Fluent dictionaries based on a given configuration.
        """

        dictionaries: Dict[str, FluentDictionary] = {}

        for language_code in config.dictionaries:
            path: str = config.dictionaries[language_code]
            dictionaries[language_code] = self.parse_by_file(
                path=path, language_code=language_code
            )

        return dictionaries
