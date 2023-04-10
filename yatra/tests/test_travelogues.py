from django.test import TestCase
from base.models import EndUser, Travelogue
from django.contrib.auth.models import User, Group
from django.urls import reverse
import yatra.settings as settings
import os
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile

class TraveloguesTestCase(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_user(username="test1", password="test1",
                                                  is_superuser=True, is_staff=True, is_active=True)

        # create test user 2
        self.group = Group.objects.create(name='enduser')
        user = User.objects.create_user(username="testenduser1", password="testenduser1")
        user.groups.add(self.group)
        user.save()
        enduser = EndUser()
        enduser.user = user
        enduser.first_name = "models.CharField(max_length=25)"
        enduser.last_name = "models.CharField(max_length=25)"
        enduser.email = "models.EmailField()@email.com"
        enduser.phone_number = "models"
        enduser.save()
        self.enduser = enduser
        self.assertEqual(self.enduser.user, user)
        self.image = SimpleUploadedFile("jeep.jpeg", content=b'', content_type='image/jpg')
        self.travelogue = Travelogue.objects.create(
            enduser=self.enduser,
            title='title',
            description='description',
            image1=self.image
        )

    def test_view_travelogues(self):
        self.client.login(username='test1', password='test1')
        response = self.client.get(reverse('all_travelogues'))
        # checking if the response is "success"
        self.assertEqual(response.status_code, 200)
        # checking if the correct template is used or not
        self.assertTemplateUsed(response, 'travelogues/travelogues.html')


    def test_add_travelogue(self):
        self.client.login(username="testenduser1", password="testenduser1")
        response = self.client.post(reverse('submit_travelogue'), {
            'enduser':self.enduser,'title':'title', 'description':'description', 'image1':open("D://car.jpg", 'rb')
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Travelogue.objects.filter(enduser=self.enduser).exists())
        self.assertRedirects(response, reverse('travelogues_uploaded'))


    def test_approve_travelogue(self):
        self.client.login(username='test1', password='test1')
        response = self.client.post(reverse('approve_travelogue', args=[self.travelogue.pk]))
        self.travelogue.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.travelogue.is_approved, 'Approved')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Travelogue approved.')
        self.assertRedirects(response, reverse('verify_travelogue'))


    def test_reject_travelogue(self):
        self.client.login(username='test1', password='test1')
        response = self.client.post(reverse('reject_travelogue', args=[self.travelogue.pk]))
        self.travelogue.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.travelogue.is_approved, 'Rejected')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Travelogue rejected.')
        self.assertRedirects(response, reverse('verify_travelogue'))