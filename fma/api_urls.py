from django.urls import path
from .api_views import VendorCreateAPIView, VendorGetAPIView, VendorDetailAPIView, PurchaseOrderCreateApiView, PurchaseOrderGetAPIView,  PurchaseOrderDetailAPIView,  VendorPerformanceAPIView, VendorPerformanceCreateApiView,AcknowledgePurchaseOrderAPIView

urlpatterns = [
    path('vendor/', VendorCreateAPIView.as_view(), name='vendor-create'),
    path('vendor/list/', VendorGetAPIView.as_view(), name='vendor-get'),
    path('vendor/<uuid:vendor_code>/', VendorDetailAPIView.as_view(), name='vendor-detail'),
    path('purchase_orders/', PurchaseOrderCreateApiView.as_view(), name='purchase-create'),
    path('purchase_orders/list/',  PurchaseOrderGetAPIView.as_view(), name='vendor-get'),
    path('purchase_orders/<uuid:po_num>/', PurchaseOrderDetailAPIView.as_view(), name='vendor-detail'),
    path('vendor/<uuid:vendor_code>/performance/', VendorPerformanceAPIView.as_view(), name='vendor-performance'),
    path('vendor/performance/', VendorPerformanceCreateApiView.as_view(), name='history-create'),
    path('purchase_orders/<uuid:po_num>/acknowledge/', AcknowledgePurchaseOrderAPIView.as_view(), name='acknoledge-pe'),
]
