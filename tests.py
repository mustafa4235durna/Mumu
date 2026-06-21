"""
Mumu WhatsApp Assistant - Test Suite
"""

import unittest
from app import app, SYSTEM_MESSAGE


class TestMumuApp(unittest.TestCase):
    """Mumu uygulamasının test suite'i"""
    
    def setUp(self):
        """Test öncesi hazırlık"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_home_endpoint(self):
        """Ana sayfa endpoint'ini test et"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Mumu', str(response.json))
    
    def test_health_endpoint(self):
        """Health endpoint'ini test et"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'healthy')
    
    def test_webhook_empty_message(self):
        """Boş mesaj webhook'u test et"""
        response = self.client.post('/webhook', data={
            'Body': '',
            'From': 'whatsapp:+1234567890'
        })
        self.assertEqual(response.status_code, 400)
    
    def test_system_message_exists(self):
        """Sistem mesajı var mı?"""
        self.assertIsNotNone(SYSTEM_MESSAGE)
        self.assertIn("Mumu", SYSTEM_MESSAGE)


class TestUtilsFunctions(unittest.TestCase):
    """Utils fonksiyonlarını test et"""
    
    def test_truncate_message(self):
        """Mesaj kesme fonksiyonunu test et"""
        from utils import truncate_message
        
        long_message = "a" * 1000
        result = truncate_message(long_message, max_length=50)
        self.assertEqual(len(result), 50)
        self.assertTrue(result.endswith("..."))
    
    def test_is_greeting(self):
        """Selamlama kontrolü"""
        from utils import is_greeting
        
        self.assertTrue(is_greeting("Merhaba!"))
        self.assertTrue(is_greeting("Selam"))
        self.assertFalse(is_greeting("Nasıl hava?"))
    
    def test_validate_message(self):
        """Mesaj doğrulama"""
        from utils import validate_message
        
        is_valid, msg = validate_message("Test mesajı")
        self.assertTrue(is_valid)
        
        is_valid, msg = validate_message("")
        self.assertFalse(is_valid)


if __name__ == '__main__':
    unittest.main()
