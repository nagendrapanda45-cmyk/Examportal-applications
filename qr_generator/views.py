from Role_based_Access.decorators import module_access_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import QRGenerate
from .forms import QRGenerateForm
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages


# @login_required
@module_access_required('Manage QR')
def qr_list(request):
    qr_codes_all = QRGenerate.objects.filter(deleted=False).order_by('-created_at')
    query = request.GET.get('search', '').strip()
    
    if query:
        qr_codes_all = qr_codes_all.filter(
            Q(name__icontains=query) |
            Q(target_url__icontains=query) |
            Q(id__icontains=query)
        )
    # Pagination
    paginator = Paginator(qr_codes_all, 10)  # Show 10 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'qr_generator/qr_list.html', {'page_obj': page_obj})
# @login_required
@module_access_required('Manage QR')
def qr_detail(request, pk):
    config = get_object_or_404(QRGenerate, pk=pk)
    return render(request, 'qr_generator/qr_detail.html', {'config': config})
# @login_required
@module_access_required('Manage QR')
def regenerate_qr(request, pk):
    config = get_object_or_404(QRGenerate, pk=pk)
    config.generate_qr_code()
    config.save()
    messages.success(request, 'QR code re-generated successfully!')
    return redirect('qr_generator:qr_detail', pk=pk)
# @login_required
@module_access_required('Manage QR')
def qr_create(request):
    if request.method == 'POST':
        form = QRGenerateForm(request.POST)
        if form.is_valid():
            qr_instance = form.save(commit=False)
            qr_instance.generate_qr_code()
            qr_instance.save()
            messages.success(request, 'QR code created successfully!')
            return redirect('qr_generator:qr_detail', pk=qr_instance.pk)
        else:
            print(form.errors)  # Debug: print form errors
    else:
        form = QRGenerateForm()

    return render(request, 'qr_generator/qr_create.html', {'form': form})

# @login_required
@module_access_required('Manage QR')
def qr_delete(request, pk):
    qr_instance = get_object_or_404(QRGenerate, pk=pk)
    qr_instance.deleted = True
    qr_instance.save()
    messages.success(request, 'QR code deleted successfully!')
    return redirect('qr_generator:qr_list')

