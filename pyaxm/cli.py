import sys
import pandas as pd
import typer
from pyaxm.client import Client
from pyaxm.abm_requests import DeviceError

app = typer.Typer()
client = Client()

@app.command()
def devices():
    """List all devices in the organization."""
    df = pd.DataFrame(client.list_devices())
    df.to_csv(sys.stdout, index=False)

@app.command()
def device(device_id: str):
    """Get a device by ID."""
    try:
        df = pd.DataFrame([client.get_device(device_id)])
        df.to_csv(sys.stdout, index=False)
    except DeviceError as e:
        typer.echo(e)

@app.command()
def mdm_servers():
    """List all MDM servers."""
    df = pd.DataFrame(client.list_mdm_servers())
    df.to_csv(sys.stdout, index=False)

@app.command()
def mdm_server(server_id: str):
    """List devices in a specific MDM server."""
    df = pd.DataFrame(client.list_devices_in_mdm_server(server_id))
    df.to_csv(sys.stdout, index=False)

@app.command()
def mdm_server_assigned(device_id: str):
    """Get the server assignment for a device."""
    try:
        df = pd.DataFrame([client.get_device_server_assignment(device_id)])
        df.to_csv(sys.stdout, index=False)
    except DeviceError as e:
        typer.echo(e)

@app.command()
def assign_device(device_id: str, server_id: str):
    """Assign a device to an MDM server."""
    df = pd.DataFrame([client.assign_unassign_device_to_mdm_server(device_id, server_id, 'ASSIGN_DEVICES')])
    df.to_csv(sys.stdout, index=False)

@app.command()
def unassign_device(device_id: str, server_id: str):
    """Unassign a device from an MDM server."""
    df = pd.DataFrame([client.assign_unassign_device_to_mdm_server(device_id, server_id, 'UNASSIGN_DEVICES')])
    df.to_csv(sys.stdout, index=False)

if __name__ == "__main__":
    app()
