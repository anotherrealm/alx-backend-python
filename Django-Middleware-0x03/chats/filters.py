import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    # Example: filter by date range and sender
    sent_after = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr="gte")
    sent_before = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr="lte")
    sender = django_filters.NumberFilter(field_name="sender__id")

    class Meta:
        model = Message
        fields = ["conversation", "sender", "sent_after", "sent_before"]
