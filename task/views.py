from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Q
from django.shortcuts import redirect, render, HttpResponse
from django.template import RequestContext
from .functions.functions import handle_uploaded_file
# from .forms import SalesOrderDocumentsForm
from .models import *
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.conf import settings
from django.core.mail import send_mail
import sys

# for converting the html to pdf
from django.http import HttpResponse
from django.views.generic import View
from .pdf_convert import render_to_pdf
from django.template.loader import render_to_string
# from cities.models import City, Region
# from django.http import JsonResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from datetime import date
from inventory.models import (
    PRODUCT_SERVICE,
    ITEM_UNIT,
    ITEM_TYPE,
    Category,
    Inventory,
    Warehouse,
    Rack
)


# Create your views here.
def home(request):
    return render(request, 'home.html')


# def get_states(request):
#     region_id = request.GET.get('region_id')
#     states = City.objects.filter(region_id=region_id).distinct('region_id')
#     state_list = []
#     for state in states:
#         state_dict = {}
#         state_dict['id'] = state.id
#         state_dict['name'] = state.region.name
#         state_list.append(state_dict)
#     return JsonResponse({'states': state_list})

# def get_cities(request):
#     state_id = request.GET.get('state_id')
#     cities = City.objects.filter(region_id=state_id)
#     city_list = []
#     for city in cities:
#         city_dict = {}
#         city_dict['id'] = city.id
#         city_dict['name'] = city.name
#         city_list.append(city_dict)
#     return JsonResponse({'cities': city_list})


def customer_registration(request):
    try:
        # regions = Region.objects.all()
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            company_name = request.POST['company_name']
            contact_number = request.POST['contact_number']
            user_name = request.POST['user_name']
            email_id = request.POST['email_id']
            country = request.POST['country']
            state = request.POST['state']
            region = request.POST['region']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            industry = request.POST['industry']

            if password != confirm_password:
                messages.error(request, 'Password are not same. Please enter valid Password')
                return redirect('/customer-registration/')

            try:
                user = User.objects.get(username=user_name)
                messages.error(request, 'The username you entered has already been taken. Please try another username.')
                return redirect('/customer-registration/')

            except User.DoesNotExist:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email_id,
                                                username=user_name, password=password)
                client = Client.objects.create(user=user, company=company_name, contact_number=contact_number,
                                               country=country, state=state, industry=industry, region=region)
                user.save()
                client.save()
                return redirect('customer-login')
        return render(request, 'customer_registration.html')
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')


def customer_registration_redirect(request):
    return render(request, 'customer_registration_redirect.html')


def customer_login(request):
    try:
        if request.method == 'POST':
            username = request.POST['user_name']
            password = request.POST['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                if request.user.is_staff:
                    messages.error(request, 'This account is not a Customer Account. Login with different account.')
                    return redirect('/customer-login/')
                else:
                    return redirect('/customer-dashboard/')
            else:
                messages.error(request, 'Invailid Credentials , Please Try Again !!!')
        return render(request, 'customer_login.html')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_tb.tb_lineno, e)


# function display customer data
@login_required(login_url='customer-login')
def customer_detail(request):
    try:
        user = request.user
        customer_detail = Client.objects.filter(user=user)  # display customer details
        return render(request, 'customer_detail.html', {'customer_detail': customer_detail})
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')


# place order home page
@login_required(login_url='customer-login')
def create_sale_order(request):
    return render(request, 'create_sale_order.html')


@login_required(login_url='customer-login')
def create_manufacturing_unit(request):
    # try:
    #list_manufacturer = Manufacturer.objects.filter(user = request.user)
    if request.method == 'POST':
        company_name = request.POST['company_name']
        if ManufacturingUnit.objects.filter(user = request.user, company_name = company_name).exists():
            messages.error(request, 'Company Name already exist')
            return redirect('/create-unit/')
        else:
            print(request.POST)
            user = request.user
            unit_type = request.POST['unit_type']
            salutation = request.POST['salutation']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            contact_person = request.POST['contact_person']
            company_name = request.POST['company_name']
            manufacturer = request.POST.get('manufacturer')
            # manufacturer_name = Manufacturer.objects.get(id = int(manufacturer))
            # print(manufacturer_name.user)

            # print('hello')
            # print(manufacturer_name)
            email = request.POST['email']
            phone_number = request.POST.get('phone_number')
            website = request.POST['website']
            pan_number = request.POST['pan_number']
            currency = request.POST['currency']
            m_payment_term = request.POST['m_payment_term']
            # manufacturing unit address
            manufacturing_unit_attention = request.POST['manufacturing_unit_attention']
            manufacturing_unit_country = request.POST['manufacturing_unit_country']
            manufacturing_unit_address = request.POST['manufacturing_unit_address']
            manufacturing_unit_city = request.POST['manufacturing_unit_city']
            manufacturing_unit_state = request.POST['manufacturing_unit_state']
            manufacturing_unit_zip_code = request.POST['manufacturing_unit_zip_code']
            manufacturing_unit_phone_number = request.POST['manufacturing_unit_phone_number']
            manufacturing_unit_fax = request.POST['manufacturing_unit_fax']

            manufacturing_unit_address = ManufacturingUnitAddress(user=user,
                                                                  manufacturing_unit_attention=manufacturing_unit_attention,
                                                                  manufacturing_unit_country=manufacturing_unit_country,
                                                                  manufacturing_unit_address=manufacturing_unit_address,
                                                                  manufacturing_unit_city=manufacturing_unit_city,
                                                                  manufacturing_unit_state=manufacturing_unit_state,
                                                                  manufacturing_unit_zip_code=manufacturing_unit_zip_code,
                                                                  manufacturing_unit_phone_number=manufacturing_unit_phone_number,
                                                                  manufacturing_unit_fax=manufacturing_unit_fax)
            manufacturing_unit_address.save()

            manufacturing_unit = ManufacturingUnit.objects.create(user=user, unit_type=unit_type,
                                                                  manufacturers=manufacturer, salutation=salutation,
                                                                  first_name=first_name, last_name=last_name,
                                                                  contact_person=contact_person, company_name=company_name,
                                                                  email=email, phone_number=phone_number, website=website,
                                                                  pan_number=pan_number, currency=currency,
                                                                  m_payment_term=m_payment_term,
                                                                  manufacturing_unit_address=manufacturing_unit_address)  # manufacturer = manufacturer_name
            # manufacturing_unit.save()
            return redirect('/update-unit/' + str(manufacturing_unit.id))
    # except:
    #     return HttpResponse('Something Went Wrong. Try Again After Some Time.')
    return render(request, 'create_manufacturing_unit.html')


@login_required(login_url='customer-login')
def update_manufacturing_unit(request, id):
    # try:
    update_manufacturing_unit = ManufacturingUnit.objects.get(id=id)
    list_manufacturer = Manufacturer.objects.all()
    update_manufacturing_unit_address = ManufacturingUnitAddress.objects.get(id=id)
    items = TempInventory.objects.filter(manufacturing_unit__id=id)
    print(items)

    if request.method == 'POST':
        print(request.POST)
        salutation = request.POST['salutation']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        contact_person = request.POST['contact_person']
        company_name = request.POST['company_name']
        manufacturer = request.POST.get('manufacturer')
        # manufacturer_name = Manufacturer.objects.get(id = manufacturer)
        # print(manufacturer_name.user)

        # print('hello')
        # print(manufacturer_name)
        email = request.POST['email']
        phone_number = request.POST.get('phone_number')
        website = request.POST['website']
        pan_number = request.POST['pan_number']
        currency = request.POST['currency']
        m_payment_term = request.POST['m_payment_term']
        # manufacturing unit address
        manufacturing_unit_attention = request.POST['attention']
        manufacturing_unit_country = request.POST['country']
        manufacturing_unit_address = request.POST['address']
        manufacturing_unit_city = request.POST['city']
        manufacturing_unit_state = request.POST['state']
        manufacturing_unit_zip_code = request.POST['zip_code']
        manufacturing_unit_phone_number = request.POST['manufacturing_unit_phone_number']
        manufacturing_unit_fax = request.POST['fax']

        update_manufacturing_unit.salutation = salutation
        update_manufacturing_unit.first_name = first_name
        update_manufacturing_unit.last_name = last_name
        update_manufacturing_unit.contact_person = contact_person
        # update_manufacturing_unit.manufacturer = manufacturer_name
        update_manufacturing_unit.company_name = company_name
        update_manufacturing_unit.email = email
        update_manufacturing_unit.phone_number = phone_number
        update_manufacturing_unit.pan_number = pan_number
        update_manufacturing_unit.website = website
        update_manufacturing_unit.currency = currency
        update_manufacturing_unit.manufacturers = manufacturer
        update_manufacturing_unit.m_payment_term = m_payment_term
        update_manufacturing_unit_address.manufacturing_unit_attention = manufacturing_unit_attention
        update_manufacturing_unit_address.manufacturing_unit_country = manufacturing_unit_country
        update_manufacturing_unit_address.manufacturing_unit_address = manufacturing_unit_address
        update_manufacturing_unit_address.manufacturing_unit_city = manufacturing_unit_city
        update_manufacturing_unit_address.manufacturing_unit_state = manufacturing_unit_state
        update_manufacturing_unit_address.manufacturing_unit_zip_code = manufacturing_unit_zip_code
        update_manufacturing_unit_address.manufacturing_unit_phone_number = manufacturing_unit_phone_number
        update_manufacturing_unit_address.manufacturing_unit_fax = manufacturing_unit_fax
        update_manufacturing_unit.save()
        update_manufacturing_unit_address.save()
        # billing_address.save()
        # customer_shipping_address.save()
        messages.success(request, 'Details Updated Successfully.')

        return redirect("/update-unit/" + str(id))
    # except:
    #     return HttpResponse('Something Went Wrong. Try Again After Some Time.')
    return render(request, 'update_manufacturing_unit.html',
                  {'update_manufacturing_unit': update_manufacturing_unit, 'list_manufacturer': list_manufacturer,
                   'update_manufacturing_unit_address': update_manufacturing_unit_address,
                   'items': items})  # 'billing_address':billing_address,


# from .telegram_bot import send_telegram_message
# import telegram
# from telegram import Contact
# function to create sales order
from django.db import transaction


