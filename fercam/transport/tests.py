from django.test import TestCase, Client
from .models import Trip, Order, User
from selenium import webdriver

def file_uri(filename):
    return pathlib.Path(os.path.abspath(filename)).as_uri()


# Create your tests here.
class TransportTestCase(TestCase):
    def setUp(self):
        user=User(username='test')
        user.save()
        order = Order(user=user, description='this is a test',distance='1', duration='1', origin='here',destination='here', date='2020-12-12', scope='national', weight='0',size='0', price='12.12')
        order.save()


    def test_is_valid_order(self):
        o = Order.objects.get(origin='here')
        self.assertFalse(o.is_valid())


    def test_index(self):
        c = Client()
        response = c.get("")
        print(response)
        self.assertEqual(response.status_code, 200)
