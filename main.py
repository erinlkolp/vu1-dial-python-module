#!/usr/bin/env python3

import os
import requests
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

LOGGER = logging.getLogger(__name__)


class VUMeter:
    def __init__(self, server_address: str, server_port: int, api_key: str):
        """
        Initialize the class with a base string.
        
        :param query: str, a sql query with proper syntax.
        :return True: bool, returns True if the insert is completed.
        """
        self.server_url = f'http://{server_address}:{server_port}'
        self.key        = api_key

    def set_dial_value(self, uuid: str, value: int) -> str:
        """
        This function executes and commits a mysql insert function.

        :param query: str, a sql query with proper syntax.
        :return True: bool, returns True if the insert is completed.
        """
        api_uri = f'/api/v0/dial/{uuid}/set'

        try:
            r = requests.get(f'{self.server_url}/{api_uri}?key={self.key}&value={value}')
        except Exception as exc:
            LOGGER.error("Insertion has encountered an error: %s", exc)
            return False

        return r.text

    def set_dial_color(self, uuid: str, red: int, green: int, blue: int) -> str:
        """
        This function executes and commits a mysql insert function.

        :param query: str, a sql query with proper syntax.
        :return True: bool, returns True if the insert is completed.
        """

        api_uri = f'/api/v0/dial/{uuid}/backlight'

        try:
            r = requests.get(f'{self.server_url}/{api_uri}?key={self.key}&red={red}&green={green}&blue={blue}')
        except Exception as exc:
            LOGGER.error("Insertion has encountered an error: %s", exc)
            return False

        return r.text

if __name__ == "__main__":
    while True:
        dial_uuid    = os.environ['TARGET_DIAL_UID']
        server_key     = os.environ['API_KEY']
        srv_address = os.environ['VU1_SERVER_ADDRESS']
        srv_port    = os.environ['VU1_SERVER_PORT']

        vu_meter  = VUMeter(srv_address, srv_port, server_key)
        result = vu_class.hello_world()
        LOGGER.info("Response: %s", result)
