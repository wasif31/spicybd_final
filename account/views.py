from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.utils.http import is_safe_url
from .forms import GuestForm
from .models import GuestEmail

# Create your views here.


def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # check password
        if password == password2:
            # check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'This User Name is Taken')
                return redirect('signup')

            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'This Email is Taken')
                    return redirect('signup')
                else:
                    user = User.objects.create_user(username=username, password=password, email=email,
                                                    first_name=first_name, last_name=last_name)
                    # direct Signin after Signup
                    # auth.signin(request,user)
                    # messages.success(request,'Successfully signed in')
                    # return redirect('index')

                    # first signup then go to signin
                    user.save()
                    messages.success(
                        request, 'Successfully signed up now go back to sign up')
                    return redirect('signin')

        else:
            messages.error(request, 'Password Do not Match ')
            return redirect('signup')
         # error
       # messages.error(request,'Testing Error Message')
        # return redirect('signup')
    else:
        return render(request, 'accounts/signup.html')


def signin(request):
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)
            else:
                return redirect('index')
        else:
            messages.error(request, 'Invalid Username and Password')
            return redirect('signin')
            try:
                del request.session['guest_email_id']
            except:
                pass
            messages.success(request, 'Successfully Signed in')

    else:
        return render(request, 'accounts/signin.html')


def signout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'Successfully logged out')
        return redirect('index')


def dashboard(request):
    return render(request, 'accounts/dashboard.html')

    # guest


def guest_register_view(request):
    form = GuestForm(request.POST or None)
    context = {
        'form': form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        email = form.cleaned_data.get('email')
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id

        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("/register/")
    return redirect("/register/")


@login_required
def account_home_view(request):
    return render(request, "accounts/user_profile.html", {})


class AccountHomeView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/user_profile.html'

    def get_object(self):
        return self.request.user
