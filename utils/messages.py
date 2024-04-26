# Import libraries
from colorama import Fore, Style


# Class to handle messages
class Messages:
    # Constants
    SUCCESS_SYMBOL = "✔"
    FAILURE_SYMBOL = "✘"
    WARNING_SYMBOL = "⚠"
    INFO_SYMBOL = "ℹ"

    @staticmethod
    def show_message(message: str, symbol: str, color: str) -> None:
        print(f"{color}[{symbol}] {message}{Style.RESET_ALL}")

    @staticmethod
    def show_info(message: str) -> None:
        Messages.show_message(message, Messages.INFO_SYMBOL, Fore.BLUE)

    @staticmethod
    def show_success(message: str) -> None:
        Messages.show_message(message, Messages.SUCCESS_SYMBOL, Fore.GREEN)

    @staticmethod
    def show_warning(message: str) -> None:
        Messages.show_message(message, Messages.WARNING_SYMBOL, Fore.YELLOW)

    @staticmethod
    def show_error(message: str) -> None:
        Messages.show_message(message, Messages.FAILURE_SYMBOL, Fore.RED)
