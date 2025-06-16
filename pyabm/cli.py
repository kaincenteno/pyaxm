from pyabm.client import Client
import sys

def query_device():
    client = Client()
    if sys.argv[1] == "device":
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

def main():
    if not len(sys.argv) > 1:
        print("Usage: python cli.py <command> [<args>]")
        print("Available commands: device mdm_servers")
        exit(1)

    match sys.argv[1]:
        case "device":
            query_device()
        case "mdm_servers":
            list_mdm_servers()
        case _:
            print("Invalid command. Available commands: device mdm_servers")
            exit(1)

if __name__ == "__main__":
    main()
