# APPER Solaire PV Dimmer companion

This a _custom component_ for [Home Assistant](https://www.home-assistant.io/).
This integration allows you to observe and control [APPER Solaire PV Dimmer](https://ota.apper-solaire.org/).

It was designed to be used in place of or in combination with the native MQTT support of the PV Dimmer. In addition to the state entities natively provided via MQTT, you will have access to additional entities that allow for complete configuration of the dimmer (MQTT configuration, auxiliary timers, etc.).

![GitHub release](https://img.shields.io/github/release/brenard/hass-apper-solaire-pvdimmer)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-appersolaire-pvdimmer.svg)](https://github.com/hacs/integration)

## Installation

### Using HACS

Firstly, you have to add the following custom repository :

- Repository : `https://github.com/brenard/hass-apper-solaire-pvdimmer`
- Category : _Integration_

After, click on _Explore & download repositories_, search and install _APPER Solaire PV Dimmer_
integration. Finally, go to _Settings_, _Devices & services_, click on _+ Add integration_ button
and search for _APPER Solaire PV Dimmer_.

### Manually

Put the `custom_components/appersolaire_pvdimmer` directory in your Home Assistant `custom_components` directory
and restart Home Assistant. You can now add this integration (look for _"APPER Solaire PV Dimmer"_) and provide the
IP address (or hostname) of your PV Dimmer.

**Note:** The `custom_components` directory is located in the same directory of the
`configuration.yaml`. If it doesn't exists, create it.

## Run development environment

A development environment is provided with this integration if you want to contribute. The `manage`
script at the root of the repository permit to create and start a Home Assistant docker container
with a pre-installation of this integration (linked to sources).

Start by create the container by running the command `./manage create` and start it by running
`./manage start` command. You can now access to Home Assistant web interface on
[http://localhost:8123](http://localhost:8123) and follow the initialization process of the Home
Assistant instance.

## Debugging

To enable debug log, edit the `configuration.yaml` file and locate the `logger` block. If it does not
exists, add it with the following content :

```yaml
logger:
  default: warn
  logs:
    custom_components.appersolaire_pvdimmer: debug
```

Don't forget to restart Home Assistant after.

**Note:** In development environment and you will be able to follow docker container logs by running
the `./manage logs` command.
