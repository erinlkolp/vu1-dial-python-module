import requests
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

LOGGER = logging.getLogger(__name__)

class VUUtil:
    def get_uri(self, server_url: str, api_key: str, api_call: str, keyword_params: str) -> str:        
        try:
            api_base = f'{server_url}/api/v0/{api_call}?key={api_key}{keyword_params}'
        except Exception as exc:
            raise exc

        return api_base

    def send_http_request(self, path_uri: str, files: dict) -> dict:      
        try:
            if files is not None:
                r = requests.post(f'{path_uri}', files=files)
            else:
                r = requests.get(f'{path_uri}')
        except Exception as exc:
            raise exc

        return r
    
class VUAdminUtil:
    def get_uri(self, server_url: str, api_key: str, api_call: str, keyword_params: str) -> str:        
        try:
            api_base = f'{server_url}/api/v0/{api_call}?admin_key={api_key}{keyword_params}'
        except Exception as exc:
            raise exc

        return api_base

    def send_http_request(self, path_uri: str, method: str) -> dict:      
        try:
            if method == "post":
                r = requests.post(f'{path_uri}')
            else:
                r = requests.get(f'{path_uri}')
        except Exception as exc:
            raise exc

        return r

class VUDial(VUUtil):
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
        api_call = 'dial/list'
        params = ''

        try:
            r_uri = self.get_uri(self.server_url, self.key, api_call, params)
            r = self.send_http_request(r_uri, None)
        except Exception as exc:
            raise exc

        return r

    def get_dial_info(self, uid: str) -> dict:
        """
        This function gets the vu-dial information.

        :param uid: str, the uid of the vu-dial.
        :return result: dict, returns the request query result.
        """
        api_call = f'dial/{uid}/status'
        params = ''

        try:
            r_uri = self.get_uri(self.server_url, self.key, api_call, params)
            r = self.send_http_request(r_uri, None)
        except Exception as exc:
            raise exc

        return r

    def set_dial_value(self, uid: str, value: int) -> dict:
        """
        This function sets the dial value.

        :param uid: str, the uid of the vu-dial.
        :return result: dict, returns the request query result.
        """
        api_call = f'dial/{uid}/set'
        params = f'&value={value}'

        try:
            r_uri = self.get_uri(self.server_url, self.key, api_call, params)
            r = self.send_http_request(r_uri, None)
        except Exception as exc:
            raise exc

        return r

    def set_dial_color(self, uid: str, red: int, green: int, blue: int) -> dict:
        """
        This function sets the dial value.

        :param uid: str, the uid of the vu-dial.
        :return result: dict, returns the request query result.
        """
        api_call = f'dial/{uid}/backlight'
        params = f'&red={red}&green={green}&blue={blue}'

        try:
            r_uri = self.get_uri(self.server_url, self.key, api_call, params)
            r = self.send_http_request(r_uri, None)
        except Exception as exc:
            raise exc

        return r

    def set_dial_background(self, file: str) -> dict:
        """
        This function sets the dial value.

        :param uid: str, the uid of the vu-dial.
        :return result: dict, returns the request query result.
        """
        api_call = f'dial/{uid}/image/set'
        params = ''

        try:
            with open(f'{file}', 'rb') as file:
                files = {'imgfile': file}

                r_uri = self.get_uri(self.server_url, self.key, api_call, params)
                r = self.send_http_request(r_uri, files)
        except Exception as exc:
            raise exc

        return r

    def get_dial_image_crc(self, uid: str) -> dict:
        """
        This function sets the dial value.

        :param uid: str, the uid of the vu-dial.
        :return result: dict, returns the request query result.
        """
        api_call = f'dial/{uid}/image/crc'
        params = ''

        try:
            r_uri = self.get_uri(self.server_url, self.key, api_call, params)
            r = self.send_http_request(r_uri, None)
        except Exception as exc:
            raise exc

        return r

    def set_dial_name(self, uid: str, name: str) -> dict:
        """
        This function sets the dial value.

        :param uid: str, the uid of the vu-dial.
        :return result: dict, returns the request query result.
        """
        api_call = f'dial/{uid}/name'
        params = f'&name={name}'

        try:
            r_uri = self.get_uri(self.server_url, self.key, api_call, params)
            r = self.send_http_request(r_uri, None)
        except Exception as exc:
            raise exc

        return r

    def reload_hw_info(self, uid: str) -> dict:
        """
        This function sets the dial value.

        :param uid: str, the uid of the vu-dial.
        :return result: dict, returns the request query result.
        """
        api_call = f'dial/{uid}/reload'
        params = ''

        try:
            r_uri = self.get_uri(self.server_url, self.key, api_call, params)
            r = self.send_http_request(r_uri, None)
        except Exception as exc:
            raise exc

        return r

    def set_dial_easing(self, uid: str, period: int, step: int) -> dict:
        """
        This function sets the dial value.

        :param uid: str, the uid of the vu-dial.
        :return result: dict, returns the request query result.
        """
        api_call = f'dial/{uid}/easing/dial'
        params = f'&period={period}&step={step}'

        try:
            r_uri = self.get_uri(self.server_url, self.key, api_call, params)
            r = self.send_http_request(r_uri, None)
        except Exception as exc:
            raise exc

        return r

    def set_backlight_easing(self, uid: str, period: int, step: int) -> dict:
        """
        This function sets the dial value.

        :param uid: str, the uid of the vu-dial.
        :return result: dict, returns the request query result.
        """
        api_call = f'dial/{uid}/easing/backlight'
        params = f'&period={period}&step={step}'

        try:
            r_uri = self.get_uri(self.server_url, self.key, api_call, params)
            r = self.send_http_request(r_uri, None)
        except Exception as exc:
            raise exc

        return r

    def get_easing_config(self, uid: str) -> dict:
        """
        This function sets the dial value.

        :param uid: str, the uid of the vu-dial.
        :return result: dict, returns the request query result.
        """
        api_call = f'dial/{uid}/easing/get'
        params = ''

        try:
            r_uri = self.get_uri(self.server_url, self.key, api_call, params)
            r = self.send_http_request(r_uri, None)
        except Exception as exc:
            raise exc

        return r

