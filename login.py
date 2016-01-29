import os
from time import sleep

import unittest

from appium import webdriver

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class SimpleAndroidTests(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '4.2'
        desired_caps['deviceName'] = 'gnex'
        desired_caps['app'] = PATH('login.apk')

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def tearDown(self):
        # end the session
        self.driver.quit()

    def login(self, usr, pwd):
        print
        print "input { username: '%s', password: '%s' }" % ( usr, pwd )
        self.driver.find_element_by_id("username").send_keys(usr)
        self.driver.find_element_by_id("password").send_keys(pwd)

        print 'click login'
        self.driver.find_element_by_id("login").click()

        output = self.driver.find_element_by_id("output").text
        print 'output ==>', output
        return output

    def test_login_fail(self):
        result = self.login('abc', 'def')
        self.assertTrue(result == 'Login fail')

    def test_login_success(self):
        result = self.login('admin', 'password')
        self.assertTrue(result == 'Login success')

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SimpleAndroidTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
