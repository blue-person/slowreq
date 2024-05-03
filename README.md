<div align="center">

# Slowreq 🦥

[![Project Status: Inactive](https://www.repostatus.org/badges/latest/inactive.svg)](https://www.repostatus.org/#inactive)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)

</div>

## Description
This Python 3 script employs HTTP requests for an HTTP flood attack, aiming to inundate a web server. Once the target is saturated with requests, rendering it incapable of responding to legitimate traffic, subsequent requests from genuine users will result in denial-of-service.

### Lite Version
For cases where the program needs to be run using only a single file, a [lite version](https://github.com/blue-person/slowsock/releases/latest/download/slowsock-lite.zip) has been created. This version compresses everything into a single file and contains only the essentials for functioning.

## Requirements
This project has been developed using Python 3.12.3. The libraries used are specified in the `requirements.txt` file.

### Library installation
To install the necessary dependencies, you can execute the following command:

```bash
pip install -r requirements.txt
```

### Operating System Compatibility
This code has been tested on Windows, Linux, and Termux. Although it has not been tested on macOS, theoretically, it should also work without issues on that system.

## License
This project is licensed under the Apache License 2.0 - please refer to the LICENSE file for more details.
