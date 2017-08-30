import os
from unittest import TestCase
from mailchimp.client import Client, ClientOauth

class MailchimpTestCases(TestCase):
    def setUp(self):
        self.access_token=os.environ.get('token')
        self.user=os.environ.get('user')
        self.apikey=os.environ.get('apikey')


