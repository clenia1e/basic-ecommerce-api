from flask import Flask
from flask import request
from flask.wrappers import Response

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/ecommerce_api"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class ProductsModel(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    price = db.Column(db.Integer())
    

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"<Product {self.name}>"

@app.route('/products', methods=['POST','GET'])
def handle_products():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_product = ProductsModel(name=data['name'], price=data['price'])
            db.session.add(new_product)
            db.session.commit()
            return {"message": f"Product {new_product.name} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        products = ProductsModel.query.all()
        results = [
            {
                "name": product.name,
                "price": product.price
            } for product in products]

        return {"count": len(results), "products": results}

@app.route('/products/<product_id>', methods=[ 'GET', 'PUT', 'DELETE'])
def handle_product(product_id):
    product = ProductsModel.query.get_or_404(product_id)

    if request.method == 'GET':
        response ={
                "name": product.name,
                "price": product.price
            } 
        return {"message": "sucess", "product": response}
    
    elif request.method == 'PUT':
        data = request.get_json()
        product.name = data['name']
        product.price = data['price']
        db.session.add(product)
        db.session.commit()
        return {"message": f"product {product.name} successfully updated"}

    elif request.method == 'DELETE':
        db.session.delete(product)
        db.session.commit()
        return {"message": f"Car {product.name} successfully deleted."}