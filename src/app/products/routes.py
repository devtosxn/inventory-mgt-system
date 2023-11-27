from app.products.controllers.product import ProductController, ProductDetailController


def init_product_routes(api):
    api.add_resource(ProductController, "/v1/products")
    api.add_resource(ProductDetailController, "/v1/products/<string:product_id>")
