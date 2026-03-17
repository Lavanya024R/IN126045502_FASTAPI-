from fastapi import FastAPI
import math

app = FastAPI()

# --- Sample Products Data ---
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics"},
    {"id": 2, "name": "USB Hub", "price": 799, "category": "Electronics"},
    {"id": 3, "name": "Notebook", "price": 99, "category": "Stationery"},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery"}
]

# --- Sample Orders Data ---
orders = []

# =====================
# Q1-Q3 endpoints (already existing in main_day6)
# =====================

@app.get("/products/search")
def search_products(keyword: str):
    result = [p for p in products if keyword.lower() in p["name"].lower()]
    if not result:
        return {"message": f"No products found for: {keyword}"}
    return {"total_found": len(result), "products": result}

@app.get("/products/sort")
def sort_products(sort_by: str = "price", order: str = "asc"):
    if sort_by not in ["price", "name"]:
        return {"error": "sort_by must be 'price' or 'name'"}
    reverse = order == "desc"
    sorted_list = sorted(products, key=lambda x: x[sort_by], reverse=reverse)
    return {"sort_by": sort_by, "order": order, "products": sorted_list}

@app.get("/products/page")
def paginate_products(page: int = 1, limit: int = 2):
    total_pages = math.ceil(len(products)/limit)
    start = (page-1)*limit
    end = start+limit
    return {"page": page, "limit": limit, "total_pages": total_pages, "products": products[start:end]}

# =====================
# Q4 - Search Orders
# =====================
@app.get("/orders/search")
def search_orders(customer_name: str):
    result = [o for o in orders if customer_name.lower() in o["customer_name"].lower()]
    if not result:
        return {"message": f"No orders found for: {customer_name}"}
    return {"customer_name": customer_name, "total_found": len(result), "orders": result}

# =====================
# Q5 - Sort Products by Category then Price
# =====================
@app.get("/products/sort-by-category")
def sort_by_category():
    sorted_list = sorted(products, key=lambda x: (x["category"], x["price"]))
    return sorted_list

# =====================
# Q6 - Browse Products (Search + Sort + Pagination)
# =====================
@app.get("/products/browse")
def browse_products(
    keyword: str = None,
    sort_by: str = "price",
    order: str = "asc",
    page: int = 1,
    limit: int = 4
):
    result = products
    # Search
    if keyword:
        result = [p for p in result if keyword.lower() in p["name"].lower()]
    # Sort
    if sort_by not in ["price", "name"]:
        return {"error": "sort_by must be 'price' or 'name'"}
    reverse = order == "desc"
    result = sorted(result, key=lambda x: x[sort_by], reverse=reverse)
    # Pagination
    total = len(result)
    total_pages = math.ceil(total/limit)
    start = (page-1)*limit
    end = start+limit
    paginated = result[start:end]
    return {
        "keyword": keyword,
        "sort_by": sort_by,
        "order": order,
        "page": page,
        "limit": limit,
        "total_found": total,
        "total_pages": total_pages,
        "products": paginated
    }

# =====================
# Root endpoint (to check server)
# =====================
@app.get("/")
def home():
    return {"message": "FastAPI is running"}