@transaction.atomic
@login_required(login_url='customer-login')
def sales_order(request):
    try:
        user = request.user
        display_manufacturing_unit = ManufacturingUnit.objects.filter(user=user)
        inventory_product = Inventory.objects.filter(user=user)
        inventory_map = {}
        inventory_dict = {}
        inventory_detail = {}
        product_price = {}
        product_gst = {}
        for i in inventory_product:
            inventory_map[str(i.id)] = i.stock
            inventory_dict[str(i.id)] = i.item_name
            inventory_detail[str(i.id)] = i
            product_price[str(i.id)] = i.price
            product_gst[str(i.id)] = i.tax
        # cur.execute("""SELECT * FROM google""")
        # out = cur.fetchall()
        # variable = {key:val for key,val in inventory_product}
        # print(variable)
        # a = Client.objects.get(contact_number = user)
        # print(a)
        # form = SalesOrderDocumentsForm()
        # print(form)
        if request.method == 'POST':
            user = request.user
            print(request.POST)
            unit_type = request.POST['distributor']
            manufacturing_unit = request.POST.get('manufacturer_unit_name')
            mf_unit_name = ManufacturingUnit.objects.get(company_name=manufacturing_unit, user= request.user)
            # print(mf_unit_name.company_name)
            # sales_order_number = request.POST['sales_order']
            # manufacturer_contact_person_name = request.POST['manufacturer_contact_person_name']
            # manufacturer_contact_person_phone_number = request.POST['manufacturer_contact_person_phone_number']
            customer_phone_number = request.POST['customer_phone_number']
            sales_order_date = request.POST['sales_order_date']
            exp_shipment_date = request.POST['expected_shipment_date']
            payment_term = request.POST.get('paymentterm')
            # order_status = request.POST['status']
            delivery_method = request.POST['delivery_method']
            customer_sales_person = request.POST['customer_sales_person']
            # print(manufacturing_unit)
            # Product Detail
            product_name = request.POST.getlist('product_name')
            # print(product_name)
            # product_length = request.POST.getlist('product_length')
            weight_calculation = request.POST.getlist('weight_calculation')
            # print(weight_calculation)
            quantity = request.POST.getlist('quantity')
            # print(quantity,"quantity")
            bundle_number = request.POST.getlist('bundle_number')
            price = request.POST.getlist('price')
            gst = request.POST.getlist('gst')
            total_cost = request.POST.getlist('product_cost')
            auto_logistic = request.POST.getlist('auto_logistic')
            terms_and_conditions = request.POST['terms_and_conditions']
            total_amount = request.POST['total_amount']

            order = SalesOrder(user=user, unit_type=unit_type, manufacturing_unit=mf_unit_name,
                               sales_order_date=sales_order_date, exp_shipment_date=exp_shipment_date,
                               customer_phone_number=customer_phone_number, payment_term=payment_term,
                               delivery_method=delivery_method, customer_sales_person=customer_sales_person,
                               terms_and_conditions=terms_and_conditions, total_amount=total_amount)

            # SMTP integration
            # print('user name', user.username)
            # print('email', user.email)
            # subject = 'Your Order Placed Successfully'
            # message = f'Hi {user.username}, Your Order Placed Successfully to {manufacturing_unit}. Your Product Detail is as follow product name & length {product_name} . Total cost of Your Order is {total_amount}. Thanks for Using Our Tool.'
            # email_from = settings.EMAIL_HOST_USER
            # recipient_list = [user.email, ]
            # send_mail( subject, message, email_from, recipient_list)

            # https://myaccount.google.com/lesssecureapps?pli=1&rapt=AEjHL4O_7wKVXiBxvGkZvsQIAMGr6kmxV-KVSpSwYomZVEIy8zFW930K1dcRxfFTHuvPUBhD5BdTuGV7E5ZTuRLBKaBSkE05KA

            order.save()
            product_details = []
            print(inventory_map)
            for i in range(len(product_name)):

                # obj = ProductDetail(product_name = product_name[i], sales_order = order)
                # print(obj)
                # obj.length_of_product = product_length[i]
                # print(product_name[i])
                print(inventory_map[str(product_name[i])])
                # print(inventory_map[product_name[i]].stock)
                print(quantity[i] <= inventory_map[str(product_name[i])])
                print(int(quantity[i]) <= int(inventory_map[str(product_name[i])]))
                print(type(inventory_map[str(product_name[i])]))
                print(inventory_map[product_name[i]])
                if product_name[i] in inventory_map and int(quantity[i]) <= int(inventory_map[str(product_name[i])]):
                    obj = ProductDetail(product_name=inventory_dict[product_name[i]], sales_order=order)
                    obj.inventory = inventory_detail[str(product_name[i])]
                    obj.weight_of_product = weight_calculation[i]
                    obj.quantity = quantity[i]
                    obj.auto_logistic_fillment = auto_logistic[i]
                    obj.bundle_number = bundle_number[i]
                    obj.cost_of_product = price[i]
                    obj.gst = gst[i]
                    obj.total_cost = total_cost[i]
                    product_details.append(obj)
                else:
                    transaction.set_rollback(True)
                    messages.error(request,
                                   f'Quantity of {inventory_dict[product_name[i]]} is equal to {inventory_map[product_name[i]]}')
                    return redirect('sales-order')

            ProductDetail.objects.bulk_create(product_details)
            # product_details.executemany
            # obj.save()
            # send_telegram_message('Success! MyModel object created.', '+917000611658')

            # Replace 'YOUR_BOT_TOKEN' with your actual bot token
            # bot = telegram.Bot(token='6227234770:AAFgsisZovWLy9V5dVnulj-FAAeRKapmfLE')

            # Replace 'USER_PHONE_NUMBER' with the phone number of the user
            # contact = Contact(phone_number='7000611658', first_name='Juzer')

            # Create the contact
            # bot.send_contact(chat_id='USER_CHAT_ID', contact=contact)

            # Send a message to the contact
            # bot.send_message(chat_id='7000611658', text='Hello, this is a message sent to your phone number!')
            # print(send_telegram_message)
            return redirect('view-sales-order-dashboard')
    # except:
    #     return HttpResponse('Something Went Wrong. Try Again After Some Time.')
    # except Exception as e: # work on python 2.x
    #     return HttpResponse('Failed to upload to ftp: '+ str(e))
    # except Exception as e:
    #     return HttpResponse(e + ' ' + str(e.__traceback__.tb_lineno))
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_tb.tb_lineno, e)
    #     return HttpResponse(
    #     type(e).__name__+' '+         # TypeError
    #     __file__+' '+                  # /tmp/example.py
    #     e.__traceback__.tb_lineno  # 2
    # )
    print(inventory_product)
    return render(request, 'sales_order.html',
                  {'display_manufacturing_unit': display_manufacturing_unit, 'inventory_product': inventory_product,
                   'product_gst': product_gst, 'product_price': product_price})


def load_product_cost(request):
    prod = request.GET.get('product_name')
    print(prod)
    product = Inventory.objects.filter(id=prod)

    return render(request, 'load_product_cost.html', {'product': product})


def load_quotation_product_cost(request):
    prod = request.GET.get('product_name')
    print(prod)
    product = TempInventory.objects.filter(id=prod)

    return render(request, 'load_quotation_product_cost.html', {'product': product})


def load_purchase_product_cost(request):
    prod = request.GET.get('product_name')
    print(prod)
    product = TempInventory.objects.filter(id=prod)

    return render(request, 'load_purchase_product_cost.html', {'product': product})


@login_required(login_url='customer-login')
def load_product(request):
    mf_unit_id = request.GET.get('manufacturer_unit_name')
    print('hhhhh', mf_unit_id)
    product = AddSalesOrderProduct.objects.filter(manufacturing_unit__company_name=mf_unit_id)
    return render(request, 'load_product.html', {'product': product})


def load_manufacturer_distributor(request):
    load = request.GET.get('distributor')
    print('hellloooo')
    manufacturer_distributor = ManufacturingUnit.objects.filter(unit_type=load, user=request.user)
    return render(request, 'load_manufacturer_distributor.html', {'manufacturer_distributor': manufacturer_distributor})


