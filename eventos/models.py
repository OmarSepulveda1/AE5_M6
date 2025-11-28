from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Event(models.Model):
    TIPO_CHOICES = [
        ("conf", "Conferencia"),
        ("conc", "Concierto"),
        ("sem", "Seminario"),
        ("otro", "Otro"),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha = models.DateTimeField()
    lugar = models.CharField(max_length=200, blank=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default="otro")
    privado = models.BooleanField(default=False)

    organizador = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="eventos_organizados"
    )

    participantes = models.ManyToManyField(User, related_name="eventos_asistidos", blank=True)

    imagen = models.ImageField(upload_to="eventos/", null=True, blank=True)

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ("can_view_private", "Puede ver eventos privados"),
        ]

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("eventos:detalle", args=[self.pk])
