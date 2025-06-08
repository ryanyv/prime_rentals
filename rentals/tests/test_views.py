import pytest
from django.urls import reverse
from django.utils import timezone
from rentals.models import Property


@pytest.mark.django_db
def test_property_list_view(client):
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
    url = reverse('rentals:property_list')
    response = client.get(url)
    assert response.status_code == 200
    assert b'P1' in response.content
