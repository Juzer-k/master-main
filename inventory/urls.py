from django.urls import path
from .views import *
from . import views


urlpatterns = [ 

    # path('add-single-inventory-item', AddInventoryItem.as_view(), name ='add-single-inventory-item'), 
    path('edit-inventory-item/<str:id>', EditInventoryItem.as_view(), name ='edit-inventory-item'),
    path('delete-inventory-item/<str:id>', DeleteInventoryItem.as_view(), name ='delete-inventory-item'),
    path('add-category', AddNewCategory.as_view(), name='add-category'),
    path('delete-category/<str:id>', DeleteCategory.as_view(), name ='delete-category'),
    path('edit-category/<str:id>', EditCategory.as_view(), name ='edit-category'),
    path('add-warehouse', AddWarehouse.as_view(), name ='add-warehouse'),
    # path('warehouse/', views.warehouse, name = 'warehouse'),
    path('edit-warehouse/<str:id>', EditWarehouse.as_view(), name ='edit-warehouse'),
    path('delete-warehouse/<str:id>', DeleteWarehouse.as_view(), name ='delete-warehouse'),
    path('add-rack', AddRack.as_view(), name ='add-rack'),
    path('delete-rack/<str:id>', DeleteRack.as_view(), name ='delete-rack'), 
    path('edit-rack/<str:id>', EditRack.as_view(), name ='edit-rack'),
    path('get-warehouse-rack/<str:name>', GetWarehouseRack.as_view(), name ='get-warehouse-rack'),
    path('load-category/', views.load_category, name='load-category'),
    path('load-rack/', views.load_rack, name='load-rack'),
    path('inventory/', views.inventory, name='inventory'),
    path('add-inventory-product/', views.add_inventory_product, name='add-inventory-product'),
    path('search-inventory-product/', views.search_inventory_product, name='search-inventory-product'),
    path('load-item-name/', views.load_item_name, name='load-item-name'),
    path('load-item-stock/', views.load_item_stock, name='load-item-stock'),
    path('load-item-gst/', views.load_item_gst, name='load-item-gst'),
    path('load-item-price/', views.load_item_price, name='load-item-price'),
    # path('barcode/<str:barcode_data>/', genrate_barcodes, name='generate_barcode'),


]