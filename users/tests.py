from django.contrib.auth import get_user_model
from django.test import TestCase


class UserModelTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="tester",
            email="tester@example.com",
            password="s3cret-pass",
        )
        self.assertEqual(user.email, "tester@example.com")
        self.assertTrue(user.check_password("s3cret-pass"))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_str_returns_something(self):
        User = get_user_model()
        user = User.objects.create_user(username="tester2", password="pw123456")
        self.assertTrue(str(user))
