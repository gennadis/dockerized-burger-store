from django.urls import path

from .views import banners_list_api, product_list_api, register_order

app_name = "foodcartapp"

urlpatterns = [
    path("products/", product_list_api),
    path("banners/", banners_list_api),
    path("order/", register_order),
]
