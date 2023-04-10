from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from base.models import ReportUser, Rents, RateRent, Vehicle, EndUser, Host, Location
from base.forms import ReportUserForm, RateRentForm

class ReportRentTestCase(TestCase):
    def setUp(self):
        self.host_user = User.objects.create_user(username='test_host', password='password')
        self.end_user = User.objects.create_user(username='test_enduser', password='password')
        self.host_user.groups.create(name='host')
        self.end_user.groups.create(name='enduser')

        self.host = Host.objects.create(user=self.host_user,
                                        first_name="test_name",
                                        last_name="test_last_name",
                                        email="testemail@gmail.com",
                                        phone_number="989932389")

        self.enduser = EndUser.objects.create(user=self.end_user,
                                              first_name="test_name",
                                              last_name="test_last_name",
                                              email="testemail@gmail.com",
                                              phone_number="989932389")

        self.location = Location.objects.create(name="Pokhara")

        self.vehicle = Vehicle.objects.create(
            number_plate="ABC123",
            host=self.host,
            location=self.location,
            bluebook_id="BB123",
            description="Test vehicle",
            feature="Test feature",
            price=50,
            type="Sedan",
            is_approved="Approved",
        )

        self.image = SimpleUploadedFile("jeep.jpeg", content=b'', content_type='image/jpg')
        self.vehicle.bluebook.save("jeep.jpeg", self.image, save=True)
        self.vehicle.image1.save("jeep.jpeg", self.image, save=True)
        self.vehicle.image2.save("jeep.jpeg", self.image, save=True)

        self.rent = Rents.objects.create(
            renter=self.enduser,
            vehicle=self.vehicle,
            start_date='2023-04-15',
            end_date='2023-04-20'
        )

    def test_report_user_GET(self):
        self.client.login(username='test_enduser', password='password')
        response = self.client.get(reverse('report_user', kwargs={'to': self.host_user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reprat/report.html')
        self.assertTrue(isinstance(response.context['form'], ReportUserForm))

    def test_report_user_POST(self):
        self.client.login(username='test_enduser', password='password')
        data = {
            'reason': 'Test reason',
            'image1': open('D:\\car.jpg', "rb"),
        }
        response = self.client.post(
                                    reverse('report_user', kwargs={'to': self.host_user.id}),
                                    data=data,
                                    follow=True,
                                    )

        self.assertTrue(ReportUser.objects.filter(by=self.end_user, to=self.host_user).exists())
        self.assertEqual(ReportUser.objects.get(by=self.end_user, to=self.host_user).reason, 'Test reason')
        self.assertTrue(ReportUser.objects.get(by=self.end_user, to=self.host_user).image1)
        self.assertEqual(ReportUser.objects.get(by=self.end_user, to=self.host_user).status, 'Pending')
        self.assertEqual(len(response.cookies), 1)
        self.assertRedirects(response, reverse('renting_history'))
        self.assertEqual(response.status_code, 200)

    def test_report_user_POST_host(self):
        self.client.login(username='test_host', password='password')

        data = {
            'reason': 'Test reason',
            'image1': open('D:\\car.jpg', "rb"),
        }
        response = self.client.post(reverse('report_user', kwargs={'to': self.end_user.id}),
                                    data=data,
                                    follow=True,
                                    )

        self.assertTrue(ReportUser.objects.filter(by=self.host_user, to=self.end_user).exists())
        self.assertEqual(ReportUser.objects.get(by=self.host_user, to=self.end_user).reason, 'Test reason')
        self.assertTrue(ReportUser.objects.get(by=self.host_user, to=self.end_user).image1)
        self.assertEqual(ReportUser.objects.get(by=self.host_user, to=self.end_user).status, 'Pending')
        self.assertEqual(len(response.cookies), 1)
        self.assertRedirects(response, reverse('rented_history'))
        self.assertEqual(response.status_code, 200)


    def test_rate_rent_POST_enduser(self):
        self.client.login(username='test_enduser', password='password')
        form = RateRentForm(data={'rating': 5})
        self.assertTrue(form.is_valid())
        response = self.client.get(reverse('rate_rent', kwargs={'pk': self.rent.id}), data={'rating': 5})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(RateRent.objects.get(rent=self.rent).rating, 5)
        self.assertEqual(len(response.cookies), 1)

    def test_rate_rent_POST_host(self):
        self.client.login(username='test_host', password='password')
        form = RateRentForm(data={'rating': 5})
        self.assertTrue(form.is_valid())
        response = self.client.get(reverse('rate_rent', kwargs={'pk': self.rent.id}), data={'rating': 5})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(RateRent.objects.get(rent=self.rent).rating, 5)
        self.assertEqual(len(response.cookies), 1)
