from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.base import TemplateResponseMixin, ContextMixin

from user.tokens import account_activation_token
from .forms import UserCreationForm, UserLoginForm
from .models import AppUser


# Create your views here.

def send_email_to_receiver(receiver, message, subject=None, html_message=None):
    """
    send email for receiver
    """
    receiver = receiver if isinstance(receiver, list) else [receiver]
    if not subject:
        subject = "Work diary notification Work Diary Conqum"
    try:
        send_mail(
            subject=subject,
            message=message,
            html_message=html_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=receiver,
            fail_silently=False,
        )
        return True
    except Exception as exc:
        print("Failed to send email: {}".format(exc))
        return False


def signup(request):
    """
        authentification sign up view
        """
    # if request.user:
    #     return redirect(reverse('home'))
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email", False)
            age = form.cleaned_data.get("age", False)
            first_name = form.cleaned_data.get("first_name", False)
            last_name = form.cleaned_data.get("last_name", False)
            password = form.cleaned_data.get("password", False)

            user = AppUser.objects.filter(email=email).first()
            if not user:
                user = AppUser.objects.create(
                    email=email,
                    age=age,
                    first_name=first_name,
                    last_name=last_name,
                    is_active=False
                )
                user.set_password(password)
                user.save()
                dom = request.META.get("HTTP_REFERER", 'home').split('/')
                domain = dom[0] + '//' + dom[2]
                print('===', domain)
                activaton_link = '{}/user/activate/{}/{}'.format(domain,
                                                                 urlsafe_base64_encode(force_bytes(user.pk)),
                                                                 account_activation_token.make_token(user)
                                                                 )
                send_email_to_receiver(
                    subject='Activate account',
                    message="Hi {},Please click on the link to confirm your registration, {}".format(user.email,
                                                                                                     activaton_link),
                    receiver=user.email
                )
                print(activaton_link)
                return JsonResponse({'message': 'User create, check your email'})
            else:
                return JsonResponse({'message': "User with this email exists! Try to log in"})
        else:
            return JsonResponse({"message": form.errors})
    form = UserCreationForm()
    return render(request, 'user/registration.html', {"form": form})


class AdminUserRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        return super(AdminUserRequiredMixin, self).dispatch(request, *args, **kwargs)

    def get_user(self, request, pk=None):
        if not pk:
            pk = request.user.id
        user = AppUser.objects.filter(pk=pk).first()
        return user


class UserLoginView(LoginView):
    """
    Login System
    """
    model = AppUser
    form_class = UserLoginForm
    template_name = "user/login.html"
    redirect_authenticated_user = False

    # def get(self, *args, **kwargs):
    #     if self.request.user:
    #         return redirect(reverse('home'))
    #     return super(UserLoginView, self).get(*args, **kwargs)

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        email = form.cleaned_data.get("email", False)
        password = form.cleaned_data.get("password", False)
        user = form.get_user(email, password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return JsonResponse({'data': 1, 'url': reverse('home')})
            else:
                return JsonResponse(
                    {'url': reverse("resend_activation_preview", kwargs={"preview": 1, "pk": user.id}),
                     'data': 1}
                )
        else:
            return JsonResponse({'message': "No such user with that email and password"})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = AppUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, AppUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        return HttpResponse('qiwghvcd')
    else:
        return HttpResponse('fwfgerg34g')


class ResendEmailView(TemplateView):
    template_name = "user/user_exist.html"

    def dispatch(self, request, *args, **kwargs):
        try:
            user = AppUser.objects.get(pk=kwargs.get("pk"))
            if not kwargs.get("preview", False):
                if user.is_active:
                    return redirect(reverse('login'))
                else:
                    dom = request.META.get("HTTP_REFERER", 'home').split('/')
                    domain = dom[0] + '//' + dom[2]
                    activation_link = '{}/user/activate/{}/{}'.format(domain,
                                                                      urlsafe_base64_encode(force_bytes(user.pk)),
                                                                      account_activation_token.make_token(user)
                                                                      )
                    send_email_to_receiver(
                        subject='Activate account',
                        message="Hi {},Please click on the link to confirm your registration, {}".format(user.email,
                                                                                                         activation_link
                                                                                                         ),
                        receiver=user.email
                    )
                    return JsonResponse({"message": 'check your email'})
        except Exception as exc:
            print("ResendEmailView fail: ", exc)
            return JsonResponse({'message': 'something problem'})
        return super(ResendEmailView, self).dispatch(request, *args, **kwargs)


def resend_email_view_ajax(request, **kwargs):
    try:
        user = AppUser.objects.get(pk=kwargs.get("pk"))
        if not kwargs.get("preview", False):
            if user.is_active:
                return redirect(reverse('login'))
            else:
                dom = request.META.get("HTTP_REFERER", 'home').split('/')
                domain = dom[0] + '//' + dom[2]
                activation_link = '{}/user/activate/{}/{}'.format(domain,
                                                                  urlsafe_base64_encode(force_bytes(user.pk)),
                                                                  account_activation_token.make_token(user)
                                                                  )
                send_email_to_receiver(
                    subject='Activate account',
                    message="Hi {},Please click on the link to confirm your registration, {}".format(user.email,
                                                                                                     activation_link),
                    receiver=user.email
                )
                return JsonResponse({"message": 'check your email', 'activation_link': activation_link})
    except Exception as exc:
        print("ResendEmailView fail: ", exc)
        return JsonResponse({'message': 'failed, try again later'})
    return JsonResponse({'message': 'link resent'})
