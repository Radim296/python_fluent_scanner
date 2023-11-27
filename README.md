# 🌟 Utility for Scanning Fluent Localization Dictionaries 📚

### Features
- Analyzing dictionaries for missing keys and variables 🕵️‍♂️
- Checking for extra unnecessary keys 🚫

### How to run
#### 1. Install the package
```bash
# poetry
poetry add git+https://github.com/Radim296/python_fluent_scanner

# pip
pip install git+https://github.com/Radim296/python_fluent_scanner
```
#### 2. Create a config file `fluent_scanner_config.json`
```json
{
    "root_locale": "en",
    "dictionaries": {
        "ru": "locales/ru.ftl",
        "en": "locales/en.ftl",
        "kz": "locales/kz.ftl"
    }
}
```
#### 3. Run the scanner
```bash
fluent_scanner
```
