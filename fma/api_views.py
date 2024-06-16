from .serializers import VendorSerializers, PurchaseOrderSerializers, HistoricalPerformanceSerializers
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from django.shortcuts import get_object_or_404
from django.db.models import Count, Avg
from django.utils import timezone
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
class VendorGetAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        vendors = Vendor.objects.all()
        serializer = VendorSerializers(vendors, many=True)
        return Response(serializer.data)


class VendorCreateAPIView(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializers

class VendorDetailAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, vendor_code, format=None):
        vendor = get_object_or_404(Vendor, vendor_code=vendor_code)
        serializer = VendorSerializers(vendor)
        return Response(serializer.data)

    def put(self, request, vendor_code, format=None):
        vendor = get_object_or_404(Vendor, vendor_code=vendor_code)
        serializer = VendorSerializers(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, vendor_code, format=None):
        vendor = self.get_object(vendor_code)
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



'''From here Purchase Order Api's Starting '''


class PurchaseOrderCreateApiView(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializers

class PurchaseOrderGetAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        po = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializers(po, many=True)
        return Response(serializer.data)

class PurchaseOrderDetailAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, po_num, format=None):
        po = get_object_or_404(PurchaseOrder, po_num=po_num)
        serializer = PurchaseOrderSerializers(po)
        return Response(serializer.data)

    def put(self, request, po_num, format=None):
        po = get_object_or_404(PurchaseOrder, po_num=po_num)
        serializer = PurchaseOrderSerializers(po, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,po_num , format=None):
        po = self.get_object(po_num)
        po.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


'''From Here The Performance matrics started'''

class VendorPerformanceCreateApiView(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializers

class VendorPerformanceAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    # def get(self, request, vendor_code, format=None):
    #     performances = HistoricalPerformance.objects.filter(vendor__vendor_code=vendor_code)
    #     serializer = HistoricalPerformanceSerializers(performances, many=True)
    #     return Response(serializer.data)
    def get(self, request, vendor_code, format=None):
        vendor = Vendor.objects.get(vendor_code=vendor_code)
        print(vendor)
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        print(completed_pos)
        completed_count = completed_pos.count()
        print(completed_count)
        if completed_count == 0:
            on_time_delivery_rate = 0
        else:
            on_time_delivered_pos = completed_pos.filter(delivery_date__lte=timezone.now())
            on_time_delivery_rate = on_time_delivered_pos.count() / completed_count

        quality_rating_avg = completed_pos.aggregate(Avg('quality_rating'))['quality_rating__avg']
        print(quality_rating_avg)
        pos_with_acknowledgment = PurchaseOrder.objects.filter(vendor=vendor, acknowledgement_date__isnull=False)
        response_times = [(po.acknowledgement_date - po.issue_date).total_seconds() for po in pos_with_acknowledgment]
        avg_response_time = sum(response_times) / len(response_times) if response_times else None
        total_pos = PurchaseOrder.objects.filter(vendor=vendor)
        total_count = total_pos.count()
        if total_count == 0:
            fulfilment_rate = 0
        else:
            successful_fulfilled_pos = total_pos.filter(status='completed', quality_rating__isnull=False)
            fulfilment_rate = successful_fulfilled_pos.count() / total_count

        return Response({
            "on_time_delivery_rate": on_time_delivery_rate,
            "quality_rating_avg": quality_rating_avg,
            "avg_response_time": avg_response_time,
            "fulfilment_rate": fulfilment_rate
        })



class VendorPerformanceAllAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, vendor_code, format=None):
        vendor = Vendor.objects.get(vendor_code=vendor_code)

        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        on_time_delivered_pos = completed_pos.filter(delivery_date__lte=timezone.now())
        on_time_delivery_rate = on_time_delivered_pos.count() / completed_pos.count()

        quality_rating_avg = completed_pos.aggregate(Avg('quality_rating'))['quality_rating__avg']

        pos_with_acknowledgment = PurchaseOrder.objects.filter(vendor=vendor, acknowledgement_date__isnull=False)
        response_times = [(po.acknowledgement_date - po.issue_date).total_seconds() for po in pos_with_acknowledgment]
        avg_response_time = sum(response_times) / len(response_times) if response_times else None

        total_pos = PurchaseOrder.objects.filter(vendor=vendor)
        successful_fulfilled_pos = total_pos.filter(status='completed', quality_rating__isnull=False)
        fulfilment_rate = successful_fulfilled_pos.count() / total_pos.count()

        return Response({
            "on_time_delivery_rate": on_time_delivery_rate,
            "quality_rating_avg": quality_rating_avg,
            "avg_response_time": avg_response_time,
            "fulfilment_rate": fulfilment_rate
        })


class AcknowledgePurchaseOrderAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, po_num, format=None):
        purchase_order = get_object_or_404(PurchaseOrder, pk=po_num)
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()
        vendor = purchase_order.vendor
        pos_with_acknowledgment = PurchaseOrder.objects.filter(vendor=vendor, acknowledgement_date__isnull=False)
        response_times = [(po.acknowledgment_date - po.issue_date).total_seconds() for po in pos_with_acknowledgment]
        avg_response_time = sum(response_times) / len(response_times) if response_times else None
        vendor.average_response_time = avg_response_time
        vendor.save()

        return Response({"message": "Purchase order acknowledged successfully."}, status=status.HTTP_200_OK)