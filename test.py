# test_shadow.py
import unittest
from app import app, db
from models import Contact

class ShadowOpsTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()

    def stealth_post(self, data):
        return self.client.post('/identify', json=data)

    def test_new_contact_creates_primary(self):
        response = self.stealth_post({'email': 'agent@hq.com', 'phoneNumber': '9999'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('primaryContactId', response.json['contact'])

    def test_duplicate_creates_secondary(self):
        self.stealth_post({'email': 'spy@safehouse.com', 'phoneNumber': '1111'})
        self.stealth_post({'email': 'spy@safehouse.com', 'phoneNumber': '2222'})
        response = self.stealth_post({'email': 'spy@safehouse.com', 'phoneNumber': '3333'})
        self.assertTrue(len(response.json['contact']['secondaryContactIds']) >= 1)

if __name__ == '__main__':
    unittest.main()
