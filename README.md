The purpose of this repo is to create a python library to easily get information using the Apple Business Manager API using Python.

A CLI command is also included, `pyacm-cli`.

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
`pip install pyaxm`

## CLI:
Usage: pyaxm-cli COMMAND [ARGS]

### Commands
`devices` -> List all devices in the organization.

`device` -> Get a device by ID.

`mdm-servers` -> List all MDM servers.

`mdm-server` -> List devices in a specific MDM server.

`mdm-server-assigned` -> Get the server assignment for a device.

The data returned is on CSV format so you can store it as a CSV if needed

# Client:
Example usage:
```from pyaxm.client import Client

axm_client = Client()

devices = axm_client.list_devices()
print(devices)

device = axm_client.get_device(device_id='SERIAL_NUMBER')
print(device)

mdm_servers = axm_client.list_mdm_servers()
print(mdm_servers)

# The MDM server ID can be extracted from listing all mdm servers
mdm_server = axm_client.list_devices_in_mdm_server(server_id="MDM_SERVER_ID")
print(mdm_server)

device_assigned_server = axm_client.list_devices_in_mdm_server(device_id='SERIAL_NUMBER')
print(device_assigned_server)
```

## Issues:
* need to add tests
* not all api functionability is there

This is still a work in progress