class VUAdmin(VUAdminUtil):
    def __init__(self, server_address: str, server_port: int, admin_key: str):
        """
        Initialize the class with required values.
        
        :param server_address: str, the server ip address.
        :param server_port: int, the vu-dial server port.
        :param api_key: str, a valid api key for the vu-dial server.
        """
        self.server_url = f'http://{server_address}:{server_port}'
        self.key        = admin_key

    def provision_dials(self) -> dict:
        """
        This function list the connected vu-dials.

        :return result: dict, returns the request query result.
        """
        api_call = 'dial/provision'
        params = ''
        method = 'get'

        try:
            r_uri = self.get_uri(self.server_url, self.key, api_call, params)
            r = self.send_http_request(r_uri, method)
        except Exception as exc:
            raise exc

        return r

    def list_api_keys(self) -> dict:
        """
        This function list the connected vu-dials.

        :return result: dict, returns the request query result.
        """
        api_call = 'admin/keys/list'
        params = ''
        method = 'get'

        try:
            r_uri = self.get_uri(self.server_url, self.key, api_call, params)
            r = self.send_http_request(r_uri, method)
        except Exception as exc:
            raise exc

        return r

    def remove_api_key(self, target_key: str) -> dict:
        """
        This function list the connected vu-dials.

        :return result: dict, returns the request query result.
        """
        api_call = 'admin/keys/remove'
        params = f'&key={target_key}'
        method = 'get'

        try:
            r_uri = self.get_uri(self.server_url, self.key, api_call, params)
            r = self.send_http_request(r_uri, method)
        except Exception as exc:
            raise exc

        return r

    def create_api_key(self, name: str, dials: str) -> dict:
        """
        This function list the connected vu-dials.

        :return result: dict, returns the request query result.
        """
        api_call = 'admin/keys/create'
        params = f'&name={name}&dials={dials}'
        method = 'post'

        try:
            r_uri = self.get_uri(self.server_url, self.key, api_call, params)
            r = self.send_http_request(r_uri, method)
        except Exception as exc:
            raise exc

        return r

    def update_api_key(self, name: str, target_key: str, dials: str) -> dict:
        """
        This function list the connected vu-dials.

        :return result: dict, returns the request query result.
        """
        api_call = 'admin/keys/update'
        params = f'&key={target_key}&name={name}&dials={dials}'
        method = 'get'

        try:
            r_uri = self.get_uri(self.server_url, self.key, api_call, params)
            r = self.send_http_request(r_uri, method)
        except Exception as exc:
            raise exc

        return r
