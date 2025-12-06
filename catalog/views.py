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
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView
from .forms import UpdateRequestStatusForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import DesignCategory
from .forms import CategoryForm


def index(request):
    completed_requests = DesignRequest.objects.filter(
        status='completed'
    ).order_by('-created_at')[:4]

    in_progress_count = DesignRequest.objects.filter(
        status='in_progress'
    ).count()

    return render(request, 'index.html', {
        'completed_requests': completed_requests,
        'in_progress_count': in_progress_count,
    })



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
            return redirect('my-requests')
    else:
        form = DesignRequestForm()
    return render(request, 'catalog/design_request.html', {'form': form})


@login_required
def my_requests_view(request):
    status = request.GET.get('status')
    requests_list = DesignRequest.objects.filter(customer=request.user)

    if status:
        requests_list = requests_list.filter(status=status)

    requests_list = requests_list.order_by('-created_at')

    return render(request, 'catalog/requests_created_by_user.html', {
        'requests_list': requests_list,
        'current_status': status
    })



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




class AllDesignRequestsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = DesignRequest
    template_name = 'catalog/all_requests.html'
    context_object_name = 'requests_list'
    ordering = ['-created_at']

    def test_func(self):
        return self.request.user.is_superuser

    def get_queryset(self):
        return DesignRequest.objects.all()




def is_admin(user):
    return user.is_superuser


@login_required
@user_passes_test(is_admin)
def update_request_status(request, request_id):
    design_request = get_object_or_404(DesignRequest, id=request_id)

    if request.method == 'POST':
        form = UpdateRequestStatusForm(
            request.POST,
            request.FILES,
            instance=design_request,
            original_status=design_request.status
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Статус заявки успешно обновлён.')
            return redirect('all-requests')
    else:
        form = UpdateRequestStatusForm(
            instance=design_request,
            original_status=design_request.status
        )

    return render(request, 'catalog/update_request_status.html', {
        'form': form,
        'request_obj': design_request
    })


@user_passes_test(is_admin)
def manage_categories(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория добавлена.')
            return redirect('manage-categories')
    else:
        form = CategoryForm()

    categories = DesignCategory.objects.all()
    return render(request, 'catalog/manage_categories.html', {
        'form': form,
        'categories': categories
    })


@user_passes_test(is_admin)
def delete_category(request, category_id):
    category = get_object_or_404(DesignCategory, id=category_id)
    category.delete()
    messages.success(request, 'Категория удалена.')
    return redirect('manage-categories')