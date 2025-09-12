# vudials_client

[![PyPI version](https://badge.fury.io/py/vudials-client.svg)](https://badge.fury.io/py/vudials-client)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python client module for Streacom's VU1 Dial development hardware. This provides a simple interface to manipulate multiple dials.

## Features

- **Full Dial API**: Easily change your dial's value, color, name, background image, and more!
- **Full Admin API**: Provides VU1 Dial Server API key management.

## Installation

```bash
pip install vudials-client
```

For development installation:

```bash
git clone git@github.com:erinlkolp/vu1-dial-python-module.git
cd vu1-dial-python-module/
pip install -e ".[dev]"
```

## Quick Start

Here's a simple example to get you started:

```python
from vudials_client import vudialsclient

dial_uid       = os.environ['TARGET_DIAL_UID']
server_key     = os.environ['API_KEY']
admin_key      = os.environ['ADMIN_API_KEY']
server_address = os.environ['VU1_SERVER_ADDRESS']
server_port    = os.environ['VU1_SERVER_PORT']

vu_meter  = vudialsclient.VUDial(server_address, server_port, server_key)
admin_api  = vudialsclient.VUAdmin(server_address, server_port, admin_key)

dial_list = vu_meter.list_dials()
print(dial_list)

api_key_list = admin_api.list_api_keys()
print(api_key_list)
```

## Documentation

For detailed documentation, see [the official documentation](https://github.com/erinlkolp/vu1-dial-python-module/blob/main/docs/api.md).

### Main Classes

#### `VUDial`

The primary class for interacting with the client-side module.

```python
vu_meter  = vudialsclient.VUDial(server_address, server_port, api_key)
```

**Parameters:**
- `server_address` (str): VU1 Dials Server host (ie. localhost)
- `server_port` (int): VU1 Dials Server port (ie. 5340)
- `api_key` (str): A valid API key for the VU1 Dials Server

**Methods:**
- `list_dials()`: Processes the given data and returns a result
- `get_dial_info(uid)`: Saves the current state to a file
- `set_dial_value(uid, value)`: Sets a dial's value (position)
- `set_dial_color(uid, red, green, blue)`: Sets a dial's backlight color
- `set_dial_background(uid, file)`: Sets a dial's background image
- `get_dial_image_crc(uid)`: Obtains a dial's image CRC
- `set_dial_name(uid, name)`: Sets a dial's name (no spaces)
- `reload_hw_info(uid)`: Reloads dial hardware information
- `set_dial_easing(uid, period, step)`: Sets dial easing
- `set_backlight_easing(uid, period, step)`: Sets dial easing
- `get_easing_config(uid)`: Gets easing config for dial (unsupported as of now)

#### `VUAdmin`

The primary class for interacting with the client-side module.

```python
admin_api  = vudialsclient.VUAdmin(server_address, server_port, admin_key)
```

**Parameters:**
- `server_address` (str): VU1 Dials Server host (ie. localhost)
- `server_port` (int): VU1 Dials Server port (ie. 5340)
- `admin_key` (str): A valid Admin API key for the VU1 Dials Server

**Methods:**
- `provision_dials()`: Provisions new dial hardware
- `list_api_keys()`: Lists all VU Server API keys
- `remove_api_key(target_key)`: Removes an API key
- `create_api_key(name, dials)`: Creates an API key (see value in return)
- `update_api_key(name, target_key, dials)`: Updates an API key

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please make sure to update tests as appropriate and follow the code style guide.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Many thanks to Aaron D. and Christopher K.!

## Changelog

### 2025.3.3 (2025-03-07)
- Adds documentation

### 2025.3.2 (2025-03-05)
- Initial release
- Partial dial api implementation

## License & Author

- Author:: Erin L. Kolp (<erinlkolpfoss@gmail.com>)

Copyright (c) 2025 Erin L. Kolp 

Licensed under the MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the 'Software'), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.