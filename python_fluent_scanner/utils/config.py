import json
from typing import Any, Dict

# The `FluentPlaceableTypes` class is an enumeration that represents different types of placeable
# objects.
from python_fluent_scanner.types.models import ScannerConfig
from python_fluent_scanner.validators.config_validators import validate_path


class ConfigReader:
    __config_filename: str

    def __init__(self, config_filename: str = "fluent_scanner_config.json") -> None:
        """
        The function initializes an object with a default configuration filename.

        :param config_filename: The `config_filename` parameter is a string that represents the name of the
        configuration file. By default, it is set to "fluent_scanner_config.json", defaults to
        fluent_scanner_config.json
        :type config_filename: str (optional)
        """
        self.__config_filename = config_filename

    def get_config(self) -> ScannerConfig:
        """
        The `get_config` function reads a JSON file, validates its path, and returns a `ScannerConfig`
        object.
        :return: an instance of the `ScannerConfig` class.
        """

        if path := validate_path(self.__config_filename):
            with open(path) as file:
                data: Dict[str, Any] = json.loads(file.read())
                config: ScannerConfig = ScannerConfig(**data)

                assert (
                    config.root_locale in config.dictionaries
                ), "Incorrect root locale value"

                return config
