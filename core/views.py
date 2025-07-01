# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BPIN, Contrato, Documento
from .forms import BPINForm, ContratoForm, DocumentForm
from django.core.paginator import Paginator
from django.utils import timezone
import logging
from django.http import HttpResponseBadRequest

logger = logging.getLogger(__name__)

@login_required
def dashboard(request):
    total_bpins = BPIN.objects.count()
    total_contratos = Contrato.objects.count()
    total_documentos = Documento.objects.count()
    ultimos_documentos = Documento.objects.all().order_by('-fecha_subida')[:5]
    logger.info(f"Loaded dashboard: BPINs={total_bpins}, Contratos={total_contratos}, Documentos={total_documentos}")
    return render(request, 'dashboard.html', {
        'total_bpins': total_bpins,
        'total_contratos': total_contratos,
        'total_documentos': total_documentos,
        'ultimos_documentos': ultimos_documentos,
    })

@login_required
def bpin_list(request):
    bpins = BPIN.objects.all()
    paginator = Paginator(bpins, 10)  # 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        print("Test form submitted successfully!")
        print("CSRF Token:", request.POST.get('csrfmiddlewaretoken'))
    return render(request, 'bpin_list.html', {'page_obj': page_obj})

@login_required
def bpin_detail(request, id):
    bpin = get_object_or_404(BPIN, id=id)
    contratos = Contrato.objects.filter(bpin=id).order_by('numero_contrato')
    documentos = Documento.objects.filter(bpin=id).order_by('-fecha_subida')
    logger.info(f"Loaded BPIN detail for {bpin.numero_bpin} (ID: {id})")
    return render(request, 'bpin_detail.html', {
        'bpin': bpin,
        'contratos': contratos,
        'documentos': documentos,
    })

@login_required
def bpin_create(request):
    if request.method == 'POST':
        form = BPINForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'BPIN creado exitosamente.')
            return redirect('bpin_list')
        else:
            messages.error(request, 'Error al crear el BPIN. Verifica los campos.')
    else:
        form = BPINForm()
    return render(request, 'bpin_create.html', {'form': form})

@login_required
def bpin_edit(request, id):
    bpin = get_object_or_404(BPIN, id=id)
    if request.method == 'POST':
        form = BPINForm(request.POST, instance=bpin)
        csrf_token = request.POST.get('csrfmiddlewaretoken', 'Missing')
        logger.info(f"Received CSRF token: {csrf_token} (Length: {len(csrf_token) if csrf_token else 0}) for BPIN {bpin.numero_bpin} edit")
        if form.is_valid():
            try:
                form.save()
                logger.info(f"Successfully updated BPIN {bpin.numero_bpin} (ID: {id})")
                return redirect('bpin_list')
            except Exception as e:
                logger.error(f"Error updating BPIN {bpin.numero_bpin}: {str(e)}")
                return HttpResponseBadRequest(f"Error al actualizar BPIN: {str(e)}")
        else:
            logger.error(f"Form validation failed for BPIN {bpin.numero_bpin}: {form.errors}")
    else:
        form = BPINForm(instance=bpin)
        logger.info(f"Loaded BPIN edit form for {bpin.numero_bpin} (ID: {id})")
    return render(request, 'bpin_form.html', {'form': form, 'bpin': bpin})

