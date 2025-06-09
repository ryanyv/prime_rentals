from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Booking, Property, PropertyImage


class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


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
    images = forms.FileField(
        widget=MultiFileInput,
        required=False,
        help_text="Upload one or more photos"
    )
    main_image_index = forms.IntegerField(widget=forms.HiddenInput(), required=False)

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
            'available_from',
            'available_to',
        ]
        widgets = {
            'amenities': forms.CheckboxSelectMultiple,
            'features': forms.CheckboxSelectMultiple,
            'available_from': forms.DateInput(attrs={'type': 'date'}),
            'available_to': forms.DateInput(attrs={'type': 'date'}),
        }

    def save(self, commit=True):
        images = self.files.getlist('images')
        main_idx = int(self.cleaned_data.get('main_image_index') or 0)
        prop = super().save(commit=commit)
        for idx, img in enumerate(images):
            photo = PropertyImage.objects.create(property=prop, image=img)
            if idx == main_idx:
                prop.main_image = photo.image
        if images and commit:
            prop.save()
        return prop
