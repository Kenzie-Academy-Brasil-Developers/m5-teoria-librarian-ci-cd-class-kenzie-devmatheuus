import ipdb
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView, Request, Response, status

from books.models import Book

from .permissions import IsAdminOrReadOnly, IsBookOwnerOrReadOnly
from .serializers import BookSerializer


class BookView(APIView, PageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request: Request) -> Response:
        books = Book.objects.all()
        result_page = self.paginate_queryset(books, request, view=self)

        serializer = BookSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(librarian=request.user)

        return Response(serializer.data, status.HTTP_201_CREATED)


class BookDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsBookOwnerOrReadOnly]

    def get(self, request: Request, book_id: int) -> Response:
        # print("=" * 100)
        # print("Executando BookDetailView GET")
        # print("=" * 100)

        book = get_object_or_404(Book, id=book_id)
        serializer = BookSerializer(book)

        return Response(serializer.data)

    def patch(self, request: Request, book_id: int) -> Response:
        # print("=" * 100)
        # print("Executando BookDetailView PATCH")
        # print("=" * 100)

        book = get_object_or_404(Book, id=book_id)
        self.check_object_permissions(request, book)
        # ipdb.set_trace()

        serializer = BookSerializer(book, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(librarian=request.user)

        return Response(serializer.data)

    def delete(self, request: Request, book_id: int) -> Response:
        # print("=" * 100)
        # print("Executando BookDetailView DELETE")
        # print("=" * 100)

        book = get_object_or_404(Book, id=book_id)
        self.check_object_permissions(request, book)

        book.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ProtectedView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    # print("=" * 100)
    # print("Executando ProtectedView")
    # print("=" * 100)
    # permission_classes = [IsAdminUser]

    # and (separador virgula [,])
    """
        GET:
            IsAuthenticatedOrReadOnly True
            IsAdminUser False
            True and False -> False
    """

    # permission_classes = [IsAuthenticatedOrReadOnly, IsAdminUser]

    # ou (separador pipe [|])
    """
        GET:
            IsAuthenticatedOrReadOnly True
            IsAdminUser False
            True or False -> True
    """
    # permission_classes = [IsAuthenticatedOrReadOnly | IsAdminUser]

    def get(self, request: Request) -> Response:
        # print("=" * 100)
        # print("Executando ProtectedView GET")
        # print("=" * 100)

        return Response({"msg": "bem vindo ao GET"})

    def post(self, request: Request) -> Response:
        # print("=" * 100)
        # print("Executando ProtectedView POST")
        # print("=" * 100)

        return Response({"msg": "bem vindo ao POST"}, status.HTTP_201_CREATED)
