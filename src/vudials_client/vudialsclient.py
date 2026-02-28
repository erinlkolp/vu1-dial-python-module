import requests
import logging
from urllib.parse import quote

# Library code must not call logging.basicConfig() — that configures the root
# logger for the entire host application. Let the application control logging.
LOGGER = logging.getLogger(__name__)


class VUUtil:
    def get_uri(self, server_url: str, api_key: str, api_call: str, keyword_params: str) -> str:
        # Security note: The API key is transmitted as a URL query parameter.
        # This means it will appear in server access logs, proxy logs, and
        # HTTP client history. If the server adds header-based authentication
        # in the future, prefer an Authorization or X-API-Key header instead.
        return f'{server_url}/api/v0/{api_call}?key={api_key}{keyword_params}'

    def send_http_request(self, path_uri: str, files: dict, timeout: int = 10) -> requests.Response:
        if files is not None:
            r = requests.post(path_uri, files=files, timeout=timeout)
        else:
            r = requests.get(path_uri, timeout=timeout)
        r.raise_for_status()
        return r


class VUAdminUtil:
    def get_uri(self, server_url: str, api_key: str, api_call: str, keyword_params: str) -> str:
        # Security note: See VUUtil.get_uri — same key-in-URL caveat applies.
        return f'{server_url}/api/v0/{api_call}?admin_key={api_key}{keyword_params}'

    def send_http_request(self, path_uri: str, method: str, timeout: int = 10) -> requests.Response:
        if method == "post":
            r = requests.post(path_uri, timeout=timeout)
        else:
            r = requests.get(path_uri, timeout=timeout)
        r.raise_for_status()
        return r


class VUDial(VUUtil):
    def __init__(self, server_address: str, server_port: int, api_key: str):
        """
        Initialize the class with required values.

        :param server_address: str, the server ip address.
        :param server_port: int, the vu-dial server port.
        :param api_key: str, a valid api key for the vu-dial server.

        Security note: Communication uses plain HTTP. Ensure the server is
        only reachable on a trusted local network interface. The API key is
        passed as a URL query parameter and will appear in server access logs.
        """
        self.server_url = f'http://{server_address}:{server_port}'
        self.key = api_key

    def list_dials(self) -> requests.Response:
        """
        List the connected vu-dials.

        :return: requests.Response
        """
        r_uri = self.get_uri(self.server_url, self.key, 'dial/list', '')
        return self.send_http_request(r_uri, None)

    def get_dial_info(self, uid: str) -> requests.Response:
        """
        Get vu-dial information.

        :param uid: str, the uid of the vu-dial.
        :return: requests.Response
        """
        api_call = f'dial/{quote(uid, safe="")}/status'
        r_uri = self.get_uri(self.server_url, self.key, api_call, '')
        return self.send_http_request(r_uri, None)

    def set_dial_value(self, uid: str, value: int) -> requests.Response:
        """
        Set the dial value.

        :param uid: str, the uid of the vu-dial.
        :param value: int, the dial value.
        :return: requests.Response
        """
        api_call = f'dial/{quote(uid, safe="")}/set'
        params = f'&value={int(value)}'
        r_uri = self.get_uri(self.server_url, self.key, api_call, params)
        return self.send_http_request(r_uri, None)

    def set_dial_color(self, uid: str, red: int, green: int, blue: int) -> requests.Response:
        """
        Set the dial backlight color.

        :param uid: str, the uid of the vu-dial.
        :param red: int, red channel (0-255).
        :param green: int, green channel (0-255).
        :param blue: int, blue channel (0-255).
        :return: requests.Response
        """
        api_call = f'dial/{quote(uid, safe="")}/backlight'
        params = f'&red={int(red)}&green={int(green)}&blue={int(blue)}'
        r_uri = self.get_uri(self.server_url, self.key, api_call, params)
        return self.send_http_request(r_uri, None)

    def set_dial_background(self, uid: str, file: str) -> requests.Response:
        """
        Set the dial background image.

        :param uid: str, the uid of the vu-dial.
        :param file: str, path to the image file to upload.
        :return: requests.Response
        """
        api_call = f'dial/{quote(uid, safe="")}/image/set'
        with open(file, 'rb') as f:
            files = {'imgfile': f}
            r_uri = self.get_uri(self.server_url, self.key, api_call, '')
            return self.send_http_request(r_uri, files)

    def get_dial_image_crc(self, uid: str) -> requests.Response:
        """
        Get the CRC of the dial background image.

        :param uid: str, the uid of the vu-dial.
        :return: requests.Response
        """
        api_call = f'dial/{quote(uid, safe="")}/image/crc'
        r_uri = self.get_uri(self.server_url, self.key, api_call, '')
        return self.send_http_request(r_uri, None)

    def set_dial_name(self, uid: str, name: str) -> requests.Response:
        """
        Set the dial name.

        :param uid: str, the uid of the vu-dial.
        :param name: str, the name to assign to the dial.
        :return: requests.Response
        """
        api_call = f'dial/{quote(uid, safe="")}/name'
        params = f'&name={quote(name)}'
        r_uri = self.get_uri(self.server_url, self.key, api_call, params)
        return self.send_http_request(r_uri, None)

    def reload_hw_info(self, uid: str) -> requests.Response:
        """
        Reload hardware info for a dial.

        :param uid: str, the uid of the vu-dial.
        :return: requests.Response
        """
        api_call = f'dial/{quote(uid, safe="")}/reload'
        r_uri = self.get_uri(self.server_url, self.key, api_call, '')
        return self.send_http_request(r_uri, None)

    def set_dial_easing(self, uid: str, period: int, step: int) -> requests.Response:
        """
        Set dial easing parameters.

        :param uid: str, the uid of the vu-dial.
        :param period: int, easing period.
        :param step: int, easing step.
        :return: requests.Response
        """
        api_call = f'dial/{quote(uid, safe="")}/easing/dial'
        params = f'&period={int(period)}&step={int(step)}'
        r_uri = self.get_uri(self.server_url, self.key, api_call, params)
        return self.send_http_request(r_uri, None)

    def set_backlight_easing(self, uid: str, period: int, step: int) -> requests.Response:
        """
        Set backlight easing parameters.

        :param uid: str, the uid of the vu-dial.
        :param period: int, easing period.
        :param step: int, easing step.
        :return: requests.Response
        """
        api_call = f'dial/{quote(uid, safe="")}/easing/backlight'
        params = f'&period={int(period)}&step={int(step)}'
        r_uri = self.get_uri(self.server_url, self.key, api_call, params)
        return self.send_http_request(r_uri, None)

    def get_easing_config(self, uid: str) -> requests.Response:
        """
        Get easing configuration for a dial.

        :param uid: str, the uid of the vu-dial.
        :return: requests.Response
        """
        api_call = f'dial/{quote(uid, safe="")}/easing/get'
        r_uri = self.get_uri(self.server_url, self.key, api_call, '')
        return self.send_http_request(r_uri, None)


