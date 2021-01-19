from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from .models import District, UserProfile, Shop, Category
import json, random

# Create your views here.

def get_districts(request):
    districts = District.objects.all()
    data = []
    if districts:
        for district in districts:
            data.append((district.id, district.name))
    return JsonResponse(data, safe=False)

def get_categories(request):
    categories = Category.objects.all()
    data = []
    if categories:
        for category in categories:
            data.append((category.id, category.name))
    return JsonResponse(data, safe=False)


def get_all_data_user(request, user_id):
    user = User.objects.get(id=user_id)
    user_profile = UserProfile.objects.get(user=user)
    data = {
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "patronymic": user_profile.patronymic,
        "phone_number": user_profile.phone_number,
        "districts": user_profile.districts,
        'email': user.email,
        'active': user.is_active,
        'group': user.groups.first().id
    }
    return JsonResponse(data, safe=False)


def submit_user(request):
    responseObject = {}
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    
    username = body["username"]
    firstName = body["first_name"]
    lastName = body["last_name"]
    patronymic = body["patronymic"]
    email = body["email"]
    phoneNumber = body["phone_number"]
    districts = body["districts"]
    group = body["group"]
    active = body["active"]

    # Generatiing password for user by his username
    password = generate_password(username)

    # Cheking user for username
    check_user = User.objects.filter(username=username)
    if check_user:
        responseObject["status"] = "USERNAME_EXISTS"
        responseObject["message"] = "Имя пользователя уже принадлежит другому"
        return JsonResponse(responseObject, safe=False)
    # Checking user for emaik
    check_user = User.objects.filter(email=email)
    if check_user:
        responseObject["status"] = "EMAIL_FOUND"
        responseObject["message"] = "Введённый Email существует!"
        return JsonResponse(responseObject, safe=False)
    # Checking user for phone number
    check_user = UserProfile.objects.filter(phone_number=phoneNumber)
    if check_user:
        responseObject["status"] = "PHONE_FOUND"
        responseObject["message"] = "Введённый телефонный номер уже существует"
        return JsonResponse(responseObject, safe=False)
    
    # Creating a base user
    groupModel = Group.objects.get(id=(int(group) + 1))

    user = User(username=username, email=email, first_name=firstName, last_name=lastName)
    user.set_password(password)
    user.is_staff = True

    if int(group) == 1:
        user.is_superuser = True
    else:
        user.is_superuser = False
    
    if active:
        user.is_active = True
    else:
        user.is_active = False
    user.save()
    groupModel.user_set.add(user)

    # After adding the user to a db, create reference to profile, containing patronymic, phone_number and districts
    profile = UserProfile(user=user)
    profile.patronymic = patronymic
    profile.phone_number = phoneNumber
    profile.password = password
    # Adding first districts to user profile
    profile.districts = {
        "districts": [i for i in districts]
    }
    profile.save()

    responseObject["status"] = "SUCCESS"
    responseObject["message"] = "Пользователь был создан"

    return JsonResponse(responseObject, safe=False)


def change_user(request, user_id):
    responseObject = {}
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    try:
        user = User.objects.get(id=user_id)
        
        username = body["username"]
        first_name = body["first_name"]
        last_name = body["last_name"]
        patronymic = body["patronymic"]
        email = body["email"]
        phone_number = body["phone_number"]
        districts = body["districts"]
        group = body["group"]
        active = body["active"]

        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.phone_number = phone_number

        if int(group) == 1:
            user.is_superuser = True
        else:
            user.is_superuser = False
        
        if active:
            user.is_active = True
        else:
            user.is_active = False
        user.save()
        
        groupModel = Group.objects.get(id=(int(group) + 1))
        groupModel.user_set.add(user)
        
        profile = UserProfile.objects.get(user=user)
        profile.patronymic = patronymic
        profile.phone_number = phone_number
        profile.districts = {
            "districts": [i for i in districts]
        }
        profile.save()

        responseObject["status"] = "SUCCESS"
        responseObject["message"] = "Пользователь был изменён"

        return JsonResponse(responseObject, safe=False)
    except:
        print("Server error")

def generate_password(key):
    number = random.randrange(0, 100000)
    return "%s%s" % (key, number)


def delete_user(request, user_id):
    responseObject = {}
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        responseObject["status"] = "SUCCESS"
        responseObject["message"] = "Пользователь был успешно удалён"
    except:
        print("Server error")
    
    return JsonResponse(responseObject, safe=False)

def add_shop(request):
    responseObject = {}
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    try:
        user = User.objects.get(id=request.user.id)
        name = body["name"]
        inn = body["inn"]
        phone_number = body["phone_number"]
        district = body["district"]
        address = body["address"]
        landmark = body["landmark"]
        category = body["category"]
        
        check_shop = Shop.objects.filter(inn=inn)
        if check_shop:
            responseObject["status"] = "INN_EXISTS"
            responseObject["message"] = "Введённый ИНН принадлежит другому магазину"
            return JsonResponse(responseObject, safe=False)
        
        check_shop = Shop.objects.filter(phone_number=phone_number)
        if check_shop:
            responseObject["status"] = "PHONE_EXISTS"
            responseObject["message"] = "Введённый номер телефона принадлежит другому магазину"
            return JsonResponse(responseObject, safe=False)

        shop = Shop(person=user, name=name, phone_number=phone_number, address=address, category=category, inn=inn, landmark=landmark, district=district)
        shop.save()
        
        responseObject["status"] = "SUCCESS"
        responseObject["message"] = "Магазин был создан"

        return JsonResponse(responseObject, safe=False)
    except:
        print("Server error")

def delete_shop(request, shop_id):
    responseObject = {}
    try:
        shop = Shop.objects.get(id=shop_id)
        shop.delete()
        responseObject["status"] = "SUCCESS"
        responseObject["message"] = "Магазин был успешно удалён"
    except:
        print("Server error")
    
    return JsonResponse(responseObject, safe=False)

def get_all_data_shop(request, shop_id):
    shop = Shop.objects.get(id=shop_id)
    data = {
        "name": shop.name,
        "inn": shop.inn,
        "phone_number": shop.phone_number,
        "district": shop.district,
        "address": shop.address,
        'landmark': shop.landmark,
        'category': shop.category,
    }
    return JsonResponse(data, safe=False)

def change_shop(request, shop_id):
    responseObject = {}
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    try:
        shop = Shop.objects.get(id=shop_id)
        if shop:
            name = body["name"]
            inn = body["inn"]
            phone_number = body["phone_number"]
            district = body["district"]
            address = body["address"]
            landmark = body["landmark"]
            category = body["category"]

            shop.name = name
            shop.inn = inn
            shop.phone_number = phone_number
            shop.address = address
            shop.landmark = landmark
            shop.category = category

            shop.save()
            responseObject["status"] = "SUCCESS"
            responseObject["message"] = "Магазин был успешно изменён"

            return JsonResponse(responseObject, safe=False)
    except:
        print("Server error")