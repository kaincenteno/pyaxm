import sys
import pandas as pd
import typer
from typing_extensions import Annotated
from typing import List, Optional
from pyaxm.client import Client
from pyaxm.utils import download_activity_csv

app = typer.Typer()


# ── device commands ─────────────────────────────────────────────────


@app.command()
def devices():
    """List all devices in the organization."""
    client = Client()
    devices = client.list_devices()
    records = []
    for d in devices:
        info = {"id": d.id}
        info.update(d.attributes.model_dump())
        records.append(info)
    df = pd.DataFrame(records)
    df.to_csv(sys.stdout, index=False)


@app.command()
def device(device_id: Annotated[str, typer.Argument()]):
    """Get a device by ID."""
    client = Client()
    d = client.get_device(device_id)
    info = {"id": d.id}
    if d.attributes:
        info.update(d.attributes.model_dump())
    df = pd.DataFrame([info])
    df.to_csv(sys.stdout, index=False)


@app.command()
def apple_care_coverage(device_id: Annotated[str, typer.Argument()]):
    """Get AppleCare coverage for a device."""
    client = Client()
    coverage = client.get_apple_care_coverage(device_id)
    records = [{"id": item.id, **item.attributes.model_dump()} for item in coverage]
    df = pd.DataFrame(records)
    df.to_csv(sys.stdout, index=False)


# ── MDM server commands ─────────────────────────────────────────────


@app.command()
def mdm_servers():
    """List all MDM servers."""
    client = Client()
    servers = client.list_mdm_servers()
    records = []
    for s in servers:
        info = {"id": s.id}
        info.update(s.attributes.model_dump())
        records.append(info)
    df = pd.DataFrame(records)
    df.to_csv(sys.stdout, index=False)


@app.command()
def mdm_server(server_id: Annotated[str, typer.Argument()]):
    """List devices in a specific MDM server."""
    client = Client()
    devices = client.list_devices_in_mdm_server(server_id)
    records = [{"id": d.id} for d in devices]
    df = pd.DataFrame(records)
    df.to_csv(sys.stdout, index=False)


@app.command()
def mdm_server_assigned(device_id: Annotated[str, typer.Argument()]):
    """Get the server assignment for a device."""
    client = Client()
    assignment = client.get_device_server_assignment(device_id)
    records = [{"id": assignment.id}]
    df = pd.DataFrame(records)
    df.to_csv(sys.stdout, index=False)


@app.command()
def assign_device(
    device_ids: Annotated[List[str], typer.Argument()],
    server_id: Annotated[str, typer.Argument()],
):
    """Assign one or more devices to an MDM server."""
    client = Client()
    activity = client.assign_unassign_device_to_mdm_server(device_ids, server_id, "ASSIGN_DEVICES")
    info = {"id": activity.id}
    if activity.attributes:
        info.update(activity.attributes.model_dump())
    df = pd.DataFrame([info])
    df.to_csv(sys.stdout, index=False)

    file_path = download_activity_csv(activity)
    if file_path:
        typer.echo(f"Report downloaded successfully to: {file_path}")


@app.command()
def unassign_device(
    device_ids: Annotated[List[str], typer.Argument()],
    server_id: Annotated[str, typer.Argument()],
):
    """Unassign one or more devices from an MDM server."""
    client = Client()
    activity = client.assign_unassign_device_to_mdm_server(device_ids, server_id, "UNASSIGN_DEVICES")
    info = {"id": activity.id}
    if activity.attributes:
        info.update(activity.attributes.model_dump())
    df = pd.DataFrame([info])
    df.to_csv(sys.stdout, index=False)

    file_path = download_activity_csv(activity)
    if file_path:
        typer.echo(f"Report downloaded successfully to: {file_path}")


# ── audit events ────────────────────────────────────────────────────


@app.command()
def audit_events(
    start_timestamp: Annotated[str, typer.Argument()],
    end_timestamp: Annotated[str, typer.Argument()],
    actor_id: Annotated[Optional[str], typer.Option("--actor-id", "-a")] = None,
    subject_id: Annotated[Optional[str], typer.Option("--subject-id", "-s")] = None,
    event_type: Annotated[Optional[str], typer.Option("--event-type", "-e")] = None,
    limit: Annotated[Optional[int], typer.Option("--limit", "-l")] = None,
    fields: Annotated[Optional[List[str]], typer.Option("--fields", "-f")] = None,
    cursor: Annotated[Optional[str], typer.Option("--cursor", "-c")] = None,
):
    """Get a list of audit events."""
    client = Client()
    events = client.get_audit_events(
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        actor_id=actor_id,
        subject_id=subject_id,
        event_type=event_type,
        limit=limit,
        fields=fields,
        cursor=cursor,
    )
    records = []
    for event in events:
        info = {"id": event.id}
        info.update(event.attributes.model_dump())
        records.append(info)
    df = pd.DataFrame(records)
    df.to_csv(sys.stdout, index=False)


# ── user commands ───────────────────────────────────────────────────


@app.command()
def users():
    """List all users in the organization."""
    client = Client()
    users = client.list_users()
    records = []
    for u in users:
        info = {"id": u.id}
        info.update(u.attributes.model_dump())
        records.append(info)
    df = pd.DataFrame(records)
    df.to_csv(sys.stdout, index=False)


@app.command()
def user(user_id: Annotated[str, typer.Argument()]):
    """Get a user by ID."""
    client = Client()
    item = client.get_user(user_id)
    info = {"id": item.id}
    if item.attributes:
        info.update(item.attributes.model_dump())
    df = pd.DataFrame([info])
    df.to_csv(sys.stdout, index=False)


if __name__ == "__main__":
    app()
