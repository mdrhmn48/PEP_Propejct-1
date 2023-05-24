from flask import Blueprint, render_template
from database_source_files.product_database import get_products
from flask_login import  login_required, login_user, current_user


views = Blueprint("views", __name__)
# @login_required
@views.route("/", methods= ["GET", "POST"])
def home():
    return render_template("home.html", currentUser=current_user)