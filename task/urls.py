from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *





urlpatterns = [
    #path('', views.home),
    # customer urls
    path('customer-registration/', views.customer_registration, name='customer-registration'),
    path('', views.customer_login, name='customer-login'),
    path('sales-order/', views.sales_order, name='sales-order'),
    path('view-sales-order-dashboard/', views.view_sales_order_dashboard, name='view-sales-order-dashboard'),
    path('sales-order-update/<int:id>', views.sales_order_update, name='sales-order-update'),
    path('sales-order-view/<int:id>', views.customer_sales_order_view, name='customer-sales-order-view'),
    path('create-unit/', views.create_manufacturing_unit, name='create-manufacturing-unit'),
    path('update-unit/<int:id>', views.update_manufacturing_unit, name='update-manufacturing-unit'),
    path('account-detail/', views.customer_detail, name='customer-detail'),
    path('create-sale-order/', views.create_sale_order, name='create-sale-order'),
    path('customer-dashboard/', views.customer_dashboard, name='customer-dashboard'),
    path('manufacturing-unit-dashboard/', views.manufacturing_unit_dashboard, name='manufacturing-unit-dashboard'),
    path('search-result/', views.customer_search, name='customer-search'),
    path('load-product/', views.load_product, name='load-product'),
    path('load-product-cost/', views.load_product_cost, name='load-product-cost'),
    path('load-purchase-product-cost/', views.load_purchase_product_cost, name='load-purchase-product-cost'),
    path('load-quotation-product-cost/', views.load_quotation_product_cost, name='load-quotation-product-cost'),
    path('load-manufacturer-distributor/', views.load_manufacturer_distributor, name='load-manufacturer-distributor'),
    # path('load-product-length/', views.load_product_length, name='load-product-length'),
    path('customer-registration-redirect/', views.customer_registration_redirect, name='customer-registration-redirect'),
    path('add-product-to-unit/<int:id>', AddTempInventoryItem.as_view(), name ='add-product-to-unit'), 
    path('edit-unit-product/<int:id>', views.edit_unit_product, name='edit-unit-product'),
    path('delete-unit-product/<int:id>', views.delete_unit_product, name ='delete-unit-product'),






    # manufacturer urls
    path('manufacturer-registration/', views.manufacturer_registration, name='manufacturer-registration'),
    path('manufacturer-registration-redirect/', views.manufacturer_registration_redirect, name='manufacturer-registration-redirect'),
    path('manufacturer-sales-order-update/<int:id>', views.manufacturer_sales_order_update, name='manufacturer-sales-order-update'),
    path('manufacturer-login/', views.manufacturer_login, name='manufacturer-login'),
    path('manufacturer-dashboard/', views.manufacturer_dashboard, name='manufacturer-dashboard'),
    path('manufacturer-packing/', views.manufacturer_packing, name='manufacturer-packing'),
    path('manufacturer-detail/', views.manufacturer_detail, name='manufacturer-detail'),
    path('manufacturer-sales-order-view/<int:id>', views.manufacturer_sales_order_view, name='manufacturer-sales-order-view'),
    path('manufacturer-search-result/', views.manufacturer_search, name='manufacturer-search'),
    
    # vendor unit urls
    path('add-vendor-unit/', views.add_vendor_unit, name='add-vendor-unit'),
    path('create-vendor-unit/', views.create_vendor_unit, name='create-vendor-unit'),
    path('vendor-unit-dashboard/', views.vendor_unit_dashboard, name='vendor-unit-dashboard'),
    path('update-vendor-unit/<int:id>', views.update_vendor_unit, name='update-vendor-unit'),
    path('purchase-order/', views.add_purchase_order, name='add-purchase-order'),
    path('create-purchase-order/', views.create_purchase_order, name='create-purchase-order'),
    path('purchase-order-dashboard/', views.purchase_order_dashboard, name='purchase-order-dashboard'),
    path('update-purchase-order/<int:id>', views.update_purchase_order, name='update-purchase-order'),
    path('view-purchase-order/<int:id>', views.view_purchase_order, name='view-purchase-order'),
    path('load-purchase-order-product/', views.load_purchase_order_product, name='load-purchase-order-product'),


    # customer unit urls
    path('add-customer-unit/', views.add_customer_unit, name='add-customer-unit'),
    path('create-customer-unit/', views.create_customer_unit, name='create-customer-unit'),
    path('update-customer-unit/<int:id>', views.update_customer_unit, name='update-customer-unit'),
    path('customer-unit-dashboard/', views.customer_unit_dashboard, name='customer-unit-dashboard'),

    # manufacturer order status urls
    path('order-status-accepted/', views.order_status_accepted, name='order-status-accepted'),
    path('order-status-accepted-with-change/', views.order_status_accepted_with_change, name='order-status-accepted-with-change'),
    path('order-status-in-production/', views.order_status_in_production, name='order-status-in-production'),
    path('order-status-packed/', views.order_status_packed, name='order-status-packed'),
    path('order-status-shipped/', views.order_status_shipped, name='order-status-shipped'),
    path('order-status-delivered/', views.order_status_delivered, name='order-status-delivered'),
    path('order-status-cancel/', views.order_status_cancel, name='order-status-cancel'),


    # vendor urls 
    path('vendor-registration/', views.vendor_registration, name='vendor-registration'),
    path('vendor-login/', views.vendor_login, name='vendor-login'),
    path('vendor-registration-redirect/', views.vendor_registration_redirect, name='vendor-registration-redirect'),
    path('vendor-dashboard/', views.vendor_dashboard, name='vendor-dashboard'),
    path('vendor-purchase-order-update/<int:id>', views.vendor_purchase_order_update, name='vendor-purchase-order-update'),
    path('vendor-purchase-order-view/<int:id>', views.vendor_purchase_order_view, name='vendor-purchase-order-view'),
    path('vendor-detail/', views.vendor_detail, name='vendor-detail'),
    path('vendor-search/', views.vendor_search, name='vendor-search'),


    # vendor order status urls
    path('vendor-order-status-accepted/', views.vendor_order_status_accepted, name='vendor-order-status-accepted'),
    path('vendor-order-status-accepted-with-change/', views.vendor_order_status_accepted_with_change, name='vendor-order-status-accepted-with-change'),
    path('vendor-order-status-in-production/', views.vendor_order_status_in_production, name='vendor-order-status-in-production'),
    path('vendor-order-status-packed/', views.vendor_order_status_packed, name='vendor-order-status-packed'),
    path('vendor-order-status-shipped/', views.vendor_order_status_shipped, name='vendor-order-status-shipped'),
    path('vendor-order-status-delivered/', views.vendor_order_status_delivered, name='vendor-order-status-delivered'),
    path('vendor-order-status-cancel/', views.vendor_order_status_cancel, name='vendor-order-status-cancel'),
    path('quotation/', views.quotation, name='quotation'),
    path('quotation-dashboard/', views.quotation_dashboard, name='quotation-dashboard'),
    path('edit-quotation/<int:id>', views.edit_quotation, name='edit-quotation'),
    path('view-quotation/<int:id>', views.view_quotation, name='view-quotation'),

    path('download-pdf/<int:id>', views.pdf_converter, name='pdf-converter'),
    path('purchase-order-download-pdf/<int:id>', views.purchase_order_pdf_converter, name='purchase-order-pdf-converter'),


    path('logout/', views.logout_user, name='logout'),

    path('download-csv/', download_csv, name='download-csv'),





]+ static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
