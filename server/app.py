from models import User, Product, Sales, Stock
from config import Resource, api, app, make_response, jsonify, request, db

class Home(Resource):
    def get(self):
        return {'message': 'Welcome to the BB API'}
    
api.add_resource(Home, '/')

# API methods for accessing API resources from the API server
class Products(Resource):
    def get(self): # GET request method for accessing API resources from the API server
        response_dict = [n.to_dict() for n in Product.query.all()]
        response = make_response(
            response_dict,
            201
        )
        return response
    
    def post(self): 
        data = request.get_json()
        new_product = Product(
            name=data['name'],
            category=data['category'],
            price=data['price'],
            stock_level=data['stock_level']
        )
        db.session.add(new_product)
        db.session.commit()
        response_dict = new_product.to_dict()
        response = make_response(
            response_dict,
            201
        )
        return response
    
api.add_resource(Products, '/products')


class ProductsByID(Resource):
    def put(self, id): # PUT request for products with ID in the database
        product = Product.query.filter_by(id=id).first()
        if not product:
            return {'message': 'Product not found'}, 404
        
        data = request.json 
        for attr in data:
            if hasattr(product, attr):
                setattr(product, attr, data[attr])
            else:
                return {'message': f'Attribute {attr} not found on product'}, 400
        
        db.session.commit()
        
        response_dict = product.to_dict()
        response = make_response(
            response_dict,
            201
        )
        return response

    def delete(self, id):
        product = Product.query.filter_by(id=id).first()
        db.session.delete(product)
        db.session.commit()
        response = make_response(
            {"message": "Product deleted successfully"},
            201
        )
        return response
    
api.add_resource(ProductsByID, '/products/<int:id>')


class Sale(Resource):
    def get(self):
        response_dict = [n.to_dict() for n in Sales.query.all()]
        response =  make_response(
            response_dict,
            201
        )
        return response
    
    def post(self):
      data = request.get_json()
      new_sale = Sales(
          product_id=data['product_id'],
          quantity=data['quantity'],
          total_price=data['total_price']
      )
      product = Product.query.get(data['product_id'])
      if product.stock_level >= data['quantity']:
          product.stock_level -= data['quantity']
          db.session.add(new_sale)
          db.session.commit()
          response_dict = new_sale.to_dict()
          response = make_response(
              response_dict,
              201
          )
          return response
      else:
          return make_response(
              {"message": "Insufficient stock level"},
              400
          )

api.add_resource(Sale, '/sales')

class StockItems(Resource):
    def get(self):
        stock_levels = Product.query.with_entities(Product.id, Product.name, Product.stock_level).all()
        response_dict = [{"id": id, "name": name, "stock_level": stock_level} for id, name, stock_level in stock_levels]
        response = make_response(
            response_dict,
            201
        )
        return response
    
    def post(self):
        data = request.get_json()
        product = Product.query.get(data['product_id'])
        if product:
            product.stock_level += data['quantity_added']
            db.session.commit()
            response = make_response(
                {"message": "Product quantity updated successfully"},
                201
            )
            return response
        else:
            return make_response(
                {"message": "Product not found"},
                404
            )

api.add_resource(StockItems, '/stock')

class ReportSales(Resource):
    def get(self):
        total_sales = db.session.query(db.func.sum(Sales.total_price)).scalar()
        sales_by_product = db.session.query(Product.name, db.func.sum(Sales.quantity)).join(Sales).group_by(Product.name).all()
        response_dict = {"total_sales": total_sales, "sales_by_product": [{"name": name, "quantity": quantity} for name, quantity in sales_by_product]}
        response = make_response(
            response_dict,
            201
        )
        return response
    

api.add_resource(ReportSales, '/sales/report')

class ReportStock(Resource):
    def get(self):
        stock_levels = db.session.query(Product.name, Product.stock_level).all()
        response_dict = [{"name": name, "stock_level": stock_level} for name, stock_level in stock_levels]
        response = make_response(
            response_dict,
            201
        )
        return response

api.add_resource(ReportStock, '/stock/report')

if __name__ == "__main__":
    app.run(debug=True,port=5555)