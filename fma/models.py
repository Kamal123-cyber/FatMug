from django.db import models
import uuid


class Vendor(models.Model):
    name = models.CharField(max_length=40)
    contact_no = models.IntegerField(null=True, blank=True)
    address = models.TextField()
    vendor_code = models.UUIDField(primary_key=True ,unique=True, default=uuid.uuid4, editable=False)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    po_num = models.UUIDField(primary_key=True ,unique=True, default=uuid.uuid4, editable=False)
    vendor =models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('canceled', 'Canceled')])
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField()
    acknowledgement_date = models.DateTimeField(null=True)



class HistoricalPerformance(models.Model):
    vendor =models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    avg_response_time = models.FloatField()
    fulfilment_rate = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

