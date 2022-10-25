import ipdb
from django.urls import reverse
from librarians.models import Librarian
from rest_framework.test import APITestCase
from rest_framework.views import status


class LibrarianRegisterViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.base_url = "/api/librarians/register/"
        cls.librarian_data = {
            "username": "new_librarian",
            "ssn": 2222,
            "birthdate": "1993-03-03",
            "password": "1234",
        }

    def test_can_register_librarian(self):
        response = self.client.post(self.base_url, data=self.librarian_data)
        # ipdb.set_trace()
        # expected_status_code = 201
        expected_status_code = status.HTTP_201_CREATED
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_register_librarian_fields(self):
        response = self.client.post(self.base_url, data=self.librarian_data)
        expected_return_fields = (
            "id",
            "username",
            "shift",
            "ssn",
            "birthdate",
            "is_superuser",
        )
        # expected_return_fields = ("id", "username", "ssn", "birthdate")

        self.assertEqual(len(response.data.keys()), 6)

        # não me garante que SOMENTE as chaves que eu defini vieram na response
        for expected_field in expected_return_fields:
            self.assertIn(expected_field, response.data)

        # verificando se SOMENTE as chaves que eu defini vieram na response
        result_return_fields = tuple(response.data.keys())

        self.assertTupleEqual(expected_return_fields, result_return_fields)


class LoginTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.base_url = reverse("login-auth-token")

        # ipdb.set_trace()

        cls.librarian_credentials = {"username": "new_librarian", "password": "1234"}

        cls.librarian_data = {
            "username": "new_librarian",
            "ssn": 2222,
            "birthdate": "1993-03-03",
            "password": "1234",
        }

        cls.librarian = Librarian.objects.create_user(**cls.librarian_data)
        # cls.librarian = Librarian.objects.create(**cls.librarian_data)

    def test_login_with_valid_credentials(self):
        response = self.client.post(self.base_url, data=self.librarian_credentials)
        self.assertEqual(200, response.status_code)

    def test_token_field_is_returned(self):
        response = self.client.post(self.base_url, data=self.librarian_credentials)

        # ipdb.set_trace()
        self.assertIn("token", response.data)
