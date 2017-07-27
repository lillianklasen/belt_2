from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Wish
import bcrypt

def flashErrors(request, errors):
    for error in errors:
        messages.error(request, error)

def currentUser(request):
    id = request.session['user_id']

    return User.objects.get(id=id)

def index(request):
    return render(request, 'belt_2/index.html')

def dashboard(request):
    if 'user_id' in request.session:
        current_user = currentUser(request)

        my_wishes = current_user.wishers.all()

        wishes = Wish.objects.all()

        context = {
            'current_user': current_user,
            'my_wishes': my_wishes,
            'wishes': wishes
        }
    return render(request, 'belt_2/dashboard.html', context)

def logout(request):
    if 'user_id' in request.session:
        request.session.pop('user_id')
        return redirect('/')

def login(request):
    if request.method == 'POST':
        errors = User.objects.validateLogin(request.POST)

        if not errors:
            user = User.objects.filter(username=request.POST['username']).first()

            if user:
                password = str(request.POST['password'])
                user_password = str(user.password)
                hashed_pw = bcrypt.hashpw(password, user_password)

                if hashed_pw == user.password:
                    request.session['user_id'] = user.id

                    return redirect('/dashboard')

            errors.append("Invalid password")

        flashErrors(request, errors)

    return redirect('/')


def register(request):
    if request.method == 'POST':
        errors = User.objects.validateRegistration(request.POST)

        if not errors:
            user = User.objects.createUser(request.POST)

            request.session['user_id'] = user.id

            return redirect('/dashboard')

        flashErrors(request, errors)

    return redirect('/')

def add(request):
    return render(request, 'belt_2/add.html')

def addItem(request):
    if request.method == 'POST':
        errors = Wish.objects.validateWish(request.POST)

        current_user = currentUser(request)

        if not errors:
            wish = Wish.objects.addWish(request.POST, current_user)

            request.session['wish_id'] = wish.id

            return redirect('/dashboard')

        else:
            flashErrors(request, errors)

    return redirect('/add')

def wishItems(request, id):
    current_user = currentUser(request)

    wish = Wish.objects.get(id=id)

    wishers = wish.wishers.all()

    context = {
        'current_user': current_user,
        'wish': wish,
        'wishers': wishers
    }

    return render(request, 'belt_2/wish_items.html', context)

def delete(request, id):
    wish = Wish.objects.get(id=id)
    wish.delete()
    return redirect('/dashboard')

def removeWish(request, id):
    if 'user_id' in request.session:
        current_user = currentUser(request)

        wish = Wish.objects.get(id=id)

        wish.wishers.remove(current_user)

    return redirect('/dashboard')

def addToMyWishes(request, id):
    current_user = currentUser(request)

    wish = Wish.objects.get(id=id)

    wish.wishers.add(current_user)

    return redirect('/dashboard')
