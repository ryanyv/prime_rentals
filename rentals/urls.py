from django.urls import path
from . import views

app_name = 'rentals'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('luxury/', views.LuxuryHomeView.as_view(), name='luxury_home'),
    path('luxury/properties/', views.LuxuryPropertiesView.as_view(), name='luxury_properties'),
    path('luxury/about/', views.LuxuryAboutView.as_view(), name='luxury_about'),
    path('properties/short-term/', views.ShortTermListView.as_view(), name='short_term_list'),
    path('properties/long-term/', views.LongTermListView.as_view(), name='long_term_list'),
    path('properties/<slug:slug>/', views.PropertyDetailView.as_view(), name='property_detail'),
    path('team/', views.TeamListView.as_view(), name='team'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('book/<int:pk>/', views.BookingCreateView.as_view(), name='book_property'),
    path('manage/properties/', views.PropertyAdminListView.as_view(), name='property_list'),
    path('admin/rentals/property/add/', views.PropertyCreateView.as_view(), name='property_add'),
]
