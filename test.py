# user.py
from app.database import db
from datetime import datetime
from sqlalchemy import func
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(255), nullable = False)
    last_name = db.Column(db.String(255), nullable = False)
    login_email = db.Column(db.String(255), unique = True, nullable = False) #adding this already as for the email activation functionality
    password = db.Column(db.String(255), nullable = False)  #only the hashed password should be saved here, should it be with __ for security?
    balance = db.Column(db.Float, default=0, nullable = False)
    is_deleted = db.Column(db.Boolean, default=False, nullable = False)
    is_admin = db.Column(db.Boolean, default=False, nullable = False)
    is_active = db.Column(db.Boolean, default=True, nullable = False)
    failed_login_count = db.Column(db.Integer, default=3)
    block_until = db.Column(db.DateTime, nullable = True)
    created_on = db.Column(db.DateTime, default = func.now())

    transactions = db.relationship("Transaction", back_populates="user", cascade = "all,delete")
    products_carts = db.relationship("ProductCart", back_populates="user", cascade = "all,delete")
    orders = db.relationship("Order", back_populates="user", cascade = "all,delete")
    ratings = db.relationship("Rating", back_populates="user", cascade = "all,delete")

#I cant thing of a scenario where we would need to specify balance when creating it so I'm not adding it to init method
    def __init__(self, name : str, last_name : str, login_email : str, password : str, created_on : datetime = None):
        self.name = name
        self.last_name = last_name
        self.login_email= login_email
        self.password = password #when does password hashing happen? probably outside the class
        
    def __repr__(self):
        return f"{self.name} id ({self.id})"
    
# transaction.py
from app.database import db
from datetime import datetime
from sqlalchemy import func
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(255), nullable = False)
    last_name = db.Column(db.String(255), nullable = False)
    login_email = db.Column(db.String(255), unique = True, nullable = False) #adding this already as for the email activation functionality
    password = db.Column(db.String(255), nullable = False)  #only the hashed password should be saved here, should it be with __ for security?
    balance = db.Column(db.Float, default=0, nullable = False)
    is_deleted = db.Column(db.Boolean, default=False, nullable = False)
    is_admin = db.Column(db.Boolean, default=False, nullable = False)
    is_active = db.Column(db.Boolean, default=True, nullable = False)
    failed_login_count = db.Column(db.Integer, default=3)
    block_until = db.Column(db.DateTime, nullable = True)
    created_on = db.Column(db.DateTime, default = func.now())

    transactions = db.relationship("Transaction", back_populates="user", cascade = "all,delete")
    products_carts = db.relationship("ProductCart", back_populates="user", cascade = "all,delete")
    orders = db.relationship("Order", back_populates="user", cascade = "all,delete")
    ratings = db.relationship("Rating", back_populates="user", cascade = "all,delete")

#I cant thing of a scenario where we would need to specify balance when creating it so I'm not adding it to init method
    def __init__(self, name : str, last_name : str, login_email : str, password : str, created_on : datetime = None):
        self.name = name
        self.last_name = last_name
        self.login_email= login_email
        self.password = password #when does password hashing happen? probably outside the class
        
    def __repr__(self):
        return f"{self.name} id ({self.id})"
    
# rating.py
from app.database import db
from sqlalchemy import func


class Rating(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    rating = db.Column(db.Float)
    created_on = db.Column(db.DateTime, default = func.now())

    product = db.relationship("Product", back_populates="ratings")
    user = db.relationship("User", back_populates="ratings")

    def __init__(self, rating, created_on=None):
        self.rating = rating
        self.created_on = created_on

    def __repr__(self):
        pass

  # product_cart.py
from app.database import db
from sqlalchemy import func

class ProductCart(db.Model):
    __tablename__ = 'product_carts'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    created_on = db.Column(db.DateTime, default = func.now())

    user = db.relationship('User', back_populates='products_carts')
    cart_items = db.relationship('CartItem', back_populates='products_carts')

    def __init__(self, created_on=None):
        self.created_on = created_on
        
    def __repr__(self):
        pass

#product.py
from app.database import db
from sqlalchemy import func

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(255), nullable = False)
    description = db.Column(db.String(255), nullable = False)
    price = db.Column(db.Float, nullable = False)
    picture = db.Column(db.String(255), nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    rating = db.Column(db.Float, nullable = True)
    is_available = db.Column(db.Boolean, default = False, nullable = False)
    is_deleted = db.Column(db.Boolean, default = False, nullable = False)
    created_on = db.Column(db.DateTime, default = func.now())

    cart_items = db.relationship("CartItem", back_populates="product")
    order_items = db.relationship("OrderItem", back_populates="product")
    ratings = db.relationship("Rating",back_populates="product")


    def __init__(self, name, description, price, picture, quantity, rating, is_available, is_deleted, created_on=None):
        self.name = name
        self.description = description
        self.price = price
        self.picture = picture
        self.quantity = quantity
        self.created_on = created_on
        self.is_available = is_available
        self.is_deleted = is_deleted
        self.rating = rating

    def __repr__(self):
        return f" Product: {self.name}, price - {self.price}, description - {self.description}"

   # order_item.py
from app.database import db

class OrderItem(db.Model):
    __tablename__ = 'orders_items'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    quantity = db.Column(db.Integer, nullable = False)

    order = db.relationship("Order", back_populates="order_items")
    product = db.relationship("Product", back_populates="order_items")


    def __init__(self, id : int, user_id : int, purchase_price : float):
        self.id = id
        self.user_id = user_id
        self.purchase_price = purchase_price


    def __repr__(self):
        pass

# order.py      
from app.database import db
from datetime import datetime
from sqlalchemy import func

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    purchase_price = db.Column(db.Float, nullable=False)
    created_on = db.Column(db.DateTime, default = func.now())

    user = db.relationship("User", back_populates="orders")
    order_items = db.relationship("OrderItem", back_populates="order")


    def __init__(self, id : int, user_id : int, purchase_price : float, created_on : datetime=None):
        self.id = id
        self.user_id = user_id
        self.purchase_price = purchase_price
        self.created_on = created_on 

    def __repr__(self):
        pass
   # cart_item.py 
from app.database import db
from datetime import datetime

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    products_cart_id = db.Column(db.Integer, db.ForeignKey('product_carts.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer, nullable = False)

    products_carts = db.relationship('ProductCart', back_populates='cart_items')
    product = db.relationship('Product', back_populates='cart_items')
    
    def __init__(self, quantity : int):
        self.quantity = quantity

    def __repr__(self):
        pass
     
Taip pat Reikia sugeneruoti vartotoją "Admin" su  el.paštu admin@admin.com ir slaptažodžiu 123          


