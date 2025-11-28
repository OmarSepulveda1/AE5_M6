from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from eventos.models import Event

admin_group, _ = Group.objects.get_or_create(name="Administradores")
org_group, _ = Group.objects.get_or_create(name="Organizadores")
asist_group, _ = Group.objects.get_or_create(name="Asistentes")

ct = ContentType.objects.get_for_model(Event)
add = Permission.objects.get(codename="add_event", content_type=ct)
change = Permission.objects.get(codename="change_event", content_type=ct)
delete = Permission.objects.get(codename="delete_event", content_type=ct)

admin_group.permissions.set([add, change, delete])
org_group.permissions.set([add, change])
asist_group.permissions.clear()

print("Roles y permisos configurados correctamente.")
