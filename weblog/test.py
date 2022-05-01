import weblog
import unittest

class WeblogTestSuite(unittest.TestCase):

    def setUp(self):
        weblog.app.testing = True
        self.app = weblog.app.test_client()

    def test_health(self):
        result = self.all.get('/health')
        self.assertEqual(result, 'Application is Healthy!')

    
if __name__ == '__main__':
    unittest.main()