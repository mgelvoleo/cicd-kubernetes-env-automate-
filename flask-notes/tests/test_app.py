import unittest
from app import app

class FlaskAppTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Welcome to Flask Notes API!", res.data)

if __name__ == '__main__':
    unittest.main()
