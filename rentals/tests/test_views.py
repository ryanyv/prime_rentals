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


from django.test import TestCase
# Property is already imported from rentals.models
# reverse is already imported from django.urls
# timezone is already imported from django.utils

class HomeViewTests(TestCase):
    def setUp(self):
        # Get current date for availability
        today = timezone.now().date()

        self.prop1 = Property.objects.create(
            title='Property Alpha in Test Location 1',
            description='Description for Alpha',
            location='Test Location 1',
            price_nightly=150.00,
            price_monthly=3000.00,
            rental_type=Property.SHORT,
            bedrooms=3,
            bathrooms=2,
            guests=6,
            sqft=1200,
            available_from=today,
            available_to=today + timezone.timedelta(days=30),
            main_image='alpha.jpg'
        )
        self.prop2 = Property.objects.create(
            title='Property Beta in Another Place',
            description='Description for Beta',
            location='Another Place',
            price_nightly=200.00,
            price_monthly=4000.00,
            rental_type=Property.LONG,
            bedrooms=4,
            bathrooms=3,
            guests=8,
            sqft=2000,
            available_from=today,
            available_to=today + timezone.timedelta(days=60),
            main_image='beta.jpg'
        )

    def test_home_search_redirects_and_filters(self):
        """
        Test that searching from the home page (luxury_home) redirects
        to the property_list page with filters applied, and that the
        results on the property_list page are correctly filtered.
        """
        search_url = reverse('rentals:luxury_home')
        query_params = {'location__icontains': 'Test Location 1'}

        # Make the GET request to luxury_home, following redirects
        response = self.client.get(search_url, query_params, follow=True)

        # Check that the final URL is the property_list page
        # The redirect chain will be a list of (URL, status_code) tuples
        self.assertEqual(len(response.redirect_chain), 1)
        redirect_url, status_code = response.redirect_chain[0]

        # Construct expected redirect URL part (without query string for this check,
        # as query string format can be tricky with urlencode)
        expected_list_url_base = reverse('rentals:property_list')
        self.assertTrue(redirect_url.startswith(expected_list_url_base))
        self.assertEqual(status_code, 302) # Status of the redirect itself

        # Check the final page after following the redirect
        self.assertEqual(response.status_code, 200)

        # Check that the correct property is present and the other is not
        self.assertContains(response, self.prop1.title)
        self.assertNotContains(response, self.prop2.title)

        # Also check for location to be more specific if titles are similar
        self.assertContains(response, self.prop1.location)
        self.assertNotContains(response, self.prop2.location)

        # Verify the query parameters were passed correctly by checking the URL in the redirect chain
        self.assertIn('location__icontains=Test+Location+1', redirect_url)
