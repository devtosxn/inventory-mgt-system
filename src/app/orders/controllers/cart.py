from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

import core.settings as config
from app.orders.services.cart import CartService
from core.resources.jwt import JWTClient
from core.utils import Response


class CartController(Resource):
    cart_service = CartService()
    jwt_client = JWTClient(config)

    @jwt_required()
    def get(self):
        jwt_identity = get_jwt_identity()
        user_id = self.jwt_client.get_user_id(jwt_identity)

        carts = self.cart_service.get_all(user_id)
        serialized_data = [
            {
                **cart,
                "_id": str(cart["_id"]),
                "created_at": str(cart["created_at"]),
                "updated_at": str(cart["updated_at"]),
                "items": [
                    {**item, "_id": str(item["_id"])} for item in cart.get("items", [])
                ],
            }
            for cart in carts
        ]

        return Response(
            success=True,
            message="Carts returned",
            data=serialized_data,
            status_code=200,
        )

    @jwt_required()
    def post(self):
        jwt_identity = get_jwt_identity()
        user_id = self.jwt_client.get_user_id(jwt_identity)
        cart_id = self.cart_service.create(user_id)

        return Response(
            success=True, message="Cart created", data=cart_id, status_code=201
        )


class CartDetailController(Resource):
    cart_service = CartService()

    @jwt_required()
    def get(self, cart_id):
        [err, data, status_code] = self.cart_service.get(cart_id)
        if err:
            return Response(success=False, message=data, status_code=status_code)

        cart = data
        serialized_data = {
            **cart,
            "_id": str(cart["_id"]),
            "items": [
                {**item, "_id": str(item["_id"])} for item in cart.get("items", [])
            ],
            "created_at": str(cart["created_at"]),
            "updated_at": str(cart["updated_at"]),
        }

        return Response(
            success=True, message="Cart returned", data=serialized_data, status_code=200
        )
