# your_app/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import F
from .models import Product, Category

@receiver(post_save, sender=Product)
def increment_product_count(sender, instance, created, **kwargs):
    if created:
        Category.objects.filter(id=instance.category.id).update(product_count=F('product_count') + 1)

@receiver(post_delete, sender=Product)
def decrement_product_count(sender, instance, **kwargs):
    Category.objects.filter(id=instance.category.id).update(product_count=F('product_count') - 1)