@login_required
def bpin_delete(request, id):
    if request.method != 'POST':
        logger.error(f"Invalid method {request.method} for bpin_delete, ID: {id}")
        return HttpResponseBadRequest("Método no permitido")
    bpin = get_object_or_404(BPIN, id=id)
    csrf_token = request.POST.get('csrfmiddlewaretoken', 'Missing')
    logger.info(f"Received CSRF token: {csrf_token} (Length: {len(csrf_token) if csrf_token else 0}) for BPIN {bpin.numero_bpin}")
    if bpin.contratos.exists() or bpin.documentos.exists():
        logger.error(f"Cannot delete BPIN {bpin.numero_bpin} due to related Contratos or Documentos")
        return HttpResponseBadRequest("No se puede eliminar el BPIN porque tiene contratos o documentos asociados.")
    try:
        logger.info(f"Attempting to delete BPIN {bpin.numero_bpin} (ID: {id})")
        bpin.delete()
        logger.info(f"Successfully deleted BPIN {bpin.numero_bpin}")
        return redirect('bpin_list')
    except Exception as e:
        logger.error(f"Error deleting BPIN {bpin.numero_bpin}: {str(e)}")
        return HttpResponseBadRequest(f"Error al eliminar BPIN: {str(e)}")

@login_required
def contrato_list(request):
    bpin_id = request.GET.get('bpin_id')
    contratos = Contrato.objects.all().order_by('numero_contrato')
    if bpin_id:
        contratos = contratos.filter(bpin_id=bpin_id)
    paginator = Paginator(contratos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    bpins = BPIN.objects.all().order_by('numero_bpin')
    logger.info(f"Loaded Contrato list, page {page_number or 1}, BPIN filter: {bpin_id or 'None'}, {contratos.count()} items")
    return render(request, 'contrato_list.html', {'page_obj': page_obj, 'bpins': bpins})

@login_required
def contrato_detail(request, id):
    contrato = get_object_or_404(Contrato, id=id)
    documentos = Documento.objects.filter(contrato=id).order_by('-fecha_subida')
    logger.info(f"Loaded Contrato detail for {contrato.numero_contrato} (ID: {id})")
    return render(request, 'contrato_detail.html', {
        'contrato': contrato,
        'documentos': documentos,
    })

@login_required
def contrato_create(request):
    if request.method == 'POST':
        form = ContratoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contrato creado exitosamente.')
            return redirect('contrato_list')
        else:
            messages.error(request, 'Error al crear el Contrato. Verifica los campos.')
    else:
        form = ContratoForm()
    return render(request, 'contrato_create.html', {'form': form})

@login_required
def contrato_edit(request, id):
    contrato = get_object_or_404(Contrato, id=id)
    if request.method == 'POST':
        form = ContratoForm(request.POST, instance=contrato)
        csrf_token = request.POST.get('csrfmiddlewaretoken', 'Missing')
        logger.info(f"Received CSRF token: {csrf_token} (Length: {len(csrf_token) if csrf_token else 0}) for Contrato {contrato.numero_contrato} edit")
        if form.is_valid():
            try:
                form.save()
                logger.info(f"Successfully updated Contrato {contrato.numero_contrato} (ID: {id})")
                return redirect('contrato_list')
            except Exception as e:
                logger.error(f"Error updating Contrato {contrato.numero_contrato}: {str(e)}")
                return HttpResponseBadRequest(f"Error al actualizar Contrato: {str(e)}")
        else:
            logger.error(f"Form validation failed for Contrato {contrato.numero_contrato}: {form.errors}")
    else:
        form = ContratoForm(instance=contrato)
        logger.info(f"Loaded Contrato edit form for {contrato.numero_contrato} (ID: {id})")
    return render(request, 'contrato_form.html', {'form': form, 'contrato': contrato})

@login_required
def contrato_delete(request, id):
    if request.method != 'POST':
        logger.error(f"Invalid method {request.method} for contrato_delete, ID: {id}")
        return HttpResponseBadRequest("Método no permitido")
    contrato = get_object_or_404(Contrato, id=id)
    csrf_token = request.POST.get('csrfmiddlewaretoken', 'Missing')
    logger.info(f"Received CSRF token: {csrf_token} (Length: {len(csrf_token) if csrf_token else 0}) for Contrato {contrato.numero_contrato}")
    if contrato.documentos.exists():
        logger.error(f"Cannot delete Contrato {contrato.numero_contrato} due to related Documentos")
        return HttpResponseBadRequest("No se puede eliminar el Contrato porque tiene documentos asociados.")
    try:
        logger.info(f"Attempting to delete Contrato {contrato.numero_contrato} (ID: {id})")
        contrato.delete()
        logger.info(f"Successfully deleted Contrato {contrato.numero_contrato}")
        return redirect('contrato_list')
    except Exception as e:
        logger.error(f"Error deleting Contrato {contrato.numero_contrato}: {str(e)}")
        return HttpResponseBadRequest(f"Error al eliminar Contrato: {str(e)}")

@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.subido_por = request.user
            document.save()
            messages.success(request, 'Documento subido exitosamente.')
            return redirect('upload_document')
        else:
            messages.error(request, 'Error al subir el documento. Verifica los campos.')
    else:
        form = DocumentForm()
    return render(request, 'upload_document.html', {'form': form})


@login_required
def documento_edit(request, id):
    documento = get_object_or_404(Documento, id=id)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=documento)
        csrf_token = request.POST.get('csrfmiddlewaretoken', 'Missing')
        logger.info(f"Received CSRF token: {csrf_token} (Length: {len(csrf_token) if csrf_token else 0}) for Documento {documento.nombre_archivo} edit")
        if form.is_valid():
            try:
                form.save()
                logger.info(f"Successfully updated Documento {documento.nombre_archivo} (ID: {id})")
                return redirect('document_list')
            except Exception as e:
                logger.error(f"Error updating Documento {documento.nombre_archivo}: {str(e)}")
                return HttpResponseBadRequest(f"Error al actualizar Documento: {str(e)}")
        else:
            logger.error(f"Form validation failed for Documento {documento.nombre_archivo}: {form.errors}")
    else:
        form = DocumentForm(instance=documento)
        logger.info(f"Loaded Documento edit form for {documento.nombre_archivo} (ID: {id})")
    return render(request, 'documento_form.html', {'form': form, 'documento': documento})

