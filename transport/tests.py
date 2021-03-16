from django.test import TestCase, Client
from .models import Trip, Order, User
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import pathlib
import os
from selenium.webdriver.common.keys import Keys
import json

def file_uri(filename):
    return pathlib.Path(os.path.abspath(filename)).as_uri()


# Create your tests here.
class TransportTestCase(TestCase):
    def setUp(self):
        
        user=User(username='test_user')
        user.set_password('1234')
        user.save()
        order = Order(user=user, description='this is a test',distance='1', duration='1', origin='here',destination='here', date='2020-12-12', scope='national', weight='0',size='0', price='12.12')
        order.save()
        

    def test_is_valid_order(self):
        '''
        test if the origin matches
        '''

        o = Order.objects.get(origin='here')
        self.assertFalse(o.is_valid())

    def test_index(self):
        '''
        test if the index page loads
        '''

        c = Client()
        response = c.get("")
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        '''
        test if login page loads
        '''

        c = Client()
        response = c.get('/login')
        self.assertEqual(response.status_code, 200)
    
    def test_profile_page(self):
        '''
        test if profile page loads
        '''
        
        c = Client()
        login = c.login(username='test_user', password='1234')
        self.assertTrue(login)

    
class BrowserTestCase(TestCase):
    def test_login_selenium(self):
        '''
        for later username dummyuser2 password dummypassword2
        '''

        self.driver = webdriver.Chrome()
        self.driver.get('http://127.0.0.1:8000/')
        self.driver.find_element_by_id('login_dropdown_button').click()
        self.driver.find_element_by_id('login_username_input').send_keys('dummyuser')
        self.driver.find_element_by_id('login_password_input').send_keys('dummy_password' + Keys.ENTER)
        self.driver.implicitly_wait(3)
        self.assertEqual(self.driver.title, 'Home')
