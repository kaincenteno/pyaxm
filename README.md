The purpose of this repo is to create a python library to easily get information using the Apple Business Manager API using Python

https://developer.apple.com/documentation/applebusinessmanagerapi

## Setup:
You will need to setup 2 environmental variables that are provided
when creating the private key in ABM:

`AXM_CLIENT_ID` and `AXM_KEY_ID`

Place the private key in your home directory inside the `.config/pyaxm` folder
and rename it `key.pem`

This location will be used to store a cached access_token that can be reused
until it expires. While testing I have experienced that requesting too many
access tokens will result in a response with status code 400 when 
trying to get a new token.

## Installation:
Download the latest release and install it using

`pip install pyaxm-<date>.tar.gz`

## CLI:
You can query directly through the terminal by running `pyaxm-cli`

`pyaxm-cli devices` -> returns all devices in ABM
`pyaxm-cli servers` -> returns all servers in ABM
`pyaxm-cli device <serial_number>` -> returns single device information
`pyaxm-cli server <server_id>` -> returns all devices in that server

# Client:
Example usage:
```from pyaxm.client import Client

axm_client = Client()

devices = axm_client.list_devices()
print(devices)
``` 

## Issues:
* Pagination is not setup yet for specific server, it does paginate if querying
all abm devices.

* Data returned needs to be pretty up. Currently it is returning objects.

This is still a work in progress