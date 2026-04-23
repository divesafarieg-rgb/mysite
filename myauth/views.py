from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from .forms import CustomUserCreationForm, ProfileUpdateForm
from .models import Profile

class AboutMeView(LoginRequiredMixin, TemplateView):
    template_name = "myauth/about-me.html"

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:login")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Регистрация прошла успешно! Пожалуйста, войдите.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки ниже.')
        return super().form_invalid(form)

class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = "myauth/profile_update.html"

    def get_object(self, queryset=None):
        user_id = self.kwargs.get('user_id')
        if user_id:
            user = get_object_or_404(User, pk=user_id)
            return user.profile
        return self.request.user.profile

    def test_func(self):
        profile = self.get_object()
        user = self.request.user

        if user.is_staff or user.is_superuser:
            return True

        return profile.user == user

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("У вас нет прав для редактирования этого профиля")
        return super().handle_no_permission()

    def get_success_url(self):
        return reverse_lazy('myauth:user_detail', kwargs={'user_id': self.object.user.id})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Профиль успешно обновлён!')
        return response

class UsersListView(ListView):
    model = User
    template_name = "myauth/users_list.html"
    context_object_name = "users"
    ordering = ['username']

class UserDetailView(DetailView):
    model = User
    template_name = "myauth/user_detail.html"
    context_object_name = "user_obj"
    pk_url_kwarg = 'user_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_edit'] = self.request.user.is_staff or self.request.user == self.get_object()
        return context