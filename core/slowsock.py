# Import libraries
import ssl
import socket
from enum import IntEnum


# Define the Slowsock class
class Slowsock:
    # Define the slots
    __slots__ = (
        "connection",
        "encoding_format",
        "host",
        "path",
        "port",
        "referer",
        "status",
        "ssl_context",
        "timeout",
        "user_agent",
    )

    # Define the Status enum
    class Status(IntEnum):
        INACTIVE = 1
        CONNECTED = 2
        DISCONNECTED = 3
        TIMEOUT = 4
        ERROR = 4
        UNKNOWN = 5

    # Handle exceptions
    class ConnectionError(Exception):
        pass

    class UnknownError(Exception):
        pass

    class TimeoutError(Exception):
        pass

    # Constructor
    def __init__(
        self,
        host: str,
        port: int,
        timeout: int = 3,
        path: str = "/",
        user_agent: str = "Mozilla/5.0",
        referer: str = "http://example.re",
        encoding_format: str = "utf-8",
    ) -> None:
        self.host = host
        self.port = port
        self.path = path
        self.user_agent = user_agent
        self.referer = referer
        self.encoding_format = encoding_format

        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.settimeout(timeout)
        self.status = self.Status.INACTIVE
        self.ssl_context = None

        if self.port == 443:
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            self.connection = ssl_context.wrap_socket(
                self.connection, server_hostname=self.host
            )

    # Getter for the status
    def get_status(self) -> Status:
        return int(self.status)

    # Method to close the connection
    def close_connection(self, status=Status.UNKNOWN) -> None:
        self.status = status
        self.connection.close()

    # Method to send data through a socket
    def send_data(self, data: str) -> int:
        try:
            self.connection.send(data.encode(self.encoding_format))
            self.status = self.Status.CONNECTED
        except socket.error as error:
            self.close_connection()
            raise self.ConnectionError(error) from error

    # Method to initiate a connection
    def initiate_connection(self) -> None:
        headers = [
            f"GET {self.path} HTTP/1.1",
            f"Accept-Language: en-US,en;q=0.9",
            f"User-Agent: {self.user_agent}",
            f"Referer: {self.referer}",
        ]
        header = "\r\n".join(headers)

        try:
            self.connection.connect((self.host, self.port))
            self.send_data(header)
        except socket.timeout as error:
            self.close_connection(self.Status.TIMEOUT)
            raise self.TimeoutError(error) from error
        except socket.error as error:
            self.close_connection(self.Status.DISCONNECTED)
            raise self.ConnectionError(error) from error
        except Exception as error:
            self.close_connection(self.Status.ERROR)
            raise self.UnknownError(error) from error
