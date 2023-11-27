from app.orders.services.cart import CartService
from core.error_handlers import AppError
from core.utils import BaseService


class PaymentService(BaseService):
    cart_service = CartService()

    def process_payment(self, cart_id):
        [err, data, status_code] = self.cart_service.get(cart_id)
        if err:
            msg = data
            return [True, msg, status_code]

        cart = data
        if cart.get("total_quantity") == 0:
            err_msg = "Cart is empty. Add items to cart"
            return [True, err_msg, 400]

        if cart.get("is_paid"):
            err_msg = "Payment already processed"
            return [True, err_msg, 400]

        data = {"state": "COMPLETED", "is_paid": True}

        try:
            self.cart_service.update(cart_id, data)
            return [False, None, 200]
        except Exception as e:
            self.logger.error("PaymentService.process_payment(): %s", e)
            raise AppError(500, "Payment failed")
