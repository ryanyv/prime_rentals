from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Booking


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