@login_required
def documento_delete(request, id):
    if request.method != 'POST':
        logger.error(f"Invalid method {request.method} for documento_delete, ID: {id}")
        return HttpResponseBadRequest("Método no permitido")
    documento = get_object_or_404(Documento, id=id)
    csrf_token = request.POST.get('csrfmiddlewaretoken', 'Missing')
    logger.info(f"Received CSRF token: {csrf_token} (Length: {len(csrf_token) if csrf_token else 0}) for Documento {documento.nombre_archivo}")
    try:
        logger.info(f"Attempting to delete Documento {documento.nombre_archivo} (ID: {id})")
        documento.delete()
        logger.info(f"Successfully deleted Documento {documento.nombre_archivo}")
        return redirect('document_list')
    except Exception as e:
        logger.error(f"Error deleting Documento {documento.nombre_archivo}: {str(e)}")
        return HttpResponseBadRequest(f"Error al eliminar Documento: {str(e)}")
    
@login_required
def document_list(request):
    bpin_id = request.GET.get('bpin_id')
    documentos = Documento.objects.all().order_by('-fecha_subida')
    if bpin_id:
        try:
            documentos = documentos.filter(bpin_id=bpin_id)
        except ValueError:
            logger.error(f"Invalid bpin_id: {bpin_id}")
            documentos = Documento.objects.none()  # Return empty queryset for invalid filter
    paginator = Paginator(documentos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    bpins = BPIN.objects.all().order_by('numero_bpin')
    logger.info(f"Loaded Documento list, page {page_number or 1}, BPIN filter: {bpin_id or 'None'}, {documentos.count()} items")
    return render(request, 'document_list.html', {'page_obj': page_obj, 'bpins': bpins})

@login_required
def documento_detail(request, id):
    documento = get_object_or_404(Documento, id=id)
    logger.info(f"Loaded Documento detail for {documento.nombre_archivo} (ID: {id})")
    return render(request, 'documento_detail.html', {
        'documento': documento,
    })