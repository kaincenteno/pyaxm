# `pyaxm-cli`

**Usage**:

```console
$ pyaxm-cli [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `devices`: List all devices in the organization.
* `device`: Get a device by ID.
* `apple-care-coverage`: Get AppleCare coverage for a device.
* `mdm-servers`: List all MDM servers.
* `mdm-server`: List devices in a specific MDM server.
* `mdm-server-assigned`: Get the server assignment for a device.
* `assign-device`: Assign one or more devices to an MDM server.
* `unassign-device`: Unassign one or more devices from an MDM...
* `audit-events`: Get a list of audit events.
* `users`: List all users in the organization.
* `user`: Get a user by ID.

## `pyaxm-cli devices`

List all devices in the organization.

**Usage**:

```console
$ pyaxm-cli devices [OPTIONS]
```

**Options**:

* `--format <str>`: Output format  [default: yaml]
* `--help`: Show this message and exit.

## `pyaxm-cli device`

Get a device by ID.

**Usage**:

```console
$ pyaxm-cli device [OPTIONS] {device_id}
```

**Arguments**:

* `device_id`: [required]

**Options**:

* `--format <str>`: Output format  [default: yaml]
* `--help`: Show this message and exit.

## `pyaxm-cli apple-care-coverage`

Get AppleCare coverage for a device.

**Usage**:

```console
$ pyaxm-cli apple-care-coverage [OPTIONS] {device_id}
```

**Arguments**:

* `device_id`: [required]

**Options**:

* `--format <str>`: Output format  [default: yaml]
* `--help`: Show this message and exit.

## `pyaxm-cli mdm-servers`

List all MDM servers.

**Usage**:

```console
$ pyaxm-cli mdm-servers [OPTIONS]
```

**Options**:

* `--format <str>`: Output format  [default: yaml]
* `--help`: Show this message and exit.

## `pyaxm-cli mdm-server`

List devices in a specific MDM server.

**Usage**:

```console
$ pyaxm-cli mdm-server [OPTIONS] {server_id}
```

**Arguments**:

* `server_id`: [required]

**Options**:

* `--format <str>`: Output format  [default: yaml]
* `--help`: Show this message and exit.

## `pyaxm-cli mdm-server-assigned`

Get the server assignment for a device.

**Usage**:

```console
$ pyaxm-cli mdm-server-assigned [OPTIONS] {device_id}
```

**Arguments**:

* `device_id`: [required]

**Options**:

* `--format <str>`: Output format  [default: yaml]
* `--help`: Show this message and exit.

## `pyaxm-cli assign-device`

Assign one or more devices to an MDM server.

**Usage**:

```console
$ pyaxm-cli assign-device [OPTIONS] {device_ids}... {server_id}
```

**Arguments**:

* `device_ids...`: [required]
* `server_id`: [required]

**Options**:

* `--format <str>`: Output format  [default: yaml]
* `--help`: Show this message and exit.

## `pyaxm-cli unassign-device`

Unassign one or more devices from an MDM server.

**Usage**:

```console
$ pyaxm-cli unassign-device [OPTIONS] {device_ids}... {server_id}
```

**Arguments**:

* `device_ids...`: [required]
* `server_id`: [required]

**Options**:

* `--format <str>`: Output format  [default: yaml]
* `--help`: Show this message and exit.

## `pyaxm-cli audit-events`

Get a list of audit events.

**Usage**:

```console
$ pyaxm-cli audit-events [OPTIONS] {start_timestamp} {end_timestamp}
```

**Arguments**:

* `start_timestamp`: Start date in YYYY-MM-DD or ISO 8601 format. Date-only values are treated as midnight UTC.  [required]
* `end_timestamp`: End date in YYYY-MM-DD or ISO 8601 format. Date-only values are treated as end of day UTC.  [required]

**Options**:

* `-a, --actor-id <str>`
* `-s, --subject-id <str>`
* `-e, --event-type <str>`
* `-l, --limit <int>`
* `-f, --fields <str>`
* `-c, --cursor <str>`
* `--format <str>`: Output format  [default: yaml]
* `--help`: Show this message and exit.

## `pyaxm-cli users`

List all users in the organization.

**Usage**:

```console
$ pyaxm-cli users [OPTIONS]
```

**Options**:

* `--format <str>`: Output format  [default: yaml]
* `--help`: Show this message and exit.

## `pyaxm-cli user`

Get a user by ID.

**Usage**:

```console
$ pyaxm-cli user [OPTIONS] {user_id}
```

**Arguments**:

* `user_id`: [required]

**Options**:

* `--format <str>`: Output format  [default: yaml]
* `--help`: Show this message and exit.
