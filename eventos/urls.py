from django.urls import path
from .views import (
    EventListView,
    EventDetailView,
    EventCreateView,
    EventUpdateView,
    EventDeleteView
)

app_name = "eventos"

urlpatterns = [
    path("", EventListView.as_view(), name="listado"),
    path("<int:pk>/", EventDetailView.as_view(), name="detalle"),
    path("crear/", EventCreateView.as_view(), name="crear"),
    path("editar/<int:pk>/", EventUpdateView.as_view(), name="editar"),
    path("eliminar/<int:pk>/", EventDeleteView.as_view(), name="eliminar"),
]
