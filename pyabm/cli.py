from client import Client
import sys

if not len(sys.argv) > 1:
    print("Usage: python cli.py <command> [<args>]")
    print("Available commands: device")
    exit(1)

if sys.argv[1] not in ["device"]:
    print("Invalid command. Available commands: device")
    exit(1)

client = Client()

if sys.argv[1] == "device":
    if len(sys.argv) < 3:
        print("Usage: python cli.py device <device_id>")
        exit(1)
    device_id = sys.argv[2]
    device = client.get_device(device_id)
    print(device)
