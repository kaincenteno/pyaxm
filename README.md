# pyaxm

A Python client library for querying the [Apple Business Manager API](https://developer.apple.com/documentation/applebusinessapi).

`pyaxm` handles authentication, token caching, and response pagination for you, and
returns strongly-typed [Pydantic](https://docs.pydantic.dev) models for every resource.
A companion command-line tool, `pyaxm-cli`, is bundled with the library for quick access
from the terminal.

## Features

- **Devices** — list all organization devices (pagination handled for you), fetch a
  device by serial number, and read its AppleCare coverage.
- **MDM servers** — list servers, list the devices assigned to a given server, and
  check which server a device is currently assigned to.
- **Device assignment** — assign/unassign devices to MDM servers, including MDM
  migration flows: assign with a migration deadline, move the deadline, or cancel an
  in-progress migration. Calls return once the activity has finished.
- **Activity reports** — completed device activities expose a downloadable CSV report.
- **Audit events** — search the audit log over a date range, with optional filters for
  actor, subject, event type, paging, and more.
- **Users** — list organization users and look up a user by ID.
- **Auth made simple** — OAuth2 client-credentials flow built on your ABM private key,
  with the access token cached on disk until it expires so you don't trip Apple's token
  rate limits.

## Installation

```bash
pip install pyaxm
```

## Authentication

Create an API client and private key in Apple Business Manager, then either configure
the environment or pass the values to the client directly.

Using environment variables:

- `AXM_CLIENT_ID` — the ABM client ID.
- `AXM_KEY_ID` — the ABM key ID.

Place the private key at `~/.config/pyaxm/key.pem`. This directory is also where the
cached access token is stored (as `token.json`) and reused until it expires. Requesting
too many tokens in a short window can cause Apple to return HTTP 400, so caching matters.

Alternatively, configure the client explicitly:

```python
from pyaxm.client import Client

axm_client = Client(
    axm_client_id="CLIENT_ID",
    axm_key_id="KEY_ID",
    key_path="/absolute/path/to/key.pem",
    token_path="/path/to/token.json",
)
```

When the environment variables are set, `Client()` works with no arguments.

## Usage

```python
from pyaxm.client import Client
from pyaxm.utils import download_activity_csv

client = Client()

# Devices
devices = client.list_devices()                      # all pages fetched automatically
device = client.get_device(device_id="SERIAL_NUMBER")
coverage = client.get_apple_care_coverage(device_id="SERIAL_NUMBER")

# MDM servers
mdm_servers = client.list_mdm_servers()
server_devices = client.list_devices_in_mdm_server(server_id="MDM_SERVER_ID")
assigned_server = client.get_device_server_assignment(device_id="SERIAL_NUMBER")

# Assign / unassign devices to an MDM server.
# The client waits for the activity to complete before returning.
activity = client.assign_unassign_device_to_mdm_server(
    device_ids=["SERIAL_NUMBER", "ANOTHER_SERIAL_NUMBER"],
    server_id="MDM_SERVER_ID",
    action="ASSIGN_DEVICES",   # or "UNASSIGN_DEVICES"
)
print(activity.attributes.status)

# MDM migration: assign with a deadline, then update or cancel it later
client.assign_unassign_device_to_mdm_server(
    device_ids=["SERIAL_NUMBER"],
    server_id="MDM_SERVER_ID",
    action="ASSIGN_DEVICES_WITH_MDM_MIGRATION_DEADLINE",
    mdm_migration_deadline_date_time="2026-10-15T17:00:00.000Z",
)

# Audit events (optional filters: actor_id, subject_id, event_type, limit, fields, cursor)
events = client.get_audit_events(
    start_timestamp="2026-08-01",
    end_timestamp="2026-08-31",
)

# Users
users = client.list_users()
user = client.get_user(user_id="USER_ID")

# Download the CSV report produced by a completed device activity.
# The report may take a few seconds to become available after the activity completes.
report_path = download_activity_csv(activity)
```

## CLI

The `pyaxm-cli` command-line tool is installed alongside the library and mirrors these
features from the terminal, with `yaml` or `csv` output. See the
[CLI documentation](docs/cli.md) for every command, its options, and examples.

## Development

Install in editable mode to work on the source:

```bash
pip install -e .
```

The CLI reference in [docs/cli.md](docs/cli.md) is generated from the code. After
changing `pyaxm/cli.py`, regenerate it with:

```bash
typer pyaxm.cli utils docs --name pyaxm-cli --output docs/cli.md
```

A GitHub workflow checks that the generated documentation stays in sync with the CLI.
