
# Introduction

This repo contains a simple implementation of a ModBus server & client.

# Installation

1. Ensure that you have python installed, this repo was tested with python 3.12.
2. Ensure you have poetry installed `python -m pip install poetry`
3. Install the requirements for this repository `poetry install`

# Server

Run the server with the following command

```sh
poetry run python -m modbus_simulator.server
```

This will launch the server. It has a single device (id=1) with a single 1-byte register (address=0). The server will switch between a value of 17 and 57 every 10 seconds.

# Client

The client will connect to the server and ping it every second, printing out the value it read from the server. If OBS is installed, it will start recording when the server value equals 57, and then stop recording when the server value changes - effectively the client will record while the server reports value 57.

Run the client with the following command

```sh
poetry run python -m modbus_simulator.client
```