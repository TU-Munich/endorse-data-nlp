import secrets
from unittest import TestCase

from services.user_service import user_hash_password


class TestUser_hash_password(TestCase):
    def test_user_hash_password(self):
        salt = secrets.token_hex(16)
        pw_hashed = user_hash_password("thisMustBeAVery1Save!Password", "PEPPER", salt)
        if self.assertIsNone(pw_hashed):
            self.fail()
