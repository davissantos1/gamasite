from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='account_profile'),
    path('profile/details/', views.profile_details, name='account_profile_details'),
    path('profile/edit/', views.edit_profile, name='account_edit_profile'),
    
]
