from django.test import TestCase
from base.models import Host, EndUser
from django.contrib.auth.models import User, Group
from django.urls import reverse


class PaymentTestCase(TestCase):
    def setUp(self):
        # create test user 1
        self.group1 = Group.objects.create(name='hosts')
        user1 = User.objects.create_user(username="testhost1", password="testhost1")
        user1.groups.add(self.group1)
        user1.save()
        host = Host()
        host.user = user1
        host.first_name = "models.CharField(max_length=25)"
        host.last_name = "models.CharField(max_length=25)"
        host.email = "models.EmailField()@email.com"
        host.phone_number = "models"
        host.save()
        self.host = host
        self.assertEqual(self.host.user, user1)


    def test_make_payment(self):
        self.client.login(username='testhost1', password='testhost1')
        response = self.client.get(reverse('handle_payment'))
        print(response)
