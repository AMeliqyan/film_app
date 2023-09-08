from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from datetime import datetime
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .tokens import account_activation_token


def home(request):
    languages = Language.objects.all()
    genr = Gener.objects.all()
    film = Film.objects.filter(active=True).all()
    params = request.GET.dict()
    if len(params.keys()) > 0:
        film = Film.objects.filter(active=True, languages=params['language'], genres=params['genre'],
                                   date=params['date']).all()
    print(film)
    return render(request, 'film/home.html', {'film': film, "languages": languages, "genr": genr})


def film_index(request, id):
    film_ind = Film.objects.get(id=id)
    return render(request, 'film/index.html', {'film': film_ind})


def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))

            return redirect('login')
    return render(request, 'film/register.html', {"form": form})


def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('film/template_activate_account.html', {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
            received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        # messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        # messages.error(request, 'Activation link is invalid!')
        pass
    return redirect('home')


def login_page(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
            if user:
                login(request, user)
                return redirect('profile')
    return render(request, 'film/login.html', {"form": form})


@login_required(login_url='login')
def profile(request):
    films = Film.objects.filter(user_id=request.user.id).all()
    return render(request, 'film/profile.html', {'films': films})


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')


def edit(request):
    form = UpdateUserForm(instance=request.user)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    return render(request, 'film/edit.html', {'form': form})


def passwordcheng(request):
    form = PasswordChangeForm(user=request.user)
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')
    return render(request, 'film/passwordcheng.html', {'form': form})


def decline_film(request, id):
    form = NotForm()
    if request.method == "POST":
        notification = Notification(user=request.user, film=Film.objects.get(id=id))
        form = NotForm(request.POST, instance=notification)
        if form.is_valid():
            form.save()
            return redirect("user_films")
    return render(request, "film/notification.html", {'form': form})


def add_film(request):
    form = FilmForm()
    if request.method == "POST":
        film = Film(user=request.user)
        print(request.FILES)
        print(request.POST)
        form = FilmForm(request.POST, request.FILES, instance=film)
        if form.is_valid():
            form.save()
            return redirect('profile')
    return render(request, "film/add_film.html", {"form": form})


def del_film(request, id):
    film = Film.objects.get(id=id)
    film.delete()
    return redirect('home')


def update_film(request, id):
    film = Film.objects.get(id=id)
    form = UpdFilms(instance=film)
    if request.method == "POST":
        film.active = False
        film.save()
        form = FilmForm(request.POST, instance=film)
        if form.is_valid():
            form.save()

            return redirect('profile')
    return render(request, "film/update_film.html", {"form": form})


def user_users(request):
    users = User.objects.filter(is_superuser=False, is_staff=False, is_active=True).all()
    return render(request, "film/user_users.html", {"users": users})


def user_films(request):
    films = Film.objects.all()
    return render(request, "film/user_films.html", {"films": films})


def accept_film(request, id):
    film = Film.objects.get(id=id)

    film.active = True
    film.save()
    notification = Notification(user=request.user, film=Film.objects.get(id=id), message=' Ֆիլմը հաստատվել է ')
    notification.save()
    return redirect('user_films')


def user_notification(request):
    user_not = Notification.objects.filter(film__user=request.user).all()
    print(user_not)
    return render(request, "film/user_notification.html", {'user_not': user_not})


def seen(request, id):
    see = Notification.objects.get(id=id)
    see.delete()
    return redirect("user_notification")


def feedback(request, id):
    form = FeedbackForm()
    if request.method == 'POST':
        feedback = Feedback(user=request.user, film=Film.objects.get(id=id))
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            return redirect("home")
    return render(request, "film/feedback.html", {'form': form})


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'film/password_reset.html'
    email_template_name = 'film/password_reset_email.html'
    subject_template_name = 'film/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('home')
