from database import db_session


class ProductsModel(db_session.Model):
    __tablename__ = 'products'

    id = db_session.Column(db_session.Integer, primary_key=True)
    name = db_session.Column(db_session.String())
    price = db_session.Column(db_session.Integer())

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"<Product {self.name}>"
