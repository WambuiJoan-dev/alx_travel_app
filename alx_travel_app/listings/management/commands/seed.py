from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from faker import Faker
import random

from listings.models import Listing, Booking, Review

User = get_user_model()
fake = Faker()

# --- Fixture Data ---
LISTING_TITLES = [
    "Cozy Beachfront Cottage",
    "Modern Downtown Loft",
    "Rustic Mountain Cabin",
    "Urban Studio near Transit",
    "Luxury Penthouse with View",
    "Secluded Lake House",
    "Family-Friendly Suburban Home"
]

class Command(BaseCommand):
    """
    Django management command to seed the database with sample data.
    """
    help = 'Seeds the database with sample Listings, Bookings, and Reviews.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Starting database seeding process..."))

        # 1. Create a default host user if one doesn't exist
        host_user, created = User.objects.get_or_create(
            username='host_user', 
            defaults={
                'email': 'host@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            host_user.set_password('password123')
            host_user.save()
            self.stdout.write(self.style.SUCCESS(f"Created superuser: {host_user.username}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Using existing host user: {host_user.username}"))
        
        # 2. Clear existing data
        Review.objects.all().delete()
        Booking.objects.all().delete()
        Listing.objects.all().delete()
        self.stdout.write(self.style.WARNING("Cleared existing Listing, Booking, and Review data."))

        # 3. Create Listings
        listings = []
        for title in LISTING_TITLES:
            listing = Listing(
                title=title,
                description=fake.paragraph(nb_sentences=5),
                price_per_night=random.uniform(50.00, 300.00),
                max_guests=random.randint(2, 8),
                host=host_user,
                is_active=True
            )
            listings.append(listing)
        
        Listing.objects.bulk_create(listings)
        self.stdout.write(self.style.SUCCESS(f"Created {len(listings)} sample listings."))
        
        # Re-fetch the created listings
        all_listings = Listing.objects.all()

        # 4. Create Bookings (using the host user as a guest for simplicity)
        bookings = []
        today = timezone.localdate()
        for listing in all_listings[:4]: # Book the first 4 listings
            check_in = today + timezone.timedelta(days=random.randint(5, 15))
            duration = random.randint(2, 7)
            check_out = check_in + timezone.timedelta(days=duration)
            
            total_price = listing.price_per_night * duration
            
            booking = Booking(
                listing=listing,
                guest=host_user,
                check_in_date=check_in,
                check_out_date=check_out,
                total_price=total_price,
                num_guests=random.randint(1, listing.max_guests)
            )
            bookings.append(booking)

        Booking.objects.bulk_create(bookings)
        self.stdout.write(self.style.SUCCESS(f"Created {len(bookings)} sample bookings."))

        # 5. Create Reviews
        reviews = []
        for listing in all_listings[3:]: # Review the last few listings
            review = Review(
                listing=listing,
                guest=host_user,
                rating=random.randint(3, 5),
                comment=fake.text(max_nb_chars=100)
            )
            reviews.append(review)
        
        Review.objects.bulk_create(reviews)
        self.stdout.write(self.style.SUCCESS(f"Created {len(reviews)} sample reviews."))

        self.stdout.write(self.style.SUCCESS("Database seeding complete!"))
