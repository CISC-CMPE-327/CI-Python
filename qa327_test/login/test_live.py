import pytest
import requests
from seleniumbase import BaseCase

from qa327_test.conftest import base_url


@pytest.mark.usefixtures('server')
def test_server_is_live():
    r = requests.get(base_url)
    assert r.status_code == 200


@pytest.mark.usefixtures('server')
class SimpleLoginTest(BaseCase):

    def register(self):
        """register new user"""
        self.open(base_url + '/register')
        self.type("#email", "test0")
        self.type("#name", "test0")
        self.type("#password", "test0")
        self.type("#password2", "test0")
        self.click('input[type="submit"]')

    def login(self):
        """ Login to Swag Labs and verify that login was successful. """
        self.open(base_url + '/login')
        self.type("#email", "test0")
        self.type("#password", "test0")
        self.click('input[type="submit"]')

    def test_register_login(self):
        """ This test checks standard login for the Swag Labs store. """
        self.register()
        self.login()
        self.open(base_url)
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test0", "#welcome-header")
