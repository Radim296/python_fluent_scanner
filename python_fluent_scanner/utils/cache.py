from genericpath import isdir
import os
from typing import Optional

from pydantic import ValidationError

from python_fluent_scanner.types.models import FluentDictionary


class ScannerCache:
    __cache_folder_path: str

    def __init__(self) -> None:
        """
        The function initializes a class instance with a private variable representing the path to a cache
        folder.
        """
        self.__cache_folder_path = f"{os.getcwd()}/.fluent_scanner_cache/"
        self.__create_cache_folder()

    def __create_cache_folder(self) -> None:
        """
        The function creates a cache folder if it does not already exist.
        """
        if not os.path.isdir(self.__cache_folder_path):
            os.mkdir(self.__cache_folder_path)

    def __get_dictionary_cache_path(self, language_code: str) -> str:
        """
        The function returns the file path for a dictionary cache file based on the given language code.

        :param language_code: The `language_code` parameter is a string that represents the code for a
        specific language. It is used to generate a unique cache path for a dictionary file associated with
        that language
        :type language_code: str
        :return: a string that represents the path to a dictionary cache file. The path is constructed by
        concatenating the `__cache_folder_path` attribute with the `language_code` parameter and the file
        extension ".json".
        """
        return f"{self.__cache_folder_path}{language_code}.json"

    def set(self, dictionary: FluentDictionary) -> None:
        """
        The function saves the state of a FluentDictionary object to a file.

        :param dictionary: The `dictionary` parameter is an instance of the `FluentDictionary` class
        :type dictionary: FluentDictionary
        """
        with open(
            self.__get_dictionary_cache_path(language_code=dictionary.language_code),
            "w",
        ) as file:
            file.write(dictionary.model_dump_json(indent=True))

    def delete(self, language_code: str) -> None:
        """
        The `delete` function deletes a dictionary file based on the provided language code.

        :param language_code: The `language_code` parameter is a string that represents the code of the
        language for which the dictionary is being deleted
        :type language_code: str
        """
        path: str = self.__get_dictionary_cache_path(language_code=language_code)

        if os.path.isfile(path):
            os.remove(path)
        else:
            raise ValueError(f"The dictionary by {language_code} does not exist")

    def get(self, language_code: str) -> Optional[FluentDictionary]:
        """
        The `get` function retrieves a FluentDictionary object from a cache file, and if the file does not
        exist or is invalid, it deletes the cache file.

        :param language_code: The `language_code` parameter is a string that represents the code of the
        language for which we want to retrieve the FluentDictionary
        :type language_code: str
        :return: The method is returning an instance of `FluentDictionary` if the file at the specified path
        exists and can be successfully parsed as JSON. If the file does not exist or cannot be parsed,
        `None` is returned.
        """
        path: str = self.__get_dictionary_cache_path(language_code=language_code)

        if os.path.isfile(path):
            with open(path) as file:
                try:
                    return FluentDictionary.model_validate_json(file.read())
                except ValidationError:
                    self.delete(language_code=language_code)
