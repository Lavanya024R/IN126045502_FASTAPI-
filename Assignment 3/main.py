from fastapi import FastAPI, HTTPException

app = FastAPI()

# Products database
products = {
    1: {"name": "Wireless Mouse", "price": 499, "in_stock": True},
    2: {"name": "Notebook", "price": 99, "in_stock": True},
    3: {"name": "USB Hub", "price": 299, "in_stock": False},
    4: {"name": "Pen Set", "price": 49, "in_stock": True}
}

cart = []
orders = []

# Add to cart
@app.post("/cart/add")
def add_to_cart(product_id: int, quantity: int = 1):

    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")

    product = products[product_id]

    if not product["in_stock"]:
        raise HTTPException(status_code=400, detail=f"{product['name']} is out of stock")

    for item in cart:
        if item["product_id"] == product_id:
            item["quantity"] += quantity
            item["subtotal"] = item["quantity"] * product["price"]
            return {"message": "Cart updated", "cart_item": item}

    new_item = {
        "product_id": product_id,
        "product_name": product["name"],
        "quantity": quantity,
        "unit_price": product["price"],
        "subtotal": quantity * product["price"]
    }

    cart.append(new_item)

    return {"message": "Added to cart", "cart_item": new_item}


# View cart
@app.get("/cart")
def view_cart():
    if not cart:
        return {"message": "Cart is empty"}

    total = sum(item["subtotal"] for item in cart)

    return {
        "items": cart,
        "item_count": len(cart),
        "grand_total": total
    }


# Remove item
@app.delete("/cart/{product_id}")
def remove_item(product_id: int):

    for item in cart:
        if item["product_id"] == product_id:
            cart.remove(item)
            return {"message": "Item removed"}

    raise HTTPException(status_code=404, detail="Item not found in cart")


# Checkout
@app.post("/cart/checkout")
def checkout(customer_name: str, delivery_address: str):

    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty — add items first")

    total = sum(item["subtotal"] for item in cart)

    for item in cart:
        order = {
            "customer_name": customer_name,
            "product": item["product_name"],
            "quantity": item["quantity"],
            "total_price": item["subtotal"]
        }
        orders.append(order)

    cart.clear()

    return {
        "message": "Order placed successfully",
        "grand_total": total
    }


# View orders
@app.get("/orders")
def view_orders():
    return {"orders": orders, "total_orders": len(orders)}
