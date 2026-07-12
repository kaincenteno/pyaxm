import sys
import os
from datetime import date
import pandas as pd
import typer
from typing_extensions import Annotated
from typing import List, Optional
from pyaxm.client import Client
from pyaxm.utils import download_activity_csv
from rich.console import Console
from rich.table import Table

app = typer.Typer()
console = Console()


def build_records(items):
    """Build a list of flat dicts from API response items."""
    records = []
    for item in items:
        record = {"id": item.id}
        if hasattr(item, "attributes") and item.attributes:
            record.update(item.attributes.model_dump())
        records.append(record)
    return records


def render_output(records, fmt, output_path, cmd_name):
    """Render records as a rich table or CSV.

    Auto-switches to CSV when stdout is piped/redirected and no
    explicit format was set.
    """
    if not records:
        console.print("[yellow]No results found.[/yellow]")
        return

    columns = list(records[0].keys())
    df = pd.DataFrame(records, columns=columns)

    # --output / -o flag: save to file (auto-name inside directories)
    if output_path:
        if os.path.isdir(output_path):
            filename = f"pyaxm-{cmd_name}-{date.today().isoformat()}.csv"
            output_path = os.path.join(output_path, filename)
        df.to_csv(output_path, index=False)
        console.print(f"[green]Saved to: {output_path}[/green]")
        return

    # When piped / redirected, default to CSV for scripts
    if fmt == "table" and not sys.stdout.isatty():
        fmt = "csv"

    if fmt == "csv":
        df.to_csv(sys.stdout, index=False)
    else:
        table = Table(show_header=True, header_style="bold cyan")
        for col in columns:
            table.add_column(str(col))
        for _, row in df.iterrows():
            table.add_row(*[str(v) if pd.notna(v) else "" for v in row])
        console.print(table)


# ── global options ──────────────────────────────────────────────────


@app.callback()
def main(
    ctx: typer.Context,
    format: Annotated[str, typer.Option("--format", help="Output format: table or csv")] = "table",
    output: Annotated[
        Optional[str],
        typer.Option("--output", "-o", help="Save output to file or directory (auto-names inside directories)"),
    ] = None,
):
    """Query Apple Business Manager using Python."""
    ctx.obj = {"format": format, "output": output}


# ── device commands ─────────────────────────────────────────────────


@app.command()
def devices(ctx: typer.Context):
    """List all devices in the organization."""
    client = Client()
    records = build_records(client.list_devices())
    render_output(records, ctx.obj["format"], ctx.obj["output"], "devices")


@app.command()
def device(ctx: typer.Context, device_id: Annotated[str, typer.Argument()]):
    """Get a device by ID."""
    client = Client()
    item = client.get_device(device_id)
    record = {"id": item.id}
    if item.attributes:
        record.update(item.attributes.model_dump())
    render_output([record], ctx.obj["format"], ctx.obj["output"], "device")


@app.command()
def apple_care_coverage(ctx: typer.Context, device_id: Annotated[str, typer.Argument()]):
    """Get AppleCare coverage for a device."""
    client = Client()
    records = build_records(client.get_apple_care_coverage(device_id))
    render_output(records, ctx.obj["format"], ctx.obj["output"], "apple-care-coverage")


# ── MDM server commands ─────────────────────────────────────────────


@app.command()
def mdm_servers(ctx: typer.Context):
    """List all MDM servers."""
    client = Client()
    records = build_records(client.list_mdm_servers())
    render_output(records, ctx.obj["format"], ctx.obj["output"], "mdm-servers")


@app.command()
def mdm_server(ctx: typer.Context, server_id: Annotated[str, typer.Argument()]):
    """List devices in a specific MDM server."""
    client = Client()
    devices = client.list_devices_in_mdm_server(server_id)
    records = [{"id": d.id} for d in devices]
    render_output(records, ctx.obj["format"], ctx.obj["output"], "mdm-server")


@app.command()
def mdm_server_assigned(ctx: typer.Context, device_id: Annotated[str, typer.Argument()]):
    """Get the server assignment for a device."""
    client = Client()
    assignment = client.get_device_server_assignment(device_id)
    records = [{"id": assignment.id}]
    render_output(records, ctx.obj["format"], ctx.obj["output"], "mdm-server-assigned")


@app.command()
def assign_device(
    ctx: typer.Context,
    device_ids: Annotated[List[str], typer.Argument()],
    server_id: Annotated[str, typer.Argument()],
):
    """Assign one or more devices to an MDM server."""
    client = Client()
    activity = client.assign_unassign_device_to_mdm_server(device_ids, server_id, "ASSIGN_DEVICES")
    record = {"id": activity.id}
    if activity.attributes:
        record.update(activity.attributes.model_dump())
    render_output([record], ctx.obj["format"], ctx.obj["output"], "assign-device")

    file_path = download_activity_csv(activity)
    if file_path:
        console.print(f"[green]Report downloaded: {file_path}[/green]")


@app.command()
def unassign_device(
    ctx: typer.Context,
    device_ids: Annotated[List[str], typer.Argument()],
    server_id: Annotated[str, typer.Argument()],
):
    """Unassign one or more devices from an MDM server."""
    client = Client()
    activity = client.assign_unassign_device_to_mdm_server(device_ids, server_id, "UNASSIGN_DEVICES")
    record = {"id": activity.id}
    if activity.attributes:
        record.update(activity.attributes.model_dump())
    render_output([record], ctx.obj["format"], ctx.obj["output"], "unassign-device")

    file_path = download_activity_csv(activity)
    if file_path:
        console.print(f"[green]Report downloaded: {file_path}[/green]")


# ── audit events ────────────────────────────────────────────────────


@app.command()
def audit_events(
    ctx: typer.Context,
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
    records = build_records(events)
    render_output(records, ctx.obj["format"], ctx.obj["output"], "audit-events")


# ── user commands ───────────────────────────────────────────────────


@app.command()
def users(ctx: typer.Context):
    """List all users in the organization."""
    client = Client()
    records = build_records(client.list_users())
    render_output(records, ctx.obj["format"], ctx.obj["output"], "users")


@app.command()
def user(ctx: typer.Context, user_id: Annotated[str, typer.Argument()]):
    """Get a user by ID."""
    client = Client()
    item = client.get_user(user_id)
    record = {"id": item.id}
    if item.attributes:
        record.update(item.attributes.model_dump())
    render_output([record], ctx.obj["format"], ctx.obj["output"], "user")


if __name__ == "__main__":
    app()
