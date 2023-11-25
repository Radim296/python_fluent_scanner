from copy import copy
from typing import Dict, List, Optional

from termcolor import colored, cprint
from python_fluent_scanner.utils.cache import ScannerCache
from python_fluent_scanner.utils.config import ConfigReader
from python_fluent_scanner.fluent_reader import FluentReader
from python_fluent_scanner.types.models import (
    ScannerConfig,
    FluentDictionary,
    FluentMessage,
    FluentPlaceable,
)


class FluentScanner:
    __config: ScannerConfig
    __dictionaries: Dict[str, FluentDictionary]

    def __init__(self) -> None:
        """
        The function initializes an object by loading configuration and dictionaries.
        """
        self.__load_config()
        self.__load_dictionaries()

    def __load_config(self):
        """
        The function loads a configuration file using a ConfigReader object and assigns the configuration to
        a class variable.
        """
        config_reader: ConfigReader = ConfigReader()
        self.__config = config_reader.get_config()

    def __load_dictionaries(self):
        """
        The function loads dictionaries using a FluentReader object and a configuration.
        """
        fluent_reader: FluentReader = FluentReader()
        self.__dictionaries = fluent_reader.parse_by_config(config=self.__config)

    def __is_root_dictionary_changed(self) -> bool:
        """
        The function checks if the root dictionary has been changed by comparing it with the saved state in
        the cache.
        :return: a boolean value. It returns True if the root dictionary has changed since it was last saved
        in the cache, and False if it has not changed.
        """
        cache: ScannerCache = ScannerCache()

        saved_root_dictionary_state: Optional[FluentDictionary] = cache.get(
            language_code=self.__config.root_locale
        )
        root_dictionary: FluentDictionary = self.__dictionaries[
            self.__config.root_locale
        ]

        if saved_root_dictionary_state:
            if saved_root_dictionary_state == root_dictionary:
                return False
            else:
                return True
        else:
            return True

    def __print_error(self, message: str, dictionary: FluentDictionary) -> None:
        print(colored(f"DICT({dictionary.language_code}):", "red"), message)

    def __check_placeables(
        self, message_name: str, dict_a: FluentDictionary, dict_b: FluentDictionary
    ) -> bool:
        """
        The function `__check_placeables` compares the placeables in two Fluent dictionaries and checks for
        any errors or mismatches.

        :param message_name: The `message_name` parameter is a string that represents the name of a message
        :type message_name: str
        :param dict_a: `dict_a` is an instance of the `FluentDictionary` class. It represents a dictionary
        of Fluent messages, where each message is identified by a unique name and contains a collection of
        placeables
        :type dict_a: FluentDictionary
        :param dict_b: `dict_b` is an instance of the `FluentDictionary` class
        :type dict_b: FluentDictionary
        :return: a boolean value indicating whether any errors were found during the comparison of
        placeables between two Fluent dictionaries.
        """
        is_error_found: bool = False

        message_a: FluentMessage = dict_a.messages[message_name]
        message_b: FluentMessage = dict_b.messages[message_name]

        message_b_placeables: Dict[str, FluentPlaceable] = copy(message_b.placeables)

        for placeable_name in message_a.placeables:
            placeable_a: FluentPlaceable = message_a.placeables[placeable_name]

            if placeable_b := message_b_placeables.get(placeable_name):
                message_b_placeables.pop(placeable_name)
                if placeable_b.placeable_type != placeable_a.placeable_type:
                    is_error_found = True
                    self.__print_error(
                        f"in message `{message_name}` placeable `{placeable_name}` types mismatch ({placeable_a.placeable_type.value} != {placeable_b.placeable_type.value})",
                        dictionary=dict_b,
                    )
            else:
                is_error_found = True
                self.__print_error(
                    f"in message `{message_name}` placeable `{placeable_name}` was not found",
                    dictionary=dict_b,
                )

        if message_b_placeables:
            is_error_found = True
            self.__print_error(
                f"in message `{message_name}` found unexpected extra placeables: {', '.join(list(message_b_placeables.keys()))}",
                dictionary=dict_b,
            )

        return is_error_found

    def __check_messages(
        self, dict_a: FluentDictionary, dict_b: FluentDictionary
    ) -> bool:
        """
        The function `__check_messages` compares two dictionaries and checks for any missing or unexpected
        messages.

        :param dict_a: FluentDictionary object representing the first dictionary of messages
        :type dict_a: FluentDictionary
        :param dict_b: The parameter `dict_b` is a FluentDictionary object
        :type dict_b: FluentDictionary
        :return: a boolean value indicating whether any errors were found during the message comparison
        process.
        """
        is_error_found: bool = False
        dict_b_messages: Dict[str, FluentMessage] = copy(dict_b.messages)

        for message_name in dict_a.messages:
            if message_name in dict_b_messages:
                dict_b_messages.pop(message_name)
                if self.__check_placeables(
                    message_name=message_name, dict_a=dict_a, dict_b=dict_b
                ):
                    if not is_error_found:
                        is_error_found = True
            else:
                is_error_found = True
                self.__print_error(
                    f"message `{message_name}` was not found", dictionary=dict_b
                )

        if dict_b_messages:
            is_error_found = True
            self.__print_error(
                f"found unexpected extra messages: {', '.join(list(dict_b_messages.keys()))}",
                dictionary=dict_b,
            )

        return is_error_found

    def __check_dictionaries(self) -> bool:
        """
        The function `__check_dictionaries` checks for errors in a collection of dictionaries and returns a
        boolean indicating whether any errors were found.
        :return: a boolean value indicating whether any errors were found during the dictionary check.
        """
        root_dictionary: FluentDictionary = self.__dictionaries[
            self.__config.root_locale
        ]

        is_error_found: bool = False

        for language_code in self.__dictionaries:
            if language_code != self.__config.root_locale:
                dictionary: FluentDictionary = self.__dictionaries[language_code]

                cprint(f"\nCHECKING DICTIONARY {language_code}:", "white")
                if not self.__check_messages(dict_a=root_dictionary, dict_b=dictionary):
                    cprint(f"✔︎ No errors found", "green")
                else:
                    if not is_error_found:
                        is_error_found = True

        return is_error_found

    def check(self) -> None:
        """
        The function checks if the root dictionary has changed and compares it with other dictionaries.
        """
        if self.__is_root_dictionary_changed():
            cprint("ℹ Root dictionary changed, comparing with others..", "yellow")

            if self.__check_dictionaries():
                cprint(
                    f"\n ℹ The state of the root dictionary not changed, you must solve the errors first",
                    "red",
                )
            else:
                cache: ScannerCache = ScannerCache()
                cache.set(
                    dictionary=self.__dictionaries[self.__config.root_locale]
                )
                cprint(f"\n✔ Dictionaries checked successfully", "green")
        else:
            cprint("✔︎ Root dictionary is up to date", "green")
