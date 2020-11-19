from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import User, Driver_pay, Size_coefficient, Time_coefficient, Weight_coefficient, Distance_coefficient, Order, Cargo_picture
from django.conf import settings
import requests
import json

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request, 'transport/index.html' , {"user": request.user})
    else:
        return render(request, 'transport/login.html')


# login function
def login_view(request):
    if request.method == "POST":
        username = request.POST['login_username']
        password = request.POST['login_password']
        print(username, password)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # login user

            login(request, user)
            return render(request, "transport/index.html")

        else:
            return render(request, "transport/login.html", {"message":"invalid login credentials"})

    else:
        return render(request, "transport/login.html", {"message": "login by clicking on the login button"})


# logout view function
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return render(request, "transport/login.html", {"message":"You have been logged out!"})
    else:
        return render(request, "transport/index.html", {"message": "You have to logout through the lougout button"})


# register view
def register_view(request):
    # check if user accessed the site via post and not by typing the url in the url bar
    if request.method == "POST":

        # collect variables
        username = request.POST['username']
        first = request.POST['first']
        last = request.POST['last']
        email = request.POST['email']
        password = request.POST['password']
        password_confirmation = request.POST['password_confirmation']

        # check if all term have been provided
        if username == '' or first == '' or last == '' or email == '':
            return render(request, 'transport/login.html', {"message": "Please provide all necessary fields"})

        # if the password and the password confirmation do not match
        if password != password_confirmation:
            return render(request, 'transport/login.html', {"message": "Passwords do not match!"})

        else:
            # try to create new user
            try:
                user = User.objects.create_user(username=username, first_name=first, last_name=last, email=email, password=password)
                user.save()

            # uf user already exists django will throw an IntegrityError
            except IntegrityError:
                return render(request, 'transport/login.html', {"message": "Username is taken"})

            # log the user in
            login(request, user)
            return HttpResponseRedirect(reverse('index'))

    # if the request wasn't made via post
    else:
        return render(request, "transport/login.html", {"message": "You have to register via the register form"})


# new order
def order(request):
    if request.method == "POST":
        pass

    else:
        return render(request, "transport/new_order.html" , {'key': settings.API_KEY})


# calculate path
def calculate_path(request):
    data = json.loads(request.body.decode("utf-8"))
    destination = data['destination']
    origin = data['origin']
    r = requests.get('https://maps.googleapis.com/maps/api/directions/json?key=' + settings.API_KEY + '&origin=' + origin + '&destination=' + destination)
    response = json.loads(r.text)
    return JsonResponse(response)


# price calculator
def calculate_price(request):
    # decode info from the request
    info = json.loads(request.body.decode("utf-8"))
    r = requests.get("http://api.eia.gov/series/?api_key=" + settings.GAS_API + "&series_id=TOTAL.MGUCUUS.M")
    text = json.loads(r.text)
    print(info)
    print(type(text))
    # extract variables
    try:
        price_per_gallon = text['series'][0]['data'][0][1]
        print(price_per_gallon)
        distance = int(info['distance'])
        duration = int(info['duration'])
        weight = abs(float(info['weight']))
        size = abs(float(info['size']))
        if weight == 0 or size == 0:
            return JsonResponse({"response": "Weight and size can not be 0"})
     # if not all the variables are provided
    except ValueError:
        return JsonResponse({"response": "Not all parameters were provided"})

    # get coefficients
    wc = Weight_coefficient.objects.get(name='regular_weight').coefficient
    sc = Size_coefficient.objects.get(name='regular_size').coefficient
    dc = Distance_coefficient.objects.get(name='regular_distance').coefficient
    tc = Time_coefficient.objects.get(name='regular_time').coefficient
    driver_pay = Driver_pay.objects.get(driver='Larry Gambino').pay

    print(driver_pay)
    print(price_per_gallon, distance, duration, weight, size)
    price = (weight * wc) + (size * sc) + (((distance/1609) * dc) * price_per_gallon) + ((duration/3600) * float(driver_pay) * tc)
    response = {'price': round(price, 2)}

    return JsonResponse(response)


# function that places the order and handles all possible wrong inputs
def place_order(request):

    if request.method == 'POST':
        # Getting order variables, try is used if to enforce variables on the server side
        try:
            print('fuuuuuuck')
            weight = request.POST['weight']
            size = request.POST['size']
            description = request.POST['description']
            date = request.POST['order_date']

            # if the user didn't select any radio option
            try:
                scope = request.POST['scopes']

            except KeyError:
                return render(request, 'transport/new_order.html', {'message': 'Not all parameters were provided'})
            origin = request.POST['origin_input_submit']
            destination = request.POST['destination_input_submit']
            distance = request.POST['distance']
            duration = request.POST['duration']
            price = request.POST['price']

        # if not all parameters were provided
        except ValueError:
            return render(request, 'transport/new_order.html', {'message': 'Not all parameters were provided'})

        pictures = request.FILES.getlist('order_pictures')
        print("pictures" ,pictures)
        if len(pictures) > 2:
            return JsonResponse({"response": "Only 2 Pictures are allowed"})
        # save new order to database
        try:
            order = Order(user=request.user, description=description, distance=distance, duration=duration, origin=origin, destination=destination, date=date, scope=scope, weight=weight, size=size, price=price)
            order.save()
        except ValueError:
            return render(request, 'transport/new_order.html', {'message': "Couldn't place order"})

        # add pictures
        pics = []
        # add pictures to the Job Pictures
        for picture in pictures:
            pic = Cargo_picture(cargo_picture=picture, user=request.user, order=order)
            pic.save()
            pics.append(pic)
        print(pics)

        return HttpResponseRedirect(reverse('order_placed', args=(order.id,)))

    else:
        return render(request, 'transport/new_order.html')


# display successfully placed order
def order_placed(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    images = Cargo_picture.objects.filter(order=order)
    return render(request, 'transport/order_placed.html', {"order": order, 'images': images})


def profile(request):
    return render(request, "transport/profile.html", {"user": request.user, "orders": Order.objects.filter(user=request.user).order_by('-time_order_was_placed')})


# order details
def order_details(request, order_id):
    context = {
    "user": request.user,
    "order": Order.objects.get(id=order_id),
    "images": Cargo_picture.objects.filter(user=request.user).filter(order=order_id)
    }
    return render(request, 'transport/order_details.html', context)



# display picture
def display_picture(request, picture):
    print(picture)
    return render(request, 'transport/picture.html', {'user': request.user, 'image': picture})

# display all pictures in an order
def order_pictures(request, order_id):
    pictures = Cargo_picture.objects.filter(order=order_id)
    print(pictures)
    return render(request, "transport/order_pictures.html", {"user": request.user, "images": pictures, "order_id": order_id})


def react(request):
    return render(request, "transport/react.html")


# contact logic...not the websocket part
def contact(request):
    return render(request, 'transport/contact.html')


# get user
def get_user(request):
    user = str(request.user)
    response = {'user': user}
    return JsonResponse(response)
