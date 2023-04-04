from django.test import TestCase
from base.models import EndUser, Travelogue
from django.contrib.auth.models import User, Group
from django.urls import reverse
import yatra.settings as settings
import os

class TraveloguesTestCase(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_user(username="test1", password="test1",
                                                  is_superuser=True, is_staff=True, is_active=True)

        # create test user 2
        self.group = Group.objects.create(name='endusers')
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
            'enduser':self.enduser,'title':'title', 'description':'description', 'image1':open("E://a.png", 'rb')
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('travelogues_uploaded'))

    def test_verify_travelogue(self):
        image = os.path.join(settings.MEDIA_ROOT,'default_photo.jpg' )
        t = Travelogue(enduser=self.enduser, title= 'title',description= 'description', image1=image)
        t.save()
        self.assertEqual(t.is_approved, "Pending")
        self.client.login(username='test1', password='test1')
        t.is_approved = "Approved"
        t.save()
        self.assertEqual(t.is_approved, "Approved")