from app.database import db
from app.models.order import Order
from app.models.user import User
from app.models.rating import Rating
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.rating import Rating
from sqlalchemy import func
from datetime import datetime

def get_orders_by_days_in_range(start_date=None, end_date=None):

    ...



def get_order_items_by_days_in_range(start_date=None, end_date=None):

    ...



def get_sales_by_month():
    month_sales = db.session.query(
        func.date_format(Order.created_on, '%Y-%m').label('month'),
        func.sum(Order.purchase_price).label('total_amount')
    ) \
    .group_by(func.date_format(Order.created_on, '%Y-%m')) \
    .order_by(func.date_format(Order.created_on, '%Y-%m')).all()
   
    return month_sales



def get_best_rated_products(limit=10):
    best_rated_products = db.session.query(
        Product.id.label('product_id'),
        Product.name.label('product_name'),
        Product.price.label('price'),
        func.coalesce(func.avg(Rating.rating), 0).label('rating'),  # Apskaičiuojamas vidutinis įvertinimas
        func.count(Rating.id).label('rating_counts'),  # Skaičiuojamas įvertinimų kiekis
        func.sum(OrderItem.quantity).label('sales_qty'),
        func.sum(Product.price * OrderItem.quantity).label('total_income')
    ) \
    .outerjoin(OrderItem, OrderItem.product_id == Product.id) \
    .outerjoin(Rating, Rating.product_id == Product.id) \
    .group_by(Product.id, Product.name, Product.price) \
    .having(func.sum(OrderItem.quantity) > 0) \
    .order_by(func.coalesce(func.avg(Rating.rating), 0).desc()) \
    .limit(limit).all()

    return best_rated_products



def get_best_sales_products(limit=10):
    best_sales_products = db.session.query(
        Product.id.label('product_id'),
        Product.name.label('product_name'),
        Product.price.label('price'),
        Product.rating.label('rating'),
        func.coalesce(func.avg(Rating.rating), 0).label('rating'),  # Apskaičiuojamas vidutinis įvertinimas
        func.count(Rating.id).label('rating_counts'),  # Skaičiuojamas įvertinimų kiekis
        func.sum(OrderItem.quantity).label('sales_qty'),
        func.sum(Product.price * OrderItem.quantity).label('total_income'),) \
    .join(OrderItem, OrderItem.product_id == Product.id) \
    .outerjoin(Rating, Rating.product_id == Product.id) \
    .group_by(Product.id, Product.name, Product.price) \
    .order_by(func.sum(Product.price * OrderItem.quantity).desc()) \
    .limit(limit).all()
    
    return best_sales_products
