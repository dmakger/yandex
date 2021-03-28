from django.urls import path, include
from .views import CourierView
from .views import OrderView, OrderAssignView, OrderCompleteView


urlpatterns = [
    path("couriers/", CourierView.as_view()),
    path("couriers/<int:courier_id>/", CourierView.as_view()),

    path("orders/", OrderView.as_view()),
    path("orders/assign/", OrderAssignView.as_view()),
    path("orders/complete/", OrderCompleteView.as_view()),
]