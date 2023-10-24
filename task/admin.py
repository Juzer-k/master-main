from django.contrib import admin
from .models import *
# Register your models here.





@admin.register(Client)
class ClientModelAdmin(admin.ModelAdmin):
    list_display =['id','user','company','contact_number','country','state', 'region']

@admin.register(Manufacturer)
class ManufacturerModelAdmin(admin.ModelAdmin):
    list_display =['id','user','m_company','m_contact_number','m_country','m_state', 'm_region']

class ProductDetailInline(admin.StackedInline):
    model = ProductDetail
    extra = 0

# class SalesOrderDocumentsInline(admin.StackedInline):
#     model = SalesOrderDocuments
#     extra = 0


@admin.register(SalesOrder)
class SalesOrderModelAdmin(admin.ModelAdmin):
    list_display =['id','manufacturing_unit','sales_order_date','exp_shipment_date','payment_term', 'order_status']
    inlines = [ProductDetailInline]


# @admin.register(ProductDetail)
# class ProductDetailModelAdmin(admin.ModelAdmin):
#     list_display =['id','product_name','length_of_product','weight_of_product','quantity','auto_logistic_fillment']


@admin.register(ManufacturingUnit)
class ManufacturingUnitModelAdmin(admin.ModelAdmin):
    list_display =['id','salutation','first_name','last_name','contact_person','company_name', 'email', 'phone_number', 'website', 'pan_number', 'currency', 'm_payment_term']

@admin.register(BillingAddress)
class BillingAddressModelAdmin(admin.ModelAdmin):
    list_display =['id','attention','country','address','city','state', 'zip_code', 'billing_phone_number', 'fax']

@admin.register(ShippingAddress)
class ShippingAddressModelAdmin(admin.ModelAdmin):
    list_display =['id','shipping_attention','shipping_country','shipping_address','shipping_city','shipping_state', 'shipping_zip_code', 'shipping_phone_number', 'shipping_fax']

@admin.register(ManufacturingUnitAddress)
class ShippingAddressModelAdmin(admin.ModelAdmin):
    list_display =['id','manufacturing_unit_attention','manufacturing_unit_country','manufacturing_unit_address','manufacturing_unit_city','manufacturing_unit_state', 'manufacturing_unit_zip_code', 'manufacturing_unit_phone_number', 'manufacturing_unit_fax']

# @admin.register(OrderPlaced)
# class OrderPlacedModelAdmin(admin.ModelAdmin):
#     list_display =['id','user','product','sales_order','shipping_address','billing_address']

@admin.register(CustomerUnit)
class CustomerUniModelAdmin(admin.ModelAdmin):
    list_display =['id','user', 'contact_person', 'company_name', 'email']

@admin.register(VendorUnit)
class VendorUnitModelAdmin(admin.ModelAdmin):
    list_display =['id','user','salutation', 'first_name', 'last_name', 'company_name', 'email', 'phone_number']
    
@admin.register(VendorUnitAddress)
class VendorBillingAddressModelAdmin(admin.ModelAdmin):
    list_display =['id','user','vendor_attention','vendor_country', 'vendor_address', 'vendor_city', 'vendor_state', 'vendor_zip_code', 'vendor_phone_number']
    
# @admin.register(LengthOfProduct)
# class LengthOfProductModelAdmin(admin.ModelAdmin):
#     list_display =['id','product_detail','length_of_product']

# @admin.register(ProductDetail)
# class LengthOfProductModelAdmin(admin.ModelAdmin):
#     list_display =['id','product_name']

class PurchaseOrderProductDetailInline(admin.StackedInline):
    model = PurchaseOrderProductDetail
    extra = 0

# class PurchaseOrderDocumentsInline(admin.StackedInline):
#     model = PurchaseOrderDocuments
#     extra = 0

@admin.register(PurchaseOrder)
class PurchaseOrderDocumentsModelAdmin(admin.ModelAdmin):
    list_display =['id', 'vendor_unit', 'purchase_order_date', 'exp_shipment_date']
    inlines = [PurchaseOrderProductDetailInline]

@admin.register(Vendor)
class VendorModelAdmin(admin.ModelAdmin):
    list_display =['id', 'user', 'vendor_company', 'vendor_contact_number', 'vendor_country', 'vendor_state', 'vendor_region']

@admin.register(AddSalesOrderProduct)
class AddSalesOrderProductModelAdmin(admin.ModelAdmin):
    list_display =['id', 'product_name_and_length', 'manufacturing_unit']


@admin.register(AddPurchaseOrderProduct)
class AddSalesOrderProductModelAdmin(admin.ModelAdmin):
    list_display =['id', 'product_name_and_length', 'vendor_unit']

@admin.register(Quotation)
class QuotationModelAdmin(admin.ModelAdmin):
    list_display =['id']

@admin.register(QuotationProduct)
class QuotationProductModelAdmin(admin.ModelAdmin):
    list_display =['id']

@admin.register(TempInventory)
class TempInventoryModelAdmin(admin.ModelAdmin):
    list_display =['id']

# @admin.register(PurchaseOrderLengthOfProduct)
# class PurchaseOrderLengthOfProductModelAdmin(admin.ModelAdmin):
#     list_display =['id', 'product_detail', 'length_of_product']

# @admin.register(SalesOrderDocuments)
# class PurchaseOrderLengthOfProductModelAdmin(admin.ModelAdmin):
#     list_display =['id']