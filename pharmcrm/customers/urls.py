from django.urls import path

from .views import (CustomerModelViewSet)


# customer  list view
customer_list = CustomerModelViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

# customer  detail view
customer_detail = CustomerModelViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('', customer_list, name='customer_list'),
    path('<int:pk>/', customer_detail, name="customer_detail")
    


]