from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CustomUser, UserRole
from django.contrib.auth.hashers import check_password

class UserAuthTests(APITestCase):
    def setUp(self):
        self.admin_user = CustomUser.objects.create_user(username='admin_user', password='password123', role=UserRole.ADMIN, is_staff=True, is_superuser=True)
        self.secretaria_user = CustomUser.objects.create_user(username='secretaria_user', password='password123', role=UserRole.SECRETARIA)
        self.profissional_user = CustomUser.objects.create_user(username='profissional_user', password='password123', role=UserRole.PROFISSIONAL_SAUDE)

        # URLs (Consider reversing them for robustness)
        self.register_url = reverse('user-register') # from usuarios.urls
        self.users_list_url = reverse('user-list') # from usuarios.urls
        # Token obtain URL - assumes djangorestframework-simplejwt is configured if needed for API auth
        # For now, using self.client.force_authenticate for simplicity

    def test_create_user_roles(self):
        self.assertEqual(self.admin_user.role, UserRole.ADMIN)
        self.assertEqual(self.secretaria_user.role, UserRole.SECRETARIA)
        self.assertEqual(self.profissional_user.role, UserRole.PROFISSIONAL_SAUDE)

    def test_user_registration(self):
        data = {
            "username": "newuser",
            "password": "newpassword123",
            "password2": "newpassword123",
            "email": "newuser@example.com",
            "role": UserRole.SECRETARIA
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(username="newuser").exists())
        new_user = CustomUser.objects.get(username="newuser")
        self.assertTrue(check_password("newpassword123", new_user.password))
        self.assertEqual(new_user.role, UserRole.SECRETARIA)

    def test_registration_password_mismatch(self):
        data = {
            "username": "anotheruser",
            "password": "password123",
            "password2": "mismatchpassword",
            "email": "another@example.com",
            "role": UserRole.PROFISSIONAL_SAUDE
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_list_users_unauthenticated(self):
        response = self.client.get(self.users_list_url)
        # Default DRF permission is IsAuthenticated, but UserListView might have custom one.
        # Assuming UserListView requires admin or is protected.
        # If RegisterView is AllowAny, UserListView is likely protected.
        # The UserListView was set with IsAdminUser permission in its template.
        # The UserListView in usuarios/views.py is currently commented out for permission_classes
        # If default is IsAuthenticated, this should be 403.
        # If default is AllowAny (unlikely for list view), this would be 200.
        # Given the script context, assuming it's protected.
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) # Or 401 if no auth at all

    def test_list_users_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.users_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 3) # admin, secretaria, profissional

    def test_list_users_as_secretaria(self):
        # Assuming IsAdminUser permission on UserListView or similar protection
        self.client.force_authenticate(user=self.secretaria_user)
        response = self.client.get(self.users_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Test permissions classes directly
    def test_permission_classes(self):
        from usuarios.permissions import IsSecretaria, IsProfissionalSaude, IsAdminUser
        from django.http import HttpRequest

        request_secretaria = HttpRequest()
        request_secretaria.user = self.secretaria_user

        request_profissional = HttpRequest()
        request_profissional.user = self.profissional_user

        request_admin = HttpRequest()
        request_admin.user = self.admin_user


        self.assertTrue(IsSecretaria().has_permission(request_secretaria, None))
        self.assertFalse(IsSecretaria().has_permission(request_profissional, None))
        self.assertTrue(IsProfissionalSaude().has_permission(request_profissional, None))
        self.assertFalse(IsProfissionalSaude().has_permission(request_secretaria, None))
        self.assertTrue(IsAdminUser().has_permission(request_admin, None))
        self.assertFalse(IsAdminUser().has_permission(request_secretaria, None))
