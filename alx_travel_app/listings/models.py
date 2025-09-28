from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

# Get the custom user model (assumes it's set up correctly)
User = get_user_model()

class Listing(models.Model):
    """
    Represents a property available for booking.
    """
    title = models.CharField(max_length=255, help_text="A short, descriptive name for the listing.")
    description = models.TextField(help_text="Detailed description of the property, amenities, and rules.")
    price_per_night = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        help_text="The price to book this listing for one night."
    )
    max_guests = models.PositiveSmallIntegerField(
        default=1, 
        help_text="Maximum number of guests allowed."
    )
    is_active = models.BooleanField(
        default=True, 
        help_text="Indicates if the listing is currently available for booking."
    )
    host = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='listings',
        help_text="The user who owns and manages this listing."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Property Listing'
        verbose_name_plural = 'Property Listings'

    def __str__(self):
        return f"{self.title} by {self.host.username}"

class Booking(models.Model):
    """
    Represents a successful booking reservation for a Listing.
    """
    listing = models.ForeignKey(
        Listing, 
        on_delete=models.CASCADE, 
        related_name='bookings',
        help_text="The listing that was booked."
    )
    guest = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='bookings_as_guest',
        help_text="The user who made the booking."
    )
    check_in_date = models.DateField(help_text="The starting date of the reservation.")
    check_out_date = models.DateField(help_text="The ending date of the reservation.")
    total_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="The final calculated price for the entire stay."
    )
    num_guests = models.PositiveSmallIntegerField(
        help_text="The number of guests for this booking."
    )
    
    class Meta:
        # Constraint to ensure a user cannot book the same listing for overlapping dates
        constraints = [
            models.UniqueConstraint(
                fields=['listing', 'check_in_date'], 
                name='unique_check_in_date'
            )
        ]
        verbose_name = 'Booking Reservation'
        verbose_name_plural = 'Booking Reservations'

    def clean(self):
        """Custom validation for dates and guests."""
        if self.check_out_date <= self.check_in_date:
            raise ValidationError('Check-out date must be after check-in date.')
        if self.num_guests > self.listing.max_guests:
            raise ValidationError(f"Booking exceeds max guests ({self.listing.max_guests}) for this listing.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Run clean before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking of {self.listing.title} by {self.guest.username}"

class Review(models.Model):
    """
    Represents a guest's review of a booked Listing.
    """
    listing = models.ForeignKey(
        Listing, 
        on_delete=models.CASCADE, 
        related_name='reviews',
        help_text="The listing being reviewed."
    )
    guest = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='reviews',
        help_text="The user who wrote the review."
    )
    rating = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        help_text="The rating given (1 to 5)."
    )
    comment = models.TextField(blank=True, null=True, help_text="Optional text comment.")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # A guest can only review a specific listing once
        unique_together = ('listing', 'guest')
        ordering = ['-created_at']
        verbose_name = 'Guest Review'
        verbose_name_plural = 'Guest Reviews'

    def clean(self):
        if not 1 <= self.rating <= 5:
            raise ValidationError('Rating must be between 1 and 5.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Review for {self.listing.title}: {self.rating}/5"
