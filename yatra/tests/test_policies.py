from django.test import TestCase
from base.models import Host, EndUser
from django.contrib.auth.models import User, Group
from django.urls import reverse


class PoliciesTestCase(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_user(username="test1", password="test1",
                                                  is_superuser=True, is_staff=True, is_active=True)

    # def test_view_privacypolicies(self):
    #     self.client.login(username='test1', password='test1')
    #     response = self.client.get(reverse('faqs'))
    #     # checking if the response is "success"
    #     self.assertEqual(response.status_code, 200)
    #     # checking if the correct template is used or not
    #     self.assertTemplateUsed(response, 'faqs/faqs.html')

    # def test_view_privacypolicies(self):
    #     response = self.client.get(reverse('faqs'))
    #     # checking if the response is "success"
    #     self.assertEqual(response.status_code, 200)
    #     # checking if the correct template is used or not
    #     self.assertTemplateUsed(response, 'base/faqs.html')

    # def test_add_privacypolicies_admin(self):
    #     self.client.login(username='test1', password='test1')
    #     response = self.client.post(reverse('add_privacy_policy'),
    #                      data={"policy":"modelsCharField",
    #                             "explanation": "modelsCharField",
    #                         }
    #                     )
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, reverse('privacy_policy'))


    def test_view_faqs(self):
        self.client.login(username='test1', password='test1')
        response = self.client.get(reverse('privacy_policy'))
        # checking if the response is "success"
        self.assertEqual(response.status_code, 200)
        # checking if the correct template is used or not
        self.assertTemplateUsed(response, 'privacypolicy/privacypolicy.html')

    def test_view_faqs(self):
        response = self.client.get(reverse('privacy_policy'))
        # checking if the response is "success"
        self.assertEqual(response.status_code, 200)
        # checking if the correct template is used or not
        self.assertTemplateUsed(response, 'base/privacypolicy.html')


    def test_add_faqs_admin(self):
        self.client.login(username='test1', password='test1')
        response = self.client.post(reverse('add_faqs'),
                                    data={"question": "modelsCharField",
                                          "answer": "modelsCharField",
                                          }
                                    )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('faqs'))

    def test_view_termsandconditions(self):
        self.client.login(username='test1', password='test1')
        response = self.client.post(reverse('terms_and_conditions'))
        # checking if the response is "success"
        self.assertEqual(response.status_code, 200)
        # checking if the correct template is used or not
        self.assertTemplateUsed(response, 'termsandconditions/termsandconditions.html')

    # def test_view_termsandconditions(self):
    #     response = self.client.post(reverse('terms_and_conditions'))
    #     # checking if the response is "success"
    #     self.assertEqual(response.status_code, 200)
    #     # checking if the correct template is used or not
    #     self.assertTemplateUsed(response, 'base/termsandconditions.html')

    # def test_add_termsandcondition_admin(self):
    #     self.client.login(username='test1', password='test1')
    #     response = self.client.post(reverse('add_terms_and_conditions'),
    #                                 data={"term": "modelsCharField",
    #                                       "explanation": "modelsCharField",
    #                                       }
    #                                 )
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, reverse('terms_and_conditions'))
