# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('bpins/', views.bpin_list, name='bpin_list'),
    path('bpin/<int:id>/delete/', views.bpin_delete, name='bpin_delete'),
    path('bpin/create/', views.bpin_create, name='bpin_create'),
    path('bpin/<int:id>/', views.bpin_detail, name='bpin_detail'),
    path('bpin/<int:id>/edit/', views.bpin_edit, name='bpin_edit'),
    path('contratos/', views.contrato_list, name='contrato_list'),
    path('contrato/<int:id>/delete/', views.contrato_delete, name='contrato_delete'),
    path('contrato/create/', views.contrato_create, name='contrato_create'),
    path('contrato/<int:id>/', views.contrato_detail, name='contrato_detail'),
    path('contrato/<int:id>/edit/', views.contrato_edit, name='contrato_edit'),
    path('documentos/', views.document_list, name='document_list'),
    path('documento/<int:id>/delete/', views.documento_delete, name='documento_delete'),
    path('documento/upload/', views.upload_document, name='upload_document'),
    path('documento/<int:id>/edit/', views.documento_edit, name='documento_edit'),
    path('documento/<int:id>/', views.documento_detail, name='documento_detail'),
]