import pytest
from vudials_client.vudialsclient import VUDial, VUAdmin


@pytest.fixture
def vudial():
    return VUDial("localhost", 5340, "test-api-key")


@pytest.fixture
def vuadmin():
    return VUAdmin("localhost", 5340, "test-admin-key")
