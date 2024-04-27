# Libraries
from colorama import Fore, Style


# Define the Messages class
class Messages:
    # Constants
    SUCCESS_SYMBOL = "✔"
    FAILURE_SYMBOL = "✘"
    WARNING_SYMBOL = "⚠"
    INFO_SYMBOL = "ℹ"

    # Constructor
    def __init__(self, verbose: bool = True) -> None:
        self.verbose = verbose

    # Methods for displaying messages
    def show_message(self, message: str, symbol: str, color: str) -> None:
        if self.verbose:
            print(f"{color}[{symbol}] {message}{Style.RESET_ALL}")

    def show_info(self, message: str) -> None:
        self.show_message(message, self.INFO_SYMBOL, Fore.WHITE)

    def show_success(self, message: str) -> None:
        self.show_message(message, self.SUCCESS_SYMBOL, Fore.GREEN)

    def show_warning(self, message: str) -> None:
        self.show_message(message, self.WARNING_SYMBOL, Fore.YELLOW)

    def show_error(self, message: str) -> None:
        self.show_message(message, self.FAILURE_SYMBOL, Fore.RED)
