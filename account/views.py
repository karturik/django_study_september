from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import  render, redirect
from .forms import NewUserForm, UserEditForm, ProfileEditForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Profile
from .forms import ContactForm


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user)
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("catalog_main")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="registration/registration_page.html", context={"register_form":form})


@login_required
def profile_edit(request):
    user_form = UserEditForm(instance=request.user)
    profile_form = ProfileEditForm(instance=request.user.profile)

    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        
    return render(request,
                    'profile/profile_edit.html',
                    {'user_form': user_form,
                    'profile_form': profile_form})


class SignUpView(CreateView):
    template_name = 'registration/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('catalog_main')

    def form_valid(self, form):
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid
    
    
def validate_username(request):
    """Проверка доступности логина"""
    username = request.GET.get('username', None)
    print(User.objects.all())
    print(User.objects.filter(username__iexact='admin'))
    response = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    print(response)
    return JsonResponse(response)


def contact_form(request):
    form = ContactForm()
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            form.save()
            return JsonResponse({"name": name}, status=200)
        else:
            errors = form.errors.as_json()
            return JsonResponse({"errors": errors}, status=400)

    return render(request, "contact/contact.html", {"form": form})


# class ContactFormView(FormView):
#     template_name = 'contact/contact.html'
#     form_class = ContactForm

#     def form_valid(self, form):
#         """
#         Если форма валидна, вернем код 200
#         вместе с именем пользователя
#         """
#         name = form.cleaned_data['name']
#         form.save()
#         return JsonResponse({"name": name}, status=200)

#     def form_invalid(self, form):
#         """
#         Если форма невалидна, возвращаем код 400 с ошибками.
#         """
#         errors = form.errors.as_json()
#         return JsonResponse({"errors": errors}, status=400)