@login_required(login_url='customer-login')
def sales_order_update(request, id):
    # try:
    user = request.user
    display_manufacturing_unit = ManufacturingUnit.objects.filter(user=user)
    # get_manufacturing_unit = ManufacturingUnit.objects.get(id =id)
    # print(get_manufacturing_unit)
    sales_order_update = SalesOrder.objects.get(id=id)
    product_list = ProductDetail.objects.filter(sales_order__id=id)
    # product_update = ProductDetail.objects.get(sales_order__id = id)
    print(len(product_list))

    print(sales_order_update)
    if request.method == 'POST':
        print(request.POST)
        manufacturing_unit = request.POST['manufacturer_unit_name']
        #   print(manufacturing_unit)
        mf_unit_name = ManufacturingUnit.objects.get(company_name=manufacturing_unit, user = request.user)
        #   print(mf_unit_name.display_name)
        sales_order = request.POST['sales_order']
        #   manufacturer_contact_person_name = request.POST['manufacturer_contact_person_name']
        #   manufacturer_contact_person_phone_number = request.POST['manufacturer_contact_person_phone_number']
        #   sales_order_date = request.POST['sales_order_date']
        #   exp_shipment_date = request.POST['expected_shipment_date']
        payment_term = request.POST.get('paymentterm')
        # order_status = request.POST['status']
        delivery_method = request.POST['delivery_method']
        customer_sales_person = request.POST['customer_sales_person']
        customer_phone_number = request.POST['customer_phone_number']
        order_status = request.POST['status']

        #   product_name = request.POST['product_name']
        product_name = request.POST.getlist('product_name')

        print(len(product_name))
        #   product_length = request.POST.getlist('product_length')
        weight_calculation = request.POST.getlist('weight_calculation')
        bundle_number = request.POST.getlist('bundle_number')
        cost_of_product = request.POST.getlist('product_cost')
        customer_approval = request.POST.getlist('customer_approval')
        #   print(weight_calculation)
        quantity = request.POST.getlist('quantity')
        #   print(quantity,"quantity")
        auto_logistic = request.POST.getlist('auto_logistic')
        #   print(product_name)
        terms_and_conditions = request.POST['terms_and_conditions']
        total_amount = request.POST['total_amount']
        # For uplaod Files

        fs = FileSystemStorage()

        if 'update_sales_order_file' in request.FILES:
            sales_order_file = request.FILES['update_sales_order_file']
            sales_order_file = fs.save(sales_order_file.name, sales_order_file)
            sales_order_update.sales_order_file = sales_order_file
            sales_order_update.save()

        if 'update_delivery_challan' in request.FILES:
            delivery_challan = request.FILES['update_delivery_challan']
            delivery_challan = fs.save(delivery_challan.name, delivery_challan)
            sales_order_update.delivery_challan = delivery_challan
            sales_order_update.save()

        if 'packing_list' in request.FILES:
            packing_list = request.FILES['packing_list']
            packing_list = fs.save(packing_list.name, packing_list)
            sales_order_update.packing_list = packing_list
            sales_order_update.save()

        if 'ev_list' in request.FILES:
            ev_list = request.FILES['ev_list']
            ev_list = fs.save(ev_list.name, ev_list)
            sales_order_update.ev_list = ev_list
            sales_order_update.save()

        sales_order_update.manufacturing_unit = mf_unit_name
        sales_order_update.sales_order = sales_order
        sales_order_update.order_status = order_status
        #   sales_order_update.manufacturer_contact_person_name = manufacturer_contact_person_name
        #   sales_order_update.manufacturer_contact_person_phone_number = manufacturer_contact_person_phone_number
        #   sales_order_update.sales_order_date = sales_order_date
        #   sales_order_update.exp_shipment_date = exp_shipment_date
        sales_order_update.payment_term = payment_term
        sales_order_update.delivery_method = delivery_method
        sales_order_update.customer_sales_person = customer_sales_person
        sales_order_update.customer_phone_number = customer_phone_number
        sales_order_update.terms_and_conditions = terms_and_conditions
        sales_order_update.total_amount = total_amount
        #   sales_order_update.sales_order_file = sales_order_file
        #   sales_order_update.delivery_challan = delivery_challan

        #   product.product_name = product_name
        #   product.length_of_product = product_length
        #   product.weight_of_product = weight_calculation
        #   product.quantity = quantity
        #   product.auto_logistic_fillment = auto_logistic

        #   product.save()
        #   print(product_name)
        #   get_manufacturing_unit.display_name = manufacturing_unit
        #   get_manufacturing_unit.save()
        print(product_name)

        num = 0

        product_details = []
        inventory_detail = []

        for rec in product_name:
            obj = ProductDetail.objects.get(id=rec)
            stock = Inventory.objects.get(id=obj.inventory.id)
            print(stock.stock)
            print(obj.quantity)
            if int(stock.stock) >= int(obj.quantity):
                if order_status == 'Accepted':
                    stock.stock = str(int(stock.stock) - int(obj.quantity))
                    inventory_detail.append(stock)
                obj.product_name = product_name[num]
                # obj.length_of_product = product_length[num]
                obj.weight_of_product = weight_calculation[num]

                obj.quantity = quantity[num]
                obj.auto_logistic_fillment = auto_logistic[num]
                obj.bundle_number = bundle_number[num]
                obj.cost_of_product = cost_of_product[num]
                # obj.order_comment = order_comment[num]
                # obj.manufacturer_order_approval = manufacturer_approval[num]
                print(obj.manufacturer_order_approval)
                product_details.append(obj)
                num = num + 1

            else:
                messages.error(request, f'Quantity of {stock.item_name} is equal to {stock.stock}')
                return redirect('/sales-order-update/' + str(int(id)))

        sales_order_update.save()

        ProductDetail.objects.bulk_update(product_details, ['quantity'])
        if order_status == 'Accepted':
            Inventory.objects.bulk_update(inventory_detail, ['stock'])

        # for obj in product_list:
        #     print(obj)
        #     obj.product_name = product_name[num]
        #     print(product_name[num])
        #     # obj = ProductDetail.objects.filter(sales_order__id = id)
        #     # print(obj, "obj")
        #     # obj.length_of_product = product_length[num]
        #     obj.weight_of_product = weight_calculation[num]
        #     obj.quantity = quantity[num]
        #     obj.auto_logistic_fillment = auto_logistic[num]
        #     obj.bundle_number = bundle_number[num]
        #     obj.cost_of_product = cost_of_product[num]
        #     obj.customer_order_approval = customer_approval[num]
        #     print(obj.customer_order_approval)
        #     obj.save()
        #     num = num+1
        #   print(f" {product_name} product name")
        return redirect('/view-sales-order-dashboard/')
    # except:
    #     return HttpResponse('Something Went Wrong. Try Again After Some Time.')
    return render(request, 'sales_order_update.html',
                  {'sales_order_update': sales_order_update, 'display_manufacturing_unit': display_manufacturing_unit,
                   'product': product_list})


@login_required(login_url='customer-login')
def customer_dashboard(request):
    try:
        user = request.user
        order_placed = SalesOrder.objects.filter(user=user)
        total_sales_order_placed = order_placed.count()

        sales_order = SalesOrder.objects.filter(Q(user=user) & Q(order_status='Accepted')).order_by(
            '-id')  # to display orders on dashboard
        total_order_accepted = sales_order.count()

        order = SalesOrder.objects.filter(
            Q(user=user) & Q(order_status='Accepted') & Q(exp_shipment_date=datetime.date.today())).order_by('-id')
    
            
        
        purchase_order = PurchaseOrder.objects.filter(Q(user=user) & Q(order_status='Accepted'))

        purchase_order_total = purchase_order.count()

        purchase_order_placed = PurchaseOrder.objects.filter(user=user)
        total_purchase_order_placed = purchase_order_placed.count()

        purchase_order_filter = PurchaseOrder.objects.filter(
            Q(user=user) & Q(order_status='Accepted') & Q(exp_shipment_date=date.today())).order_by(
            '-id')  # to display orders on dashboard

        context = {'orders': order, 'total_order_accepted': total_order_accepted,
                   'total_sales_order_placed': total_sales_order_placed, 'purchase_order_total': purchase_order_total,
                   'total_purchase_order_placed': total_purchase_order_placed,
                   'purchase_order_filter': purchase_order_filter}
        return render(request, 'customer_dashboard.html', context)
        # return HttpResponse()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_tb.tb_lineno, e)


def view_sales_order_dashboard(request):
    user = request.user
    order = SalesOrder.objects.filter(user=user).order_by('-id')
    paginator = Paginator(order, 10, orphans=3)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return render(request, 'view_sales_order_dashboard.html', {'orders': page_object})


@login_required(login_url='customer-login')
def customer_sales_order_view(request, id):
    try:
        user = request.user
        display_manufacturing_unit = ManufacturingUnit.objects.filter(user=user)
        sales_order_update = SalesOrder.objects.get(id=id)
        product_list = ProductDetail.objects.filter(sales_order__id=id)
        return render(request, 'customer_sales_order_view.html',
                      {'display_manufacturing_unit': display_manufacturing_unit,
                       'sales_order_update': sales_order_update, 'product': product_list})
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')


@login_required(login_url='customer-login')
def manufacturing_unit_dashboard(request):
    try:
        user = request.user
        manufacturing_unit_data = ManufacturingUnit.objects.filter(user=user)
        return render(request, 'manufacturing_unit_dashboard.html',
                      {'manufacturing_unit_data': manufacturing_unit_data})
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')


# search function for sales order
@login_required(login_url='customer-login')
def sales_order_search(request):
    try:
        user = request.user
        sales_order_search_query = request.GET.get('search')
        # search_result = ManufacturingUnit.objects.filter(Q(display_name__icontains = customer_search_query), user = user)
        search_result = SalesOrder.objects.filter(Q(sales_order__icontains=sales_order_search_query) | Q(
            manufacturing_unit__company_name__icontains=sales_order_search_query), user=user).order_by("-id")
        return render(request, 'sales_order_search.html',
                      {'search_result': search_result, 'sales_order_search_query': sales_order_search_query})

    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')

def edit_manufacturer_quotation(request,id):
    quotation = Quotation.objects.get(id=id)
    product_list = QuotationProduct.objects.filter(quotation__id=id)

    if request.method == 'POST':
        print(request.POST)
        status = request.POST.get('status')
        terms_and_conditions = request.POST.get('terms_and_conditions')
        product = request.POST.getlist('product_name')
        
        cost = request.POST.getlist('price')
        total_amount = request.POST.get('total_amount')
        quantity = request.POST.getlist('quantity')

        for i in range(len(product)):
            print('check--', product[i])
            quotationProduct = QuotationProduct.objects.get(id= product[i])
            quotationProduct.quantity = quantity[i]
            quotationProduct.price = cost[i]
            quotationProduct.save()
        record = Quotation.objects.get(id=id)
        record.status = status
        record.terms_and_condition = terms_and_conditions
        record.total_amount = total_amount
        record.save()

        return redirect('manufacturer-quotation-dashboard')


    return render(request, 'edit_manufacturer_quotation.html', {'quotation': quotation, 'product_list': product_list})


# search function for quotation order
@login_required(login_url='customer-login')
def quotation_search(request):

    user = request.user
    quotation_search_query = request.GET.get('search')
    search_result = Quotation.objects.filter(Q(assigning__manufacturers__icontains=quotation_search_query), user=user).order_by("-id")
    print(search_result)
    return render(request, 'search_quotation.html',
                      {'search_result': search_result, 'quotation_search_query': quotation_search_query})

@login_required(login_url='manufacturer-login')
def manufacturer_quotation_search(request):
    user = request.user
    quotation_search_query = request.GET.get('search')
    search_result = Quotation.objects.filter(Q(assigning__company_name__icontains=quotation_search_query), user=user).order_by("-id")
    return render(request, 'manufacturer_quotation_search.html', {'search_result': search_result, 'quotation_search_query': quotation_search_query})

# search function for manufacturing unit
@login_required(login_url='customer-login')
def search_manufacturering_unit(request):

    user = request.user
    manufacturing_unit_search_query = request.GET.get('search')
    search_result = ManufacturingUnit.objects.filter(Q(company_name__icontains=manufacturing_unit_search_query), user=user).order_by("-id")
    return render(request, 'search_manufacturing_unit.html',
                      {'search_result': search_result, 'manufacturing_unit_search_query': manufacturing_unit_search_query})


# search function for purchase order
@login_required(login_url='customer-login')
def search_purchase_order(request):

    user = request.user
    purchase_order_search_query = request.GET.get('search')
    search_result = PurchaseOrder.objects.filter(Q(
    manufacturing_unit__company_name__icontains=purchase_order_search_query), user=user).order_by("-id")
    return render(request, 'purchase_order_search.html',
                      {'search_result': search_result, 'purchase_order_search_query': purchase_order_search_query})


# Quotation

def create_quotation(request):
    return render(request, "create_quotation.html")

