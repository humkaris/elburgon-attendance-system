from django.urls import path
from .views import import_students

urlpatterns = [
    path("import/", import_students, name="import_students"),
]
