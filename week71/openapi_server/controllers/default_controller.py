import connexion
import uuid
from typing import Dict, Tuple, Union
from pymongo import MongoClient

from openapi_server.models.product import Product  # noqa: E501
from openapi_server.models.product_input import ProductInput  # noqa: E501
from openapi_server import util

# Kết nối MongoDB
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['shop']
products_collection = db['products']

def _serialize_product(doc):
    return Product(
        id=doc.get("id"),
        name=doc.get("name"),
        description=doc.get("description"),
        price=doc.get("price")
    )

def create_product(body=None):  # noqa: E501
    """Create a product"""
    product_input = body
    if connexion.request.is_json:
        product_input = ProductInput.from_dict(connexion.request.get_json())
    
    new_product = {
        "id": str(uuid.uuid4()),
        "name": product_input.name,
        "description": product_input.description,
        "price": product_input.price
    }
    products_collection.insert_one(new_product)
    
    return _serialize_product(new_product), 201

def delete_product(id):  # noqa: E501
    """Delete a product"""
    result = products_collection.delete_one({"id": id})
    if result.deleted_count == 0:
        return "Product not found", 404
    return "Deleted", 204

def get_product_by_id(id):  # noqa: E501
    """Get a product by ID"""
    doc = products_collection.find_one({"id": id})
    if not doc:
        return "Product not found", 404
    return _serialize_product(doc), 200

def get_products():  # noqa: E501
    """Get all products"""
    docs = products_collection.find({})
    return [_serialize_product(doc) for doc in docs], 200

def update_product(id, body=None):  # noqa: E501
    """Update a product"""
    product_input = body
    if connexion.request.is_json:
        product_input = ProductInput.from_dict(connexion.request.get_json())
    
    update_data = {
        "name": product_input.name,
        "description": product_input.description,
        "price": product_input.price
    }
    
    from pymongo import ReturnDocument
    doc = products_collection.find_one_and_update(
        {"id": id},
        {"$set": update_data},
        return_document=ReturnDocument.AFTER
    )
    
    if not doc:
        return "Product not found", 404
    return _serialize_product(doc), 200
