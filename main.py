#!/usr/bin/env python3

# Blah
# Blah blah.

import os
import requests

target_dial_uid    = os.environ['TARGET_DIAL_UID']
server_api_key     = os.environ['API_KEY']
vu1_server_address = os.environ['VU1_SERVER_ADDRESS']
vu1_server_port    = os.environ['VU1_SERVER_PORT']

endpoint_set_dial_value = f"/api/v0/dial/{target_dial_uid}/set"
endpoint_set_dial_color = f"/api/v0/dial/{target_dial_uid}/backlight"

current_dial_value = 35

# Kinda purple!
current_dial_color_red = 70
current_dial_color_green = 35
current_dial_color_blue = 70

payload = {'key': server_api_key, 'value': current_dial_value}

r = requests.get(f'http://{vu1_server_address}:{vu1_server_port}/{endpoint_set_dial_value}?key={server_api_key}&value={current_dial_value}')
print(r.text)

r = requests.get(f'http://{vu1_server_address}:{vu1_server_port}/{endpoint_set_dial_color}?key={server_api_key}&red={current_dial_color_red}&green={current_dial_color_green}&blue={current_dial_color_blue}')
print(r.text)

