from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm
from django.contrib import messages
from .forms import DesignRequestForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import DesignRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404

from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DeleteView



def index(request):

    return render(request, 'index.html')

# def login(request):
#
#     return render(request, 'login.html')


# views.py


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():

            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password2'],
            )

            login(request, user)
            return redirect('index')
    else:
        form = RegistrationForm()
    return render(request, 'registration/registration.html', {'form': form})



@login_required
def design_request_view(request):
    if request.method == 'POST':
        form = DesignRequestForm(request.POST, request.FILES)
        if form.is_valid():
            design_request = form.save(commit=False)
            if request.user.is_authenticated:
                design_request.customer = request.user
            design_request.save()
            messages.success(request, 'Ваша заявка успешно отправлена!')
            return redirect('index')
    else:
        form = DesignRequestForm()
    return render(request, 'catalog/design_request.html', {'form': form})


class RequestsCreatedByUserListView(LoginRequiredMixin, generic.ListView):
    model = DesignRequest
    template_name = 'catalog/requests_created_by_user.html'
    context_object_name = 'requests_list'

    def get_queryset(self):
        return(
            DesignRequest.objects.filter(customer=self.request.user)
        )


class DesignRequestDeleteView(LoginRequiredMixin, DeleteView):
    model = DesignRequest
    template_name = 'catalog/design_request_confirm_delete.html'
    context_object_name = 'request'
    success_url = reverse_lazy('my-requests')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.customer != self.request.user:
            raise Http404("Заявка не найдена или у вас нет прав на её удаление.")
        return obj

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.status in ['in_progress', 'completed']:
            messages.error(
                request,
                'Нельзя удалить заявку, которая находится в работе или уже выполнена.'
            )
            return redirect('my-requests')
        return super().post(request, *args, **kwargs)

