from django.shortcuts import HttpResponseRedirect

from django.views.generic import CreateView, TemplateView

from django.contrib.auth import logout as auth_logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages

from django.urls import reverse_lazy

from main.forms import SignUpForm
from main.models import File


class LogInView(LoginView):
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('main:profile') 
        
    def form_valid(self, form):
        user = form.get_user()
        if user.is_confirmed:
            return super().form_valid(form)
        else:
            messages.error(self.request, 'حساب کاربری شما نیازمند تایید پشتیبانی می باشد، لطفا شکیبا باشید.')
            return self.render_to_response(self.get_context_data(form=form))
    
    def form_invalid(self, form):
        messages.error(self.request, 'شماره یا رمزی که وارد کردید را دوباره چک کنید')
        return self.render_to_response(self.get_context_data(form=form))


class SignUpView(CreateView):
    authenticated_redirect_url = reverse_lazy("main:profile")
    
    template_name = 'registration/signup.html'
    form_class = SignUpForm
    
    def get_success_url(self):
        return reverse_lazy('main:signed') 
    
    def form_invalid(self, form):
        messages.error(self.request, 'دوباره فیلد هایی که وارد کردید را بررسی کنید!')
        return self.render_to_response(self.get_context_data(form=form))


class ProfileView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'next'

    template_name = 'main/profile.html'
    

class SignedView(TemplateView):
    template_name = 'main/thankyou.html'


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/")


class FilesView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'next'

    model = File
    fields = ['file', ]
    
    template_name = 'main/files.html'
    
    def get_success_url(self):
        return reverse_lazy('main:files') 
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'فایل با موفقیت ارسال شد!')
        return super().form_valid(form)
