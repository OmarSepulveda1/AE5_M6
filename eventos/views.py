from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse_lazy
from django.db import models as dj_models
from .models import Event
from .forms import EventForm


class EventListView(ListView):
    model = Event
    template_name = "eventos/event_list.html"
    context_object_name = "eventos"
    paginate_by = 10

    def get_queryset(self):
        qs = Event.objects.order_by("-fecha")
        user = self.request.user

        if user.is_authenticated:
            if user.is_superuser or user.has_perm("eventos.can_view_private"):
                return qs

            return qs.filter(
                dj_models.Q(privado=False)
                | dj_models.Q(organizador=user)
                | dj_models.Q(participantes=user)
            )

        return qs.filter(privado=False)


class EventDetailView(DetailView):
    model = Event
    template_name = "eventos/event_detail.html"

    def dispatch(self, request, *args, **kwargs):
        event = self.get_object()
        user = request.user

        if event.privado:
            if not user.is_authenticated:
                messages.error(request, "Debes iniciar sesión para ver este evento privado.")
                return redirect("login")

            if (
                user.is_superuser
                or user.has_perm("eventos.can_view_private")
                or event.organizador == user
                or user in event.participantes.all()
            ):
                return super().dispatch(request, *args, **kwargs)

            messages.error(request, "No tienes permiso para ver este evento privado.")
            return redirect("eventos:acceso_denegado")

        return super().dispatch(request, *args, **kwargs)


class EventCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "eventos/event_form.html"
    permission_required = "eventos.add_event"

    def form_valid(self, form):
        form.instance.organizador = self.request.user
        messages.success(self.request, "Evento creado correctamente.")
        return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = "eventos/event_form.html"
    permission_required = "eventos.change_event"

    def dispatch(self, request, *args, **kwargs):
        event = self.get_object()
        user = request.user

        if not user.is_superuser and event.organizador != user and not user.has_perm("eventos.change_event"):
            messages.error(request, "No tienes permiso para editar este evento.")
            return redirect("eventos:acceso_denegado")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Evento actualizado correctamente.")
        return super().form_valid(form)


class EventDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Event
    template_name = "eventos/event_confirm_delete.html"
    success_url = reverse_lazy("eventos:listado")
    permission_required = "eventos.delete_event"

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if not (user.is_superuser or user.groups.filter(name="Administradores").exists()):
            messages.error(request, "Solo administradores pueden eliminar eventos.")
            return redirect("eventos:acceso_denegado")

        return super().dispatch(request, *args, **kwargs)


# Vista para acceso denegado
from django.views import View

class AccessDeniedView(View):
    def get(self, request):
        return render(request, "eventos/access_denied.html")
        
