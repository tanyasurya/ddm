try:
    from weblog import app
    import unittest

except Exception as e:
    print('Some modules are missiing {}'.format(e))

class FlaskTestCase(unittest.TestCase):

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/")
        statuscode = response.status_code
        print('Testing Index status code is.....', statuscode)
        self.assertEqual(statuscode, 200)

    def test_healthStatus(self):
        tester = app.test_client(self)
        response = tester.get("/health")
        statuscode = response.status_code
        print('Testing Health status code is.....', statuscode)
        self.assertEqual(statuscode, 200)
    

    def test_healthData(self):
        tester = app.test_client(self)
        response = tester.get("/health")
        print('Testing Health, response data is...', response.data)
        self.assertTrue(b'Application is Healthy!' in response.data )

    
if __name__ == '__main__':
    unittest.main()