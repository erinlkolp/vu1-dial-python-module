# vudials_client

[![PyPI version](https://badge.fury.io/py/vudials-client.svg)](https://badge.fury.io/py/vudials-client)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python client module for Streacom's VU1 Dial development hardware. This provides a simple interface to manipulate multiple dials.

## Features

- **Full Dial API**: Easily change your dial's value, color, name, background image, and more!
- **Full Admin API**: Provides VU1 Dial Server API key management.

## Installation

```bash
pip install vudials_client --extra-index-url https://test.pypi.org/simple/
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
srv_address    = os.environ['VU1_SERVER_ADDRESS']
srv_port       = os.environ['VU1_SERVER_PORT']

vu_meter  = vudialsclient.VUDial(srv_address, srv_port, server_key)

result = vu_meter.get_dial_image_crc(dial_uid)
print(result)
```

## Documentation

For detailed documentation, see [the official documentation](https://github.com/erinlkolp/vu1-dial-python-module/blob/main/docs/api.md).

### Main Classes

#### `VUDial`

The primary class for interacting with the module.

```python
vu_meter  = vudialsclient.VUDial(srv_address, srv_port, server_key)
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

- Many thanks to everyone who code reviewed!

## Changelog

### 2025.3.2 (2025-03-05)
- Initial release
- Partial dial api implementede Z

## License & Author

- Author:: Erin L. Kolp (<erinlkolpfoss@gmail.com>)

Copyright (c) 2025 Erin L. Kolp 

Licensed under the MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the 'Software'), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.