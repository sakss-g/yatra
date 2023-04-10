from django.test import TestCase
from base.models import Vehicle, Location, Host, EndUser
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import reverse


class VehicleRelatedTest(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_user(username="test1", password="test1",
                                                  is_superuser=True, is_staff=True, is_active=True)
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

        self.vehicle_data = {
            'number_plate': 'ABC123',
            'location': self.location.id,
            'bluebook_id': '123456',
            'description': 'Test vehicle',
            'feature': 'Test feature',
            'price': 100,
            'type': 'Sedan',
            'bluebook': open("D://car.jpg", 'rb'),
            'image1': open("D://car.jpg", 'rb'),
            'image2': open("D://car.jpg", 'rb'),
        }

    def test_add_vehicle_get(self):
        self.client.login(username="test_host", password="password")
        response = self.client.get(reverse('add_vehicles'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vehicles/add_vehicles.html')

    def test_add_vehicle_post(self):
        self.client.login(username="test_host", password="password")
        response = self.client.post(reverse('add_vehicles'), data=self.vehicle_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Vehicle.objects.count(), 1)
        self.assertEqual(Vehicle.objects.first().number_plate, self.vehicle_data['number_plate'])
        self.assertEqual(Vehicle.objects.first().host, self.host)
        self.assertEqual(Vehicle.objects.first().location.id, self.vehicle_data['location'])
        self.assertEqual(Vehicle.objects.first().bluebook_id, self.vehicle_data['bluebook_id'])
        self.assertEqual(Vehicle.objects.first().description, self.vehicle_data['description'])
        self.assertEqual(Vehicle.objects.first().feature, self.vehicle_data['feature'])
        self.assertEqual(Vehicle.objects.first().price, self.vehicle_data['price'])
        self.assertEqual(Vehicle.objects.first().type, self.vehicle_data['type'])


    def test_update_vehicle_get(self):
        self.client.login(username="test_host", password="password")
        self.client.post(reverse('add_vehicles'), data=self.vehicle_data)
        vehicle = Vehicle.objects.first()
        response = self.client.get(reverse('update_vehicles', args=['1']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vehicles/update_vehicles.html')

    def test_update_post_request(self):
        # log in as the host
        self.client.login(username='test_host', password='password')
        self.client.post(reverse('add_vehicles'), data=self.vehicle_data)
        vehicle = Vehicle.objects.first()
        # create valid form data
        form_data = {
            'number_plate': 'XYZ789',
            'location': vehicle.location.id,
            'bluebook_id': 'newbluebookid',
            'description': 'new vehicle description',
            'feature': 'new vehicle features',
            'price': 200,
            'type': 'SUV',
        }

        # send POST request with valid form data
        response = self.client.post(reverse('update_vehicles', args=['1']), data=form_data, follow=True)

        # assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # assert that the correct template is used
        self.assertTemplateUsed(response, 'vehicles/host_vehicles.html')
        vehicle.refresh_from_db()
        # assert that the response context contains the updated vehicle
        self.assertEqual(vehicle.number_plate, form_data['number_plate'])
        self.assertEqual(vehicle.bluebook_id, form_data['bluebook_id'])
        self.assertEqual(vehicle.description, form_data['description'])
        self.assertEqual(vehicle.feature, form_data['feature'])
        self.assertEqual(vehicle.price, form_data['price'])
        self.assertEqual(vehicle.type, form_data['type'])

    def test_approve_vehicle_view(self):
        self.client.login(username='test_host', password='password')
        self.client.post(reverse('add_vehicles'), data=self.vehicle_data)
        vehicle = Vehicle.objects.first()
        self.client.logout()
        self.client.login(username='test1', password='test1')
        response = self.client.post(reverse('approve_vehicle', args=[vehicle.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('hosting_request'))
        vehicle.refresh_from_db()
        self.assertEqual(vehicle.is_approved, 'Approved')

    def test_reject_vehicle_view(self):
        self.client.login(username='test_host', password='password')
        self.client.post(reverse('add_vehicles'), data=self.vehicle_data)
        vehicle = Vehicle.objects.first()
        self.client.logout()
        self.client.login(username='test1', password='test1')
        response = self.client.post(reverse('reject_vehicle', args=[vehicle.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('hosting_request'))
        vehicle.refresh_from_db()
        self.assertEqual(vehicle.is_approved, 'Rejected')

    def test_delete_vehicle_view(self):
        self.client.login(username='test_host', password='password')
        self.client.post(reverse('add_vehicles'), data=self.vehicle_data)
        vehicle = Vehicle.objects.first()
        response = self.client.post(reverse('delete_vehicles', args=[vehicle.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('host_vehicles'))
        with self.assertRaises(vehicle.DoesNotExist):
            vehicle.refresh_from_db()