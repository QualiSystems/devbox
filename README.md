![quali](quali.png)


## Features

DevBox allows to deploy a topology as a sandbox with your code for testing, staging and production purposes.
DevBox uses standard YAML files in OASIS TOSCA format to define the topology structure.
DevBox uses Ansible for provisioning containers and virtual machines.
Currently supported container provider(s): Docker

## Prerequisites:

Python 2.7

```bash
$ pip install ansible

```


## Installation

```bash
$ pip install git+git://github.com/qualisystems/devbox.git

```


## Usage

Get list of available commands:

```bash
$ devbox
```

Get help on specific command:

```bash
$ devbox <COMMAND> --help
```


## Troubleshooting and Help

For questions, bug reports or feature requests, please refer to the [Issue Tracker](https://github.com/QualiSystems/devbox/issues).  Also, make sure you check out our [Issue Template](.github/issue_template.md).

## Contributing


All your contributions are welcomed and encouraged.  We've compiled detailed information about:

* [Contributing](.github/contributing.md)
* [Creating Pull Requests](.github/pull_request_template.md)


## License
[Apache License 2.0](https://github.com/QualiSystems/devbox/blob/master/LICENSE)
