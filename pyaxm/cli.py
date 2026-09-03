import sys
from datetime import datetime, timezone

import pandas as pd
import typer
import yaml
from typing_extensions import Annotated
from typing import List, Optional
from pyaxm.client import Client
from pyaxm.utils import download_activity_csv

app = typer.Typer()


def _output(data, format: str):
    """Output data as YAML or CSV to stdout."""
    if format == "csv":
        if isinstance(data, dict):
            data = [data]
        df = pd.DataFrame(data)
        df.to_csv(sys.stdout, index=False)
    else:
        yaml.dump(data, sys.stdout, default_flow_style=False)


def _parse_audit_timestamp(value: str, *, end_of_day: bool = False) -> str:
    """Parse a date/timestamp argument.

    Accepts YYYY-MM-DD or full ISO 8601 datetimes (with or without a trailing Z).
    Date-only values are converted to UTC start/end of day.
    """
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise typer.BadParameter(
            "Invalid date/time format. Use YYYY-MM-DD or ISO 8601 like 2025-12-31 or 2025-12-31T23:59:59Z."
        )

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)

    if end_of_day and len(value) == 10:
        parsed = parsed.replace(hour=23, minute=59, second=59, microsecond=0)

    return parsed.isoformat().replace("+00:00", "Z")


def _run_device_activity(activity, format: str):
    """Output an org device activity result and download its CSV report."""
    info = {"id": activity.id}
    if activity.attributes:
        info.update(activity.attributes.model_dump())

    _output(info, format)

    file_path = download_activity_csv(activity)
    if not file_path:
        status = activity.attributes.status if activity.attributes else "UNKNOWN"
        typer.echo(
            f"No report is available for activity {activity.id} (status: {status}). "
            "The activity may still be pending or its report is not ready yet. "
            "Check the Apple Business Manager console for the activity results.",
            err=True,
        )


# ── device commands ─────────────────────────────────────────────────


@app.command()
def devices(
    format: Annotated[str, typer.Option("--format", help="Output format")] = "yaml",
):
    """List all devices in the organization."""
    client = Client()
    devices = client.list_devices()
    records = []
    for d in devices:
        info = {"id": d.id}
        info.update(d.attributes.model_dump())
        records.append(info)

    _output(records, format)


@app.command()
def device(
    device_id: Annotated[str, typer.Argument()],
    format: Annotated[str, typer.Option("--format", help="Output format")] = "yaml",
):
    """Get a device by ID."""
    client = Client()
    d = client.get_device(device_id)
    info = {"id": d.id}
    if d.attributes:
        info.update(d.attributes.model_dump())

    _output(info, format)


@app.command()
def apple_care_coverage(
    device_id: Annotated[str, typer.Argument()],
    format: Annotated[str, typer.Option("--format", help="Output format")] = "yaml",
):
    """Get AppleCare coverage for a device."""
    client = Client()
    coverage = client.get_apple_care_coverage(device_id)
    records = [{"id": item.id, **item.attributes.model_dump()} for item in coverage]

    _output(records, format)


# ── MDM server commands ─────────────────────────────────────────────


@app.command()
def mdm_servers(
    format: Annotated[str, typer.Option("--format", help="Output format")] = "yaml",
):
    """List all MDM servers."""
    client = Client()
    servers = client.list_mdm_servers()
    records = []
    for s in servers:
        info = {"id": s.id}
        info.update(s.attributes.model_dump())
        records.append(info)

    _output(records, format)


@app.command()
def mdm_server(
    server_id: Annotated[str, typer.Argument()],
    format: Annotated[str, typer.Option("--format", help="Output format")] = "yaml",
):
    """List devices in a specific MDM server."""
    client = Client()
    devices = client.list_devices_in_mdm_server(server_id)
    records = [{"id": d.id} for d in devices]

    _output(records, format)


@app.command()
def mdm_server_assigned(
    device_id: Annotated[str, typer.Argument()],
    format: Annotated[str, typer.Option("--format", help="Output format")] = "yaml",
):
    """Get the server assignment for a device."""
    client = Client()
    assignment = client.get_device_server_assignment(device_id)
    info = {"id": assignment.id}

    _output(info, format)


@app.command()
def assign_device(
    device_ids: Annotated[List[str], typer.Argument()],
    server_id: Annotated[str, typer.Argument()],
    deadline: Annotated[
        Optional[str],
        typer.Option(
            "--deadline",
            help="Migration deadline: YYYY-MM-DD or ISO 8601 (e.g. 2026-03-15 or "
            "2026-03-15T17:00:00.000Z), max 90 days in the future. When set, devices are "
            "assigned with an MDM migration deadline.",
        ),
    ] = None,
    format: Annotated[str, typer.Option("--format", help="Output format")] = "yaml",
):
    """Assign one or more devices to an MDM server."""
    client = Client()
    action = "ASSIGN_DEVICES_WITH_MDM_MIGRATION_DEADLINE" if deadline else "ASSIGN_DEVICES"
    activity = client.assign_unassign_device_to_mdm_server(
        device_ids,
        server_id,
        action,
        mdm_migration_deadline_date_time=_parse_audit_timestamp(deadline) if deadline else None,
    )
    _run_device_activity(activity, format)


