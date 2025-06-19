from pyaxm.client import Client
import sys
import pandas as pd

def list_devices():
    client = Client()
    devices = client.list_devices()
    df = pd.DataFrame(devices)
    df.to_csv(sys.stdout, index=False)

def query_device():
    client = Client()
    if len(sys.argv) < 3:
        print("Usage: pyaxm-cli device <device_id>")
        exit(1)
    device_id = sys.argv[2]
    device = client.get_device(device_id)
    df = pd.DataFrame([device])
    df.to_csv(sys.stdout, index=False)

def list_mdm_servers():
    client = Client()
    servers = client.list_mdm_servers()
    df = pd.DataFrame(servers)
    df.to_csv(sys.stdout, index=False)

def list_devices_in_mdm_server():
    if len(sys.argv) < 3:
        print("Usage: pyaxm-cli mdm_server <server_id>")
        print("You can get the server_id from the 'mdm_servers' command.")
        exit(1)
    server_id = sys.argv[2]
    client = Client()
    devices = client.list_devices_in_mdm_server(server_id)
    df = pd.DataFrame(devices)
    df.to_csv(sys.stdout, index=False)

def get_device_server_assignment():
    client = Client()
    if len(sys.argv) < 3:
        print("Usage: pyaxm-cli mdm_server_assigned <device_id>")
        exit(1)
    device_id = sys.argv[2]
    device = client.get_device_server_assignment(device_id)
    df = pd.DataFrame([device])
    df.to_csv(sys.stdout, index=False)

def main():
    if not len(sys.argv) > 1:
        print("Usage: pyaxm-cli <command> [<args>]")
        print("Available commands: devices device mdm_servers mdm_server mdm_server_assigned")
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
        case "mdm_server_assigned":
            get_device_server_assignment()
        case _:
            print("Invalid command.")
            print("Available commands: devices device mdm_servers mdm_server mdm_server_assigned")
            exit(1)

if __name__ == "__main__":
    main()
