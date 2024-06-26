from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
# models
from mainapp.models import Login
from bookings.models import Bookinghotel
from payments.models import Paymentdetail
from django.contrib import messages

# Create your views here.

# signup page 
def signup(request):
    if request.method == 'POST':
        un = request.POST.get('name')
        email = request.POST.get('useremail')
        pw = request.POST.get('password')
        cpw = request.POST.get('cpassword')

        if pw != cpw:
            messages.error( request, 'password and confirm password must be same !')
            return render(request, 'signup.html')

        elif len(pw) < 8:
            messages.warning(request, 'password length must be of 8 digit !')
            return render(request, 'signup.html')

        else:
            if (
                Login.objects.filter(username=un).exists()
                | Login.objects.filter(email=email).exists()
            ):
                messages.warning(  request, 'username or email already exist select another !' )
                return render(request, 'signup.html')
            else:
                pw = make_password(pw)
                maindata = Login(username=un, email=email, password=pw)
                maindata.save()
                messages.success( request, 'you have registered succesfully, now you can login !' )
                url = '/login/'
                return HttpResponseRedirect(url)

    if request.method == 'GET':
        if request.session.get('user_id'):
            id = request.session['user_id']
            hl = 'all'
            url = '/hotellist/{}/{}'.format(hl, id)
            messages.info(
                request, 'you are already logged in so you cant access signup page, you need to log out for accessing this page !')
            return HttpResponseRedirect(url)
        else:
            messages.info(request, 'Here you can open your new account !')
            return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        un = request.POST.get('name')
        pw = request.POST.get('password')

        if un == '' or pw == '':
            messages.error(request, 'all fields are required !')
            return render(request, 'login.html')
        else:
            try:
                user = Login.objects.get(username=un)
            except Login.DoesNotExist:
                user = None

            if user is not None and check_password(pw, user.password):
                hl = 'all'
                request.session['user_{}_uname'.format( user.id)] = user.username
                request.session['user_{}_uemail'.format(user.id)] = user.email
                request.session['user_{}_upass'.format( user.id)] = user.password
                id = user.id
                request.session['user_id'] = id
                url = '/hotellist/{}/{}'.format(hl, id)
                messages.success(  request, f'welcome mr. {user.username} you are successfully logged in, now you can do your bookings !')
                return HttpResponseRedirect(url)
            else:
                messages.error(
                    request, 'you are not registered create account to login !')
                return render(request, 'login.html')

    if request.method == 'GET':
        # User is already logged in, redirect to hotellist page
        if request.session.get('user_id'):
            id = request.session['user_id']
            hl = 'all'
            url = '/hotellist/{}/{}'.format(hl, id)
            messages.info(
                request, 'you are already logged in so you cant access login page, you need to log out for accessing this page !')
            return HttpResponseRedirect(url)
        else:
            messages.warning(request, 'for booking you need to login first !')
            return render(request, 'login.html')

def logout_user(request, id):
    if (
        'user_{}_uname'.format(id) not in request.session
        and 'user_{}_upass'.format(id) not in request.session
        and 'user_{}_uemail'.format(id) not in request.session
    ):
        return HttpResponseRedirect('/login/')
    elif (
        'user_{}_uname'.format(id) in request.session
        and 'user_{}_uemail'.format(id) in request.session
        and 'user_{}_upass'.format(id) in request.session
    ):
        user = Login.objects.get(
            username=request.session.get('user_{}_uname'.format(id))
        )
        del request.session['user_{}_uname'.format(user.id)]
        del request.session['user_{}_uemail'.format(user.id)]
        del request.session['user_{}_upass'.format(user.id)]
        request.session.flush()  # delete all the cookies corresponding to the session key...
        request.session.clear_expired()   # delete all the deleted data from the table....
        messages.info(request, 'you are logged out !')
    return HttpResponseRedirect('/login/')


# this is for forgot password and this is before login ...
def update(request):
    if request.method == 'GET':
        messages.warning(request, 'enter new password here !')
        return render(request, 'update_password.html')

    if request.method == 'POST':
        name = request.POST.get('name')
        new = request.POST.get('newpassword')
        cnew = request.POST.get('confirm_newpassword')
        if Login.objects.filter(username=name).exists():
            main = Login.objects.get(username=name)
            oldpassword = main.password
            if len(new) < 8:
                messages.warning(
                    request, 'your new password must be of atleast 8 digit !'
                )
            # here cnew is the newconfirm password....
            elif new == cnew:
                if check_password(new, oldpassword):
                    messages.warning(
                        request,
                        'your new password is to similar to old password select another !',
                    )
                else:
                    updatedpassword = make_password(new)
                    Login.objects.filter(username=name).update(
                        password=updatedpassword)
                    # when we update the password we have to update it in the Bookinghotel and payment table also othewise data is not properly displayed...
                    Bookinghotel.objects.filter(username=name).update(
                        userpassword=updatedpassword
                    )
                    Paymentdetail.objects.filter(username=name).update(
                        password=updatedpassword
                    )
                    messages.success(
                        request,
                        'your password is updated successfully now you can login !',
                    )
                    url = '/login/'
                    return HttpResponseRedirect(url)
            else:
                messages.error(
                    request, 'password and confirm password must be same !')
        else:
            messages.error(
                request, 'No such account is exist pls enter a valid username !'
            )
    return render(request, 'update_password.html')
