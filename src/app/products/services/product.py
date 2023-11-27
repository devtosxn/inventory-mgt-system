# from app.products.models import Product, ProductCategory, ProductLabel
from datetime import datetime

from bson import ObjectId

from core.error_handlers import AppError
from core.resources.database import client
from core.utils.utils import BaseService


class ProductService(BaseService):
    def create(self, product_data):
        if "quantity" not in product_data:
            err_msg = "Quantity is required when creating a product"
            # raise AppError(400, err_msg)
            return [True, err_msg, 400]

        product_data["in_stock"] = product_data.get("quantity", 0) > 0
        product_data["created_at"] = product_data["updated_at"] = datetime.utcnow()
        try:
            client.db.products.insert_one(product_data)
        except Exception as e:
            self.logger.error("ProductService.create(): %s", str(e))
            raise AppError(500)

        return [False, product_data, 201]

    def get_all(self):
        try:
            products = list(client.db.products.find())
        except Exception as e:
            self.logger.error("ProductService.get_all(): %s", str(e))
            raise AppError(500)

        return products

    def get(self, product_id):
        try:
            product = client.db.products.find_one({"_id": ObjectId(product_id)})
        except Exception as e:
            self.logger.error("ProductService.get(): %s", str(e))
            raise AppError(500)

        if not product:
            err_msg = "Product not found"
            # raise AppError(404, err_msg)
            return [True, err_msg, 404]

        return [False, product, 200]

    def update(self, product_id, update_data):
        update_data["updated_at"] = datetime.utcnow()
        try:
            client.db.products.update_one(
                {"_id": ObjectId(product_id)}, {"$set": update_data}
            )
        except Exception as e:
            self.logger.error("ProductService.update(): %s", str(e))
            raise AppError(500)

    def delete(self, product_id):
        try:
            client.db.products.delete_one({"_id": ObjectId(product_id)})
        except Exception as e:
            self.logger.error("ProductService.delete(): %s", str(e))
            raise AppError(500)
