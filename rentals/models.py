from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.db.models import Avg
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver


class Amenity(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Feature(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Property(models.Model):
    SHORT = 'short'
    LONG = 'long'
    RENTAL_CHOICES = [
        (SHORT, 'Short-term'),
        (LONG, 'Long-term'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    location = models.CharField(max_length=200)
    price_nightly = models.DecimalField(max_digits=10, decimal_places=2)
    price_monthly = models.DecimalField(max_digits=10, decimal_places=2)
    rental_type = models.CharField(max_length=10, choices=RENTAL_CHOICES)
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    guests = models.PositiveIntegerField()
    sqft = models.PositiveIntegerField(verbose_name="Square footage")
    amenities = models.ManyToManyField(Amenity, blank=True)
    features = models.ManyToManyField(Feature, blank=True)
    main_image = models.ImageField(upload_to='properties/main/', blank=True, null=True)
    available_from = models.DateField()
    available_to = models.DateField()
    rating = models.FloatField(default=0, blank=True)

    def __str__(self):
        return self.title

    def average_rating(self):
        avg = self.reviews.aggregate(r=Avg('rating'))['r']
        return avg or 0


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='gallery', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='properties/gallery/', blank=True, null=True)

    def __str__(self):
        return f"Image for {self.property.title}"


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    years_experience = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='team/', blank=True, null=True)
    specialties = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        (CANCELLED, 'Cancelled'),
    ]

    property = models.ForeignKey(Property, related_name='bookings', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveIntegerField()
    message = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking for {self.property.title} by {self.first_name}"


class Payment(models.Model):
    booking = models.ForeignKey(Booking, related_name='payments', on_delete=models.CASCADE)
    stripe_payment_intent_id = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='usd')
    status = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.amount} for {self.booking}"


class Review(models.Model):
    property = models.ForeignKey(Property, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user} on {self.property}"


@receiver(pre_save, sender=Property)
def populate_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


@receiver([post_save, post_delete], sender=Review)
def update_property_rating(sender, instance, **kwargs):
    prop = instance.property
    prop.rating = prop.average_rating()
    prop.save(update_fields=['rating'])

