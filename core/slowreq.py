# Libraries
import random
import grequests
import requests
from typing import Self
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


# Define the Slowreq class
class Slowreq:
    # Slots
    __slots__ = (
        "method",
        "host",
        "port",
        "timeout",
        "user_agent",
        "referer",
    )

    # Static method
    def __new__(
        cls,
        method: str,
        url: str,
        timeout: int = None,
        user_agent: str = "Mozilla/5.0",
        referer: str = "http://example.re",
    ) -> grequests.AsyncRequest:
        content_length = random.randint(1, 500)
        payload = {"x": random.randbytes(content_length)}
        headers = {
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Keep-Alive": str(random.randint(5, 1000)),
            "Content-Type": "application/json",
            "Content-Length": str(content_length),
            "Referer": referer,
        }
        match method:
            case "GET":
                return grequests.get(
                    url, headers=headers, verify=False, timeout=timeout
                )
            case "POST":
                return grequests.post(
                    url, headers=headers, data=payload, verify=False, timeout=timeout
                )
            case "PUT":
                return grequests.put(
                    url, headers=headers, data=payload, verify=False, timeout=timeout
                )
            case _:
                raise ValueError("Invalid method")

    # Method to send multiple requests concurrently
    @staticmethod
    def send_group(requests_list: list[Self], amount: int) -> grequests.AsyncRequest:
        return grequests.imap_enumerated(requests_list, size=amount)
