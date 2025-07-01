# core/models.py
from django.db import models
from django.contrib.auth.models import User

class BPIN(models.Model):
    numero_bpin = models.CharField(max_length=50, unique=True)
    nombre_proyecto = models.CharField(max_length=255)
    vigencia = models.IntegerField()
    presupuesto = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.numero_bpin} - {self.nombre_proyecto}"

    class Meta:
        indexes = [
            models.Index(fields=['numero_bpin']),
            models.Index(fields=['nombre_proyecto']),
        ]

class Contrato(models.Model):
    numero_contrato = models.CharField(max_length=50, unique=True)
    objeto_contrato = models.TextField()
    fecha_suscripcion = models.DateField()
    valor_contrato = models.DecimalField(max_digits=15, decimal_places=2)
    bpin = models.ForeignKey(BPIN, on_delete=models.CASCADE, related_name='contratos')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Contrato {self.numero_contrato} - BPIN {self.bpin.numero_bpin}"

class Resolucion(models.Model):
    numero_resolucion = models.CharField(max_length=50, unique=True)
    fecha_resolucion = models.DateField()
    valor_pagado = models.DecimalField(max_digits=15, decimal_places=2)
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name='resoluciones')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Resolución {self.numero_resolucion} - Contrato {self.contrato.numero_contrato}"

class Documento(models.Model):
    TIPO_DOCUMENTO = (
        ('contrato', 'Contrato'),
        ('resolucion', 'Resolución'),
        ('adenda', 'Adenda'),
        ('otro', 'Otro'),
    )

    nombre_archivo = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='documentos/%Y/%m/%d/')
    tipo_documento = models.CharField(max_length=20, choices=TIPO_DOCUMENTO)
    descripcion = models.TextField(blank=True, null=True)
    subido_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    bpin = models.ForeignKey(BPIN, on_delete=models.CASCADE, null=True, blank=True, related_name='documentos')
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, null=True, blank=True, related_name='documentos')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_archivo

    class Meta:
        indexes = [
            models.Index(fields=['bpin', 'contrato']),
            models.Index(fields=['fecha_subida']),
        ]