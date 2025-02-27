#!/usr/bin/env python3

import os
import requests
import logging
import time
import random

# logging.basicConfig(
#     format='%(asctime)s %(levelname)-8s %(message)s',
#     level=logging.INFO,
#     datefmt='%Y-%m-%d %H:%M:%S')

# LOGGER = logging.getLogger(__name__)


class VUMeter:
    def __init__(self, server_address: str, server_port: int, api_key: str):
        """
        Initialize the class with required values.
        
        :param server_address: str, the server ip address.
        :param server_port: int, the vu-dial server port.
        :param api_key: str, a valid api key for the vu-dial server.

        """
        self.server_url = f'http://{server_address}:{server_port}'
        self.key        = api_key

    def list_dials(self) -> str:
        """
        This function list the connected vu-dials.

        :param uuid: str, the uuid of the vu-dial.
        :param value: int, value of dial position between 0 and 100.
        :return result: str, returns the request query result.
        """
        api_uri = '/api/v0/dial/list'

        try:
            r = requests.get(f'{self.server_url}/{api_uri}?key={self.key}')
        except Exception as exc:
            raise exc

        return r.text
    
    def get_dial_info(self, uuid: str) -> str:
        """
        This function sets the dial position.

        :param uuid: str, the uuid of the vu-dial.
        :param value: int, value of dial position between 0 and 100.
        :return result: str, returns the request query result.
        """
        api_uri = f'/api/v0/dial/{uuid}/status'

        try:
            r = requests.get(f'{self.server_url}/{api_uri}?key={self.key}')
        except Exception as exc:
            raise exc

        return r.text

    def get_image_crc(self, uuid: str) -> str:
        """
        This function sets the dial position.

        :param uuid: str, the uuid of the vu-dial.
        :param value: int, value of dial position between 0 and 100.
        :return result: str, returns the request query result.
        """
        api_uri = f'/api/v0/dial/{uuid}/image/crc'

        try:
            r = requests.get(f'{self.server_url}/{api_uri}?key={self.key}')
        except Exception as exc:
            raise exc

        return r.text
    
    def set_dial_value(self, uuid: str, value: int) -> str:
        """
        This function sets the dial position.

        :param uuid: str, the uuid of the vu-dial.
        :param value: int, value of dial position between 0 and 100.
        :return result: str, returns the request query result.
        """
        api_uri = f'/api/v0/dial/{uuid}/set'

        try:
            r = requests.get(f'{self.server_url}/{api_uri}?key={self.key}&value={value}')
        except Exception as exc:
            raise exc

        return r.text

    def set_dial_color(self, uuid: str, red: int, green: int, blue: int) -> str:
        """
        This function sets the dial color.

        :param uuid: str, the uuid of the vu-dial.
        :param red: int, the brightness of the red led - from 0 to 100.
        :param green: the brightness of the green led - from 0 to 100.
        :param blue: the brightness of the blue led - from 0 to 100.
        :return result: str, returns the request query result.
        """

        api_uri = f'/api/v0/dial/{uuid}/backlight'

        try:
            r = requests.get(f'{self.server_url}/{api_uri}?key={self.key}&red={red}&green={green}&blue={blue}')
        except Exception as exc:
            raise exc

        return r.text

# if __name__ == "__main__":
#     while True:
#         dial_uuid    = os.environ['TARGET_DIAL_UID']
#         server_key     = os.environ['API_KEY']
#         srv_address = os.environ['VU1_SERVER_ADDRESS']
#         srv_port    = os.environ['VU1_SERVER_PORT']

#         red = random.randint(0, 100)
#         green = random.randint(0, 100)
#         blue = random.randint(0, 100)

#         value = random.randint(0, 100)

#         vu_meter  = VUMeter(srv_address, srv_port, server_key)
#         result = vu_meter.set_dial_value(dial_uuid, value)
#         LOGGER.info("Response: %s", result)
#         time.sleep(1)

#         result = vu_meter.list_dials()
#         LOGGER.info("Response: %s", result)
#         time.sleep(1)

#         result = vu_meter.get_dial_info(dial_uuid)
#         LOGGER.info("Response: %s", result)
#         time.sleep(1)
                
#         result = vu_meter.get_image_crc(dial_uuid)
#         LOGGER.info("Response: %s", result)
#         time.sleep(1)
