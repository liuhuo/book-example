__author__ = 'liuhuo'

from .base import FunctionalTest
from selenium.webdriver.support.ui import WebDriverWait
import time


class LoginTest(FunctionalTest):
    def switch_to_new_window(self, text_in_title):
        retries = 60
        while retries > 0:
            for handle in self.browser.window_handles:
                self.browser.switch_to_window(handle)
                if text_in_title in self.browser.title:
                    return
            retries -= 1
            time.sleep(0.5)
        self.fail('could not find window')

    def wait_for_element_with_id(self, element_id):
        WebDriverWait(self.browser, timeout=30).until(lambda b: b.find_element_by_id(element_id))

    def test_login_with_persona(self):
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('login').click()

        self.switch_to_new_window('Mozilla Persona')

        self.browser.find_element_by_id('authentication_email').send_keys('huoliu@mockmyid.com')
        self.browser.find_element_by_tag_name('button').click()

        self.switch_to_new_window('To-Do')

        self.wait_for_element_with_id('logout')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn('huoliu@mockmyid.com', navbar.text)

