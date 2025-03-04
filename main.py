import os
import requests
import time
import random
import json


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

    def list_dials(self) -> dict:
        """
        This function list the connected vu-dials.

        :return result: dict, returns the request query result.
        """
        api_uri = '/api/v0/dial/list'

        try:
            r = requests.get(f'{self.server_url}/{api_uri}?key={self.key}')
        except Exception as exc:
            raise exc

        return json.loads(r.text)
    
    def get_dial_info(self, uid: str) -> dict:
        """
        This function gets the vu-dial information.

        :param uid: str, the uid of the vu-dial.
        :return result: dict, returns the request query result.
        """
        api_uri = f'/api/v0/dial/{uid}/status'

        try:
            r = requests.get(f'{self.server_url}/{api_uri}?key={self.key}')
        except Exception as exc:
            raise exc

        return json.loads(r.text)

    def get_image_crc(self, uid: str) -> dict:
        """
        This function sets the vu-dial position.

        :param uid: str, the uid of the vu-dial.
        :return result: dict, returns the request query result.
        """
        api_uri = f'/api/v0/dial/{uid}/image/crc'

        try:
            r = requests.get(f'{self.server_url}/{api_uri}?key={self.key}')
        except Exception as exc:
            raise exc

        return json.loads(r.text)
    
    def set_dial_value(self, uid: str, value: int) -> dict:
        """
        This function sets the vu-dial position.

        :param uid: str, the uid of the vu-dial.
        :param value: int, value of dial position between 0 and 100.
        :return result: dict, returns the request query result.
        """
        api_uri = f'/api/v0/dial/{uid}/set'

        try:
            r = requests.get(f'{self.server_url}/{api_uri}?key={self.key}&value={value}')
        except Exception as exc:
            raise exc

        return json.loads(r.text)

    def set_dial_color(self, uid: str, red: int, green: int, blue: int) -> dict:
        """
        This function sets the dial color.

        :param uid: str, the uid of the vu-dial.
        :param red: int, the brightness of the red led - from 0 to 100.
        :param green: the brightness of the green led - from 0 to 100.
        :param blue: the brightness of the blue led - from 0 to 100.
        :return result: dict, returns the request query result.
        """

        api_uri = f'/api/v0/dial/{uid}/backlight'

        try:
            r = requests.get(f'{self.server_url}/{api_uri}?key={self.key}&red={red}&green={green}&blue={blue}')
        except Exception as exc:
            raise exc

        return json.loads(r.text)
    
    def set_dial_background(self, uid: str, file: str) -> dict:
        """
        This function sets the dial background image from PNG file.

        :param uid: str, the uid of the vu-dial.
        :param file: str, the full path to the file to upload. Example: '/home/user/sample.png'
        :return result: dict, returns the request query result.
        """

        api_uri = f'/api/v0/dial/{uid}/image/set'

        try:
            files = {'imgfile': open(f'{file}', 'rb')}
            r = requests.post(f'{self.server_url}/{api_uri}?key={self.key}',files=files)
        except Exception as exc:
            raise exc

        return json.loads(r.text)

if __name__ == "__main__":
    dial_uid    = os.environ['TARGET_DIAL_UID']
    server_key     = os.environ['API_KEY']
    srv_address = os.environ['VU1_SERVER_ADDRESS']
    srv_port    = os.environ['VU1_SERVER_PORT']

    while True:
        red = random.randint(0, 100)
        green = random.randint(0, 100)
        blue = random.randint(0, 100)

        value = random.randint(0, 100)

        vu_meter  = VUMeter(srv_address, srv_port, server_key)

        # result = vu_meter.set_dial_color(dial_uid, red, green, blue)
        # print(json.dumps(result))

        # result = vu_meter.set_dial_value(dial_uid, value)
        # print(json.dumps(result))
        # time.sleep(2)

        # result = vu_meter.list_dials()
        # print(json.dumps(result))

        # result = vu_meter.get_dial_info(dial_uid)
        # print(json.dumps(result))

        # result = vu_meter.get_image_crc(dial_uid)
        # print(json.dumps(result))

        result = vu_meter.set_dial_background(dial_uid, '/Users/ekolp/workspace/vu1-dial-python-module/sample.png')
        print(json.dumps(result))
