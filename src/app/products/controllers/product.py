from bson import ObjectId
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from app.products.services.product import ProductService
from core.utils import Response


class ProductController(Resource):
    product_service = ProductService()

    def get(self):
        products = self.product_service.get_all()
        serialized_data = [
            {
                **product,
                "_id": str(product["_id"]),
                "created_at": str(product["created_at"]),
                "updated_at": str(product["updated_at"]),
            }
            for product in products
        ]

        return Response(
            success=True,
            message="Products retrieved",
            data=serialized_data,
            status_code=200,
        )

    @jwt_required()
    def post(self):
        data = request.json
        [err, data, status_code] = self.product_service.create(data)
        if err:
            return Response(success=False, message=data, status_code=status_code)
        return Response(
            success=True, message="Product created successfully", status_code=201
        )


class ProductDetailController(Resource):
    product_service = ProductService()

    def get(self, product_id):
        [err, data, status_code] = self.product_service.get(product_id)
        if err:
            return Response(success=False, message=data, status_code=status_code)

        product = data
        serialized_data = {
            **product,
            "_id": str(product["_id"]),
            "created_at": str(product["created_at"]),
            "updated_at": str(product["updated_at"]),
        }

        return Response(
            success=True,
            message="Product retrieved successfully",
            data=serialized_data,
            status_code=200,
        )

    @jwt_required()
    def patch(self, product_id):
        data = request.json
        [err, data, status_code] = self.product_service.update(product_id, data)
        if err:
            return Response(success=False, message=data, status_code=status_code)

        return Response(
            success=True, message="Product updated successfully", status_code=status_code
        )

    @jwt_required()
    def delete(self, product_id):
        [err, data, status_code] = self.product_service.delete(product_id)
        if err:
            return Response(success=False, message=data, status_code=status_code)

        return Response(
            success=True, message="Product deleted successfully", status_code=status_code
        )
