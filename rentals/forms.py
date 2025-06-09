from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Booking, Property, PropertyImage


class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultiImageField(forms.ImageField):
    widget = MultiFileInput

    def to_python(self, data):
        if not data:
            return []
        if not isinstance(data, (list, tuple)):
            data = [data]
        files = []
        for item in data:
            files.append(super().to_python(item))
        return files

    def validate(self, data):
        if self.required and not data:
            raise ValidationError(self.error_messages['required'], code='required')

    def run_validators(self, data):
        for file in data:
            super().run_validators(file)


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'first_name',
            'last_name',
            'email',
            'check_in',
            'check_out',
            'guests',
            'message',
        ]

    def clean(self):
        cleaned = super().clean()
        check_in = cleaned.get('check_in')
        check_out = cleaned.get('check_out')
        if check_in and check_out and check_in >= check_out:
            raise ValidationError('Check-out must be after check-in.')
        if check_in and check_in < timezone.now().date():
            raise ValidationError('Check-in cannot be in the past.')
        return cleaned


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)

    def clean_honeypot(self):
        if self.cleaned_data.get('honeypot'):
            raise ValidationError('Bad bot!')
        return ''


class PropertyForm(forms.ModelForm):
    images = MultiImageField(required=False, help_text="Upload one or more photos")
    main_image_index = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Price fields become optional; validation handled in clean()
        self.fields['price_nightly'].required = False
        self.fields['price_monthly'].required = False
        self.fields['sqft'].required = False

    def clean(self):
        cleaned = super().clean()
        r_type = cleaned.get('rental_type')
        nightly = cleaned.get('price_nightly')
        monthly = cleaned.get('price_monthly')

        if r_type == Property.SHORT and not nightly:
            self.add_error('price_nightly', 'This field is required for short-term rentals.')
        if r_type == Property.LONG and not monthly:
            self.add_error('price_monthly', 'This field is required for long-term rentals.')
        if r_type == Property.BOTH:
            if not nightly:
                self.add_error('price_nightly', 'This field is required when rental type is both.')
            if not monthly:
                self.add_error('price_monthly', 'This field is required when rental type is both.')
        return cleaned

    class Meta:
        model = Property
        fields = [
            'title',
            'description',
            'location',
            'price_nightly',
            'price_monthly',
            'rental_type',
            'bedrooms',
            'bathrooms',
            'guests',
            'sqft',
            'amenities',
            'features',
        ]
        widgets = {
            'amenities': forms.CheckboxSelectMultiple,
            'features': forms.CheckboxSelectMultiple,
        }

    def save(self, commit=True):
        images = self.cleaned_data.get('images', [])
        main_idx = int(self.cleaned_data.get('main_image_index') or 0)
        prop = super().save(commit=commit)
        for idx, img in enumerate(images):
            photo = PropertyImage.objects.create(property=prop, image=img)
            if idx == main_idx:
                prop.main_image = photo.image
        if images and commit:
            prop.save()
        return prop
