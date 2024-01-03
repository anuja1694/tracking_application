import unittest
from main import app
import os


class TestRegister(unittest.TestCase):

    def setUp(self):
        app.testing = True
        app.config['SECRET_KEY'] = os.urandom(24)
        self.client = app.test_client()



    def test_register_existing_user(self):
        response = self.client.post('', data=dict(name='test_user', password='test_password'))
        response = self.client.post('/register', data=dict(name='test_user', password='test_password'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Username already taken', response.data)




