from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# List to store orders (Temporary Database)
final_cafe_orders = [] 

# Menu Items Data
MENU_ITEMS = [
    {"name": "Latte", "price": 120, "image": "latte.png"},
    {"name": "Cappuccino", "price": 140, "image": "cappuccino.png"},
    {"name": "Espresso", "price": 100, "image": "espresso.png"},
    {"name": "Mocha", "price": 160, "image": "mocha.png"},
    {"name": "Pizza", "price": 300, "image": "pizza.png"},
]

# 1. Login Page Route (Table detection added)
@app.route('/')
def login():
    # Agar QR scan hua hai toh URL mein table number hoga (e.g., /?table=3)
    # Agar nahi hai toh default "Counter" rahega
    table_no = request.args.get('table', 'Counter') 
    return render_template('login.html', table_no=table_no)

# 2. Menu Page Route (Table data transfer)
@app.route('/menu', methods=['GET', 'POST'])
def menu():
    user_name = request.form.get('name') or request.args.get('name') or "Guest"
    # Hidden input se table number nikalna
    table_no = request.form.get('table_no') or "Counter"
    
    print(f"\n**********************************************")
    print(f">>> ALERT: Order Request from Table: {table_no} <<<")
    print(f">>> User: {user_name}                          <<<")
    print(f"**********************************************\n")
    
    return render_template('menu.html', name=user_name, table_no=table_no, menu=MENU_ITEMS)

# 3. Place Order Route (Saving Table info in Order)
@app.route('/place_order', methods=['POST'])
def place_order():
    data = request.get_json(force=True)
    if data:
        # data mein ab 'table' key bhi hogi jo frontend se aayegi
        final_cafe_orders.append(data)
        print(f"DEBUG: Naya Order Table {data.get('table')} se aaya -> {data}")
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 400

# 4. Admin Dashboard Route
@app.route('/admin')
def admin_dashboard():
    return render_template('admin.html', orders=list(final_cafe_orders))

# 5. Complete/Delete Order Route
@app.route('/complete_order/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    try:
        if 0 <= order_id < len(final_cafe_orders):
            removed_order = final_cafe_orders.pop(order_id)
            print(f"DONE: Order for {removed_order['customer']} removed.")
            return jsonify({"status": "success"})
    except Exception as e:
        print(f"Delete Error: {e}")
        return jsonify({"status": "error"}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)