def quotation(request):
    user = request.user
    product = TempInventory.objects.filter(user=user)
    display_manufacturing_unit = ManufacturingUnit.objects.filter(user=request.user)
    if request.method == 'POST':
        print(request.POST)
        manufacturing_unit = request.POST.get('vendor_unit_name')
        print(manufacturing_unit)
        # 
        # print(mf_unit_name)
        # Product Detail
        product_name = request.POST.getlist('product_name')
        quantity = request.POST.getlist('quantity')
        # bundle_number = request.POST.getlist('bundle_number')
        cost_of_product = request.POST.getlist('product_cost')
        price = request.POST.getlist('price')
        gst = request.POST.getlist('gst')
        terms_and_conditions = request.POST['terms_and_conditions']
        total_amount = request.POST['total_amount']

        mf_unit_name = ManufacturingUnit.objects.get(company_name=manufacturing_unit, user = request.user)
        quotation = Quotation.objects.create(assigning=mf_unit_name,
                                             user=user,
                                             total_amount=total_amount,
                                             status='Placed',
                                             terms_and_condition=terms_and_conditions)

        for i in range(len(product_name)):
            quotation_product = TempInventory.objects.get(id=product_name[i])
            print(quotation_product)
            products = QuotationProduct.objects.create(user=user,
                                                       tempproduct=quotation_product,
                                                       quotation=quotation)
            products.quantity = quantity[i]
            products.cost_of_product = cost_of_product[i]
            products.gst = gst[i]
            products.price = price[i]
            products.save()

        return redirect('/quotation-dashboard/')

    return render(request, 'quotation.html',
                  {'display_manufacturing_unit': display_manufacturing_unit, 'product': product})

def manufacturer_quotation_dashboard(request):
    quotation = Quotation.objects.filter(assigning__manufacturer__user=request.user).order_by('-id')
    print(quotation)
    paginator = Paginator(quotation, 10, orphans=3)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return render(request, 'manufacturer_quotation_dashboard.html',{'quotation':page_object})

def quotation_dashboard(request):
    quotation = Quotation.objects.filter(user=request.user).order_by('-id')
    paginator = Paginator(quotation, 10, orphans=3)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    return render(request, 'quotation_dashboard.html', {'quotation': page_object})


def edit_quotation(request, id):
    quotation = Quotation.objects.get(id=id)
    product_list = QuotationProduct.objects.filter(quotation__id=id)

    if request.method == 'POST':
        print(request.POST)
        status = request.POST.get('status')
        terms_and_conditions = request.POST.get('terms_and_conditions')
        product = request.POST.getlist('product_name')
        
        cost = request.POST.getlist('price')
        total_amount = request.POST.get('total_amount')
        quantity = request.POST.getlist('quantity')

        for i in range(len(product)):
            print('check--', product[i])
            quotationProduct = QuotationProduct.objects.get(id= product[i])
            quotationProduct.quantity = quantity[i]
            quotationProduct.price = cost[i]
            quotationProduct.save()
        record = Quotation.objects.get(id=id)
        record.status = status
        record.terms_and_condition = terms_and_conditions
        record.total_amount = total_amount
        record.save()

        return redirect('quotation-dashboard')


    return render(request, 'edit_quotation.html', {'quotation': quotation, 'product_list': product_list})


def view_quotation(request, id):
    quotation = Quotation.objects.get(id=id)
    product_list = QuotationProduct.objects.filter(quotation__id=id)
    print('product_list---', product_list)
    return render(request, 'view_quotation.html', {'quotation': quotation, 'product_list': product_list})


# def add_product_to_unit(request):

#     return render(request, 'add_product_to_unit.html')


class AddTempInventoryItem(View):
    template_name: str = "update_manufacturing_unit.html"

    def get(self, request, id):
        # categories = Warehouse.objects.filter(user = request.user)
        items = TempInventory.objects.filter(Q(user=request.user) & Q(manufacturing_unit=id))
        categories = Category.objects.values('name').distinct().filter(user=request.user)
        search_id = request.GET.get("search_by_id")
        search_name = request.GET.get("search_by_name")
        search_category = request.GET.get("search_by_category")
        search_type = request.GET.get("search_by_type")
        search_hsn = request.GET.get("search_by_hsncode")
        units = ITEM_UNIT
        product_services = PRODUCT_SERVICE
        item_types = ITEM_TYPE
        return render(request, self.template_name, locals())

    def post(self, request, id):
        user = request.user
        # item_sku = request.POST.get("item_sku")
        item_name = request.POST.get("item_name")
        # if TempInventory.objects.filter(item_name = item_name).exists():
        #    messages.error(request, 'Product already exists..!!!')
        #    return redirect("/update-unit/"+str(id))
        # else:
        tax = request.POST.get("tax")
        price = request.POST.get("item_price")
        category = request.POST.get("category")
        manufacturing_unit = request.POST.get("manufacturer")

        if ManufacturingUnit.objects.filter(id=id).exists():
            mf_unit = ManufacturingUnit.objects.get(id=id)
        else:
            messages.error(request, 'Enter Correct Company Name of Manufacturing Unit')
            return HttpResponseRedirect(reverse("add-product-to-unit"), locals())

        #if Category.objects.filter(name=category).exists():
        #    for i in Category.objects.get(name=category):
        #        item_category = i
        #else:
        #    item_category = Category.objects.create(user=user, name=category)
        # items_rack = Rack.objects.get(id = rack)
        # print(request.POST)

        TempInventory.objects.create(user=request.user, manufacturing_unit=mf_unit, price=price, item_name=item_name,
                                     tax=tax, itemCategory=category)  # item_category=user_category,
        messages.success(request, 'Product Added Successfully.')
        # Category(user = user, name = category_name).save()
        # Rack(rack = rack_name).save()
        # categories = Category.objects.filter(user = request.user)

        return redirect("/update-unit/" + str(id))


def edit_unit_product(request, id):
    product = TempInventory.objects.filter(id=id)
    if request.method == 'POST':
        item_name = request.POST['item_name']
        item_category = request.POST['category']
        price = request.POST['item_price']
        tax = request.POST['tax']
        # product.item_name = item_name
        # product.item_category = item_category
        # product.price = price
        # product.tax = tax
        # product.save()
        item = TempInventory.objects.filter(id=id).update(item_name=item_name, price=price, tax=tax, itemCategory = item_category)
        items = TempInventory.objects.get(id=id)
        # print(items.manufacturing_unit.id)
        return redirect('/update-unit/' + str(items.manufacturing_unit.id))
    return render(request, 'edit_unit_product.html', {'product': product})


def delete_unit_product(request, id):
    item_detail = TempInventory.objects.get(id=id)
    item_detail.delete()
    return redirect("/update-unit/" + str(item_detail.manufacturing_unit.id))


# manufacturer functions
def manufacturer_registration(request):
    try:
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            company_name = request.POST['company_name']
            contact_number = request.POST['contact_number']
            user_name = request.POST['user_name']
            email_id = request.POST['email_id']
            country = request.POST['country']
            state = request.POST['state']
            region = request.POST['region']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            industry = request.POST['industry']

            if password != confirm_password:
                messages.error(request, 'Password are not same. Please enter valid Password')
                return redirect('/manufacturer-registration/')

            try:
                user = User.objects.get(username=user_name)
                messages.error(request, 'The username you entered has already been taken. Please try another username.')
                return redirect('/manufacturer-registration/')

            except User.DoesNotExist:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email_id,
                                                username=user_name, password=password)
                manufacturer = Manufacturer.objects.create(user=user, m_company=company_name,
                                                           m_contact_number=contact_number, m_country=country,
                                                           m_state=state, m_industry=industry, m_region=region)
                user.save()
                manufacturer.save()
                return redirect('/manufacturer-registration-redirect/')
        return render(request, 'manufacturer_registration.html')
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')


def manufacturer_login(request):
    try:
        if request.method == 'POST':
            username = request.POST['user_name']
            password = request.POST['password'] 

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                if request.user.is_staff:
                    return redirect('/manufacturer-dashboard/')
                else:
                    messages.error(request, 'This is not a Manufacturer Account. Login with different Account.')
                    return redirect('/manufacturer-login/')
            else:
                messages.error(request, 'Invailid Credentials , Please Try Again !!!')
                return redirect('/manufacturer-login/')
        return render(request, 'manufacturer_login.html')
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')
    
@login_required(login_url='manufacturer-login')
def manufacturer_dash(request):
        user = request.user
        print("useer------",user)
        # sales_order = SalesOrder.objects.all()
        print(PurchaseOrder.objects.all())
        sales_order = PurchaseOrder.objects.filter(manufacturing_unit__manufacturer__user = user).order_by('-id')
        # dividing data into pages
        paginator = Paginator(sales_order, 10, orphans=3)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)

        # mf_unit = SalesOrder.objects.all()
        # order = ManufacturingUnit.objects.all()

        return render(request, 'manufacturer_dash.html',{'order': page_object})

def manufacturer_purchase_order_update(request, id):
    user = request.user
    display_manufacturer_unit = ManufacturingUnit.objects.filter(user=user)
    purchase_order_update = PurchaseOrder.objects.get(id=id)
    product_list = PurchaseOrderProductDetail.objects.filter(purchase_order__id=id)
    print(sales_order_update)
    if request.method == 'POST':
        print(request.POST)
        
        payment_term = request.POST.get('paymentterm')
        delivery_method = request.POST['delivery_method']
        product_name = request.POST.getlist('product_name')

        print(len(product_name))
        product_length = request.POST.getlist('product_length')
        weight_calculation = request.POST.getlist('weight_calculation')
        bundle_number = request.POST.getlist('bundle_number')
        cost_of_product = request.POST.getlist('product_cost')
        gst = request.POST.getlist('gst')
        total_cost = request.POST.getlist('total_cost')
        manufacturer_approval = request.POST.getlist('manufacturer_approval')
        order_comment = request.POST.getlist('order_comment')
        quantity = request.POST.getlist('quantity')
        auto_logistic = request.POST.getlist('auto_logistic')
        order_status = request.POST['status']
        terms_and_conditions = request.POST['terms_and_conditions']
        # total_amount = request.POST['total_amount']
        # For uplaod Files
        fs = FileSystemStorage()
        if 'purchase_order_file' in request.FILES:
            purchase_order_file = request.FILES['purchase_order_file']
            purchase_order_file = fs.save(purchase_order_file.name, purchase_order_file)
            purchase_order_update.purchase_order_file = purchase_order_file
            purchase_order_update.save()

        if 'update_delivery_challan' in request.FILES:
            delivery_challan = request.FILES['update_delivery_challan']
            delivery_challan = fs.save(delivery_challan.name, delivery_challan)
            purchase_order_update.delivery_challan = delivery_challan
            purchase_order_update.save()

        if 'packing_list' in request.FILES:
            packing_list = request.FILES['packing_list']
            packing_list = fs.save(packing_list.name, packing_list)
            purchase_order_update.packing_list = packing_list
            purchase_order_update.save()

        if 'ev_list' in request.FILES:
            ev_list = request.FILES['ev_list']
            ev_list = fs.save(ev_list.name, ev_list)
            purchase_order_update.ev_list = ev_list
            purchase_order_update.save()


        purchase_order_update.payment_term = payment_term
        purchase_order_update.delivery_method = delivery_method
   
        purchase_order_update.terms_and_conditions = terms_and_conditions
        purchase_order_update.order_status = order_status

        purchase_order_update.save()
        print(product_name)

        num = 0
        for obj in product_list:
            print('check')
            print(obj)
            obj.product_name = product_name[num]
            print(product_name[num])
            obj.weight_of_product = weight_calculation[num]
            obj.quantity = quantity[num]
            obj.auto_logistic_fillment = auto_logistic[num]
            obj.bundle_number = bundle_number[num]
            obj.cost_of_product = cost_of_product[num]
            obj.gst = gst[num]
            obj.total_cost = total_cost[num]
            obj.vendor_order_approval = manufacturer_approval[num]
            obj.order_comment = order_comment[num]
            # print(obj.customer_order_approval)
            obj.save()
            num = num + 1
            print(f" {order_comment} product name")
        return redirect('/manufacturer-dashboard/')

    return render(request, 'manufacturer_update_purchase_order.html', {'display_manufacturer_unit': display_manufacturer_unit,
                                                          'purchase_order_update': purchase_order_update,
                                                          'product_list': product_list})



