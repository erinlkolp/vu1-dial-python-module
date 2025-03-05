<a id="__init__"></a>

# \_\_init\_\_

<a id="vudialsclient"></a>

# vudialsclient

<a id="vudialsclient.VUDial"></a>

## VUDial Objects

```python
class VUDial()
```

<a id="vudialsclient.VUDial.__init__"></a>

#### \_\_init\_\_

```python
def __init__(server_address: str, server_port: int, api_key: str)
```

Initialize the class with required values.

**Arguments**:

- `server_address`: str, the server ip address.
- `server_port`: int, the vu-dial server port.
- `api_key`: str, a valid api key for the vu-dial server.

<a id="vudialsclient.VUDial.list_dials"></a>

#### list\_dials

```python
def list_dials() -> dict
```

This function list the connected vu-dials.

**Returns**:

`result`: dict, returns the request query result.

<a id="vudialsclient.VUDial.get_dial_info"></a>

#### get\_dial\_info

```python
def get_dial_info(uid: str) -> dict
```

This function gets the vu-dial information.

**Arguments**:

- `uid`: str, the uid of the vu-dial.

**Returns**:

`result`: dict, returns the request query result.

<a id="vudialsclient.VUDial.get_image_crc"></a>

#### get\_image\_crc

```python
def get_image_crc(uid: str) -> dict
```

This function sets the vu-dial position.

**Arguments**:

- `uid`: str, the uid of the vu-dial.

**Returns**:

`result`: dict, returns the request query result.

<a id="vudialsclient.VUDial.set_dial_value"></a>

#### set\_dial\_value

```python
def set_dial_value(uid: str, value: int) -> dict
```

This function sets the vu-dial position.

**Arguments**:

- `uid`: str, the uid of the vu-dial.
- `value`: int, value of dial position between 0 and 100.

**Returns**:

`result`: dict, returns the request query result.

<a id="vudialsclient.VUDial.set_dial_color"></a>

#### set\_dial\_color

```python
def set_dial_color(uid: str, red: int, green: int, blue: int) -> dict
```

This function sets the dial color.

**Arguments**:

- `uid`: str, the uid of the vu-dial.
- `red`: int, the brightness of the red led - from 0 to 100.
- `green`: the brightness of the green led - from 0 to 100.
- `blue`: the brightness of the blue led - from 0 to 100.

**Returns**:

`result`: dict, returns the request query result.

<a id="vudialsclient.VUDial.set_dial_background"></a>

#### set\_dial\_background

```python
def set_dial_background(uid: str, file: str) -> dict
```

This function sets the dial background image from PNG file.

**Arguments**:

- `uid`: str, the uid of the vu-dial.
- `file`: str, the full path to the file to upload. Example: '/home/user/sample.png'

**Returns**:

`result`: dict, returns the request query result.

<a id="vudialsclient.VUDial.get_dial_image_crc"></a>

#### get\_dial\_image\_crc

```python
def get_dial_image_crc(uid: str) -> dict
```

This function gets the vu-dial image crc.

**Arguments**:

- `uid`: str, the uid of the vu-dial.

**Returns**:

`result`: dict, returns the request query result.

<a id="vudialsclient.VUDial.set_dial_name"></a>

#### set\_dial\_name

```python
def set_dial_name(uid: str, name: str) -> dict
```

This function sets the vu-dial name.

**Arguments**:

- `uid`: str, the uid of the vu-dial.
- `name`: str, the name of the vu-dial you wish to apply.

**Returns**:

`result`: dict, returns the request query result.

