# from app.orders.models import Cart
from datetime import datetime

from bson import ObjectId

from core.error_handlers import AppError
from core.resources.database import client
from core.utils.utils import BaseService


class CartService(BaseService):
    def create(self, user_id):
        new_cart = {
            "_id": ObjectId(),
            "items": [],
            "total_quantity": 0,
            "total_amount": 0.0,
            "is_paid": False,
            "state": "DRAFT",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        try:
            client.db.users.update_one(
                {"_id": ObjectId(user_id)}, {"$push": {"carts": new_cart}}
            )
        except Exception as e:
            self.logger.error("CartService.create_cart(): %s", e)
            raise AppError(500)

        return {"id": str(new_cart["_id"])}

    def get(self, cart_id):
        try:
            user_cart = client.db.users.find_one({"carts._id": ObjectId(cart_id)})
        except Exception as e:
            self.logger.error("CartService.get_cart(): %s", e)
            raise AppError(500)

        if not user_cart:
            err_msg = "Cart not found"
            return [True, err_msg, 404]

        cart = next(cart for cart in user_cart["carts"] if str(cart["_id"]) == cart_id)
        return [False, cart, 200]

    def get_all(self, user_id):
        try:
            user_carts = client.db.users.find_one(
                {"_id": ObjectId(user_id)}, {"carts": 1}
            )
        except Exception as e:
            self.logger.error("CartService.get_all(): %s", e)
            raise AppError(500)

        if not user_carts or "carts" not in user_carts:
            return []

        return user_carts["carts"]
