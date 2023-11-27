from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

import core.settings as config
from app.orders.services.cart_item import CartItemService
from core.resources.jwt import JWTClient
from core.utils import Response


class CartItemController(Resource):
    cart_item_service = CartItemService()
    jwt_client = JWTClient(config)

    @jwt_required()
    def get(self, cart_id):
        jwt_identity = get_jwt_identity()
        user_id = self.jwt_client.get_user_id(jwt_identity)

        [err, data, status_code] = self.cart_item_service.get_all(user_id, cart_id)
        if err:
            return Response(success=False, message=data, status_code=status_code)

        serialized_data = [
            {
                **cart_item,
                "_id": str(cart_item["_id"]),
            }
            for cart_item in data
        ]

        return Response(
            success=True,
            message="Cart items returned",
            data=serialized_data,
            status_code=200,
        )

    @jwt_required()
    def post(self, cart_id):
        jwt_identity = get_jwt_identity()
        user_id = self.jwt_client.get_user_id(jwt_identity)

        cart_item = request.json
        [err, data, status_code] = self.cart_item_service.create(
            user_id, cart_id, cart_item
        )
        if err:
            return Response(success=False, message=data, status_code=status_code)

        return Response(
            success=True, message="Cart item created", status_code=status_code
        )


class CartItemDetailController(Resource):
    cart_item_service = CartItemService()
    jwt_client = JWTClient(config)

    @jwt_required()
    def get(self, cart_id, cart_item_id):
        jwt_identity = get_jwt_identity()
        user_id = self.jwt_client.get_user_id(jwt_identity)

        [err, data, status_code] = self.cart_item_service.get(
            user_id, cart_id, cart_item_id
        )
        if err:
            return Response(success=False, message=data, status_code=status_code)

        serialized_data = {
            **data,
            "_id": str(data["_id"]),
        }

        return Response(
            success=True,
            message="Cart item returned",
            data=serialized_data,
            status_code=200,
        )

    @jwt_required()
    def put(self, cart_id, cart_item_id):
        jwt_identity = get_jwt_identity()
        user_id = self.jwt_client.get_user_id(jwt_identity)

        data = request.json
        [err, data, status_code] = self.cart_item_service.update(
            user_id, cart_id, cart_item_id, data
        )
        if err:
            return Response(success=False, message=data, status_code=status_code)

        return Response(success=True, message="Cart item updated", status_code=200)

    @jwt_required()
    def delete(self, cart_id, cart_item_id):
        jwt_identity = get_jwt_identity()
        user_id = self.jwt_client.get_user_id(jwt_identity)

        [err, data, status_code] = self.cart_item_service.delete(
            user_id, cart_id, cart_item_id
        )
        if err:
            return Response(success=False, message=data, status_code=status_code)

        return Response(success=True, message="Cart item deleted", status_code=204)
