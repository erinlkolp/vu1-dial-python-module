import requests
import json
import logging

import os

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

LOGGER = logging.getLogger(__name__)

requests_log = logging.getLogger("requests")
requests_log.setLevel(logging.WARNING)

class VUDial:
    def __init__(self, server_address: str, server_port: int, api_key: str):
        """
        Initialize the class with required values.
        
        :param server_address: str, the server ip address.
        :param server_port: int, the vu-dial server port.
        :param api_key: str, a valid api key for the vu-dial server.
        """
        self.server_url = f'http://{server_address}:{server_port}'
        self.key        = api_key

        LOGGER.debug(f"Instantiated VU1Dial Server at {self.server_url}")

    def _get_uri(self, short_uri: str, **kwargs) -> str:
        server_version = 'v0'

        LOGGER.debug(f"VU1Dial Server version: {server_version}")
        LOGGER.debug(f"Looking up full path uri for: {short_uri}")

        if short_uri == 'dial/list':
            api_uri = f'{self.server_url}/api/{server_version}/dial/list?key={self.key}'
        elif short_uri == 'dial/info':
            api_uri = f'{self.server_url}/api/{server_version}/dial/{kwargs.get('uid')}/status?key={self.key}'
        elif short_uri == 'dial/value':
            api_uri = f'{self.server_url}/api/{server_version}/dial/{kwargs.get('uid')}/set?key={self.key}&value={kwargs.get('value')}'
        elif short_uri == 'dial/backlight':
            api_uri = f'{self.server_url}/api/{server_version}/dial/{kwargs.get('uid')}/backlight?key={self.key}&red={kwargs.get('red')}&green={kwargs.get('green')}&blue={kwargs.get('blue')}'
        elif short_uri == 'dial/crc':
            api_uri = f'{self.server_url}/api/{server_version}/dial/{kwargs.get('uid')}/image/crc?key={self.key}'
        elif short_uri == 'dial/name':
            api_uri = f'{self.server_url}/api/{server_version}/dial/{kwargs.get('uid')}/name?key={self.key}&name={kwargs.get('name')}'
        elif short_uri == 'dial/background':
            api_uri = f'{self.server_url}/api/{server_version}/dial/{kwargs.get('uid')}/image/set?key={self.key}'
        else:
            LOGGER.error(f"Lookup key not supported: {short_uri}")


        LOGGER.debug(f"Returning full path uri: {api_uri}")

        return api_uri

    def _send_http_request(self, path_uri: str, files: dict) -> dict:        
        try:
            LOGGER.debug(f"Making http request: {path_uri}")

            if files is not None:
                r = requests.post(f'{path_uri}', files=files)
            else:
                r = requests.get(f'{path_uri}')
        except Exception as exc:
            raise exc

        return r.text

    def list_dials(self) -> dict:
        """
        This function list the connected vu-dials.

        :return result: dict, returns the request query result.
        """
        uri_base  = 'dial/list'

        try:
            full_uri = self._get_uri(uri_base)
            r = self._send_http_request(full_uri, None)
        except Exception as exc:
            raise exc

        return r
        
    def get_dial_info(self, uid: str) -> dict:
        """
        This function gets the vu-dial information.

        :param uid: str, the uid of the vu-dial.
        :return result: dict, returns the request query result.
        """
        uri_base  = 'dial/info'

        try:
            full_uri = self._get_uri(uri_base, uid=f"{uid}")
            r = self._send_http_request(full_uri, None)
        except Exception as exc:
            raise exc

        return r

    def set_dial_value(self, uid: str, value: int) -> dict:
        """
        This function sets the vu-dial position.

        :param uid: str, the uid of the vu-dial.
        :param value: int, value of dial position between 0 and 100.
        :return result: dict, returns the request query result.
        """
        uri_base  = 'dial/value'

        try:
            full_uri = self._get_uri(uri_base, uid=f"{uid}", value=f"{value}")
            r = self._send_http_request(full_uri, None)
        except Exception as exc:
            raise exc

        return r

    def set_dial_color(self, uid: str, red: int, green: int, blue: int) -> dict:
        """
        This function sets the dial color.

        :param uid: str, the uid of the vu-dial.
        :param red: int, the brightness of the red led - from 0 to 100.
        :param green: the brightness of the green led - from 0 to 100.
        :param blue: the brightness of the blue led - from 0 to 100.
        :return result: dict, returns the request query result.
        """

        uri_base  = 'dial/backlight'

        try:
            full_uri = self._get_uri(uri_base, uid=f"{uid}", red=f"{red}", green=f"{green}", blue=f"{blue}")
            r = self._send_http_request(full_uri, None)
        except Exception as exc:
            raise exc

        return r

    def get_dial_image_crc(self, uid: str) -> dict:
        """
        This function gets the vu-dial image crc.

        :param uid: str, the uid of the vu-dial.
        :return result: dict, returns the request query result.
        """
        uri_base  = 'dial/crc'

        try:
            full_uri = self._get_uri(uri_base, uid=f"{uid}")
            r = self._send_http_request(full_uri, None)
        except Exception as exc:
            raise exc

        return r

    def set_dial_name(self, uid: str, name: str) -> dict:
        """
        This function sets the vu-dial name.

        :param uid: str, the uid of the vu-dial.
        :param name: str, the name of the vu-dial you wish to apply.
        :return result: dict, returns the request query result.
        """
        uri_base  = 'dial/name'

        try:
            full_uri = self._get_uri(uri_base, uid=f"{uid}", name=f"{name}")
            r = self._send_http_request(full_uri, None)
        except Exception as exc:
            raise exc

        return r

    def set_dial_background(self, uid: str, file: str) -> dict:
        """
        This function sets the dial background image from PNG file.

        :param uid: str, the uid of the vu-dial.
        :param file: str, the full path to the file to upload. Example: '/home/user/sample.png'
        :return result: dict, returns the request query result.
        """

        uri_base  = 'dial/background'

        try:
            full_uri = self._get_uri(uri_base, uid=f"{uid}")

            with open(f'{file}', 'rb') as file:
                files = {'imgfile': file}        
                r = self._send_http_request(full_uri, files)
        except Exception as exc:
            raise exc

        return r

dial_uid       = os.environ['TARGET_DIAL_UID']
server_key     = os.environ['API_KEY']
srv_address    = os.environ['VU1_SERVER_ADDRESS']
srv_port       = os.environ['VU1_SERVER_PORT']

vu_meter  = VUDial(srv_address, srv_port, server_key)

result = vu_meter.list_dials()
LOGGER.debug(f"{result}")
result = vu_meter.get_dial_info(dial_uid)
LOGGER.debug(f"{result}")
result = vu_meter.set_dial_value(dial_uid, 25)
LOGGER.debug(f"{result}")
result = vu_meter.get_dial_image_crc(dial_uid)
LOGGER.debug(f"{result}")
result = vu_meter.set_dial_name(dial_uid, "erindial")
LOGGER.debug(f"{result}")
result = vu_meter.set_dial_background(dial_uid, "/Users/ekolp/workspace/vu1-dial-python-module/image.png")
LOGGER.debug(f"{result}")
