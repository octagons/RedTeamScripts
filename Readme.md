# Red Team Scripts
A collection of scripts to receive notifications about social engineering events via the API https://pushover.net.

## payload_watch.py
A script that watches the Apache access.log file for new access entries. It alerts the first time a new IP accesses anything on the server, and always alerts when an IP accesses your payload.
By default it is configured for HTA payloads, but ClickOnce, etc. could also be used.

## alert_beacon.py
When used in conjunction with alert_beacon.cna, this script will notify you when a new beacon arrives on your Cobalt Strike teamserver.

# Notes
- You may need to modify the path at the top oc alert_beacon.cna to reflect to the location of this cloned repository.
- Both scripts assume you have created your own app on Pushover. Place your user and app tokens in the config.yaml file.
