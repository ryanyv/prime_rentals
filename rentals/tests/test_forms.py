import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.datastructures import MultiValueDict
from PIL import Image
from io import BytesIO
from rentals.forms import PropertyForm
from rentals.models import Property

@pytest.mark.django_db
def test_property_form_with_images(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    buf = BytesIO()
    Image.new('RGB', (1, 1)).save(buf, format='JPEG')
    img = SimpleUploadedFile('img.jpg', buf.getvalue(), content_type='image/jpeg')
    form = PropertyForm(
        data={
            'title': 'FormProp',
            'description': 'd',
            'location': 'loc',
            'price_nightly': '10',
            'price_monthly': '100',
            'rental_type': Property.BOTH,
            'bedrooms': 1,
            'bathrooms': 1,
            'guests': 2,
            'main_image_index': '0',
            'sqft': '',
        },
        files=MultiValueDict({'images': [img]}),
    )
    assert form.is_valid(), form.errors
    prop = form.save()
    assert prop.gallery.count() == 1
