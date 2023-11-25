from typing import Dict
from typing_extensions import Annotated
from pydantic import AfterValidator, BaseModel
from python_fluent_scanner.types.enums import FluentPlaceableTypes

from python_fluent_scanner.validators.config_validators import (
    validate_dictionaries_dict,
    validate_path,
)

DictionaryPath = Annotated[str, AfterValidator(validate_path)]
ScannerConfigDict = Annotated[
    Dict[str, DictionaryPath], AfterValidator(validate_dictionaries_dict)
]


class ScannerConfig(BaseModel):
    root_locale: str
    dictionaries: Dict[str, DictionaryPath]


class FluentPlaceable(BaseModel):
    placeable_type: FluentPlaceableTypes


class FluentMessage(BaseModel):
    placeables: Dict[str, FluentPlaceable]


class FluentDictionary(BaseModel):
    language_code: str
    path: str
    messages: Dict[str, FluentMessage]
