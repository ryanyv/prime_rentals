import pytest
from django.urls import reverse
from django.utils import timezone
from rentals.models import Property
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
def test_short_term_list_view(client):
    Property.objects.create(
        title='P1',
        description='d',
        location='loc',
        price_nightly=10,
        price_monthly=100,
        rental_type=Property.SHORT,
        bedrooms=1,
        bathrooms=1,
        guests=2,
        sqft=100,
        main_image='a.jpg',
        available_from=timezone.now().date(),
        available_to=timezone.now().date(),
    )
    url = reverse('rentals:short_term_list')
    response = client.get(url)
    assert response.status_code == 200
    assert b'P1' in response.content


@pytest.mark.django_db
def test_property_add_requires_login(client):
    url = reverse('rentals:property_add')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_property_add_view_staff(client, django_user_model):
    user = django_user_model.objects.create_user('staff', 's@example.com', 'pw', is_staff=True)
    client.force_login(user)
    url = reverse('rentals:property_add')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_property_list_requires_login(client):
    url = reverse('rentals:property_list')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_property_list_view_staff(client, django_user_model):
    user = django_user_model.objects.create_user('staff2', 's2@example.com', 'pw', is_staff=True)
    Property.objects.create(
        title='P2',
        description='d',
        location='loc',
        price_nightly=10,
        price_monthly=100,
        rental_type=Property.SHORT,
        bedrooms=1,
        bathrooms=1,
        guests=2,
        sqft=100,
        main_image='a.jpg',
        available_from=timezone.now().date(),
        available_to=timezone.now().date(),
    )
    client.force_login(user)
    url = reverse('rentals:property_list')
    response = client.get(url)
    assert response.status_code == 200
    assert b'P2' in response.content


