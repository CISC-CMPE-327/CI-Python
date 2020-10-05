import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash


test_user = User(
    email='test_frontend@test.com',
    name='test_frontend',
    password=generate_password_hash('test_frontend')
)

test_tickets = [
    {'name': 't1', 'price': '100'}
]


class FrontEndHomePageTest(BaseCase):

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_login_success(self, *_):
        """ Login and verify if the tickets are correctly listed."""
        self.open(base_url + '/login')
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "test_frontend")
        self.click('input[type="submit"]')
        self.open(base_url)
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test_frontend", "#welcome-header")
        self.assert_element("#tickets div h4")
        self.assert_text("t1 100", "#tickets div h4")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_login_password_failed(self, *_):
        """ Login and verify if the tickets are correctly listed."""
        self.open(base_url + '/login')
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "wrong_password")
        self.click('input[type="submit"]')
        self.assert_element("#message")
        self.assert_text("login failed", "#message")
