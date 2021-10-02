from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User, Account_Profile
from random import randint


class LandingPage(View):
    def get(self, request):
        template_name = "users/landingpage.html"
        
        return render(request, template_name, context={})
        



class LoginView(View):
    def get(self, request):
        template_name = "users/login.html"
        if request.user.is_authenticated:
            return redirect("users:landing")
        return render(request, template_name, context={})
        

    def post(self, request):
        username = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            print('user exists')

            if user.is_active:
                print('user is active')

                login(request, user)
                print('logged in')
                return redirect("users:landing")
                
            else:
                messages.error(request, "Your account has been disabled.")
                return redirect("users:login")
        else:
            messages.error(request, "Invalid login credentials.")
            return redirect("users:login")
        



class CreateUser(View):
    def get(self, request):
        template_name = "users/createuser.html"
        if request.user.is_authenticated:
            return redirect("users:dashboard")
        return render(request, template_name, context={})


    def post(self, request):
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

        # account_number = request.POST["account_number"] this should be automatically generated
        account_type = request.POST["account_type"]
        country = request.POST["country"]
        state = request.POST["state"]
        address = request.POST["address"]
        phone_number = request.POST["phone_number"]
        # sms = request.POST["sms"]
        # email = request.POST["email"]
        # internet_banking_id = request.POST["internet_banking_id"] this should be automatically generated
        password = request.POST["password"]
        account_balance = request.POST["account_balance"]
        account_number = randint(10000000000, 100000000000)
        internet_banking_id = randint(111111, 999999)

        if not User.objects.filter(email=email).exists():
            created_user = User.objects.create(
                first_name=first_name, last_name=last_name, email=email
            )
            created_user.set_password(password)
            created_user.save()
            print(created_user)
            Account_Profile.objects.create(user=created_user, account_number=account_number,
            account_type=account_type,
            country=country,
            # city=city,
            phone_number=phone_number,
            address=address,
            # sms=sms,
            # email=email,
            account_balance=account_balance,
            internet_banking_id=internet_banking_id,)
            messages.success(request, "Account Created successfully. login to approve account and start banking with us")
            return redirect("users:login")
        else:
            messages.error(request, "user with email already exist")
            return redirect("users:create_user")






def Logout(request):
    logout(request)
    return redirect("users:login")