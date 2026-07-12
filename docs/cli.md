# `pyaxm-cli`

Query Apple Business Manager using Python.

**Usage**:

```console
$ pyaxm-cli [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--format TEXT`: Output format: table or csv  [default: table]
* `-o, --output TEXT`: Save output to file or directory (auto-names inside directories)
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

* `--help`: Show this message and exit.

## `pyaxm-cli device`

Get a device by ID.

**Usage**:

```console
$ pyaxm-cli device [OPTIONS] DEVICE_ID
```

**Arguments**:

* `DEVICE_ID`: [required]

**Options**:

* `--help`: Show this message and exit.

## `pyaxm-cli apple-care-coverage`

Get AppleCare coverage for a device.

**Usage**:

```console
$ pyaxm-cli apple-care-coverage [OPTIONS] DEVICE_ID
```

**Arguments**:

* `DEVICE_ID`: [required]

**Options**:

* `--help`: Show this message and exit.

## `pyaxm-cli mdm-servers`

List all MDM servers.

**Usage**:

```console
$ pyaxm-cli mdm-servers [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `pyaxm-cli mdm-server`

List devices in a specific MDM server.

**Usage**:

```console
$ pyaxm-cli mdm-server [OPTIONS] SERVER_ID
```

**Arguments**:

* `SERVER_ID`: [required]

**Options**:

* `--help`: Show this message and exit.

## `pyaxm-cli mdm-server-assigned`

Get the server assignment for a device.

**Usage**:

```console
$ pyaxm-cli mdm-server-assigned [OPTIONS] DEVICE_ID
```

**Arguments**:

* `DEVICE_ID`: [required]

**Options**:

* `--help`: Show this message and exit.

## `pyaxm-cli assign-device`

Assign one or more devices to an MDM server.

**Usage**:

```console
$ pyaxm-cli assign-device [OPTIONS] DEVICE_IDS... SERVER_ID
```

**Arguments**:

* `DEVICE_IDS...`: [required]
* `SERVER_ID`: [required]

**Options**:

* `--help`: Show this message and exit.

## `pyaxm-cli unassign-device`

Unassign one or more devices from an MDM server.

**Usage**:

```console
$ pyaxm-cli unassign-device [OPTIONS] DEVICE_IDS... SERVER_ID
```

**Arguments**:

* `DEVICE_IDS...`: [required]
* `SERVER_ID`: [required]

**Options**:

* `--help`: Show this message and exit.

## `pyaxm-cli audit-events`

Get a list of audit events.

**Usage**:

```console
$ pyaxm-cli audit-events [OPTIONS] START_TIMESTAMP END_TIMESTAMP
```

**Arguments**:

* `START_TIMESTAMP`: [required]
* `END_TIMESTAMP`: [required]

**Options**:

* `-a, --actor-id TEXT`
* `-s, --subject-id TEXT`
* `-e, --event-type TEXT`
* `-l, --limit INTEGER`
* `-f, --fields TEXT`
* `-c, --cursor TEXT`
* `--help`: Show this message and exit.

## `pyaxm-cli users`

List all users in the organization.

**Usage**:

```console
$ pyaxm-cli users [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `pyaxm-cli user`

Get a user by ID.

**Usage**:

```console
$ pyaxm-cli user [OPTIONS] USER_ID
```

**Arguments**:

* `USER_ID`: [required]

**Options**:

* `--help`: Show this message and exit.