def view_manufacturer_purchase_order(request,id):
    
    purchase_order_update = PurchaseOrder.objects.get(id=id)
    product_list = PurchaseOrderProductDetail.objects.filter(purchase_order__id=id)
    return render(request, 'view_manufacturer_purchase_order.html',
                      {'purchase_order_update': purchase_order_update, 'product_list': product_list})





@login_required(login_url='manufacturer-login')
def manufacturer_packing(request):
    try:
        return render(request, 'manufacturer_packing.html')
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')


@login_required(login_url='manufacturer-login')
def manufacturer_detail(request):
    try:
        user = request.user
        manufacturer_details = Manufacturer.objects.filter(user=user)
        return render(request, 'manufacturer_detail.html', {'data': manufacturer_details})
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')


def manufacturer_registration_redirect(request):
    return render(request, 'manufacturer_registration_redirect.html')


@login_required(login_url='manufacturer-login')
def manufacturer_sales_order_update(request, id):
    try:
        user = request.user
        display_manufacturing_unit = ManufacturingUnit.objects.filter(user=user)
        sales_order_update = SalesOrder.objects.get(id=id)
        # sales_order_update_date = SalesOrder.objects.get(id = id)
        product_list = ProductDetail.objects.filter(sales_order__id=id)
        # documents = SalesOrderDocuments.objects.filter(sales_order__id = id)

        if request.method == 'POST':
            #   doc = request.FILES #returns a dict-like object
            #   doc_name = doc['update_sales_order_file']
            delivery_method = request.POST['delivery_method']
            payment_term = request.POST['payment_term']
            order_status = request.POST['status']
            total_amount = request.POST['total_amount']
            product_name = request.POST.getlist('product_name')
            #   product_length = request.POST.getlist('product_length')
            weight_calculation = request.POST.getlist('weight_calculation')
            quantity = request.POST.getlist('quantity')
            auto_logistic = request.POST.getlist('auto_logistic')
            order_comment = request.POST.getlist('order_comment')
            bundle_number = request.POST.getlist('bundle_number')
            cost_of_product = request.POST.getlist('product_cost')
            manufacturer_approval = request.POST.getlist('manufacturer_approval')

            fs = FileSystemStorage()

            if 'update_sales_order_file' in request.FILES:
                sales_order_file = request.FILES['update_sales_order_file']
                sales_order_file = fs.save(sales_order_file.name, sales_order_file)
                sales_order_update.sales_order_file = sales_order_file
                sales_order_update.save()

            if 'update_delivery_challan' in request.FILES:
                delivery_challan = request.FILES['update_delivery_challan']
                delivery_challan = fs.save(delivery_challan.name, delivery_challan)
                sales_order_update.delivery_challan = delivery_challan
                sales_order_update.save()

            if 'packing_list' in request.FILES:
                packing_list = request.FILES['packing_list']
                packing_list = fs.save(packing_list.name, packing_list)
                sales_order_update.packing_list = packing_list
                sales_order_update.save()

            if 'ev_list' in request.FILES:
                ev_list = request.FILES['ev_list']
                ev_list = fs.save(ev_list.name, ev_list)
                sales_order_update.ev_list = ev_list
                sales_order_update.save()

            sales_order_update.delivery_method = delivery_method
            sales_order_update.payment_term = payment_term
            sales_order_update.total_amount = total_amount

            sales_order_update.order_status = order_status
            sales_order_update.save()

            num = 0
            product_details = []
            inventory_detail = []

            for obj in product_list:
                stock = Inventory.objects.get(id=obj.inventory)
                if stock.stock >= obj.quantity:
                    if order_status == 'Accepted':
                        stock.stock = stock.stock - obj.quantity
                        inventory_detail.append(stock)
                    obj.product_name = product_name[num]
                    # obj.length_of_product = product_length[num]
                    obj.weight_of_product = weight_calculation[num]

                    obj.quantity = quantity[num]
                    obj.auto_logistic_fillment = auto_logistic[num]
                    obj.bundle_number = bundle_number[num]
                    obj.cost_of_product = cost_of_product[num]
                    obj.order_comment = order_comment[num]
                    obj.manufacturer_order_approval = manufacturer_approval[num]
                    print(obj.manufacturer_order_approval)
                    product_details.append(obj)
                    num = num + 1

                else:
                    messages.error(request, f'{stock.item_name} is out of stock.')

            ProductDetail.objects.bulk_update(product_details)
            if order_status == 'Accepted':
                Inventory.objects.bulk_update(inventory_detail)

            try:
                if 'change_shipment_date' in request.POST:
                    change_shipment_date = request.POST['change_shipment_date']
                    sales_order_update.exp_shipment_date = change_shipment_date
                    sales_order_update.save()
            except:
                return redirect('/manufacturer-dashboard/')
            return redirect('/manufacturer-dashboard/')
        return render(request, 'manufacturer_sales_order_update.html',
                      {'display_manufacturing_unit': display_manufacturing_unit,
                       'sales_order_update': sales_order_update, 'product': product_list})
    except:
        return HttpResponse('Something went wrong By Our End.Please Try Again After Some Time.', status=500)


@login_required(login_url='manufacturer-login')
def manufacturer_search(request):
    try:
        # user=request.user
        # manufacturer_search_query = request.GET.get('search_query')
        # print(manufacturer_search_query)
        # search_result = SalesOrder.objects.filter(user__username__icontains = manufacturer_search_query, user = user).order_by('-id')
        # print(search_result)
        return render(request,
                      'manufacturer_search.html')  # 'search_result':search_result,'manufacturer_search_query':manufacturer_search_query
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')


@login_required(login_url='manufacturer-login')
def add_customer_unit(request):
    return render(request, 'add_customer_unit.html')


@login_required(login_url='manufacturer-login')
def create_customer_unit(request):
    try:
        if request.method == 'POST':
            # manufacturer Unit Name
            print(request.POST)
            user = request.user
            salutation = request.POST['salutation']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            contact_person = request.POST['contact_person']
            company_name = request.POST['company_name']
            # manufacturer = request.POST.get('manufacturer')
            # manufacturer_name = Manufacturer.objects.get(id = int(manufacturer))
            # print(manufacturer_name.user)

            # print('hello')
            # print(manufacturer_name)
            email = request.POST['email']
            phone_number = request.POST.get('phone_number')
            website = request.POST['website']
            pan_number = request.POST['pan_number']
            currency = request.POST['currency']
            m_payment_term = request.POST['m_payment_term']
            # billing address
            attention = request.POST['attention']
            country = request.POST['country']
            address = request.POST['address']
            city = request.POST['city']
            state = request.POST['state']
            zip_code = request.POST['zip_code']
            billing_phone_number = request.POST['billing_phone_number']
            fax = request.POST['fax']
            # Shipping Address
            shipping_attention = request.POST['s_attention']
            shipping_country = request.POST['s_country']
            shipping_address = request.POST['s_address']
            shipping_city = request.POST['s_city']
            shipping_state = request.POST['s_state']
            shipping_zip_code = request.POST['s_zip_code']
            shipping_phone_number = request.POST['s_phone_number']
            shipping_fax = request.POST['s_fax']

            billing_address = BillingAddress(user=user, attention=attention, country=country, address=address,
                                             city=city, state=state, zip_code=zip_code,
                                             billing_phone_number=billing_phone_number, fax=fax)

            # manufacturers = ManufacturingUnit.objects.filter(manufacturer__user = manufacturer)
            shipping_address = ShippingAddress(user=user, shipping_attention=shipping_attention,
                                               shipping_country=shipping_country, shipping_address=shipping_address,
                                               shipping_city=shipping_city, shipping_state=shipping_state,
                                               shipping_zip_code=shipping_zip_code,
                                               shipping_phone_number=shipping_phone_number, shipping_fax=shipping_fax)
            customer_unit = CustomerUnit(user=user, salutation=salutation, first_name=first_name, last_name=last_name,
                                         contact_person=contact_person, company_name=company_name, email=email,
                                         phone_number=phone_number, website=website, pan_number=pan_number,
                                         currency=currency, m_payment_term=m_payment_term,
                                         billing_address=billing_address, shipping_address=shipping_address)
            billing_address.save()
            shipping_address.save()
            customer_unit.save()
            return redirect('/customer-unit-dashboard/')
        return render(request, 'create_customer_unit.html')
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')


