from python_fluent_scanner.fluent_scanner import FluentScanner


def main() -> None:
    """
    The main function creates an instance of the FluentScanner class and calls its check method.
    """
    scanner = FluentScanner()
    scanner.check()


if __name__ == "__main__":
    main()
