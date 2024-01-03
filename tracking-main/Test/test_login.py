import unittest
from flask import session
from main import app

class TestLogin(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test-secret-key'
        self.client = app.test_client()

    def test_failed_login(self):
        with self.client:
            response = self.client.post('/login', data=dict(
                name='testuser',
                password='wrongpassword'
            ), follow_redirects=True)
            self.assertIn(b'Username or password did not match', response.data)
            self.assertFalse(session.get('user'))

if __name__ == '__main__':
    unittest.main()
