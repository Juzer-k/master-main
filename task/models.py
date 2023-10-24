from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.


class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.CharField(max_length = 50)
    contact_number = models.IntegerField()
    country = models.CharField(max_length = 50)
    state = models.CharField(max_length = 50)
    industry = models.CharField(max_length=30, default="")
    region = models.CharField(max_length = 50)

class Manufacturer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    m_company = models.CharField(max_length = 50)
    m_contact_number = models.IntegerField()
    m_country = models.CharField(max_length = 50)
    m_state = models.CharField(max_length = 50)
    m_industry = models.CharField(max_length=30, default="")
    m_region = models.CharField(max_length = 50)

    def __str__(self):
        return self.user.username

    # billing address
class BillingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    attention = models.CharField(max_length = 30)
    country = models.CharField(max_length = 50)
    address = models.TextField(max_length = 100)
    city = models.CharField(max_length = 50)
    state = models.CharField(max_length = 50)
    zip_code = models.PositiveIntegerField()
    billing_phone_number = models.CharField(max_length=10)
    fax = models.CharField(max_length = 50)

     # Shipping address
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    shipping_attention = models.CharField(max_length = 30)
    shipping_country = models.CharField(max_length = 50)
    shipping_address = models.TextField(max_length = 100)
    shipping_city = models.CharField(max_length = 50)
    shipping_state = models.CharField(max_length = 50)
    shipping_zip_code = models.PositiveIntegerField()
    shipping_phone_number = models.IntegerField()
    shipping_fax = models.CharField(max_length = 50)


class CustomerUnit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    salutations = (
        ('Mr','Mr'),
        ('Mrs','Mrs')
    )
    customer = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    salutation = models.CharField(max_length = 5, choices = salutations)
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    contact_person = models.CharField(max_length = 30)
    company_name = models.CharField(max_length = 50)
    email = models.CharField(max_length = 30)
    phone_number = models.CharField(max_length=10)
    website = models.CharField(max_length = 50)
    # other Details
    pan_number = models.CharField(max_length = 20)
    currency = models.CharField(max_length = 20)
    m_payment_term = models.CharField(max_length = 20)
    billing_address = models.ForeignKey(BillingAddress, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE)

    def __str__(self):
        return self.company_name

class ManufacturingUnitAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    manufacturing_unit_attention = models.CharField(max_length = 30)
    manufacturing_unit_country = models.CharField(max_length = 50)
    manufacturing_unit_address = models.TextField(max_length = 100)
    manufacturing_unit_city = models.CharField(max_length = 50)
    manufacturing_unit_state = models.CharField(max_length = 50)
    manufacturing_unit_zip_code = models.PositiveIntegerField()
    manufacturing_unit_phone_number = models.IntegerField()
    manufacturing_unit_fax = models.CharField(max_length = 50)

     # manufacturing unit detail
class ManufacturingUnit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    unit_type = models.CharField(max_length=20, null=True, blank=True, default="")
    salutations = (
        ('Mr','Mr'),
        ('Mrs','Mrs')
    )
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, null=True, blank=True)
    manufacturers = models.CharField(max_length= 30, null=True, blank=True, default="")
    salutation = models.CharField(max_length = 5, choices = salutations)
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    contact_person = models.CharField(max_length = 30) 
    company_name = models.CharField(max_length = 50) 
    email = models.CharField(max_length = 30)
    phone_number = models.CharField(max_length=10)
    website = models.CharField(max_length = 50)
    # other Details
    pan_number = models.CharField(max_length = 20)
    currency = models.CharField(max_length = 20)
    m_payment_term = models.CharField(max_length = 20)
    manufacturing_unit_address = models.ForeignKey(ManufacturingUnitAddress, on_delete=models.CASCADE)

    def __str__(self):
        return self.company_name



    

# vendor tables

# vendor registration
class Vendor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vendor_company = models.CharField(max_length = 50)
    vendor_contact_number = models.IntegerField()
    vendor_country = models.CharField(max_length = 50)
    vendor_state = models.CharField(max_length = 50)
    vendor_industry = models.CharField(max_length=30, default="")
    vendor_region = models.CharField(max_length = 50)

    def __str__(self):
        return self.user.username

# vendor Unit address address
class VendorUnitAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    vendor_attention = models.CharField(max_length = 30)
    vendor_country = models.CharField(max_length = 50)
    vendor_address = models.TextField(max_length = 100)
    vendor_city = models.CharField(max_length = 50)
    vendor_state = models.CharField(max_length = 50)
    vendor_zip_code = models.PositiveIntegerField()
    vendor_phone_number = models.CharField(max_length=10)
    vendor_fax = models.CharField(max_length = 50)

