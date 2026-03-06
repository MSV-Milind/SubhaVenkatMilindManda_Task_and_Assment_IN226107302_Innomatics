from fastapi import FastAPI, Query
app = FastAPI()

# data
products = [
    {"id":1, "name":"Wireless Mouse", "price":499, "category":"Electronics", "in_stock":True},
    {"id":2, "name":"Notebook", "price":99, "category":"Stationery", "in_stock":True},
    {"id":3, "name":"USB Hub", "price":799, "category":"Electronics", "in_stock":False},
    {"id":4, "name":"Pen Set", "price":49, "category":"Stationery", "in_stock":True},
    {"id":5, "name":"Laptop Stand", "price":370, "category":"Stationery", "in_stock":True},
    {"id":6, "name":"Mechanical Keyboard", "price":2499, "category":"Electronics", "in_stock":True},
    {"id":7, "name":"Web Cam", "price":1399, "category":"Electronics", "in_stock":False},
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
    in_stock: bool = Query(None, description="True = in stock only")
):
    result = products

    if category:
        result = [p for p in result if p["category"] == category]
    
    if max_price:
        result = [p for p in result if p["price"] <= max_price]

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