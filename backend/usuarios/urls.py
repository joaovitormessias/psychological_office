from django.urls import path
from .views import UserListView, UserDetailView, RegisterUserView, CurrentUserView

urlpatterns = [
    path("me/", CurrentUserView.as_view(), name="user-me"),
    path('', UserListView.as_view(), name='user-list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('register/', RegisterUserView.as_view(), name='user-register'),
]
