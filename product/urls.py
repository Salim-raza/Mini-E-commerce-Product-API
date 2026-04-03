from django.urls import path
from .views import *

urlpatterns = [
    path("product_add/", product_add, name="product_add"),
    path("updata_product/<int:id>/", updata_product, name="updata_product"),
    path("delete_product/<int:id>/", delete_product, name="delete_product"),
    path("all_product/", all_product, name="all_product"),
    path("product_search/<str:name>/", product_search, name="product_search"),
    path("category/<str:category>/", category_search, name="category_search"),
    path("order_product/", order_product, name="order_product"),
]