
from django.urls import path
from .views import UserListCreateView, UserRetrieveUpdateDestroyView, UserUpdateView, PasswordChangeView, LoginView, LogoutView

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),
    path('users/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path('users/<int:pk>/passwordchange/', PasswordChangeView.as_view(), name='password-change'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/<int:pk>/logout/', LogoutView.as_view(), name='logout'),
]