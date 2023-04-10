from django.test import TestCase
from django.urls import reverse
from base.models import Vehicle, RentRequest, Rents, Location, Host, EndUser
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
import datetime


class RentVehicleTest(TestCase):
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

        image = SimpleUploadedFile("jeep.jpeg", content=b'', content_type='image/jpg')
        self.vehicle.bluebook.save("jeep.jpeg", image, save=True)
        self.vehicle.image1.save("jeep.jpeg", image, save=True)
        self.vehicle.image2.save("jeep.jpeg", image, save=True)

        self.rent_request = RentRequest.objects.create(
            renter=self.enduser,
            vehicle=self.vehicle,
            start_date='2023-04-15',
            end_date='2023-04-20'
        )

    def test_vehicle_details_view(self):
        url = reverse('vehicle_details', kwargs={'pk': self.vehicle.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vehicles/vehicle_detail.html')

    def test_request_rent(self):
        self.client.login(username="test_enduser", password="password")  # log in as the end user
        data = {
                'start': datetime.date(2023, 4, 25),
                'end': datetime.date(2023, 4, 28),
            }
        response = self.client.post(
            reverse('vehicle_details', args=[self.vehicle.id]),
            data=data,
            follow=True
        )

        self.assertEqual(response.status_code, 200)

        rent_requests = RentRequest.objects.filter(vehicle=self.vehicle, renter=self.enduser)
        print("Total Requests",len(rent_requests))
        self.assertEqual(len(rent_requests), 2)
        self.assertEqual(rent_requests[1].start_date, datetime.date(2023, 4, 25))
        self.assertEqual(rent_requests[1].end_date, datetime.date(2023, 4, 28))

    def test_rent_request_view(self):
        self.client.login(username='test_host', password='password')
        url = reverse('rent_request')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'host/rent_request.html')

    def test_approve_rent_view(self):
        self.client.login(username='test_host', password='password')
        response = self.client.post(reverse('approve_rent', kwargs={'rid': self.rent_request.pk}))
        self.assertEqual(response.status_code, 302)  # Redirects to rent_request view
        self.assertEqual(Rents.objects.count(), 1)
        self.assertEqual(RentRequest.objects.count(), 0)

    def test_reject_rent_view(self):
        self.client.login(username='test_host', password='password')
        response = self.client.post(reverse('reject_rent', kwargs={'rid': self.rent_request.pk}))
        self.assertEqual(response.status_code, 302)  # Redirects to rent_request view
        self.assertEqual(Rents.objects.count(), 0)
        self.assertEqual(RentRequest.objects.count(), 0)