@app.command()
def unassign_device(
    device_ids: Annotated[List[str], typer.Argument()],
    server_id: Annotated[str, typer.Argument()],
    format: Annotated[str, typer.Option("--format", help="Output format")] = "yaml",
):
    """Unassign one or more devices from an MDM server."""
    client = Client()
    activity = client.assign_unassign_device_to_mdm_server(device_ids, server_id, "UNASSIGN_DEVICES")
    _run_device_activity(activity, format)


@app.command()
def update_mdm_migration_deadline(
    device_ids: Annotated[List[str], typer.Argument()],
    deadline: Annotated[
        str,
        typer.Argument(
            help="Migration deadline: YYYY-MM-DD or ISO 8601 (e.g. 2026-03-15 or "
            "2026-03-15T17:00:00.000Z), max 90 days in the future."
        ),
    ],
    format: Annotated[str, typer.Option("--format", help="Output format")] = "yaml",
):
    """Update the MDM migration deadline for one or more devices."""
    client = Client()
    activity = client.assign_unassign_device_to_mdm_server(
        device_ids,
        None,
        "UPDATE_MDM_MIGRATION_DEADLINE",
        mdm_migration_deadline_date_time=_parse_audit_timestamp(deadline),
    )
    _run_device_activity(activity, format)


@app.command()
def cancel_mdm_migration(
    device_ids: Annotated[List[str], typer.Argument()],
    format: Annotated[str, typer.Option("--format", help="Output format")] = "yaml",
):
    """Cancel an in-progress MDM migration for one or more devices."""
    client = Client()
    activity = client.assign_unassign_device_to_mdm_server(device_ids, None, "CANCEL_MDM_MIGRATION")
    _run_device_activity(activity, format)


@app.command()
def release_device(
    device_ids: Annotated[List[str], typer.Argument()],
    format: Annotated[str, typer.Option("--format", help="Output format")] = "yaml",
):
    """Release one or more devices from the organization."""
    client = Client()
    activity = client.release_devices(device_ids)
    _run_device_activity(activity, format)


# ── audit events ────────────────────────────────────────────────────


@app.command()
def audit_events(
    start_timestamp: Annotated[
        str,
        typer.Argument(
            ...,
            help="Start date in YYYY-MM-DD or ISO 8601 format. Date-only values are treated as midnight UTC.",
        ),
    ],
    end_timestamp: Annotated[
        str,
        typer.Argument(
            ...,
            help="End date in YYYY-MM-DD or ISO 8601 format. Date-only values are treated as end of day UTC.",
        ),
    ],
    actor_id: Annotated[Optional[str], typer.Option("--actor-id", "-a")] = None,
    subject_id: Annotated[Optional[str], typer.Option("--subject-id", "-s")] = None,
    event_type: Annotated[Optional[str], typer.Option("--event-type", "-e")] = None,
    limit: Annotated[Optional[int], typer.Option("--limit", "-l")] = None,
    fields: Annotated[Optional[List[str]], typer.Option("--fields", "-f")] = None,
    cursor: Annotated[Optional[str], typer.Option("--cursor", "-c")] = None,
    format: Annotated[str, typer.Option("--format", help="Output format")] = "yaml",
):
    """Get a list of audit events."""
    start_timestamp = _parse_audit_timestamp(start_timestamp, end_of_day=False)
    end_timestamp = _parse_audit_timestamp(end_timestamp, end_of_day=True)
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

    _output(records, format)


# ── user commands ───────────────────────────────────────────────────


@app.command()
def users(
    format: Annotated[str, typer.Option("--format", help="Output format")] = "yaml",
):
    """List all users in the organization."""
    client = Client()
    users = client.list_users()
    records = []
    for u in users:
        info = {"id": u.id}
        info.update(u.attributes.model_dump())
        records.append(info)

    _output(records, format)


@app.command()
def user(
    user_id: Annotated[str, typer.Argument()],
    format: Annotated[str, typer.Option("--format", help="Output format")] = "yaml",
):
    """Get a user by ID."""
    client = Client()
    item = client.get_user(user_id)
    info = {"id": item.id}
    if item.attributes:
        info.update(item.attributes.model_dump())

    _output(info, format)


if __name__ == "__main__":
    app()