@login_required(login_url='manufacturer-login')
def update_customer_unit(request, id):
    try:
        update_customer_unit = CustomerUnit.objects.get(id=id)
        update_billing_address = BillingAddress.objects.get(id=id)
        update_shipping_address = ShippingAddress.objects.get(id=id)
        if request.method == 'POST':
            print(request.POST)
            salutation = request.POST['salutation']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            contact_person = request.POST['contact_person']
            company_name = request.POST['company_name']
            # manufacturer = request.POST.get('manufacturer')
            # manufacturer_name = Manufacturer.objects.get(id = int(manufacturer))
            # print(manufacturer_name.user)

            # print('hello')
            # print(manufacturer_name)
            email = request.POST['email']
            phone_number = request.POST.get('phone_number')
            website = request.POST['website']
            pan_number = request.POST['pan_number']
            currency = request.POST['currency']
            m_payment_term = request.POST['m_payment_term']
            # billing address
            attention = request.POST['attention']
            country = request.POST['country']
            address = request.POST['address']
            city = request.POST['city']
            state = request.POST['state']
            zip_code = request.POST['zip_code']
            billing_phone_number = request.POST['billing_phone_number']
            fax = request.POST['fax']
            # Shipping Address
            shipping_attention = request.POST['s_attention']
            shipping_country = request.POST['s_country']
            shipping_address = request.POST['s_address']
            shipping_city = request.POST['s_city']
            shipping_state = request.POST['s_state']
            shipping_zip_code = request.POST['s_zip_code']
            shipping_phone_number = request.POST['s_phone_number']
            shipping_fax = request.POST['s_fax']
            # for customer unit update
            update_customer_unit.salutation = salutation
            update_customer_unit.first_name = first_name
            update_customer_unit.last_name = last_name
            update_customer_unit.contact_person = contact_person
            update_customer_unit.company_name = company_name
            update_customer_unit.email = email
            update_customer_unit.phone_number = phone_number
            update_customer_unit.website = website
            update_customer_unit.pan_number = pan_number
            update_customer_unit.currency = currency
            update_customer_unit.m_payment_term = m_payment_term
            # for billing address update
            update_billing_address.attention = attention
            update_billing_address.country = country
            update_billing_address.address = address
            update_billing_address.city = city
            update_billing_address.state = state
            update_billing_address.zip_code = zip_code
            update_billing_address.billing_phone_number = billing_phone_number
            update_billing_address.fax = fax
            # for shipping address update
            update_shipping_address.shipping_attention = shipping_attention
            update_shipping_address.shipping_country = shipping_country
            update_shipping_address.shipping_address = shipping_address
            update_shipping_address.shipping_city = shipping_city
            update_shipping_address.shipping_state = shipping_state
            update_shipping_address.shipping_zip_code = shipping_zip_code
            update_shipping_address.shipping_phone_number = shipping_phone_number
            update_shipping_address.shipping_fax = shipping_fax

            update_customer_unit.save()
            update_billing_address.save()
            update_shipping_address.save()
            return redirect('/customer-unit-dashboard/')
        return render(request, 'update_customer_unit.html',
                      {'update_customer_unit': update_customer_unit, 'update_billing_address': update_billing_address,
                       'update_shipping_address': update_shipping_address})
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')


@login_required(login_url='manufacturer-login')
def customer_unit_dashboard(request):
    try:
        customer_unit_data = CustomerUnit.objects.all()
        return render(request, 'customer_unit_dashboard.html', {'customer_unit_data': customer_unit_data})
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')


@login_required(login_url='manufacturer-login')
def manufacturer_sales_order_view(request, id):
    try:
        user = request.user
        display_manufacturing_unit = ManufacturingUnit.objects.filter(user=user)
        sales_order_update = SalesOrder.objects.get(id=id)
        product_list = ProductDetail.objects.filter(sales_order__id=id)
        return render(request, 'manufacturer_sales_order_view.html',
                      {'display_manufacturing_unit': display_manufacturing_unit,
                       'sales_order_update': sales_order_update, 'product': product_list})
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')


@login_required(login_url='manufacturer-login')
def vendor_unit_dashboard(request):
    try:
        vendor_unit_data = VendorUnit.objects.all()
        return render(request, 'vendor_unit_dashboard.html', {'vendor_unit_data': vendor_unit_data})
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')


@login_required(login_url='manufacturer-login')
def update_vendor_unit(request, id):
    try:
        update_vendor_unit = VendorUnit.objects.get(id=id)
        update_vendor_unit_address = VendorUnitAddress.objects.get(id=id)
        list_vendor = Vendor.objects.all()
        if request.method == 'POST':
            print(request.POST)
            salutation = request.POST['salutation']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            contact_person = request.POST['contact_person']
            company_name = request.POST['company_name']
            vendor = request.POST.get('vendor')
            vendor_name = Vendor.objects.get(id=vendor)
            print(vendor_name.user)

            # print('hello')
            # print(manufacturer_name)
            email = request.POST['email']
            phone_number = request.POST.get('phone_number')
            website = request.POST['website']
            pan_number = request.POST['pan_number']
            currency = request.POST['currency']
            payment_term = request.POST['payment_term']
            # billing address
            attention = request.POST['attention']
            country = request.POST['country']
            address = request.POST['address']
            city = request.POST['city']
            state = request.POST['state']
            zip_code = request.POST['zip_code']
            vendor_phone_number = request.POST['vendor_phone_number']
            fax = request.POST['fax']
            # for vendor unit update
            update_vendor_unit.salutation = salutation
            update_vendor_unit.first_name = first_name
            update_vendor_unit.last_name = last_name
            update_vendor_unit.contact_person = contact_person
            update_vendor_unit.company_name = company_name
            update_vendor_unit.email = email
            update_vendor_unit.phone_number = phone_number
            update_vendor_unit.website = website
            update_vendor_unit.pan_number = pan_number
            update_vendor_unit.currency = currency
            update_vendor_unit.payment_term = payment_term
            update_vendor_unit.vendor = vendor_name
            # for vendor unit address update
            update_vendor_unit_address.vendor_attention = attention
            update_vendor_unit_address.vendor_country = country
            update_vendor_unit_address.vendor_address = address
            update_vendor_unit_address.vendor_city = city
            update_vendor_unit_address.vendor_state = state
            update_vendor_unit_address.vendor_zip_code = zip_code
            update_vendor_unit_address.vendor_phone_number = vendor_phone_number
            update_vendor_unit_address.vendor_fax = fax

            update_vendor_unit.save()
            update_vendor_unit_address.save()
            return redirect('/vendor-unit-dashboard/')
        return render(request, 'update_vendor_unit.html', {'update_vendor_unit': update_vendor_unit,
                                                           'update_vendor_unit_address': update_vendor_unit_address,
                                                           'list_vendor': list_vendor})
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')


@login_required(login_url='manufacturer-login')
def add_purchase_order(request):
    return render(request, 'add_purchase_order.html')


@login_required(login_url='manufacturer-login')
def create_purchase_order(request):
    try:
        user = request.user
        display_vendor_unit = ManufacturingUnit.objects.filter(user=user)
        if request.method == 'POST':
            user = request.user
            print(request.POST)
            unit_type = request.POST['distributor']
            vendor_unit = request.POST.get('vendor_unit_name')
            vendor_unit_name = ManufacturingUnit.objects.get(company_name=vendor_unit, user=request.user)
            print(vendor_unit_name.company_name)
            # purchase_order_number = request.POST['purchase_order_number']
            customer_phone_number = request.POST['customer_phone_number']
            purchase_order_date = request.POST['purchase_order_date']
            exp_shipment_date = request.POST['expected_shipment_date']
            payment_term = request.POST.get('paymentterm')

            delivery_method = request.POST['delivery_method']
            customer_sales_person = request.POST['customer_sales_person']

            # Product Detail
            product_name = request.POST.getlist('product_name')
            print(product_name)
            weight_calculation = request.POST.getlist('weight_calculation')
            print(weight_calculation)
            quantity = request.POST.getlist('quantity')
            print(quantity, "quantity")
            bundle_number = request.POST.getlist('bundle_number')
            price = request.POST.getlist('price')
            gst = request.POST.getlist('gst')
            total_cost = request.POST.getlist('product_cost')
            auto_logistic = request.POST.getlist('auto_logistic')
            terms_and_conditions = request.POST['terms_and_conditions']
            total_amount = request.POST['total_amount']

            order = PurchaseOrder(user=user, unit_type=unit_type, manufacturing_unit=vendor_unit_name,
                                  purchase_order_date=purchase_order_date, exp_shipment_date=exp_shipment_date,
                                  customer_phone_number=customer_phone_number, payment_term=payment_term,
                                  delivery_method=delivery_method, customer_sales_person=customer_sales_person,
                                  terms_and_conditions=terms_and_conditions, total_amount=total_amount)
            order.save()

            for i in range(len(product_name)):
                prod = TempInventory.objects.get(id= product_name[i])
                obj = PurchaseOrderProductDetail.objects.create(product_name=prod.item_name, purchase_order=order)
                print(obj)
                obj.weight_of_product = weight_calculation[i]
                obj.quantity = quantity[i]
                obj.auto_logistic_fillment = auto_logistic[i]
                obj.bundle_number = bundle_number[i]
                obj.cost_of_product = price[i]
                obj.gst = gst[i]
                obj.total_cost = total_cost[i]

                obj.save()

            return redirect('/purchase-order-dashboard/')
        return render(request, 'create_purchase_order.html', {'display_vendor_unit': display_vendor_unit})
    except Exception as e:  # work on python 2.x
        return HttpResponse('Failed to upload to ftp: ' + str(e))


@login_required(login_url='manufacturer-login')
def load_purchase_order_product(request):
    vendor_unit = request.GET.get('vendor_unit_name')
    print(vendor_unit)
    product = TempInventory.objects.filter(manufacturing_unit__company_name=vendor_unit, user = request.user)
    return render(request, 'load_purchase_order_product.html', {'product': product})

@login_required(login_url='manufacturer-login')
def purchase_order_dash(request):
    user = request.user
    purchase_order = PurchaseOrder.objects.filter(user=user)
    return render(request,'purchase_order_dash.html',{'purchase_order': purchase_order})




