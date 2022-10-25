from books.models import Book
from books.models import Author
from django.urls import reverse
from librarians.models import Librarian
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from rest_framework.views import Response, status


class TestBookAuth(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        # Não é necessário, apenas da uma dica sobre tipagem
        cls.client: APIClient
        # cls.client: dict

        common_user_data = {
            "username": "common_user",
            "ssn": 111,
            "birthdate": "1993-03-03",
            "password": "456",
        }

        admin_user_data = {
            "username": "admin_user",
            "ssn": 222,
            "birthdate": "1993-03-03",
            "password": "456",
        }

        # Criando usuário comum e seu Token
        common_user = Librarian.objects.create_user(**common_user_data)
        cls.common_token = Token.objects.create(user=common_user)

        # Criando usuário admin e seu Token
        admin_user = Librarian.objects.create_superuser(**admin_user_data)
        cls.admin_token = Token.objects.create(user=admin_user)

        cls.book_data_1 = {
            "title": "The Lord of The Rings - The Fellowship of The Rings",
            "published_date": "1954-07-29",
            "isbn": "9781002122821",
            "authors": [{
                "name": "Tolkien, JRR",
                "children": 10
            }]
        }

        book_data_2 = {
            "title": "The Lord of The Rings - The Fellowship of The Rings",
            "published_date": "1954-07-29",
            "isbn": "9781002122822",
        }

        book_1 = Book.objects.create(**book_data_2, librarian=admin_user)

        cls.base_books_url = reverse("book-view")
        cls.base_book_detail_url = reverse(
            "book-detail", kwargs={"book_id": book_1.id})

    def test_common_user_cannot_add_book(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.common_token.key)
        response: Response = self.client.post(
            self.base_books_url, data=self.book_data_1
        )

        expected_status_code = status.HTTP_403_FORBIDDEN
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_unauthenticated_user_cannot_add_book(self):
        response: Response = self.client.post(
            self.base_books_url, data=self.book_data_1
        )

        expected_status_code = status.HTTP_401_UNAUTHORIZED
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_user_cannot_update_book_from_another_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.common_token.key)
        response: Response = self.client.patch(
            self.base_book_detail_url, data={"title": "Title Patch"}
        )

        expected_status_code = status.HTTP_403_FORBIDDEN
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_unauthenticated_user_cannot_update_book(self):
        response: Response = self.client.patch(
            self.base_book_detail_url, data={"title": "Title Patch"}
        )

        expected_status_code = status.HTTP_401_UNAUTHORIZED
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_user_can_update_own_book(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.admin_token.key)
        response: Response = self.client.patch(
            self.base_book_detail_url, data={"title": "Title Patch"}
        )

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_user_cannot_delete_book_from_another_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.common_token.key)
        response: Response = self.client.delete(self.base_book_detail_url)

        expected_status_code = status.HTTP_403_FORBIDDEN
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_unauthenticated_user_cannot_delete_book(self):
        response: Response = self.client.delete(self.base_book_detail_url)

        expected_status_code = status.HTTP_401_UNAUTHORIZED
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_user_can_delete_own_book(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.admin_token.key)
        response: Response = self.client.delete(self.base_book_detail_url)

        expected_status_code = status.HTTP_204_NO_CONTENT
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