# vendor unit details
class VendorUnit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    salutations = (
        ('Mr','Mr'),
        ('Mrs','Mrs')
    )
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True)
    salutation = models.CharField(max_length = 5, choices = salutations)
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    contact_person = models.CharField(max_length = 30)
    company_name = models.CharField(max_length = 50)
    email = models.CharField(max_length = 30)
    phone_number = models.CharField(max_length=10)
    website = models.CharField(max_length = 50)
    # other Details
    pan_number = models.CharField(max_length = 20)
    currency = models.CharField(max_length = 20)
    payment_term = models.CharField(max_length = 20)
    vendor_unit_address = models.ForeignKey(VendorUnitAddress, on_delete=models.CASCADE)

    def __str__(self):
        return self.company_name

# purchase order
class PurchaseOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    unit_type = models.CharField(max_length=50, null=True, blank=True, default="")
    # purchase order detail
    vendor_unit = models.ForeignKey(VendorUnit, on_delete=models.CASCADE, null=True, blank=True)
    # purchase_order = models.CharField(max_length = 30) 
    manufacturing_unit = models.ForeignKey(ManufacturingUnit, on_delete=models.CASCADE, blank=True, null=True)
    purchase_order_date = models.DateField(blank=True, null=True)
    exp_shipment_date = models.DateField(blank=True, null=True)
    payment_options = (
        ('Advance Paid', 'Advance Paid'),
        ('Due next of the month','Due next of the month'),
        ('Due end of the month','Due end of the month'),
        ('Due on receipt','Due on receipt')
    )
    payment_term = models.CharField(max_length = 30, choices = payment_options)
    status = (
        ('order placed','order placed'),
        ('Accepted','Accepted'),
        ('Accepted with change', 'Accepted with change'),
        ('In Production','In Production'),
        ('Packed','Packed'),
        ('Shipped','Shipped'),
        ('Delivered','Delivered'),
        ('Cancel','Cancel'),
    )
    order_status = models.CharField(max_length = 40 ,choices= status, default = "order placed")
    delivery_method = models.CharField(max_length = 30)
    customer_sales_person = models.CharField(max_length = 30)
    customer_phone_number = models.IntegerField()
    terms_and_conditions = models.CharField(max_length=50, null=True)
    total_amount = models.CharField(max_length=40, blank=True, null=True)
    gst = models.CharField(max_length=40, blank=True, null=True)

    # purchase order documents
    purchase_order_file = models.FileField(upload_to="purchase_order_file", blank=True, null=True)
    delivery_challan = models.FileField(upload_to="purchase_delivery_challan", blank=True, null=True)
    packing_list = models.FileField(upload_to="purchase_packing_list", blank=True, null=True)
    ev_list = models.FileField(upload_to="purchase_ev_list", blank=True, null=True)





# purchase order products
class PurchaseOrderProductDetail(models.Model):
    product_name = models.CharField(max_length = 100, null=True)
    length_of_product = models.CharField(max_length = 50, null=True)
    weight_of_product = models.CharField(max_length = 50, null=True)
    quantity = models.PositiveIntegerField(null=True)
    auto_logistic_fillment = models.CharField(max_length = 50, null=True)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, null=True)
    bundle_number = models.CharField(max_length=30, default="")
    cost_of_product = models.CharField(max_length=30, default="")
    order_comment = models.TextField(max_length=50, null=True, default="")
    customer_approval = (
        ('Order Placed','Order Placed'),
        ('Accepted', 'Accepted'),
        ('Cancel', 'Cancel')
    )

    customer_order_approval = models.CharField(max_length=50 , choices = customer_approval, default = "Order Placed")

    vendor_approval = (
        ('Accepted', 'Accepted'),
        ('Accepted with change', 'Accepted with change'),
        ('Cancel', 'Cancel')
    )

    vendor_order_approval = models.CharField(max_length=30, choices = vendor_approval)
    price = models.CharField(max_length=50, blank=True, null=True)  # remove this feild
    gst = models.CharField(max_length=50, blank=True, null=True)
    total_cost = models.CharField(max_length=30, default="", null=True)



    def __str__(self):
        return self.product_name


from inventory.models import Inventory , Category

class SalesOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # sales order detail
    unit_type = models.CharField(max_length=40, null=True, blank=True, default="")
    manufacturing_unit = models.ForeignKey(ManufacturingUnit, on_delete=models.CASCADE, blank=True, null=True)
    sales_order = models.CharField(max_length = 30, null=True, blank=True) 
    sales_order_date = models.DateField(blank=True, null=True)# remove auto_now
    exp_shipment_date = models.DateField(blank=True, null=True)
    payment_options = (
        ('Advance Paid', 'Advance Paid'),
        ('Due next of the month','Due next of the month'),
        ('Due end of the month','Due end of the month'),
        ('Due on receipt','Due on receipt')
    )
    payment_term = models.CharField(max_length = 30, choices = payment_options)
    status = (
        ('order placed','order placed'),
        ('Accepted','Accepted'),
        ('Accepted with change', 'Accepted with change'),
        ('In Production','In Production'),
        ('Packed','Packed'),
        ('Shipped','Shipped'),
        ('Delivered','Delivered'),
        ('Cancel','Cancel'),
    )
    order_status = models.CharField(max_length = 30 ,choices= status, default = "order placed")
    delivery_method = models.CharField(max_length = 30)
    customer_sales_person = models.CharField(max_length = 30)
    customer_phone_number = models.IntegerField()
    terms_and_conditions = models.CharField(max_length=50, null=True) # null = True
    total_amount = models.CharField(max_length=40, blank=True, null=True)
    gst = models.CharField(max_length=40, blank=True, null=True)
    # sales order documents
    sales_order_file = models.FileField(upload_to="sales_order_file", default="", blank=True)
    delivery_challan = models.FileField(upload_to="delivery_challan",blank=True, null=True)
    packing_list = models.FileField(upload_to="packing_list", blank=True, null=True)
    ev_list = models.FileField(upload_to="ev_list", blank=True, null=True)
    

    # def __str__(self):
    #     return self.sales_order



# add inventory key
class ProductDetail(models.Model):
    product_name = models.CharField(max_length = 100, null=True)
    weight_of_product = models.CharField(max_length = 50, null=True)
    quantity = models.PositiveIntegerField(null=True)
    auto_logistic_fillment = models.CharField(max_length = 50, null=True)
    sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, null=True, blank=True)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, null=True, blank=True)
    bundle_number = models.CharField(max_length=30, default="")
    cost_of_product = models.CharField(max_length=30, default="")
    order_comment = models.TextField(max_length=50, null=True, default="")
    customer_approval = (
        ('Order Placed','Order Placed'),
        ('Accepted', 'Accepted'),
        ('Cancel', 'Cancel')
    )

    customer_order_approval = models.CharField(max_length=40 , choices = customer_approval, default = "Order Placed")

    manufacturer_approval = (
        ('Accepted', 'Accepted'),
        ('Accepted with change', 'Accepted with change'),
        ('Cancel', 'Cancel')
    )

    manufacturer_order_approval = models.CharField(max_length=20, choices = manufacturer_approval, blank=True)
    price = models.CharField(max_length=40, blank=True, null=True)# remove this feild
    gst = models.CharField(max_length=40, blank=True, null=True)
    total_cost = models.CharField(max_length=30, default="", null=True)

    def __str__(self):
        return self.product_name



class AddSalesOrderProduct(models.Model):
    manufacturing_unit = models.ForeignKey(ManufacturingUnit, on_delete=models.CASCADE, null=True)
    product_name_and_length = models.CharField(max_length=20, null = True)

    def __str__(self):
        return self.product_name_and_length



class AddPurchaseOrderProduct(models.Model):
    vendor_unit = models.ForeignKey(VendorUnit, on_delete=models.CASCADE, null=True, blank=True)
    manufacturing_unit = models.ForeignKey(ManufacturingUnit, on_delete=models.CASCADE, blank=True, null=True)
    product_name_and_length = models.CharField(max_length=20, null = True)

    def __str__(self):
        return self.product_name_and_length
    

class Quotation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assigning = models.ForeignKey(ManufacturingUnit, on_delete=models.CASCADE, blank=True, null=True)
    # unit_type = models.CharField(max_length=20, null=True, blank=True, default="")
    total_amount = models.CharField(max_length=30, null=True, blank=True)
    terms_and_condition = models.TextField(max_length=100, null=True, blank=True)
    quotation_status = (
        ('Placed', 'Placed'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Cancel', 'Cancel')
    )
    status = models.CharField(max_length=20, choices = quotation_status, default='Placed')

    # def __str__(self):
    #     return self.assigning
    




class TempInventory(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    item_category = models.ForeignKey(Category,on_delete = models.CASCADE,null = True, blank=True)
    manufacturing_unit = models.ForeignKey(ManufacturingUnit, on_delete=models.CASCADE, blank=True, null=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, null=True, blank=True)
    item_name = models.CharField(max_length=200, null=True, blank=True)
    price = models.CharField(max_length=200, null=True, blank=True)
    tax = models.CharField(max_length=200, null=True, blank=True)
    total_cost = models.CharField(max_length=200, null=True, blank=True)
    itemCategory = models.CharField(max_length=200, null=True, blank=True)


class QuotationProduct(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE, blank=True, null=True)
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Inventory,on_delete=models.CASCADE, blank=True, null=True)
    tempproduct = models.ForeignKey(TempInventory,on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.CharField(max_length=50, null=True, blank=True)
    cost_of_product = models.CharField(max_length=50, null=True, blank=True)
    price = models.CharField(max_length=50, null=True, blank=True)
    gst = models.CharField(max_length=50, null=True, blank=True)
    new_product = models.CharField(max_length=50, null=True, blank=True)
