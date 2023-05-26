from flask import Blueprint, render_template, request, flash, session
from database_source_files.product_database import get_products
from flask_login import  login_required, login_user, current_user
from database_source_files.product_database import my_connection

db_cursor = my_connection.cursor(buffered=True)

views = Blueprint("views", __name__)


@views.route("/", methods= ["GET", "POST"])
@login_required
def home():
    current_user_email = current_user.id
    
    db_cursor.execute("""SELECT * FROM products""")
    result = db_cursor.fetchall()
    if request.method == "POST":
        product_id  = int(request.form.get("product"))
        quantity = int(request.form.get("quantity"))
        current_user_email = current_user.id
        print(f"prod_name: {product_id }, {quantity}")
        product = get_product_from_database(product_id)
        print("product: ",product)
        if product:
            if quantity > 0 and product[2] >= quantity:
                total_price = product[3] * quantity
                update_order_in_database(product_id)
                flash(f"{current_user_email} Order Placed Successfully! Your Total: {total_price}", category="success")
            else:
                flash(f"We are out of stock on {product[1]}! Try a different quantity.", category="error")
        else:
            flash("Invalid product selected! Try again.", category="error")

    return render_template("home.html", currentUser=current_user_email, result=result)

# ... other code ...
def get_product_from_database(product_id):
   
    db_query = "SELECT * FROM products WHERE product_id = %s"
    db_cursor.execute(db_query, (product_id,))
    product = db_cursor.fetchone()
    return product


def update_order_in_database(product_id):
    db_query = "UPDATE products SET product_quantity = product_quantity - 1 WHERE product_id = %s"
    db_cursor.execute(db_query, (product_id,))
    my_connection.commit()




def get_all_product_from_database():
    query = "SELECT * FROM products"
    db_cursor.execute(query)
    products = db_cursor.fetchall()
    
    return products

