"""Comprehensive tests for vudials_client."""
import io
import re
import pytest
import responses as resp
from requests.exceptions import HTTPError
from unittest.mock import patch, mock_open

from vudials_client.vudialsclient import VUUtil, VUAdminUtil, VUDial, VUAdmin


BASE = "http://localhost:5340"


# ---------------------------------------------------------------------------
# VUUtil
# ---------------------------------------------------------------------------


class TestVUUtilGetUri:
    def setup_method(self):
        self.util = VUUtil()

    def test_basic_construction(self):
        uri = self.util.get_uri("http://localhost:5340", "mykey", "dial/list", "")
        assert uri == "http://localhost:5340/api/v0/dial/list?key=mykey"

    def test_with_keyword_params(self):
        uri = self.util.get_uri("http://localhost:5340", "mykey", "dial/abc/set", "&value=50")
        assert uri == "http://localhost:5340/api/v0/dial/abc/set?key=mykey&value=50"

    def test_empty_keyword_params(self):
        uri = self.util.get_uri("http://localhost:5340", "mykey", "dial/list", "")
        assert uri.endswith("?key=mykey")

    def test_key_query_param_name(self):
        uri = self.util.get_uri("http://localhost:5340", "secret", "dial/list", "")
        assert "?key=secret" in uri

    def test_api_path_format(self):
        uri = self.util.get_uri("http://192.168.1.1:8080", "k", "some/endpoint", "")
        assert uri.startswith("http://192.168.1.1:8080/api/v0/")

    def test_multiple_keyword_params(self):
        uri = self.util.get_uri(
            "http://localhost:5340", "k", "dial/abc/backlight", "&red=255&green=128&blue=0"
        )
        assert "red=255" in uri
        assert "green=128" in uri
        assert "blue=0" in uri

    def test_key_with_special_chars_url_encoded(self):
        # A key containing & and = must not break the query string structure.
        uri = self.util.get_uri("http://localhost:5340", "k&admin_key=evil", "dial/list", "")
        assert "k%26admin_key%3Devil" in uri
        assert "admin_key=evil" not in uri


class TestVUUtilSendHttpRequest:
    def setup_method(self):
        self.util = VUUtil()

    @resp.activate
    def test_get_when_files_none(self):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/list", json={}, status=200)
        r = self.util.send_http_request(f"{BASE}/api/v0/dial/list", None)
        assert resp.calls[0].request.method == "GET"
        assert r.status_code == 200

    @resp.activate
    def test_post_when_files_provided(self):
        resp.add(resp.POST, f"{BASE}/api/v0/dial/abc/image/set", json={}, status=200)
        files = {"imgfile": io.BytesIO(b"fake image data")}
        r = self.util.send_http_request(f"{BASE}/api/v0/dial/abc/image/set", files)
        assert resp.calls[0].request.method == "POST"
        assert r.status_code == 200

    @resp.activate
    def test_raises_on_404(self):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/list", status=404)
        with pytest.raises(HTTPError):
            self.util.send_http_request(f"{BASE}/api/v0/dial/list", None)

    @resp.activate
    def test_raises_on_500(self):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/list", status=500)
        with pytest.raises(HTTPError):
            self.util.send_http_request(f"{BASE}/api/v0/dial/list", None)

    @resp.activate
    def test_raises_on_403(self):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/list", status=403)
        with pytest.raises(HTTPError):
            self.util.send_http_request(f"{BASE}/api/v0/dial/list", None)

    @resp.activate
    def test_returns_response_body(self):
        resp.add(resp.GET, f"{BASE}/test", json={"data": "value"}, status=200)
        r = self.util.send_http_request(f"{BASE}/test", None)
        assert r.json() == {"data": "value"}

    @resp.activate
    def test_default_timeout_accepted(self):
        resp.add(resp.GET, f"{BASE}/test", json={}, status=200)
        r = self.util.send_http_request(f"{BASE}/test", None)
        assert r.status_code == 200

    @resp.activate
    def test_custom_timeout_accepted(self):
        resp.add(resp.GET, f"{BASE}/test", json={}, status=200)
        r = self.util.send_http_request(f"{BASE}/test", None, timeout=30)
        assert r.status_code == 200


