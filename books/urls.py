from django.urls import path

from . import views

urlpatterns = [
    path("books/protected/", views.ProtectedView.as_view()),
    path("books/", views.BookView.as_view(), name="book-view"),
    path("books/<int:book_id>/", views.BookDetailView.as_view(), name="book-detail"),
]
