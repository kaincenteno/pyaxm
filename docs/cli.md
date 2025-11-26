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
$ pyaxm-cli assign-device [OPTIONS] DEVICE_ID... SERVER_ID
```

**Arguments**:

* `DEVICE_ID...`: [required]
* `SERVER_ID`: [required]

**Options**:

* `--help`: Show this message and exit.

## `pyaxm-cli unassign-device`

Unassign one or more devices from an MDM server.

**Usage**:

```console
$ pyaxm-cli unassign-device [OPTIONS] DEVICE_ID... SERVER_ID
```

**Arguments**:

* `DEVICE_ID...`: [required]
* `SERVER_ID`: [required]

**Options**:

* `--help`: Show this message and exit.