# ---------------------------------------------------------------------------
# VUAdminUtil
# ---------------------------------------------------------------------------


class TestVUAdminUtilGetUri:
    def setup_method(self):
        self.util = VUAdminUtil()

    def test_uses_admin_key_param(self):
        uri = self.util.get_uri("http://localhost:5340", "adminkey", "admin/keys/list", "")
        assert "admin_key=adminkey" in uri

    def test_does_not_use_key_param(self):
        uri = self.util.get_uri("http://localhost:5340", "adminkey", "admin/keys/list", "")
        assert "?key=" not in uri

    def test_basic_construction(self):
        uri = self.util.get_uri("http://localhost:5340", "adminkey", "admin/keys/list", "")
        assert uri == "http://localhost:5340/api/v0/admin/keys/list?admin_key=adminkey"

    def test_with_params(self):
        uri = self.util.get_uri(
            "http://localhost:5340", "adminkey", "admin/keys/create", "&name=foo&dials=all"
        )
        assert "admin_key=adminkey" in uri
        assert "&name=foo&dials=all" in uri

    def test_api_path_format(self):
        uri = self.util.get_uri("http://192.168.0.1:9000", "k", "admin/keys/list", "")
        assert uri.startswith("http://192.168.0.1:9000/api/v0/")

    def test_admin_key_with_special_chars_url_encoded(self):
        # A key containing & and = must not inject extra query parameters.
        uri = self.util.get_uri("http://localhost:5340", "a&key=evil", "admin/keys/list", "")
        assert "a%26key%3Devil" in uri
        assert "key=evil" not in uri


class TestVUAdminUtilSendHttpRequest:
    def setup_method(self):
        self.util = VUAdminUtil()

    @resp.activate
    def test_get_method(self):
        resp.add(resp.GET, f"{BASE}/api/v0/admin/keys/list", json={}, status=200)
        r = self.util.send_http_request(f"{BASE}/api/v0/admin/keys/list", "get")
        assert resp.calls[0].request.method == "GET"
        assert r.status_code == 200

    @resp.activate
    def test_post_method(self):
        resp.add(resp.POST, f"{BASE}/api/v0/admin/keys/create", json={}, status=200)
        r = self.util.send_http_request(f"{BASE}/api/v0/admin/keys/create", "post")
        assert resp.calls[0].request.method == "POST"
        assert r.status_code == 200

    @resp.activate
    def test_non_post_defaults_to_get(self):
        resp.add(resp.GET, f"{BASE}/api/v0/test", json={}, status=200)
        self.util.send_http_request(f"{BASE}/api/v0/test", "put")
        assert resp.calls[0].request.method == "GET"

    @resp.activate
    def test_raises_on_404(self):
        resp.add(resp.GET, f"{BASE}/api/v0/test", status=404)
        with pytest.raises(HTTPError):
            self.util.send_http_request(f"{BASE}/api/v0/test", "get")

    @resp.activate
    def test_raises_on_500(self):
        resp.add(resp.GET, f"{BASE}/api/v0/test", status=500)
        with pytest.raises(HTTPError):
            self.util.send_http_request(f"{BASE}/api/v0/test", "get")

    @resp.activate
    def test_custom_timeout_accepted(self):
        resp.add(resp.GET, f"{BASE}/api/v0/test", json={}, status=200)
        r = self.util.send_http_request(f"{BASE}/api/v0/test", "get", timeout=60)
        assert r.status_code == 200


# ---------------------------------------------------------------------------
# VUDial — constructor
# ---------------------------------------------------------------------------


