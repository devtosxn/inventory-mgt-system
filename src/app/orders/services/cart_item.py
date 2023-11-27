# from app.orders.models import CartItem
from bson import ObjectId

from app.orders.services.cart import CartService
from app.products.services.product import ProductService
from core.error_handlers import AppError
from core.resources.database import client
from core.utils import BaseService


class CartItemService(BaseService):
    collection = client.db.users
    product_service = ProductService()
    cart_service = CartService()

    # helpers
    def get_user_and_cart(self, user_id, cart_id):
        user = self.collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            err_msg = "User not found"
            # raise AppError(404, "User not found")
            return [True, err_msg, 404]

        cart = next(
            (c for c in user.get("carts", []) if c["_id"] == ObjectId(cart_id)), None
        )
        if not cart:
            err_msg = "Cart not found"
            # raise AppError(404, "Cart not found")
            return [True, err_msg, 404]

        data = {"user": user, "cart": cart}
        return [False, data, 200]

    def calculate_total_quantity(self, cart):
        return sum(item["quantity"] for item in cart.get("items", []))

    def calculate_total_amount(self, cart):
        total_amount = 0
        for item in cart.get("items", []):
            product_id = item.get("product_id")
            [err, product, status_code] = self.product_service.get(product_id)
            total_amount += product["price"] * item["quantity"]
        return total_amount

    def update_cart_totals(self, user_id, cart):
        total_quantity = self.calculate_total_quantity(cart)
        total_amount = self.calculate_total_amount(cart)

        try:
            self.collection.update_one(
                {"_id": ObjectId(user_id), "carts._id": ObjectId(cart["_id"])},
                {
                    "$set": {
                        "carts.$.total_quantity": total_quantity,
                        "carts.$.total_amount": total_amount,
                    }
                },
            )
        except Exception as e:
            self.logger.error("CartItemService.update_cart_totals(): %s", e)
            raise AppError(500)

    def check_stock(self, product_id, product_quantity, cart):
        [err, data, status_code] = self.product_service.get(product_id)
        if err:
            err_msg = data
            return [True, err_msg, status_code]

        product = data
        current_quantity = product.get("quantity", 0)

        if current_quantity - product_quantity < 0:
            err_msg = "Product does not have enough stock"
            return [True, err_msg, 400]

        if current_quantity < product_quantity:
            err_msg = "Product out of stock"
            # raise AppError(400, err_msg)
            return [True, err_msg, 400]

        if cart["state"] == "COMPLETED":
            err_msg = "Cannot add item to completed cart"
            # raise AppError(400, err_msg)
            return [True, err_msg, 400]

        return [False, product, 200]

    def update_product_quantity(self, product_id, product_quantity):
        products_collection = client.db.products
        filter_query = {"_id": ObjectId(product_id)}
        update_query = {"$inc": {"quantity": -product_quantity}}
        products_collection.update_one(filter_query, update_query)

    def get_all(self, user_id, cart_id):
        try:
            [err, data, status_code] = self.get_user_and_cart(user_id, cart_id)
            if err:
                msg = data
                return [True, msg, status_code]
            cart = data.get("cart", [])
            return [False, cart.get("items", []), 200]
        except Exception as e:
            self.logger.error("CartItemService.get_all(): %s", str(e))
            raise AppError(500)

    def get(self, user_id, cart_id, cart_item_id):
        [err, data, status_code] = self.get_user_and_cart(user_id, cart_id)
        if err:
            return [True, data, status_code]

        cart_item = next(
            (
                item
                for item in data["cart"].get("items", [])
                if item["_id"] == ObjectId(cart_item_id)
            ),
            None,
        )
        if not cart_item:
            err_msg = "Cart item not found"
            return [True, err_msg, 404]

        return [False, cart_item, 200]

    def create(self, user_id, cart_id, cart_item_data):
        product_id = cart_item_data.get("product_id")
        product_quantity = cart_item_data.get("quantity")

        if not product_id or not product_quantity:
            self.logger.error(
                "CartItemService.create(): Product ID or quantity not provided"
            )
            err_msg = "Product ID and quanity not provided"
            return [True, err_msg, 400]

        [err, data, status_code] = self.get_user_and_cart(user_id, cart_id)
        if err:
            msg = data
            return [True, msg, status_code]

        user = data.get("user", {})
        cart = data.get("cart", {})

        item_in_cart = None
        for item in cart.get("items", []):
            if item["product_id"] == product_id:
                item_in_cart = item
                break

        if item_in_cart:
            err_msg = "Item already in cart"
            # raise AppError(400, err_msg)
            return [True, err_msg, status_code]

        [err, data, status_code] = self.check_stock(product_id, product_quantity, cart)
        if err:
            msg = data
            return [True, msg, status_code]

        try:
            cart_item_data["_id"] = ObjectId()
            cart["items"].append(cart_item_data)
            self.collection.update_one(
                {"_id": ObjectId(user_id), "carts._id": ObjectId(cart_id)},
                {"$push": {"carts.$.items": cart_item_data}},
            )
            [err, data, status_code] = self.product_service.get(product_id)
            if err:
                err_msg = data
                return [True, err_msg, status_code]
            product = data
            self.update_product_quantity(product["_id"], product_quantity)
            self.update_cart_totals(user_id, cart)

        except Exception as e:
            self.logger.error("CartItemService.create(): %s", e)
            raise AppError(500)

        return [False, None, 201]

    def update(self, user_id, cart_id, cart_item_id, cart_item_data):
        [err, data, status_code] = self.get_user_and_cart(user_id, cart_id)
        if err:
            return [True, data, status_code]

        cart = data["cart"]
        cart_item = next(
            (
                item
                for item in cart.get("items", [])
                if item["_id"] == ObjectId(cart_item_id)
            ),
            None,
        )
        if not cart_item:
            err_msg = "Cart item not found"
            return [True, err_msg, 404]

        # for key, value in cart_item_data.items():
        #     cart_item[key] = value
        new_quantity = cart_item_data.get("quantity")
        if (
            new_quantity is None
            or not isinstance(new_quantity, int)
            or new_quantity < 0
        ):
            err_msg = "Provide a valid positive integer quantity to update"
            return [True, err_msg, 400]

        [err, data, status_code] = self.check_stock(
            cart_item["product_id"], new_quantity, cart
        )
        if err:
            msg = data
            return [True, msg, status_code]

        try:
            cart_item["quantity"] = new_quantity
            self.collection.update_one(
                {"_id": ObjectId(user_id), "carts._id": ObjectId(cart_id)},
                {"$set": {"carts.$.items": cart["items"]}},
            )
            self.update_cart_totals(user_id, cart)
            quantity_difference = new_quantity - cart_item["quantity"]
            self.update_product_quantity(cart_item["product_id"], new_quantity)

        except Exception as e:
            self.logger.error("CartItemService.update(): %s", e)
            raise AppError(500)

        return [False, None, 200]

    def delete(self, user_id, cart_id, cart_item_id):
        [err, data, status_code] = self.get_user_and_cart(user_id, cart_id)
        if err:
            return [True, data, status_code]

        cart = data["cart"]
        cart_item = next(
            (
                item
                for item in cart.get("items", [])
                if item["_id"] == ObjectId(cart_item_id)
            ),
            None,
        )
        if not cart_item:
            err_msg = "Cart item not found"
            return [True, err_msg, 404]

        try:
            self.update_product_quantity(
                cart_item["product_id"], -cart_item["quantity"]
            )

            cart["items"] = [
                item for item in cart["items"] if item["_id"] != cart_item["_id"]
            ]

            self.collection.update_one(
                {"_id": ObjectId(user_id), "carts._id": ObjectId(cart_id)},
                {"$set": {"carts.$.items": cart["items"]}},
            )
            self.update_cart_totals(user_id, cart)
        except Exception as e:
            self.logger.error("CartItemService.delete(): %s", e)
            raise AppError(500)

        return [False, None, 204]
