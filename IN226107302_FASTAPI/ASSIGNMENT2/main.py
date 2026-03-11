from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# data
products = [
    {"id":1, "name":"Wireless Mouse", "price":499, "category":"Electronics", "in_stock":True},
    {"id":2, "name":"Notebook", "price":99, "category":"Stationery", "in_stock":True},
    {"id":3, "name":"USB Hub", "price":799, "category":"Electronics", "in_stock":False},
    {"id":4, "name":"Pen Set", "price":49, "category":"Stationery", "in_stock":True},
]

# Endpoint 0 - HOME 
@app.get("/")
def home():
    return {"message":"Welcome to app!"}

# Endpoint 1 - Return all prodcuts
@app.get("/products")
def get_all_products():
    return {"products":products, "total":len(products)}

@app.get("/products/filter")
def filter_products(
    category: str = Query(None, description="Electronics or Stationery"),
    max_price: int = Query(None, description="Maximum price"),
    min_price: int = Query(None, description="Minimum price"), # Q1 Adding Min price 
    in_stock: bool = Query(None, description="True = in stock only")
):
    result = products

    if category:
        result = [p for p in result if p["category"] == category]
    
    if max_price:
        result = [p for p in result if p["price"] <= max_price]

    if min_price:
        result = [p for p in result if p["price"] >= min_price]

    if in_stock is not None:
        result = [p for p in result if p["in_stock"] == in_stock]
    
    return {"filtered_products": result, "count":len(result)}

# Endpoint 4 - Returns instock items
@app.get("/products/instock")
def get_instock():
    result = [i for i in products if i["in_stock"] == True]
    return {"in_stock_products": result, "count": len(result)}

# Endpoint 5 - Summary of store
@app.get("/store/summary")
def get_summary():
    instock_count = 0
    outstock_count = 0
    for i in products:
        if i["in_stock"] == True:
            instock_count += 1
        else:
            outstock_count += 1
    
    categories = [i["category"] for i in products]

    return { "store_name": "My E-commerce Store", "total_products": instock_count + outstock_count, "in_stock": instock_count, 
            "out_of_stock": outstock_count, "categories": list(set(categories)) }

# Endpoint 7 - Return expensive and cheap deals
@app.get("/products/deals")
def get_deals():
    cheap_deal = min(products, key=lambda i:i["price"])
    expensive_deal = max(products, key=lambda i:i["price"])

    return { "best_deal": cheap_deal, "premium_pick": expensive_deal }

# Q4 Endpoint - Gets product summary
@app.get("/products/summary")
def get_product_summary():
    instock_count = 0
    outstock_count = 0
    for i in products:
        if i["in_stock"] == True:
            instock_count += 1
        else:
            outstock_count += 1
    most_expensive = max(products, key=lambda p:p["price"])
    cheapest = min(products, key=lambda p:p["price"])
    categories = list(set(p["category"] for p in products))

    return {
  "total_products":    instock_count+outstock_count,
  "in_stock_count":    instock_count,
  "out_of_stock_count": outstock_count,
  "most_expensive":    {"name":most_expensive["name"],  "price":most_expensive["price"]},
  "cheapest":         {"name":cheapest["name"], "price":cheapest["price"]},
  "categories":       categories
}

# Endpoint 2 - Return one product by its ID
@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return {"product":product}
    return {"error": "Product not found"}

# Endpoint 3 - Returns category items in new page
@app.get("/products/category/{category_name}")
def get_category(category_name: str):
    # result = products
    result = [i for i in products if i["category"] == category_name]
    if not result:
        return {"error": "No products found in this category"}
    return {"category":category_name, "products":result, "total":len(result)}

# Endpoint 6 - Return product by search
@app.get("/products/search/{keyword}")
def get_search(keyword: str):
    results = [i for i in products if keyword.lower() in i["name"].lower()]
    if not results:
        return {"message": "No products matched your search"}
    return {"keyword":keyword, "results":results, "count":len(results)}

# Q2
# Endpoint 8 - Return product name and price
@app.get("/products/{product_id}/price")
def get_product_price(product_id:int):
    for product in products:
        if product["id"] == product_id:
            return {"name":product["name"], "price":product["price"]}
    return {"error": "Product not found"}

# Q3 Pydantic model - CustomerFeedback
class CustomerFeedback(BaseModel):
    customer_name:str = Field(..., min_length=2, max_length=100)
    product_id:int = Field(..., gt=0)
    rating:int = Field(..., ge=1, le=5)
    comment:Optional[str] = Field(None, max_length=300)

feedback = []
# Q3 Endpoint - post feedback
@app.post("/feedback")
def submit_feedback(data: CustomerFeedback):
    feedback.append(data.model_dump())
    return {
        "message": "Feedback submitted successfully",
        "feedback": data.model_dump(),
        "total_feedback": len(feedback)
    }

# Q5 - Pydantic model - OrderItem & BulkOrder
class OrderItem(BaseModel):
    product_id:int = Field(..., gt=0)
    quantity:int = Field(..., ge=1, le=50)

class BulkOrder(BaseModel):
    company_name:str = Field(..., min_length=2)
    contact_email:str = Field(..., min_length=5)
    items:list[OrderItem] = Field(...,min_items=1)

# Endpoint - post orders/bulk
@app.post("/orders/bulk")
def bulk_order(order: BulkOrder):
    confirmed, failed, grand_total = [], [], 0
    for i in order.items:
        product = next((p for p in products if p["id"] == i.product_id), None)
        if not product:
            failed.append({"product_id": i.product_id, "reason": "Product not found"})
        elif not product["in_stock"]:
            failed.append({"product_id": i.product_id, "reason": f"{product['name']} is out of stock"})
        else:
            subtotal = product["price"] * i.quantity
            grand_total += subtotal
            confirmed.append({"product": product["name"], "qty": i.quantity, "subtotal": subtotal})
    return {"company": order.company_name, "confirmed": confirmed,
            "failed": failed, "grand_total": grand_total}

# Bonus question
orders = []
order_counter = 1

# Pydantic model - OrderRequest
class OrderRequest(BaseModel):
    customer_name:    str = Field(..., min_length=2, max_length=100)
    product_id:       int = Field(..., gt=0)
    quantity:         int = Field(..., gt=0, le=100)
    delivery_address: str = Field(..., min_length=10)

# Endpoint - post orders
@app.post("/orders")
def place_order(order_data: OrderRequest):

    global order_counter

    product = None

    for p in products:
        if p["id"] == order_data.product_id:
            product = p
            break

    if not product:
        return {"error":"Product not found"}

    if not product["in_stock"]:
        return {"error":f"{product['name']} is out of stock"}

    total = product["price"] * order_data.quantity

    order = {
        "order_id":order_counter,
        "customer_name":order_data.customer_name,
        "product":product["name"],
        "quantity":order_data.quantity,
        "delivery_address":order_data.delivery_address,
        "total_price":total,
        "status":"pending"
    }

    orders.append(order)

    order_counter += 1

    return {
        "message":"Order placed successfully",
        "order":order
    }

# Endpoint - get orders/{order_id}
@app.get("/orders/{order_id}")
def get_order(order_id:int):
    for i in orders:
        if i["order_id"] == order_id:
            return {"order":i}
    return {"error":"Order not found"}

# Endpoint - add patch
@app.patch("/orders/{order_id}/confirm")
def confirm_order(order_id:int):
    for i in orders:
        if i["order_id"] == order_id:
            if i["status"] == "confirmed":
                return {"message":"Order already confirmed"}
            i["status"] = "confirmed"
            return {
                "message":"Order confirmed",
                "order":i
            }
    return {"error":"Order not found"}