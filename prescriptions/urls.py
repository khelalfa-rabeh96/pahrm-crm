from django.urls import path

from .views import ChronicPrescriptionListView

urlpatterns = [
    path('', ChronicPrescriptionListView.as_view(), name='chronic_prescription_list'),

]
