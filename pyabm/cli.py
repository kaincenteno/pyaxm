from pyabm.client import Client
import sys

def query_device():
    client = Client()
    if len(sys.argv) < 3:
        print("Usage: python cli.py device <device_id>")
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
        print("Usage: python cli.py mdm_server <server_id>")
        print("You can get the server_id from the 'mdm_servers' command.")
        exit(1)
    server_id = sys.argv[2]
    client = Client()
    devices = client.list_devices_in_mdm_server(server_id)
    for device in devices:
        print(device)

def main():
    if not len(sys.argv) > 1:
        print("Usage: python cli.py <command> [<args>]")
        print("Available commands: device mdm_servers mdm_server")
        exit(1)

    match sys.argv[1]:
        case "device":
            query_device()
        case "mdm_servers":
            list_mdm_servers()
        case "mdm_server":
            list_devices_in_mdm_server()
        case _:
            print("Invalid command.")
            print("Available commands: device mdm_servers mdm_server")
            exit(1)

if __name__ == "__main__":
    main()