@login_required(login_url='manufacturer-login')
def update_purchase_order(request, id):
    # try:
    user = request.user
    display_manufacturer_unit = ManufacturingUnit.objects.filter(user=user)
    purchase_order_update = PurchaseOrder.objects.get(id=id)
    product_list = PurchaseOrderProductDetail.objects.filter(purchase_order__id=id)
    print(sales_order_update)
    if request.method == 'POST':
        print(request.POST)
        # vendor_unit = request.POST['manufacturer_unit']
        # #   print(manufacturing_unit)
        # vendor_unit_name = ManufacturingUnit.objects.get(company_name = vendor_unit)
        payment_term = request.POST.get('paymentterm')
        delivery_method = request.POST['delivery_method']
        customer_sales_person = request.POST['customer_sales_person']
        customer_phone_number = request.POST['customer_phone_number']
        product_name = request.POST.getlist('product_name')

        print(len(product_name))
        #   product_length = request.POST.getlist('product_length')
        weight_calculation = request.POST.getlist('weight_calculation')
        bundle_number = request.POST.getlist('bundle_number')
        cost_of_product = request.POST.getlist('product_cost')
        gst = request.POST.getlist('gst')
        total_cost = request.POST.getlist('total_cost')
        customer_approval = request.POST.getlist('customer_approval')
        quantity = request.POST.getlist('quantity')
        auto_logistic = request.POST.getlist('auto_logistic')
        order_comment = request.POST.getlist('order_comment')
        order_status = request.POST['status']
        terms_and_conditions = request.POST['terms_and_conditions']
        total_amount = request.POST['total_amount']
        # For uplaod Files
        fs = FileSystemStorage()
        if 'purchase_order_file' in request.FILES:
            purchase_order_file = request.FILES['purchase_order_file']
            purchase_order_file = fs.save(purchase_order_file.name, purchase_order_file)
            purchase_order_update.purchase_order_file = purchase_order_file
            purchase_order_update.save()

        if 'update_delivery_challan' in request.FILES:
            delivery_challan = request.FILES['update_delivery_challan']
            delivery_challan = fs.save(delivery_challan.name, delivery_challan)
            purchase_order_update.delivery_challan = delivery_challan
            purchase_order_update.save()

        if 'packing_list' in request.FILES:
            packing_list = request.FILES['packing_list']
            packing_list = fs.save(packing_list.name, packing_list)
            purchase_order_update.packing_list = packing_list
            purchase_order_update.save()

        if 'ev_list' in request.FILES:
            ev_list = request.FILES['ev_list']
            ev_list = fs.save(ev_list.name, ev_list)
            purchase_order_update.ev_list = ev_list
            purchase_order_update.save()

        # purchase_order_update.vendor_unit = vendor_unit_name

        purchase_order_update.payment_term = payment_term
        purchase_order_update.delivery_method = delivery_method
        purchase_order_update.customer_sales_person = customer_sales_person
        purchase_order_update.customer_phone_number = customer_phone_number
        purchase_order_update.terms_and_conditions = terms_and_conditions
        purchase_order_update.total_amount = total_amount
        purchase_order_update.order_status = order_status

        purchase_order_update.save()
        print(product_name)

        num = 0
        for obj in product_list:
            print('check')
            print(obj)
            obj.product_name = product_name[num]
            print(product_name[num])
            # obj.length_of_product = product_length[num]
            obj.weight_of_product = weight_calculation[num]
            obj.quantity = quantity[num]
            obj.auto_logistic_fillment = auto_logistic[num]
            obj.bundle_number = bundle_number[num]
            obj.cost_of_product = cost_of_product[num]
            obj.gst = gst[num]
            obj.total_cost = total_cost[num]
            obj.customer_order_approval = customer_approval[num]
            obj.order_comment = order_comment[num]
            # print(obj.customer_order_approval)
            obj.save()
            num = num + 1
            #   print(f" {product_name} product name")
            return redirect('/purchase-order-dashboard/')

    return render(request, 'update_purchase_order.html', {'display_manufacturer_unit': display_manufacturer_unit,
                                                          'purchase_order_update': purchase_order_update,
                                                          'product_list': product_list})


# except:
#     return HttpResponse('Something Went Wrong. Try Again After Some Time.')

# @login_required(login_url='manufacturer-login')
# def view_purchase_order(request, id):
#     try:
#         purchase_order_update = PurchaseOrder.objects.get(id=id)
#         product_list = PurchaseOrderProductDetail.objects.filter(purchase_order__id=id)
#         return render(request, 'view_purchase_order.html',
#                       {'purchase_order_update': purchase_order_update, 'product_list': product_list})

#     except Exception as e:
#         exc_type, exc_obj, exc_tb = sys.exc_info()
#         print(exc_tb.tb_lineno, e)

def vie_purchase_order(request, id):
        purchase_order_update = PurchaseOrder.objects.get(id=id)
        product_list = PurchaseOrderProductDetail.objects.filter(purchase_order__id=id)
        return render(request, 'view_purchase_order.html',
                      {'purchase_order_update': purchase_order_update, 'product_list': product_list})



# @login_required(login_url='manufacturer-login')
# def purchase_order_dashboard(request):
#     try:
#         user = request.user
#         purchase_order = PurchaseOrder.objects.filter(user=user)
#         return render(request, 'purchase_order_dashboard.html', {'purchase_order': purchase_order})
#     except Exception as e:
#         exc_type, exc_obj, exc_tb = sys.exc_info()
#         print(exc_tb.tb_lineno, e)


@login_required(login_url='manufacturer-login')
def add_vendor_unit(request):
    return render(request, 'add_vendor_unit.html')


@login_required(login_url='manufacturer-login')
def create_vendor_unit(request):
    try:
        list_vendor = Vendor.objects.all()

        if request.method == 'POST':
            # Vendor Unit Name
            print(request.POST)
            user = request.user
            salutation = request.POST['salutation']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            contact_person = request.POST['contact_person']
            company_name = request.POST['company_name']
            vendor = request.POST.get('vendor')
            vendor_name = Vendor.objects.get(id=vendor)
            print(vendor_name.user)

            # print('hello')
            email = request.POST['email']
            phone_number = request.POST.get('phone_number')
            website = request.POST['website']
            pan_number = request.POST['pan_number']
            currency = request.POST['currency']
            payment_term = request.POST['m_payment_term']
            # Vendor Unit address
            attention = request.POST['attention']
            country = request.POST['country']
            address = request.POST['address']
            city = request.POST['city']
            state = request.POST['state']
            zip_code = request.POST['zip_code']
            vendor_phone_number = request.POST['vendor_phone_number']
            fax = request.POST['fax']

            vendor_address = VendorUnitAddress(user=user, vendor_attention=attention, vendor_country=country,
                                               vendor_address=address, vendor_city=city, vendor_state=state,
                                               vendor_zip_code=zip_code, vendor_phone_number=vendor_phone_number,
                                               vendor_fax=fax)

            vendor_unit = VendorUnit(user=user, salutation=salutation, first_name=first_name, last_name=last_name,
                                     contact_person=contact_person, company_name=company_name, email=email,
                                     phone_number=phone_number, website=website, pan_number=pan_number,
                                     currency=currency, payment_term=payment_term, vendor_unit_address=vendor_address,
                                     vendor=vendor_name)
            vendor_address.save()
            vendor_unit.save()
            return redirect('/vendor-unit-dashboard/')
        return render(request, 'create_vendor_unit.html', {'list_vendor': list_vendor})
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')


# manufacturer order status functions
@login_required(login_url='manufacturer-login')
def order_status_accepted(request):
    try:
        user = request.user
        # sales_order = SalesOrder.objects.all()
        sales_order = PurchaseOrder.objects.filter(
            Q(manufacturing_unit__manufacturer__user=user) & Q(order_status='Accepted')).order_by('-id')
        # dividing data into pages
        paginator = Paginator(sales_order, 10, orphans=3)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)
        return render(request, 'order_status_accept.html', {'order': page_object, 'sales_order': sales_order})
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')


@login_required(login_url='manufacturer-login')
def order_status_in_production(request):
    try:
        user = request.user
        # sales_order = SalesOrder.objects.all()
        sales_order = PurchaseOrder.objects.filter(
            Q(manufacturing_unit__manufacturer__user=user) & Q(order_status='In Production')).order_by('-id')
        # dividing data into pages
        paginator = Paginator(sales_order, 10, orphans=3)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)
        return render(request, 'order_status_in_production.html', {'order': page_object, 'sales_order': sales_order})
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')


@login_required(login_url='manufacturer-login')
def order_status_packed(request):
    try:
        user = request.user
        # sales_order = SalesOrder.objects.all()
        sales_order = PurchaseOrder.objects.filter(
            Q(manufacturing_unit__manufacturer__user=user) & Q(order_status='Packed')).order_by('-id')
        # dividing data into pages
        paginator = Paginator(sales_order, 10, orphans=3)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)
        return render(request, 'order_status_packed.html', {'order': page_object, 'sales_order': sales_order})
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')


@login_required(login_url='manufacturer-login')
def order_status_shipped(request):
    try:
        user = request.user
        # sales_order = SalesOrder.objects.all()
        sales_order = PurchaseOrder.objects.filter(
            Q(manufacturing_unit__manufacturer__user=user) & Q(order_status='Shipped')).order_by('-id')
        # dividing data into pages
        paginator = Paginator(sales_order, 10, orphans=3)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)
        return render(request, 'order_status_shipped.html', {'order': page_object, 'sales_order': sales_order})
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')


@login_required(login_url='manufacturer-login')
def order_status_delivered(request):
    try:
        user = request.user
        # sales_order = SalesOrder.objects.all()
        sales_order = PurchaseOrder.objects.filter(
            Q(manufacturing_unit__manufacturer__user=user) & Q(order_status='Delivered')).order_by('-id')
        # dividing data into pages
        paginator = Paginator(sales_order, 10, orphans=3)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)
        return render(request, 'order_status_delivered.html', {'order': page_object, 'sales_order': sales_order})
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')


@login_required(login_url='manufacturer-login')
def order_status_cancel(request):
    try:
        user = request.user
        # sales_order = SalesOrder.objects.all()
        sales_order = PurchaseOrder.objects.filter(
            Q(manufacturing_unit__manufacturer__user=user) & Q(order_status='Cancel')).order_by('-id')
        # dividing data into pages
        paginator = Paginator(sales_order, 10, orphans=3)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)
        return render(request, 'order_status_cancel.html', {'order': page_object, 'sales_order': sales_order})
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')


@login_required(login_url='manufacturer-login')
def order_status_accepted_with_change(request):
    try:
        user = request.user
        # sales_order = SalesOrder.objects.all()
        sales_order = PurchaseOrder.objects.filter(
            Q(manufacturing_unit__manufacturer__user=user) & Q(order_status='Accepted with change')).order_by('-id')
        # dividing data into pages
        paginator = Paginator(sales_order, 10, orphans=3)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)
        return render(request, 'order_status_accepted_with_change.html',
                      {'order': page_object, 'sales_order': sales_order})
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')


# vendor

def vendor_registration(request):
    try:
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            company_name = request.POST['company_name']
            contact_number = request.POST['contact_number']
            user_name = request.POST['user_name']
            email_id = request.POST['email_id']
            country = request.POST['country']
            state = request.POST['state']
            region = request.POST['region']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            industry = request.POST['industry']

            if password != confirm_password:
                messages.error(request, 'Password are not same. Please enter valid Password')
                return redirect('/manufacturer-registration/')

            try:
                user = User.objects.get(username=user_name)
                messages.error(request, 'The username you entered has already been taken. Please try another username.')
                return redirect('/manufacturer-registration/')

            except User.DoesNotExist:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email_id,
                                                username=user_name, password=password)
                vendor = Vendor.objects.create(user=user, vendor_company=company_name,
                                               vendor_contact_number=contact_number, vendor_country=country,
                                               vendor_state=state, vendor_industry=industry, vendor_region=region)
                user.save()
                vendor.save()
                return redirect('/vendor-registration-redirect/')

        return render(request, 'vendor_registration.html')
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')


