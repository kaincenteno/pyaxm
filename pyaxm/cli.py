import sys
import pandas as pd
import typer
from typing_extensions import Annotated
from typing import List
from pyaxm.client import Client
from pyaxm.utils import download_activity_csv

app = typer.Typer()

@app.command()
def devices():
    """List all devices in the organization."""
    client = Client()
    devices = client.list_devices()
    devices_data = []
    for device in devices:
        device_info = {'id': device.id}
        device_info.update(device.attributes.model_dump())
        devices_data.append(device_info)
    df = pd.DataFrame(devices_data)
    df.to_csv(sys.stdout, index=False)

@app.command()
def device(device_id: Annotated[str, typer.Argument()]):
    """Get a device by ID."""
    client = Client()
    device = client.get_device(device_id)
    device_info = {'id': device.id}
    device_info.update(device.attributes.model_dump())
    df = pd.DataFrame([device_info])
    df.to_csv(sys.stdout, index=False)

@app.command()
def apple_care_coverage(device_id: Annotated[str, typer.Argument()]):
    """Get AppleCare coverage for a device."""
    client = Client()
    coverage = client.get_apple_care_coverage(device_id)
    coverage_data = [item.attributes.model_dump() for item in coverage]
    df = pd.DataFrame(coverage_data)
    df.to_csv(sys.stdout, index=False)

@app.command()
def mdm_servers():
    """List all MDM servers."""
    client = Client()
    servers = client.list_mdm_servers()
    servers_data = []
    for server in servers:
        server_info = {'id': server.id}
        server_info.update(server.attributes.model_dump())
        servers_data.append(server_info)
    df = pd.DataFrame(servers_data)
    df.to_csv(sys.stdout, index=False)

@app.command()
def mdm_server(server_id: Annotated[str, typer.Argument()]):
    """List devices in a specific MDM server."""
    client = Client()
    devices = client.list_devices_in_mdm_server(server_id)
    devices_data = [{'id': device.id} for device in devices]
    df = pd.DataFrame(devices_data)
    df.to_csv(sys.stdout, index=False)

@app.command()
def mdm_server_assigned(device_id: Annotated[str, typer.Argument()]):
    """Get the server assignment for a device."""
    client = Client()
    server_assignment = client.get_device_server_assignment(device_id)
    assignment_info = {'id': server_assignment.id}
    df = pd.DataFrame([assignment_info])
    df.to_csv(sys.stdout, index=False)

@app.command()
def assign_device(device_id: Annotated[List[str], typer.Argument()], server_id: Annotated[str, typer.Argument()]):
    """Assign one or more devices to an MDM server."""
    client = Client()
    activity = client.assign_unassign_device_to_mdm_server(device_id, server_id, 'ASSIGN_DEVICES')
    activity_data = {'id': activity.id}
    activity_data.update(activity.attributes.model_dump())
    df = pd.DataFrame([activity_data])
    df.to_csv(sys.stdout, index=False)

    file_path = download_activity_csv(activity)
    if file_path:
        typer.echo(f"Report downloaded successfully to: {file_path}")

@app.command()
def unassign_device(device_id: Annotated[List[str], typer.Argument()], server_id: Annotated[str, typer.Argument()]):
    """Unassign one or more devices from an MDM server."""
    client = Client()
    activity = client.assign_unassign_device_to_mdm_server(device_id, server_id, 'UNASSIGN_DEVICES')
    activity_data = {'id': activity.id}
    activity_data.update(activity.attributes.model_dump())
    df = pd.DataFrame([activity_data])
    df.to_csv(sys.stdout, index=False)
    
    file_path = download_activity_csv(activity)
    if file_path:
        typer.echo(f"Report downloaded successfully to: {file_path}")

if __name__ == "__main__":
    app()
