from app import app
import unittest

# Each test should only test one piece of functionality

class FlaskTestCase(unittest.TestCase):

    # Ensure that flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text') # use unittest library to call the login route
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()