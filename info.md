[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]][license]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]

The component provide a Home Assistant integration for [APPER Solaire PV Dimmer](https://ota.apper-solaire.org/).

It was designed to be used in place of or in combination with the native MQTT support of the PV Dimmer. In addition to the state entities natively provided via MQTT, you will have access to additional entities that allow for complete configuration of the dimmer (MQTT configuration, auxiliary timers, etc.).

## Installation

1. Click install.
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "APPER Solaire PV Dimmer".

## Configuration is done in the UI

When adding the integration, you will have to provide :

- The IP address (or the hostname) of the PV Dimmer
- Check the case if you want to include entities also provided by the native MQTT support
- The refresh rate of the information of the PV Dimmer (default: 60 seconds)
- The timeout on requesting the PV Dimmer (default: 5 seconds)

**Note:** The provided IP address (or hostname) will be used to connect on your PV Dimmer. Please configure a static IP address (or reserved it on your DHCP configuration) to be sure it will not changed. Otherwise, you will have to reconfigure the integration in Home-Assistant on each change.

---

[commits-shield]: https://img.shields.io/github/commit-activity/y/brenard/hass-apper-solaire-pvdimmer.svg?style=for-the-badge
[commits]: https://github.com/brenard/hass-apper-solaire-pvdimmer/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[license]: https://github.com/brenard/hass-apper-solaire-pvdimmer/blob/main/LICENSE
[license-shield]: https://img.shields.io/github/license/brenard/hass-apper-solaire-pvdimmer.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40brenard-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/brenard/hass-apper-solaire-pvdimmer.svg?style=for-the-badge
[releases]: https://github.com/brenard/hass-apper-solaire-pvdimmer/releases
[user_profile]: https://github.com/brenard
