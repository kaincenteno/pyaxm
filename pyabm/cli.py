from pyabm.client import Client
import sys

def list_devices():
    client = Client()
    devices = client.list_devices()
    for device in devices:
        print(device)

def query_device():
    client = Client()
    if len(sys.argv) < 3:
        print("Usage: pyabm-cli device <device_id>")
        exit(1)
    device_id = sys.argv[2]
    device = client.get_device(device_id)
    print(device)

def list_mdm_servers():
    client = Client()
    servers = client.list_mdm_servers()
    for server in servers:
        print(server)

def list_devices_in_mdm_server():
    if len(sys.argv) < 3:
        print("Usage: pyabm-cli mdm_server <server_id>")
        print("You can get the server_id from the 'mdm_servers' command.")
        exit(1)
    server_id = sys.argv[2]
    client = Client()
    devices = client.list_devices_in_mdm_server(server_id)
    for device in devices:
        print(device)

def main():
    if not len(sys.argv) > 1:
        print("Usage: pyabm-cli <command> [<args>]")
        print("Available commands: devices device mdm_servers mdm_server")
        exit(1)

    match sys.argv[1]:
        case "devices":
            list_devices()
        case "device":
            query_device()
        case "mdm_servers":
            list_mdm_servers()
        case "mdm_server":
            list_devices_in_mdm_server()
        case _:
            print("Invalid command.")
            print("Available commands: devices device mdm_servers mdm_server")
            exit(1)

if __name__ == "__main__":
    main()
