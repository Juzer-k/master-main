from typing import Optional
from django.shortcuts import render, redirect, HttpResponse
from core_app.models import UserDetails, User, Token
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from inventory.utils import send_password_reset_email
from django.db.models import Q
import string
import random
from inventory.models import Inventory, Warehouse
from inventory.models import *
from django.core.paginator import Paginator
from django.contrib import messages









@method_decorator([login_required], name="dispatch")
class Home(View):
    template_name: str = "inventory_home.html"

    def get(self, request):
        user = request.user
        data = Warehouse.objects.filter(user = user)
        # warehouse = request.GET.get('warehouse_count')
        # print(warehouse)
        Warehouse_product_count = Inventory.objects.filter(warehouse__id = '1').count()
        print(Warehouse_product_count)
        # j = Inventory.objects.filter(warehouse__id='2').extra(select={'inventory':'price'})
        # select Warehouse__id, ware__name, count(Warehouse__id) as  count from Inventory groupby Warehouse__id
        # total = 0
        # for i in j:
        #     total += sum(i.price)
        # get_inventory_data = Inventory.objects.filter(warehouse__id = id)
        # print(get_inventory_data)
        # i = Inventory.objects.filter(user = user)
        # print(i)
        paginator = Paginator(data, 8)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)
        if user.is_superuser:
            userdetails: UserDetails = UserDetails.objects.all()
            total_item = Inventory.objects.all()
            total_item_count = total_item.count()
            total_price = 0
            total_stock = 0
            for i in total_item:
                total_price += int(i.price) * int(i.stock)
                total_stock += int(i.stock)  
        else:
            # userdetails: UserDetails = UserDetails.objects.get(user = user)
            total_item = Inventory.objects.filter(user = user)
            total_item_count = total_item.count()
            total_price = 0
            total_stock = 0
            for i in total_item:
                total_price += float(i.price) * float(i.stock)
                total_stock += float(i.stock)

            # data = Category.objects.filter(user = request.user)
            # paginator = Paginator(data, 4)
            # page_number = request.GET.get('page')
            # page_object = paginator.get_page(page_number)
        return render(request, self.template_name, locals())


def search_warehouse(request):
    user=request.user
    search_query = request.GET.get('search')
    print(search_query)
    #search_result = ManufacturingUnit.objects.filter(Q(display_name__icontains = customer_search_query), user = user)
    search_result = Category.objects.filter(Q(name__icontains = search_query) | Q(warehouse__name__icontains = search_query) | Q(warehouse__address__icontains = search_query), user = user)
    return render(request, 'search_warehouse.html', {'search_result':search_result, 'search_query':search_query})

@method_decorator([login_required], name="dispatch")
class ChangePassword(View):
    template_name: str = "change_user_password.html"

    def get(self, request):
        return render(request, self.template_name)
    def post(self, request):
        new_password =  request.POST.get("new_password")
        re_password = request.POST.get("re_password")
        if new_password == re_password:
            user = User.objects.get(username=request.user)
            user.set_password(new_password)
            user.save()
        else:
            message: str = "Password doesn't matched"
        return render(request, self.template_name)





class SendForgetPasswordEmail(View):
    template_name: str = "send_forget_password_email.html"
    def get(self, request):
        return render(request, self.template_name)
    def post(self, request):
        email = request.POST.get("user_email")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            N = 8
            token = ''.join(random.choices(string.ascii_uppercase +string.digits, k=N))
            Token.objects.create(user_id = user, token=token)
            token = Token.objects.get(token=token)
            send_password_reset_email(token.token)
            message: str = "Email Sent Check your email"
        else:
            message: str = "User not resgistered with this email"

        return render(request, self.template_name,locals())


class ResetForgetPassword(View):
    template_name: str = "forget_password.html"
    def get(self, request, token):
        return render(request, self.template_name, locals())
    def post(self, request, token):
        new_password = request.POST.get("new_password")
        user_detail = Token.objects.get(token=token)
        user = User.objects.get(username=user_detail.user_id)
        user.set_password(new_password)
        user.save()
        token = Token.objects.get(token = user_detail.token)
        token.delete()
        message: str = "Password Updated Successfully"
        return redirect("login")