class VUAdmin(VUAdminUtil):
    def __init__(self, server_address: str, server_port: int, admin_key: str):
        """
        Initialize the class with required values.

        :param server_address: str, the server ip address.
        :param server_port: int, the vu-dial server port.
        :param admin_key: str, a valid admin key for the vu-dial server.

        Security note: Communication uses plain HTTP. Ensure the server is
        only reachable on a trusted local network interface. The admin key is
        passed as a URL query parameter and will appear in server access logs.
        """
        self.server_url = f'http://{server_address}:{server_port}'
        self.key = admin_key

    def provision_dials(self) -> requests.Response:
        """
        Provision connected vu-dials.

        :return: requests.Response
        """
        r_uri = self.get_uri(self.server_url, self.key, 'dial/provision', '')
        return self.send_http_request(r_uri, 'get')

    def list_api_keys(self) -> requests.Response:
        """
        List all configured API keys.

        :return: requests.Response
        """
        r_uri = self.get_uri(self.server_url, self.key, 'admin/keys/list', '')
        return self.send_http_request(r_uri, 'get')

    def remove_api_key(self, target_key: str) -> requests.Response:
        """
        Remove an API key.

        :param target_key: str, the key to remove.
        :return: requests.Response
        """
        params = f'&key={quote(target_key)}'
        r_uri = self.get_uri(self.server_url, self.key, 'admin/keys/remove', params)
        return self.send_http_request(r_uri, 'get')

    def create_api_key(self, name: str, dials: str) -> requests.Response:
        """
        Create a new API key.

        :param name: str, the name for the new key.
        :param dials: str, the dials to associate with the key.
        :return: requests.Response
        """
        params = f'&name={quote(name)}&dials={quote(dials)}'
        r_uri = self.get_uri(self.server_url, self.key, 'admin/keys/create', params)
        return self.send_http_request(r_uri, 'post')

    def update_api_key(self, name: str, target_key: str, dials: str) -> requests.Response:
        """
        Update an existing API key.

        :param name: str, the new name for the key.
        :param target_key: str, the key to update.
        :param dials: str, the updated dials to associate.
        :return: requests.Response
        """
        params = f'&key={quote(target_key)}&name={quote(name)}&dials={quote(dials)}'
        r_uri = self.get_uri(self.server_url, self.key, 'admin/keys/update', params)
        return self.send_http_request(r_uri, 'get')
