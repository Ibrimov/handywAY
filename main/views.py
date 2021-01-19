from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from .models import District, UserProfile
import json, random

# Create your views here.

def get_districts(request):
    districts = District.objects.all()
    data = []
    if districts:
        for district in districts:
            data.append((district.id, district.name))
    return JsonResponse(data, safe=False)


def get_all_data(request, user_id):
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
    customDistricts = body["custom_districts"]
    group = body["group"]
    active = body["active"]

    # Generatiing password for user by his username
    password = generate_password(username)

    profile_districts = []
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
    
    # Cheking if new districts were added and then adds if a paricular 
    # district does not exist in a database
    if len(customDistricts) > 0:
        if ',' in customDistricts:
            if (len(districts) + len(customDistricts.split(","))) > 5:
                responseObject["status"] = "TOO_MANY_VALUES"
                responseObject["message"] = "Пользователю можно присвоить только до 5 районов"
                return JsonResponse(responseObject, safe=False)

            values = customDistricts.split(',')
            for value in values:
                if len(value) > 0:
                    check_district = District.objects.filter(name=value)
                    if check_district:
                        continue
                    district = District(name=value)
                    district.save()
                    profile_districts.append(district.id)
    
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
    profile.districts["districts"] = profile.districts["districts"] + profile_districts
    profile.save()

    responseObject["status"] = "SUCCESS"
    responseObject["message"] = "Пользователь был создан"

    return JsonResponse(responseObject, safe=False)


def change_user(request, user_id):
    responseObject = {}
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        user = User.objects.filter(id=user_id)
        if user:
            pass

    except:
        responseObject["status"] = "SERVER_ERROR"
        responseObject["message"] = "Something went wrong. Please try again!"
        return responseObject

def generate_password(key):
    number = random.randrange(0, 100000)
    return "%s%s" % (key, number)