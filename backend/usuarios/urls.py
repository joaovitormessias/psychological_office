from django.urls import path
from .views import UserListView, UserDetailView, RegisterUserView

urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('register/', RegisterUserView.as_view(), name='user-register'),
]
