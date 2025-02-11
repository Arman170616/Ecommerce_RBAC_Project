from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from django.core.mail import send_mail

@receiver(post_save, sender=Order)
def notify_vendors_on_order(sender, instance, created, **kwargs):
    if created:
        vendors = set(item.product.vendor for item in instance.items.all())
        for vendor in vendors:
            send_mail(
                subject="New Order Received",
                message=f"Hello {vendor.username}, you have a new order containing your products.",
                from_email="noreply@ecommerce.com",
                recipient_list=[vendor.email],
            )
