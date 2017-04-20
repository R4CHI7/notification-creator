# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime, timedelta

from django.test import TestCase, Client
from django.contrib.auth.models import User

from .models import Notification
from .forms import NotificationForm
from .common import getNotificationCountByStatus
from .tasks import notify


class NotificationTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a test user for logging in.
        User.objects.create_user('test', 'test123@gmail.com', 'testpassword')

        # Create a notification object.
        Notification.objects.create(header='Use Code TRANSFORM10 Today!',
                                    content='10% OFF on your Recommended Plan',
                                    image_url='http://i.imgur.com/0K40axT.jpg',
                                    user_query='SELECT id FROM auth_user',
                                    send_at=datetime.utcnow() + timedelta(minutes=2))

    def test_index(self):
        # Call the index URL without logging in.
        response = self.client.get('/notification/')

        # The response should be a redirect to the login page.
        self.assertEqual(response.status_code, 302)

        # Login using the test user.
        login_response = self.client.login(username='test', password='testpassword')
        self.assertTrue(login_response)

        # Call the index URL again.
        response = self.client.get('/notification/')

        # The response should be a valid HTML page.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    def test_create_get(self):
        # Call the index URL without logging in.
        response = self.client.get('/notification/create/')

        # The response should be a redirect to the login page.
        self.assertEqual(response.status_code, 302)

        # Login using the test user.
        login_response = self.client.login(username='test', password='testpassword')
        self.assertTrue(login_response)

        # Call the index URL again.
        response = self.client.get('/notification/create/')

        # The response should be a valid HTML page.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

        # Test the template which was rendered for this view.
        templates = response.templates
        self.assertEqual(templates[0].name, 'notification/create.html')

    def test_create_post(self):
        # Login using the test user.
        login_response = self.client.login(username='test', password='testpassword')
        self.assertTrue(login_response)

        # Prepare invalid data.
        invalid_payload = {
            'header': 'Not 20 characters',
            'content': 'Not 20 characters',
            'image_url': 'invalid_url',
            'user_query': 'SELECT id FROM auth_user;',
            'send_at': 'invalid_date'
        }

        # Test the form.
        form = NotificationForm(data=invalid_payload)
        self.assertFalse(form.is_valid())

        # Test the view. The response should be a 200 with the create form rendered.
        response = self.client.post('/notification/create/', data=invalid_payload)
        self.assertEqual(response.status_code, 200)
        templates = response.templates
        self.assertEqual(templates[0].name, 'notification/create.html')

        # Prepare valid data.
        valid_payload = {
            'header': 'Use Code TRANSFORM10 Today!',
            'content': '10% OFF on your Recommended Plan',
            'image_url': 'http://i.imgur.com/0K40axT.jpg',
            'user_query': 'SELECT id FROM auth_user;',
            'send_at': '22/04/2017 22:30'
        }

        # Test the form.
        form = NotificationForm(data=valid_payload)
        self.assertTrue(form.is_valid())

        # Test the view. The response should be a 302 with the index page rendered.
        response = self.client.post('/notification/create/', data=valid_payload)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/notification/')

    def test_getNotificationCountByStatus(self):
        # Test the helper method which returns number of notifications by status.
        count = getNotificationCountByStatus(1)
        self.assertEqual(count, 1)

    def test_task(self):
        result = notify.apply_async((1,))
        self.assertTrue(result)
