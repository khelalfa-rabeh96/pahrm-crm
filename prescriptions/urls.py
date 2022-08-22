from django.urls import path

from .views import (ChronicPrescriptionListView, ChronicPrescriptionDetailView,
                    PrescriptionItemDetailView)

urlpatterns = [
    path('', ChronicPrescriptionListView.as_view(), name='chronic_prescription_list'),
    path('<int:pk>/', ChronicPrescriptionDetailView.as_view(), name='chronic_prescription_detail'),
    path('precription_items/<int:pk>/', PrescriptionItemDetailView.as_view(), name='chronic_prescription_item_detail')


]