def vendor_login(request):
    try:
        if request.method == 'POST':
            username = request.POST['user_name']
            password = request.POST['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                if request.user.is_staff:
                    return redirect('/vendor-dashboard/')
                else:
                    messages.error(request, 'This is not a Vendor Account. Login with different Account.')
                    return redirect('/vendor-login/')
            else:
                messages.error(request, 'Invailid Credentials , Please Try Again !!!')
                return redirect('/vendor-login/')

        return render(request, 'vendor_login.html')
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')


def vendor_registration_redirect(request):
    return render(request, 'vendor_registration_redirect.html')


@login_required(login_url='vendor-login')
def vendor_detail(request):
    try:
        user = request.user
        vendor_detail = Vendor.objects.filter(user=user)  # display customer details
        print(vendor_detail)
        return render(request, 'vendor_detail.html', {'vendor_detail': vendor_detail})
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')


@login_required(login_url='vendor-login')
def vendor_dashboard(request):
    try:
        user = request.user
        purchase_order = PurchaseOrder.objects.filter(vendor_unit__vendor__user=user)
        print(purchase_order)
        paginator = Paginator(purchase_order, 10, orphans=3)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)
        return render(request, 'vendor_dashboard.html', {'purchase_order': page_object})
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')


@login_required(login_url='vendor-login')
def vendor_purchase_order_update(request, id):
    try:
        # user = request.user
        # display_manufacturing_unit = ManufacturingUnit.objects.filter(user = user)
        purchase_order_update = PurchaseOrder.objects.get(id=id)
        product_list = PurchaseOrderProductDetail.objects.filter(purchase_order__id=id)
        print(request.POST)

        if request.method == 'POST':
            #   doc = request.FILES #returns a dict-like object
            #   doc_name = doc['update_sales_order_file']
            #   change_shipment_date = request.POST['change_shipment_date']
            delivery_method = request.POST['delivery_method']
            payment_term = request.POST['payment_term']
            order_status = request.POST['status']
            total_amount = request.POST['total_amount']
            product_name = request.POST.getlist('product_name')
            #   product_length = request.POST.getlist('product_length')
            weight_calculation = request.POST.getlist('weight_calculation')
            quantity = request.POST.getlist('quantity')
            auto_logistic = request.POST.getlist('auto_logistic')
            order_comment = request.POST.getlist('order_comment')
            bundle_number = request.POST.getlist('bundle_number')
            cost_of_product = request.POST.getlist('product_cost')
            vendor_approval = request.POST.getlist('vendor_approval')
            print(auto_logistic)

            fs = FileSystemStorage()
            if 'purchase_order_file' in request.FILES:
                purchase_order_file = request.FILES['purchase_order_file']
                purchase_order_file = fs.save(purchase_order_file.name, purchase_order_file)
                purchase_order_update.purchase_order_file = purchase_order_file
                purchase_order_update.save()

            if 'update_delivery_challan' in request.FILES:
                delivery_challan = request.FILES['update_delivery_challan']
                delivery_challan = fs.save(delivery_challan.name, delivery_challan)
                purchase_order_update.delivery_challan = delivery_challan
                purchase_order_update.save()

            if 'packing_list' in request.FILES:
                packing_list = request.FILES['packing_list']
                packing_list = fs.save(packing_list.name, packing_list)
                purchase_order_update.packing_list = packing_list
                purchase_order_update.save()

            if 'ev_list' in request.FILES:
                ev_list = request.FILES['ev_list']
                ev_list = fs.save(ev_list.name, ev_list)
                purchase_order_update.ev_list = ev_list
                purchase_order_update.save()

            #   purchase_order_update.exp_shipment_date = change_shipment_date
            purchase_order_update.delivery_method = delivery_method
            purchase_order_update.payment_term = payment_term
            purchase_order_update.total_amount = total_amount
            purchase_order_update.order_status = order_status
            #   sales_order_update.sales_order_file = sales_order_file
            #   sales_order_update.delivery_challan = delivery_challan

            print(order_status)
            purchase_order_update.save()

            num = 0
            for obj in product_list:
                obj.product_name = product_name[num]
                # obj.length_of_product = product_length[num]
                obj.weight_of_product = weight_calculation[num]
                obj.quantity = quantity[num]
                obj.auto_logistic_fillment = auto_logistic[num]
                obj.bundle_number = bundle_number[num]
                obj.cost_of_product = cost_of_product[num]
                obj.order_comment = order_comment[num]
                obj.vendor_order_approval = vendor_approval[num]
                obj.save()
                num = num + 1

            try:
                if 'change_shipment_date' in request.POST:
                    change_shipment_date = request.POST['change_shipment_date']
                    purchase_order_update.exp_shipment_date = change_shipment_date
                    purchase_order_update.save()
            except:
                return redirect('/vendor-dashboard/')

            return redirect('/vendor-dashboard/')

        return render(request, 'vendor_purchase_order_update.html',
                      {'purchase_order_update': purchase_order_update, 'product_list': product_list})
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')


@login_required(login_url='vendor-login')
def vendor_purchase_order_view(request, id):
    try:
        purchase_order_update = PurchaseOrder.objects.get(id=id)
        product_list = PurchaseOrderProductDetail.objects.filter(purchase_order__id=id)
        return render(request, 'vendor_purchase_order_view.html',
                      {'purchase_order_update': purchase_order_update, 'product_list': product_list})
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')


# vendor order status

@login_required(login_url='vendor-login')
def vendor_order_status_accepted(request):
    try:
        user = request.user
        # sales_order = SalesOrder.objects.all()
        purchase_order = PurchaseOrder.objects.filter(
            Q(vendor_unit__vendor__user=user) & Q(order_status='Accepted')).order_by('-id')
        return render(request, 'vendor_order_status_accept.html', {'purchase_order': purchase_order})
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')


@login_required(login_url='vendor-login')
def vendor_order_status_accepted_with_change(request):
    try:
        user = request.user
        # sales_order = SalesOrder.objects.all()
        purchase_order = PurchaseOrder.objects.filter(
            Q(vendor_unit__vendor__user=user) & Q(order_status='Accepted with change')).order_by('-id')
        return render(request, 'vendor_order_status_accepted_with_change.html', {'purchase_order': purchase_order})
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')


@login_required(login_url='vendor-login')
def vendor_order_status_in_production(request):
    try:
        user = request.user
        # sales_order = SalesOrder.objects.all()
        purchase_order = PurchaseOrder.objects.filter(
            Q(vendor_unit__vendor__user=user) & Q(order_status='In Production')).order_by('-id')
        return render(request, 'vendor_order_status_in_production.html', {'purchase_order': purchase_order})
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')


@login_required(login_url='vendor-login')
def vendor_order_status_packed(request):
    try:
        user = request.user
        # sales_order = SalesOrder.objects.all()
        purchase_order = PurchaseOrder.objects.filter(
            Q(vendor_unit__vendor__user=user) & Q(order_status='Packed')).order_by('-id')

        return render(request, 'vendor_order_status_packed.html', {'purchase_order': purchase_order})
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')


@login_required(login_url='vendor-login')
def vendor_order_status_shipped(request):
    try:
        user = request.user
        # sales_order = SalesOrder.objects.all()
        purchase_order = PurchaseOrder.objects.filter(
            Q(vendor_unit__vendor__user=user) & Q(order_status='Shipped')).order_by('-id')

        return render(request, 'vendor_order_status_shipped.html', {'purchase_order': purchase_order})
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')


@login_required(login_url='vendor-login')
def vendor_order_status_delivered(request):
    try:
        user = request.user
        # sales_order = SalesOrder.objects.all()
        purchase_order = PurchaseOrder.objects.filter(
            Q(vendor_unit__vendor__user=user) & Q(order_status='Delivered')).order_by('-id')

        return render(request, 'vendor_order_status_delivered.html', {'purchase_order': purchase_order})
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')


@login_required(login_url='vendor-login')
def vendor_order_status_cancel(request):
    try:
        user = request.user
        # sales_order = SalesOrder.objects.all()
        purchase_order = PurchaseOrder.objects.filter(
            Q(vendor_unit__vendor__user=user) & Q(order_status='Cancel')).order_by('-id')

        return render(request, 'vendor_order_status_cancel.html', {'purchase_order': purchase_order})
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')


@login_required(login_url='vendor-login')
def vendor_search(request):
    try:
        user = request.user
        # vendor_search_query = request.GET.get('search_query')
        # search_result = PurchaseOrder.objects.filter(Q(user__username__icontains = vendor_search_query)).order_by('-id')
        return render(request,
                      'vendor_search.html')  # ,{'vendor_search_query': vendor_search_query, 'search_result':search_result}
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')


import csv
from django.http import HttpResponse


def download_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="QuotationProduct.csv"'

    writer = csv.writer(response)
    writer.writerow(['Quotation', 'Product'])
    my_data = QuotationProduct.objects.filter(user=request.user)
    print(my_data)
    for data in my_data:
        print('data', data)
        writer.writerow([data.quotation.assigning, data.tempproduct.item_name])

    return response


# Creating a class based view for pdf convertor
def pdf_converter(self, id):
    print("hello")
    data = SalesOrder.objects.filter(id=id)
    product_list = ProductDetail.objects.filter(sales_order__id=id)

    print(data)
    open('templates/temp.html', "w").write(
        render_to_string('result.html', {'data': data, 'product_list': product_list}))

    # Converting the HTML template into a PDF file
    pdf = render_to_pdf('temp.html')

    # rendering the template
    return HttpResponse(pdf, content_type='application/pdf')


# Creating a class based view for pdf convertor
def purchase_order_pdf_converter(self, id):
    print("hello")
    data = PurchaseOrder.objects.filter(id=id)
    product_list = PurchaseOrderProductDetail.objects.filter(purchase_order__id=id)

    print(data)
    open('templates/temp.html', "w").write(
        render_to_string('purchase_order_pdf_result.html', {'data': data, 'product_list': product_list}))

    # Converting the HTML template into a PDF file
    pdf = render_to_pdf('temp.html')

    # rendering the template
    return HttpResponse(pdf, content_type='application/pdf')


# logout function

def logout_user(request):
    try:
        logout(request)
        return redirect('/')
    except:
        return HttpResponse('Something Went Wrong. Try Again After Some Time.')
