<div align="center">

# Slowsock 🦥

[![Project Status: Inactive](https://www.repostatus.org/badges/latest/inactive.svg)](https://www.repostatus.org/#inactive)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)

</div>

## Description
This Python 3 implementation utilizes sockets for a Slowloris attack. It aims to overwhelm a web server by creating multiple HTTP requests and keeping connections open for as long as possible by periodically sending headers, preventing legitimate users from accessing the server's resources.

### Lite Version

For cases where the program needs to be run using only a single file, a `slowsock-lite` version has been created. This version compresses everything into a single file and contains only the essentials for functioning.

## Requirements
This project has been developed using Python 3.12.3. The libraries used are included in this Python version. However, in case `colorama` or `typing` libraries are not available for any reason, they are specified in the `requirements.txt` file.

### Installation Requirements

To install the necessary dependencies, you can execute the following command:

```bash
pip install -r requirements.txt
```

### Operating System Compatibility

This code has been tested on Windows, Linux, and Termux. Although it has not been tested on MacOS, theoretically, it should also work without issues on that system.

## License
This project is licensed under the Apache License 2.0 - please refer to the LICENSE file for more details.
