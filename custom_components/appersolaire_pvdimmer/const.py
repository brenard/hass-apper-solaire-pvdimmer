"""Constants for the APPER Solaire PV Dimmer integration."""

DOMAIN = "appersolaire_pvdimmer"
MANUFACTURER = "APPER Solaire"
CONF_HOST = "host"
CONF_INCLUDE_STATE_ENTITIES = "include_state_entities"
CONF_REFRESH_RATE = "refresh_rate"
CONF_TIMEOUT = "timeout"

CONF_DEFAULTS = {
    CONF_INCLUDE_STATE_ENTITIES: True,
    CONF_REFRESH_RATE: 60,
    CONF_TIMEOUT: 5,
}
TO_REDACT = {
    "password",
}
