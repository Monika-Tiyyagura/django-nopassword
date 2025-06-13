# -*- coding: utf8 -*-
import time
from datetime import datetime
from unittest.mock import patch

from django.contrib.auth import authenticate, get_user_model
from django.test import TestCase
from django.test.utils import override_settings
from django.utils import timezone
from django.utils.timezone import make_aware, get_current_timezone

from nopassword.models import LoginCode


class TestLoginCodes(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username='test_user')
        self.user2 = get_user_model().objects.create(username='test_user2')
        self.inactive_user = get_user_model().objects.create(username='inactive', is_active=False)
        self.loginCodeInstance = LoginCode(
            id="2b6e8fa2c164f78bf37d998930e848968991f5bf9c36a92b591bf34a9540c11e", 
            user=self.user,
            expires_at=make_aware(datetime(2024, 2, 21, 11, 50, 19), get_current_timezone())
        )
        self.code = LoginCode.create_code_for_user(self.user)

    def tearDown(self):
        LoginCode.objects.all().delete()
    
    def test_created_model(self):
        self.assertEqual(len(self.loginCodeInstance.id), 64)
        self.assertTrue(isinstance(self.loginCodeInstance.id, str))
        self.assertEqual(self.loginCodeInstance.user, self.user)
        self.assertEqual(self.loginCodeInstance.timestamp, make_aware(datetime(2022, 2, 21, 15, 30, 0), get_current_timezone()))
        timestamp_recovered = make_aware(datetime.strptime(str(self.loginCodeInstance.timestamp), "%Y-%m-%d %H:%M:%S"), get_current_timezone())
        self.assertTrue(isinstance(timestamp_recovered, datetime))
        self.assertTrue(isinstance(self.loginCodeInstance.expires_at, datetime))
        self.assertTrue(self.loginCodeInstance.expires_at > timezone.now() + timezone.timedelta(minutes=4, seconds=50))
        self.assertTrue(self.loginCodeInstance.expires_at < timezone.now() + timezone.timedelta(minutes=5, seconds=1))
        self.assertEqual(self.loginCodeInstance.next, "")

    def test_login_backend(self):
        self.assertEqual(len(self.code.code), 64)
        self.assertIsNotNone(authenticate(username=self.user.username, code=self.code.code))
        self.assertIsNone(LoginCode.create_code_for_user(self.inactive_user))
    
    @patch("nopassword.models.timezone.now")
    def test_login_backend_after_expired_at(self, mock_now):
        mock_now.return_value = make_aware(datetime(2100, 1, 1, 0, 0, 1), get_current_timezone())
        expired_login = LoginCode(
            id="d5d9e97b-85b1-4e18-9c59-75ea31761945", 
            user=self.user2
        )
        code = expired_login.create_code_for_user(self.user2)
        self.assertIsNone(authenticate(username=self.user2.username, code=code))

    @override_settings(NOPASSWORD_NUMERIC_CODES=True)
    def test_numeric_code(self):
        code = LoginCode.create_code_for_user(self.user)
        self.assertGreater(len(code.code), 64)
        self.assertTrue(code.code.isdigit())

    def test_next_value(self):
        code = LoginCode.create_code_for_user(self.user, next='/secrets/')
        self.assertEqual(code.next, '/secrets/')

    @override_settings(NOPASSWORD_LOGIN_CODE_TIMEOUT=1)
    def test_code_timeout(self):
        timeout_code = LoginCode.create_code_for_user(self.user)
        time.sleep(3)
        self.assertIsNone(authenticate(username=self.user.username, code=timeout_code.code))

    def test_str(self):
        code = LoginCode(user=self.user, timestamp=make_aware(datetime(2018, 7, 1), get_current_timezone()))
        self.assertEqual(str(code), 'test_user - 2018-07-01 00:00:00')
