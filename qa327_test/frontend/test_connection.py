import pytest
import requests

from qa327_test.conftest import base_url

"""
Simple test case for server connection
"""

@pytest.mark.usefixtures('server')
def test_server_is_live():
    r = requests.get(base_url)
    assert r.status_code == 200
