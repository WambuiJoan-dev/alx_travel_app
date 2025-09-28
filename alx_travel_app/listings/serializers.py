from rest_framework import serializers
from .models import Listing, Booking, Review

class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.
    """
    guest_username = serializers.ReadOnlyField(source='guest.username')

    class Meta:
        model = Review
        fields = ['id', 'listing', 'guest', 'guest_username', 'rating', 'comment', 'created_at']
        read_only_fields = ['guest', 'listing']

class ListingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Listing model, including host and reviews.
    """
    host_username = serializers.ReadOnlyField(source='host.username')
    # Use the ReviewSerializer to show nested reviews
    reviews = ReviewSerializer(many=True, read_only=True)
    
    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'price_per_night', 'max_guests', 
            'is_active', 'host', 'host_username', 'created_at', 'reviews'
        ]
        read_only_fields = ['host']

class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Booking model.
    """
    guest_username = serializers.ReadOnlyField(source='guest.username')
    listing_title = serializers.ReadOnlyField(source='listing.title')

    class Meta:
        model = Booking
        fields = [
            'id', 'listing', 'listing_title', 'guest', 'guest_username', 
            'check_in_date', 'check_out_date', 'total_price', 'num_guests'
        ]
        read_only_fields = ['guest', 'total_price']