class TestVUDialInit:
    def test_server_url_constructed(self):
        d = VUDial("localhost", 5340, "mykey")
        assert d.server_url == "http://localhost:5340"

    def test_key_stored(self):
        d = VUDial("localhost", 5340, "mykey")
        assert d.key == "mykey"

    def test_different_port(self):
        d = VUDial("192.168.1.100", 9000, "k")
        assert d.server_url == "http://192.168.1.100:9000"

    def test_ip_address(self):
        d = VUDial("10.0.0.1", 5340, "k")
        assert "10.0.0.1" in d.server_url


# ---------------------------------------------------------------------------
# VUDial — list_dials
# ---------------------------------------------------------------------------


class TestVUDialListDials:
    @resp.activate
    def test_success(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/list", json=[], status=200)
        r = vudial.list_dials()
        assert r.status_code == 200

    @resp.activate
    def test_correct_endpoint(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/list", json=[], status=200)
        vudial.list_dials()
        assert "/api/v0/dial/list" in resp.calls[0].request.url

    @resp.activate
    def test_uses_get(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/list", json=[], status=200)
        vudial.list_dials()
        assert resp.calls[0].request.method == "GET"

    @resp.activate
    def test_includes_api_key(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/list", json=[], status=200)
        vudial.list_dials()
        assert "key=test-api-key" in resp.calls[0].request.url

    @resp.activate
    def test_http_error_propagates(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/list", status=401)
        with pytest.raises(HTTPError):
            vudial.list_dials()


# ---------------------------------------------------------------------------
# VUDial — get_dial_info
# ---------------------------------------------------------------------------


class TestVUDialGetDialInfo:
    @resp.activate
    def test_success(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/uid123/status", json={}, status=200)
        r = vudial.get_dial_info("uid123")
        assert r.status_code == 200

    @resp.activate
    def test_correct_endpoint(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/uid123/status", json={}, status=200)
        vudial.get_dial_info("uid123")
        assert "/dial/uid123/status" in resp.calls[0].request.url

    @resp.activate
    def test_uid_url_encoded(self, vudial):
        resp.add(resp.GET, re.compile(r".*uid%2Fspecial.*"), json={}, status=200)
        vudial.get_dial_info("uid/special")
        assert "uid%2Fspecial" in resp.calls[0].request.url

    @resp.activate
    def test_http_error_propagates(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/uid123/status", status=404)
        with pytest.raises(HTTPError):
            vudial.get_dial_info("uid123")


# ---------------------------------------------------------------------------
# VUDial — set_dial_value
# ---------------------------------------------------------------------------


class TestVUDialSetDialValue:
    @resp.activate
    def test_success(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/uid1/set", json={}, status=200)
        r = vudial.set_dial_value("uid1", 75)
        assert r.status_code == 200

    @resp.activate
    def test_correct_endpoint(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/uid1/set", json={}, status=200)
        vudial.set_dial_value("uid1", 75)
        assert "/dial/uid1/set" in resp.calls[0].request.url

    @resp.activate
    def test_correct_value_param(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/uid1/set", json={}, status=200)
        vudial.set_dial_value("uid1", 75)
        assert "value=75" in resp.calls[0].request.url

    @resp.activate
    def test_value_zero(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/uid1/set", json={}, status=200)
        vudial.set_dial_value("uid1", 0)
        assert "value=0" in resp.calls[0].request.url

    @resp.activate
    def test_http_error_propagates(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/uid1/set", status=500)
        with pytest.raises(HTTPError):
            vudial.set_dial_value("uid1", 50)


# ---------------------------------------------------------------------------
# VUDial — set_dial_color
# ---------------------------------------------------------------------------


class TestVUDialSetDialColor:
    @resp.activate
    def test_success(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/uid1/backlight", json={}, status=200)
        r = vudial.set_dial_color("uid1", 255, 128, 0)
        assert r.status_code == 200

    @resp.activate
    def test_correct_endpoint(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/uid1/backlight", json={}, status=200)
        vudial.set_dial_color("uid1", 255, 128, 0)
        assert "/dial/uid1/backlight" in resp.calls[0].request.url

    @resp.activate
    def test_correct_rgb_params(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/uid1/backlight", json={}, status=200)
        vudial.set_dial_color("uid1", 255, 128, 0)
        url = resp.calls[0].request.url
        assert "red=255" in url
        assert "green=128" in url
        assert "blue=0" in url

    @resp.activate
    def test_min_values(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/uid1/backlight", json={}, status=200)
        vudial.set_dial_color("uid1", 0, 0, 0)
        url = resp.calls[0].request.url
        assert "red=0" in url
        assert "green=0" in url
        assert "blue=0" in url

    @resp.activate
    def test_max_values(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/uid1/backlight", json={}, status=200)
        vudial.set_dial_color("uid1", 255, 255, 255)
        url = resp.calls[0].request.url
        assert "red=255" in url
        assert "green=255" in url
        assert "blue=255" in url

    @resp.activate
    def test_http_error_propagates(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/uid1/backlight", status=500)
        with pytest.raises(HTTPError):
            vudial.set_dial_color("uid1", 255, 0, 0)


# ---------------------------------------------------------------------------
# VUDial — set_dial_background
# ---------------------------------------------------------------------------


class TestVUDialSetDialBackground:
    @resp.activate
    def test_success(self, vudial):
        resp.add(resp.POST, f"{BASE}/api/v0/dial/uid1/image/set", json={}, status=200)
        with patch("builtins.open", mock_open(read_data=b"fake image")):
            r = vudial.set_dial_background("uid1", "image.png")
        assert r.status_code == 200

    @resp.activate
    def test_uses_post(self, vudial):
        resp.add(resp.POST, f"{BASE}/api/v0/dial/uid1/image/set", json={}, status=200)
        with patch("builtins.open", mock_open(read_data=b"fake image")):
            vudial.set_dial_background("uid1", "image.png")
        assert resp.calls[0].request.method == "POST"

    @resp.activate
    def test_correct_endpoint(self, vudial):
        resp.add(resp.POST, f"{BASE}/api/v0/dial/uid1/image/set", json={}, status=200)
        with patch("builtins.open", mock_open(read_data=b"fake image")):
            vudial.set_dial_background("uid1", "image.png")
        assert "/dial/uid1/image/set" in resp.calls[0].request.url

    @resp.activate
    def test_http_error_propagates(self, vudial):
        resp.add(resp.POST, f"{BASE}/api/v0/dial/uid1/image/set", status=500)
        with patch("builtins.open", mock_open(read_data=b"fake image")):
            with pytest.raises(HTTPError):
                vudial.set_dial_background("uid1", "image.png")

    def test_missing_file_raises(self, vudial):
        with pytest.raises(FileNotFoundError):
            vudial.set_dial_background("uid1", "/nonexistent/path/image.png")


# ---------------------------------------------------------------------------
# VUDial — get_dial_image_crc
# ---------------------------------------------------------------------------


class TestVUDialGetDialImageCrc:
    @resp.activate
    def test_success(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/uid1/image/crc", json={}, status=200)
        r = vudial.get_dial_image_crc("uid1")
        assert r.status_code == 200

    @resp.activate
    def test_correct_endpoint(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/uid1/image/crc", json={}, status=200)
        vudial.get_dial_image_crc("uid1")
        assert "/dial/uid1/image/crc" in resp.calls[0].request.url

    @resp.activate
    def test_http_error_propagates(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/uid1/image/crc", status=404)
        with pytest.raises(HTTPError):
            vudial.get_dial_image_crc("uid1")


# ---------------------------------------------------------------------------
# VUDial — set_dial_name
# ---------------------------------------------------------------------------


class TestVUDialSetDialName:
    @resp.activate
    def test_success(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/uid1/name", json={}, status=200)
        r = vudial.set_dial_name("uid1", "My Dial")
        assert r.status_code == 200

    @resp.activate
    def test_correct_endpoint(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/uid1/name", json={}, status=200)
        vudial.set_dial_name("uid1", "TestName")
        assert "/dial/uid1/name" in resp.calls[0].request.url

    @resp.activate
    def test_correct_name_param(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/uid1/name", json={}, status=200)
        vudial.set_dial_name("uid1", "TestName")
        assert "name=TestName" in resp.calls[0].request.url

    @resp.activate
    def test_name_url_encoded(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/uid1/name", json={}, status=200)
        vudial.set_dial_name("uid1", "My Dial")
        url = resp.calls[0].request.url
        assert "My%20Dial" in url or "My+Dial" in url

    @resp.activate
    def test_http_error_propagates(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/uid1/name", status=400)
        with pytest.raises(HTTPError):
            vudial.set_dial_name("uid1", "Name")


# ---------------------------------------------------------------------------
# VUDial — reload_hw_info
# ---------------------------------------------------------------------------


class TestVUDialReloadHwInfo:
    @resp.activate
    def test_success(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/uid1/reload", json={}, status=200)
        r = vudial.reload_hw_info("uid1")
        assert r.status_code == 200

    @resp.activate
    def test_correct_endpoint(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/uid1/reload", json={}, status=200)
        vudial.reload_hw_info("uid1")
        assert "/dial/uid1/reload" in resp.calls[0].request.url

    @resp.activate
    def test_http_error_propagates(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/uid1/reload", status=500)
        with pytest.raises(HTTPError):
            vudial.reload_hw_info("uid1")


# ---------------------------------------------------------------------------
# VUDial — set_dial_easing
# ---------------------------------------------------------------------------


class TestVUDialSetDialEasing:
    @resp.activate
    def test_success(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/uid1/easing/dial", json={}, status=200)
        r = vudial.set_dial_easing("uid1", 100, 5)
        assert r.status_code == 200

    @resp.activate
    def test_correct_endpoint(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/uid1/easing/dial", json={}, status=200)
        vudial.set_dial_easing("uid1", 100, 5)
        assert "/dial/uid1/easing/dial" in resp.calls[0].request.url

    @resp.activate
    def test_correct_params(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/uid1/easing/dial", json={}, status=200)
        vudial.set_dial_easing("uid1", 100, 5)
        url = resp.calls[0].request.url
        assert "period=100" in url
        assert "step=5" in url

    @resp.activate
    def test_http_error_propagates(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/uid1/easing/dial", status=500)
        with pytest.raises(HTTPError):
            vudial.set_dial_easing("uid1", 100, 5)


# ---------------------------------------------------------------------------
# VUDial — set_backlight_easing
# ---------------------------------------------------------------------------


class TestVUDialSetBacklightEasing:
    @resp.activate
    def test_success(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/uid1/easing/backlight", json={}, status=200)
        r = vudial.set_backlight_easing("uid1", 200, 10)
        assert r.status_code == 200

    @resp.activate
    def test_correct_endpoint(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/uid1/easing/backlight", json={}, status=200)
        vudial.set_backlight_easing("uid1", 200, 10)
        assert "/dial/uid1/easing/backlight" in resp.calls[0].request.url

    @resp.activate
    def test_correct_params(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/uid1/easing/backlight", json={}, status=200)
        vudial.set_backlight_easing("uid1", 200, 10)
        url = resp.calls[0].request.url
        assert "period=200" in url
        assert "step=10" in url

    @resp.activate
    def test_http_error_propagates(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/uid1/easing/backlight", status=500)
        with pytest.raises(HTTPError):
            vudial.set_backlight_easing("uid1", 200, 10)


# ---------------------------------------------------------------------------
# VUDial — get_easing_config
# ---------------------------------------------------------------------------


class TestVUDialGetEasingConfig:
    @resp.activate
    def test_success(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/uid1/easing/get", json={}, status=200)
        r = vudial.get_easing_config("uid1")
        assert r.status_code == 200

    @resp.activate
    def test_correct_endpoint(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/uid1/easing/get", json={}, status=200)
        vudial.get_easing_config("uid1")
        assert "/dial/uid1/easing/get" in resp.calls[0].request.url

    @resp.activate
    def test_http_error_propagates(self, vudial):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/uid1/easing/get", status=404)
        with pytest.raises(HTTPError):
            vudial.get_easing_config("uid1")


# ---------------------------------------------------------------------------
# VUAdmin — constructor
# ---------------------------------------------------------------------------


class TestVUAdminInit:
    def test_server_url_constructed(self):
        a = VUAdmin("localhost", 5340, "adminkey")
        assert a.server_url == "http://localhost:5340"

    def test_key_stored(self):
        a = VUAdmin("localhost", 5340, "adminkey")
        assert a.key == "adminkey"

    def test_different_address_and_port(self):
        a = VUAdmin("10.0.0.5", 9000, "k")
        assert a.server_url == "http://10.0.0.5:9000"


# ---------------------------------------------------------------------------
# VUAdmin — provision_dials
# ---------------------------------------------------------------------------


class TestVUAdminProvisionDials:
    @resp.activate
    def test_success(self, vuadmin):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/provision", json={}, status=200)
        r = vuadmin.provision_dials()
        assert r.status_code == 200

    @resp.activate
    def test_correct_endpoint(self, vuadmin):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/provision", json={}, status=200)
        vuadmin.provision_dials()
        assert "/api/v0/dial/provision" in resp.calls[0].request.url

    @resp.activate
    def test_uses_admin_key(self, vuadmin):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/provision", json={}, status=200)
        vuadmin.provision_dials()
        assert "admin_key=test-admin-key" in resp.calls[0].request.url

    @resp.activate
    def test_http_error_propagates(self, vuadmin):
        resp.add(resp.GET, f"{BASE}/api/v0/dial/provision", status=500)
        with pytest.raises(HTTPError):
            vuadmin.provision_dials()


# ---------------------------------------------------------------------------
# VUAdmin — list_api_keys
# ---------------------------------------------------------------------------


class TestVUAdminListApiKeys:
    @resp.activate
    def test_success(self, vuadmin):
        resp.add(resp.GET, f"{BASE}/api/v0/admin/keys/list", json=[], status=200)
        r = vuadmin.list_api_keys()
        assert r.status_code == 200

    @resp.activate
    def test_correct_endpoint(self, vuadmin):
        resp.add(resp.GET, f"{BASE}/api/v0/admin/keys/list", json=[], status=200)
        vuadmin.list_api_keys()
        assert "/api/v0/admin/keys/list" in resp.calls[0].request.url

    @resp.activate
    def test_uses_admin_key(self, vuadmin):
        resp.add(resp.GET, f"{BASE}/api/v0/admin/keys/list", json=[], status=200)
        vuadmin.list_api_keys()
        assert "admin_key=test-admin-key" in resp.calls[0].request.url

    @resp.activate
    def test_http_error_propagates(self, vuadmin):
        resp.add(resp.GET, f"{BASE}/api/v0/admin/keys/list", status=403)
        with pytest.raises(HTTPError):
            vuadmin.list_api_keys()


# ---------------------------------------------------------------------------
# VUAdmin — remove_api_key
# ---------------------------------------------------------------------------


class TestVUAdminRemoveApiKey:
    @resp.activate
    def test_success(self, vuadmin):
        resp.add(resp.GET, f"{BASE}/api/v0/admin/keys/remove", json={}, status=200)
        r = vuadmin.remove_api_key("key-to-remove")
        assert r.status_code == 200

    @resp.activate
    def test_correct_endpoint(self, vuadmin):
        resp.add(resp.GET, f"{BASE}/api/v0/admin/keys/remove", json={}, status=200)
        vuadmin.remove_api_key("key-to-remove")
        assert "/api/v0/admin/keys/remove" in resp.calls[0].request.url

    @resp.activate
    def test_passes_target_key(self, vuadmin):
        resp.add(resp.GET, f"{BASE}/api/v0/admin/keys/remove", json={}, status=200)
        vuadmin.remove_api_key("key-to-remove")
        assert "key=key-to-remove" in resp.calls[0].request.url

    @resp.activate
    def test_target_key_url_encoded(self, vuadmin):
        resp.add(resp.GET, f"{BASE}/api/v0/admin/keys/remove", json={}, status=200)
        vuadmin.remove_api_key("key with spaces")
        url = resp.calls[0].request.url
        assert "key+with+spaces" in url or "key%20with%20spaces" in url

    @resp.activate
    def test_http_error_propagates(self, vuadmin):
        resp.add(resp.GET, f"{BASE}/api/v0/admin/keys/remove", status=404)
        with pytest.raises(HTTPError):
            vuadmin.remove_api_key("no-such-key")


# ---------------------------------------------------------------------------
# VUAdmin — create_api_key
# ---------------------------------------------------------------------------


class TestVUAdminCreateApiKey:
    @resp.activate
    def test_success(self, vuadmin):
        resp.add(resp.POST, f"{BASE}/api/v0/admin/keys/create", json={}, status=200)
        r = vuadmin.create_api_key("mykey", "all")
        assert r.status_code == 200

    @resp.activate
    def test_uses_post(self, vuadmin):
        resp.add(resp.POST, f"{BASE}/api/v0/admin/keys/create", json={}, status=200)
        vuadmin.create_api_key("mykey", "all")
        assert resp.calls[0].request.method == "POST"

    @resp.activate
    def test_correct_endpoint(self, vuadmin):
        resp.add(resp.POST, f"{BASE}/api/v0/admin/keys/create", json={}, status=200)
        vuadmin.create_api_key("mykey", "all")
        assert "/api/v0/admin/keys/create" in resp.calls[0].request.url

    @resp.activate
    def test_correct_params(self, vuadmin):
        resp.add(resp.POST, f"{BASE}/api/v0/admin/keys/create", json={}, status=200)
        vuadmin.create_api_key("mykey", "dial1,dial2")
        url = resp.calls[0].request.url
        assert "name=mykey" in url
        assert "dials=" in url

    @resp.activate
    def test_http_error_propagates(self, vuadmin):
        resp.add(resp.POST, f"{BASE}/api/v0/admin/keys/create", status=400)
        with pytest.raises(HTTPError):
            vuadmin.create_api_key("badkey", "all")


# ---------------------------------------------------------------------------
# VUAdmin — update_api_key
# ---------------------------------------------------------------------------


class TestVUAdminUpdateApiKey:
    @resp.activate
    def test_success(self, vuadmin):
        resp.add(resp.GET, f"{BASE}/api/v0/admin/keys/update", json={}, status=200)
        r = vuadmin.update_api_key("newname", "existing-key", "all")
        assert r.status_code == 200

    @resp.activate
    def test_correct_endpoint(self, vuadmin):
        resp.add(resp.GET, f"{BASE}/api/v0/admin/keys/update", json={}, status=200)
        vuadmin.update_api_key("newname", "existing-key", "all")
        assert "/api/v0/admin/keys/update" in resp.calls[0].request.url

    @resp.activate
    def test_uses_get(self, vuadmin):
        resp.add(resp.GET, f"{BASE}/api/v0/admin/keys/update", json={}, status=200)
        vuadmin.update_api_key("newname", "existing-key", "all")
        assert resp.calls[0].request.method == "GET"

    @resp.activate
    def test_correct_params(self, vuadmin):
        resp.add(resp.GET, f"{BASE}/api/v0/admin/keys/update", json={}, status=200)
        vuadmin.update_api_key("newname", "existing-key", "all")
        url = resp.calls[0].request.url
        assert "name=newname" in url
        assert "key=existing-key" in url
        assert "dials=all" in url

    @resp.activate
    def test_http_error_propagates(self, vuadmin):
        resp.add(resp.GET, f"{BASE}/api/v0/admin/keys/update", status=404)
        with pytest.raises(HTTPError):
            vuadmin.update_api_key("name", "no-such-key", "all")
