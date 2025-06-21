from django.urls import path
from . import views

urlpatterns = [
    # Registration and profile editing removed - only admin can create/edit users
    path('profile/', views.profile, name='profile'),
]