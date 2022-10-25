import ipdb
from rest_framework import permissions
from rest_framework.views import Request, View

from books.models import Book


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        # print("=" * 100)
        # print("Executando IsAdminOrReadOnly has_permission")
        # print("=" * 100)
        # ipdb.set_trace()

        # if request.method == "GET":
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_superuser


class IsBookOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, book: Book):
        # print("=" * 100)
        # print("Executando IsBookOwnerOrReadOnly has_object_permission")
        # print("=" * 100)

        return request.user == book.librarian
