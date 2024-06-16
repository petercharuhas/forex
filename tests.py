import unittest
from app import app

class ForexConverterTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_invalid_currency_from(self):
        response = self.app.post('/convert', data=dict(
            currency_from='XXX', currency_to='USD', amount='100'
        ))
        self.assertIn(b"Invalid 'from' currency", response.data)

    def test_invalid_currency_to(self):
        response = self.app.post('/convert', data=dict(
            currency_from='USD', currency_to='XXX', amount='100'
        ))
        self.assertIn(b"Invalid 'to' currency", response.data)

    def test_invalid_amount(self):
        response = self.app.post('/convert', data=dict(
            currency_from='USD', currency_to='EUR', amount='abc'
        ))
        self.assertIn(b"Invalid amount", response.data)

    def test_valid_conversion(self):
        response = self.app.post('/convert', data=dict(
            currency_from='USD', currency_to='EUR', amount='100'
        ))
        self.assertIn(b"Converted Amount", response.data)

if __name__ == '__main__':
    unittest.main()
