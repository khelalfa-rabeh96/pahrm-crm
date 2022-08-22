from django.urls import path

from .views import (ChronicPrescriptionListView, ChronicPrescriptionDetailView)

urlpatterns = [
    path('', ChronicPrescriptionListView.as_view(), name='chronic_prescription_list'),
    path('<int:pk>/', ChronicPrescriptionDetailView.as_view(), name='chronic_prescription_detail'),


]
