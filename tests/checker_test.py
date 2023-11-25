import os
import unittest

from python_fluent_scanner.utils.cache import ScannerCache
from python_fluent_scanner.utils.config import ConfigReader
from python_fluent_scanner.fluent_reader import FluentReader
from python_fluent_scanner.types.enums import FluentPlaceableTypes
from python_fluent_scanner.types.models import (
    ScannerConfig,
    FluentDictionary,
    FluentMessage,
    FluentPlaceable,
)


class TestCheck(unittest.TestCase):
    TEST_DICTIONARY_DATA: str = (
        "a = alksjdf\n"
        "b = { $var_b }\n"
        "c = { $var_c ->\n"
        "[one] one_text\n"
        "*[other] other_text\n"
        "}"
    )

    def test_cache(self):
        """
        The `test_cache` function tests the functionality of the `ScannerCache` class by setting a
        dictionary in the cache and then retrieving it.
        """
        dictionary: FluentDictionary = FluentDictionary(
            language_code="en",
            path="en.ftl",
            messages={
                "a": FluentMessage(placeables={}),
                "b": FluentMessage(
                    placeables={
                        "select": FluentPlaceable(
                            placeable_type=FluentPlaceableTypes.SELECT_EXPRESSION
                        )
                    }
                ),
            },
        )
        cache = ScannerCache()
        cache.set(dictionary)

        assert dictionary == cache.get(language_code=dictionary.language_code)

        os.rmdir(".fluent_scanner_cache")

    def test_config_reader(self) -> ScannerConfig:
        """
        The function `test_config_reader` writes test data to files and uses the `ConfigReader` class to
        read and retrieve a `ScannerConfig` object.
        """
        with open("test_dict_file.ftl", "w") as file:
            file.write(self.TEST_DICTIONARY_DATA)

        config: ScannerConfig = ScannerConfig(
            root_locale="en",
            dictionaries={
                "en": "test_dict_file.ftl"
            }
        )
        with open("testconfigconfig.json", "w") as file:
            file.write(config.model_dump_json())

        config = ConfigReader(config_filename="testconfigconfig.json").get_config()

        os.remove("test_dict_file.ftl")
        os.remove("testconfigconfig.json")

    def test_reader(self) -> FluentDictionary:
        """
        The `test_reader` function creates a test Fluent dictionary file, configures a FluentReader with the
        file, parses the dictionary using the reader, and then removes the test file.
        """
        with open("test_dict_file.ftl", "w") as file:
            file.write(self.TEST_DICTIONARY_DATA)

        config: ScannerConfig = ScannerConfig(
            root_locale="en",
            dictionaries={
                "en": "test_dict_file.ftl"
            }
        )

        reader: FluentReader = FluentReader()
        dictionaries = reader.parse_by_config(config)

        assert dictionaries

        os.remove("test_dict_file.ftl")

if __name__ == "__main__":
    unittest.main()
