import datetime
import json

import jdatetime
from django.contrib import messages
from django.contrib.auth import logout as auth_logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, JsonResponse
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, TemplateView, UpdateView

from main.forms import SignUpForm
from main.models import BankInfo, Code, File, User, Shift, ControlShift


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
        messages.error(self.request, form.errors)
        return self.render_to_response(self.get_context_data(form=form))


class ProfileView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'next'

    model = User
    fields = ['first_name', 'last_name', 'address', 'profile_picture']

    template_name = 'main/profile.html'

    def get_success_url(self):
        return reverse_lazy('main:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'تغییرات با موفقیت ثبت شد!')
        return super().form_valid(form)


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


class BankInfoView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'next'

    model = BankInfo
    fields = ['sheba', ]

    template_name = 'main/bankinfo.html'

    def get_success_url(self):
        return reverse_lazy('main:bankinfo')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'اطلاعات با موفقیت ثبت شد!')
        return super().form_valid(form)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'رمز ورود به روز رسانی شد!')
        else:
            messages.error(request, 'تغییر رمز دچار مشکل شد، لطفا مجدد تلاش کنید!')

    return redirect('main:profile')


@csrf_exempt
def send_code(request):
    if request.method == 'POST':
        data = request.POST
        phone_number = data.get("phone_number", None)
        if phone_number and len(phone_number) == 11:
            # code = secrets.choice(range(1000, 9999))
            code = 1234

            # To-Do: SEND CODE VIA SMS
            Code.objects.create(
                phone_number=phone_number,
                code=str(code)
            )
            return HttpResponse("Done!", status=200)
        else:
            return HttpResponse("Wrong Phone Number!", status=400)

    else:
        return HttpResponse("Not Valid!", status=403)


# sjd is here

@csrf_exempt
def next_month_shift_view(request):
    if request.method == "GET":
        month = jdatetime.date.today().month
        shifts = Shift.objects.filter(user=request.user)
        list_of_shifts = []

        if month < 12:
            next_month = month + 1
        else:
            next_month = 1
        query = shifts.filter(date__exact=jdatetime.date(jdatetime.date.today().year , next_month , 1))
        if query:
            print(request.user)
            list_of_shifts = shifts.filter(string_date__startswith=str(str(jdatetime.date.today().year)+"/"+str(next_month)))

        else:
            date = jdatetime.date(jdatetime.date.today().year , next_month  ,1 )
            while date.month < next_month+1:
                shift_record = Shift.objects.create(date=date, user=request.user , string_date=date.strftime("%Y/%m/%d"))
                shift_record.save()
                list_of_shifts.append(shift_record)
                date += jdatetime.timedelta(days=1)
        print(list_of_shifts)
        control_over_shifts = ControlShift.objects.get(user = request.user , year=jdatetime.date.today().year , month = next_month )
        if not control_over_shifts :
            ControlShift.objects.create(user=request.user, year=jdatetime.date.today().year, month=next_month)
        return render(request, 'main/tables-basic-Copy.html', {'current_month': month , 'list_of_shifts' : list_of_shifts , 'control' : control_over_shifts})
    else :
        print(request.body)
        table_data = json.loads(request.POST.get("table_data"))
        print(table_data)
        return JsonResponse({"s":"salam"})
