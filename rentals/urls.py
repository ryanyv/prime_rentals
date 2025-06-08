from django.urls import path
from . import views

app_name = 'rentals'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('properties/', views.PropertyListView.as_view(), name='property_list'),
    path('properties/<slug:slug>/', views.PropertyDetailView.as_view(), name='property_detail'),
    path('team/', views.TeamListView.as_view(), name='team'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('book/<int:pk>/', views.BookingCreateView.as_view(), name='book_property'),
]
