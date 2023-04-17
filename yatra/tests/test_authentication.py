from django.test import TestCase
from base.models import Host, EndUser
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.shortcuts import reverse


class AuthenticationTestCase(TestCase):
    def setUp(self):
        # create test user 1
        self.group1 = Group.objects.create(name='host')
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

        # create test user 2
        self.group2 = Group.objects.create(name='enduser')
        user2 = User.objects.create_user(username="testenduser1", password="testenduser1")
        user1.groups.add(self.group2)
        user2.save()
        enduser = EndUser()
        enduser.user = user2
        enduser.first_name = "models.CharField(max_length=25)"
        enduser.last_name = "models.CharField(max_length=25)"
        enduser.email = "models.EmailField()@email.com"
        enduser.phone_number = "models"
        enduser.save()
        self.enduser = enduser
        self.assertEqual(self.enduser.user, user2)

    def test_host_can_login(self):
        self.client.login(username='testhost1', password='testhost1')
        response = self.client.get(reverse('host_profile'))
        # checking if the user is logged in
        self.assertEqual(str(response.context['user']), 'testhost1')
        # checking if the response is "success"
        self.assertEqual(response.status_code, 200)
        # checking if the correct template is used or not
        self.assertTemplateUsed(response, 'host/host_profile.html')


    def test_redirecthost_if_not_logged_in(self):
        response = self.client.get(reverse('host_profile'))
        self.assertRedirects(response, '/login/?next=/hostprofile/')


    def test_enduser_can_login(self):
        self.client.login(username='testenduser1', password='testenduser1')
        response = self.client.get(reverse('home'))
        # checking if the user is logged in
        self.assertEqual(str(response.context['user']), 'testenduser1')
        # checking if the response is "success"
        self.assertEqual(response.status_code, 200)
        # checking if the correct template is used or not
        self.assertTemplateUsed(response, 'base/home.html')


    def test_redirectenduser_if_not_logged_in(self):
        response = self.client.get(reverse('host_profile'))
        self.assertRedirects(response, '/login/?next=/hostprofile/')


    def test_redirect_if_logged_out(self):
        self.client.login(username='testhost1', password='testhost1')
        self.client.logout()
        response = self.client.get(reverse('login'))
        # checking if the response is "success"
        self.assertEqual(response.status_code, 200)
        # checking if the correct template is used or not
        self.assertTemplateUsed(response, 'base/login.html')


    def test_register_host(self):
        response = self.client.post(reverse('register_host'),
                         data={"first_name":"modelsCharField",
                            "last_name": "modelsCharField",
                            "email": "models@email.com",
                            "phone_number" : "models",
                            "password":"password123"}
                         )
        print(response)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))



    def test_register_enduser(self):
        response = self.client.post(reverse('register_enduser'),
                                    data={"first_name": "modelsCharField",
                                          "last_name": "modelsCharField",
                                          "email": "models@email.com",
                                          "phone_number": "models",
                                          "password": "password123"}
                                    )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
