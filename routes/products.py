from flask import request, make_response
import json
from sqlalchemy.orm.exc import NoResultFound as NotFound
from database import db_session
from models.product import ProductsModel


def _response(data, code):
    return make_response(json.dumps(data, ensure_ascii=False), code)


def init_app(app):
    @ app.route('/products', methods=['GET'])
    def get_products():
        products = ProductsModel.query.all()
        results = dict(count=len(products),
                       products=[{"name": product.name,
                                  "price": product.price}
                                 for product in products])
        return _response(results, 200)

    @ app.route('/products', methods=['POST'])
    def create_products():
        data = request.get_json()
        if not data['name'] or not data['price']:
            return _response({"message": "Bad request"}, 400)

        new_product = ProductsModel(name=data['name'], price=data['price'])
        db_session.session.add(new_product)
        db_session.session.commit()

        return _response({"message": f"Product {new_product.name} has been created successfully."}, 200)

    @ app.route('/products/<product_id>', methods=['GET'])
    def get_product(product_id):
        try:
            product = ProductsModel.query.get_or_404(product_id)
            return _response(product.to_dict(), 200)
        except NotFound:
            return _response({"message": "Produto não encontrado"}, 404)

    @ app.route('/products/<product_id>', methods=['PUT'])
    def update_product(product_id):
        try:
            product = ProductsModel.query.get_or_404(product_id)
            data = request.get_json()
            {product.update(db_session, key, value)
             for (key, value) in data.items()}
            return _response({"message": f"product {product.name} successfully updated"}, 200)
        except NotFound:
            return _response({"message": "Produto não encontrado"}, 404)

    @ app.route('/products/<product_id>', methods=['DELETE'])
    def delete_product(product_id):
        try:
            product = ProductsModel.query.get_or_404()
            db_session.removeProduct(product)
            return _response({"message": f"Car {product.name} successfully deleted."}, 200)
        except NotFound:
            return _response({"message": "Produto não encontrado"}, 404)
