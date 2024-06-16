from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import PurchaseOrder, Vendor, HistoricalPerformance
from django.utils import timezone
from django.db.models import Count, Avg

@receiver(post_save, sender=PurchaseOrder)
def update_performance_metrics_on_save(sender, instance, created, **kwargs):
    if instance.status == 'completed':
        vendor = instance.vendor
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        on_time_delivered_pos = completed_pos.filter(delivery_date__lte=instance.delivery_date)
        on_time_delivery_rate = on_time_delivered_pos.count() / completed_pos.count()

        completed_pos_with_quality_rating = completed_pos.exclude(quality_rating__isnull=True)
        quality_rating_avg = completed_pos_with_quality_rating.aggregate(Avg('quality_rating'))['quality_rating__avg']

        pos_with_acknowledgment = PurchaseOrder.objects.filter(vendor=vendor, acknowledgement_date__isnull=False)
        response_times = [(po.acknowledgment_date - po.issue_date).total_seconds() for po in pos_with_acknowledgment]
        avg_response_time = sum(response_times) / len(response_times) if response_times else None

        successful_fulfilled_pos = completed_pos.exclude(
            quality_rating__lt=0)
        fulfilment_rate = successful_fulfilled_pos.count() / completed_pos.count()

        vendor.on_time_delivery_rate = on_time_delivery_rate
        vendor.quality_rating_avg = quality_rating_avg
        vendor.average_response_time = avg_response_time
        vendor.fulfilment_rate = fulfilment_rate
        vendor.save()

        HistoricalPerformance.objects.create(
            vendor=vendor,
            date=timezone.now(),
            on_time_delivery_rate=on_time_delivery_rate,
            quality_rating_avg=quality_rating_avg,
            avg_response_time=avg_response_time,
            fulfilment_rate=fulfilment_rate
        )


@receiver(post_delete, sender=PurchaseOrder)
def update_performance_metrics_on_delete(sender, instance, **kwargs):
    if instance.status == 'completed':
        vendor = instance.vendor
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        on_time_delivered_pos = completed_pos.filter(delivery_date__lte=instance.delivery_date)
        on_time_delivery_rate = on_time_delivered_pos.count() / completed_pos.count()

        completed_pos_with_quality_rating = completed_pos.exclude(quality_rating__isnull=True)
        quality_rating_avg = completed_pos_with_quality_rating.aggregate(Avg('quality_rating'))['quality_rating__avg']

        pos_with_acknowledgment = PurchaseOrder.objects.filter(vendor=vendor, acknowledgement_date__isnull=False)
        response_times = [(po.acknowledgment_date - po.issue_date).total_seconds() for po in pos_with_acknowledgment]
        avg_response_time = sum(response_times) / len(response_times) if response_times else None

        successful_fulfilled_pos = completed_pos.exclude(
            quality_rating__lt=0)
        fulfilment_rate = successful_fulfilled_pos.count() / completed_pos.count()

        vendor.on_time_delivery_rate = on_time_delivery_rate
        vendor.quality_rating_avg = quality_rating_avg
        vendor.average_response_time = avg_response_time
        vendor.fulfilment_rate = fulfilment_rate
        vendor.save()

        HistoricalPerformance.objects.create(
            vendor=vendor,
            date=timezone.now(),
            on_time_delivery_rate=on_time_delivery_rate,
            quality_rating_avg=quality_rating_avg,
            avg_response_time=avg_response_time,
            fulfilment_rate=fulfilment_rate
        )
