"""Constants for the OpenEVSE PV Load Manager integration."""

DOMAIN = "openevse_pv_loadmanager"

# Config keys
CONF_NUM_STATIONS = "num_stations"

# Default MQTT topics (must match add-on publish topics)
LM_TOPIC_MODE = "loadmanager/mode"
LM_TOPIC_MODE_SET = "loadmanager/mode/set"
LM_TOPIC_TOTAL_ALLOCATED = "loadmanager/total_allocated"
LM_TOPIC_STATUS = "loadmanager/status"
LM_TOPIC_CONFIG_HYSTERESIS = "loadmanager/config/hysteresis"
LM_TOPIC_CONFIG_HYSTERESIS_SET = "loadmanager/config/hysteresis/set"
LM_TOPIC_CONFIG_RAMP_DELAY = "loadmanager/config/ramp_delay"
LM_TOPIC_CONFIG_RAMP_DELAY_SET = "loadmanager/config/ramp_delay/set"

# Per-station topics (format with station_id)
LM_TOPIC_EVSE_SETPOINT = "evse/{}/setpoint"
LM_TOPIC_EVSE_ACTUAL = "evse/{}/actual_current"
LM_TOPIC_EVSE_STATE = "evse/{}/state"
LM_TOPIC_EVSE_ENERGY = "evse/{}/energy"

# Device info
DEVICE_IDENTIFIER = "openevse_pv_loadmanager"
DEVICE_NAME = "OpenEVSE PV Load Manager"
DEVICE_MANUFACTURER = "Custom"
DEVICE_MODEL = "PV Load Manager v1.0"
