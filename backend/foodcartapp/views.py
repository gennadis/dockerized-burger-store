from django.db import transaction
from django.http import JsonResponse
from django.templatetags.static import static
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import CharField, IntegerField, ModelSerializer

from foodcartapp.models import Order, OrderProduct, Product
from locations.geocoding import fetch_coordinates
from locations.models import Location


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse(
        [
            {
                "title": "Burger",
                "src": static("burger.jpg"),
                "text": "Tasty Burger at your door step",
            },
            {
                "title": "Spices",
                "src": static("food.jpg"),
                "text": "All Cuisines",
            },
            {
                "title": "New York",
                "src": static("tasty.jpg"),
                "text": "Food is incomplete without a tasty dessert",
            },
        ],
        safe=False,
        json_dumps_params={
            "ensure_ascii": False,
            "indent": 4,
        },
    )


def product_list_api(request):
    products = Product.objects.select_related("category").available()

    dumped_products = []
    for product in products:
        dumped_product = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "special_status": product.special_status,
            "description": product.description,
            "category": {
                "id": product.category.id,
                "name": product.category.name,
            }
            if product.category
            else None,
            "image": product.image.url,
            "restaurant": {
                "id": product.id,
                "name": product.name,
            },
        }
        dumped_products.append(dumped_product)
    return JsonResponse(
        dumped_products,
        safe=False,
        json_dumps_params={
            "ensure_ascii": False,
            "indent": 4,
        },
    )


class OrderProductSerializer(ModelSerializer):
    quantity = IntegerField(source="amount")

    class Meta:
        model = OrderProduct
        fields = ["product", "quantity"]


class OrderSerializer(ModelSerializer):
    products = OrderProductSerializer(many=True, allow_empty=False)
    firstname = CharField(source="first_name")
    lastname = CharField(source="last_name")
    phonenumber = PhoneNumberField(source="phone_number")

    class Meta:
        model = Order
        fields = [
            "firstname",
            "lastname",
            "phonenumber",
            "address",
            "products",
        ]


@transaction.atomic
@api_view(["POST"])
def register_order(request):
    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    order_address = serializer.validated_data["address"]

    latitude, longitude = fetch_coordinates(order_address)
    place, created = Location.objects.get_or_create(
        address=order_address,
        longitude=longitude,
        latitude=latitude,
    )
    order = Order.objects.create(
        first_name=serializer.validated_data["first_name"],
        last_name=serializer.validated_data["last_name"],
        phone_number=serializer.validated_data["phone_number"],
        address=order_address,
        location=place,
    )

    order_products = serializer.validated_data["products"]
    order_products_instances = [
        OrderProduct(
            order=order,
            product=product["product"],
            amount=product["amount"],
            static_price=product["product"].price * product["amount"],
        )
        for product in order_products
    ]
    OrderProduct.objects.bulk_create(order_products_instances)

    return Response(data=serializer.data, status=status.HTTP_200_OK)
