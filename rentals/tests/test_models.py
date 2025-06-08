import pytest
from django.contrib.auth import get_user_model
from rentals.models import Property, Amenity, Feature, Review
from django.utils import timezone


@pytest.mark.django_db
def test_property_average_rating():
    amenity = Amenity.objects.create(name='WiFi')
    feature = Feature.objects.create(name='Pool')
    prop = Property.objects.create(
        title='Test Property',
        description='desc',
        location='loc',
        price_nightly=100,
        price_monthly=1000,
        rental_type=Property.SHORT,
        bedrooms=1,
        bathrooms=1,
        guests=2,
        sqft=500,
        main_image='test.jpg',
        available_from=timezone.now().date(),
        available_to=timezone.now().date(),
    )
    prop.amenities.add(amenity)
    prop.features.add(feature)
    user = get_user_model().objects.create(username='u')
    Review.objects.create(property=prop, user=user, rating=4)
    Review.objects.create(property=prop, user=user, rating=2)
    assert prop.average_rating() == 3
