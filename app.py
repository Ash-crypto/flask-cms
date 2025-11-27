# ------------------------------------------------------
# CLEAN + FIXED Flask CMS Application
# ------------------------------------------------------

import os
import re
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user, logout_user,
    login_required, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash


# ------------------------------------------------------
# APP CONFIG
# ------------------------------------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_FILE = os.path.join(BASE_DIR, "cms.sqlite")

app = Flask(__name__)
app.config["SECRET_KEY"] = "replace_this_with_env_secret"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_FILE}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"


# ------------------------------------------------------
# MODELS
# ------------------------------------------------------
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="user")  # "admin" or "user"


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(300))
    email = db.Column(db.String(200))
    phone = db.Column(db.String(30))
    job = db.Column(db.String(120))
    salary = db.Column(db.Float)


# ------------------------------------------------------
# LOGIN LOADER
# ------------------------------------------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ------------------------------------------------------
# HELPER FUNCTIONS
# ------------------------------------------------------
def valid_password(pw: str) -> bool:
    """Validate strong password rules."""
    if (len(pw) < 6 or
        not re.search(r"[A-Z]", pw) or
        not re.search(r"[a-z]", pw) or
        not re.search(r"\d", pw) or
        not re.search(r"[!@#$%^&*(),.?\":{}|<>]", pw)):
        return False
    return True


def first_user_exists() -> bool:
    return User.query.count() > 0


def admin_required(fn):
    """Admin-only route decorator."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return login_manager.unauthorized()
        if current_user.role != "admin":
            flash("Admin access required.", "warning")
            return redirect(url_for("dashboard"))
        return fn(*args, **kwargs)
    return wrapper


# ------------------------------------------------------
# ROUTES
# ------------------------------------------------------
@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if first_user_exists() and (not current_user.is_authenticated or current_user.role != "admin"):
        flash("Registration disabled. Ask an admin to create your account.", "warning")
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        if not valid_password(password):
            flash("Password must be strong (upper, lower, digit, special char).", "danger")
            return render_template("register.html")

        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "danger")
            return render_template("register.html")

        hashed = generate_password_hash(password)

        role = "admin" if not first_user_exists() else "user"
        if current_user.is_authenticated and current_user.role == "admin":
            role = request.form.get("role", "user")

        user = User(name=name, email=email, password=hashed, role=role)
        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        user = User.query.filter(
            (User.email == username.lower()) | (User.name.ilike(username))
        ).first()

        if not user or not check_password_hash(user.password, password):
            flash("Invalid username/email or password.", "danger")
            return render_template("login.html")

        login_user(user)
        flash("Logged in successfully!", "success")
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.", "info")
    return redirect(url_for("home"))


@app.route("/dashboard")
@login_required
def dashboard():
    total_customers = Customer.query.count()
    return render_template("dashboard.html", total_customers=total_customers)


# ------------------------------------------------------
# CUSTOMER CRUD
# ------------------------------------------------------
@app.route("/customers")
@login_required
def customers():
    all_customers = Customer.query.order_by(Customer.id.desc()).all()
    return render_template("customer_list.html", customers=all_customers)


@app.route("/customers/add", methods=["GET", "POST"])
@login_required
def add_customer():
    if request.method == "POST":
        name = request.form["name"].strip()
        salary = request.form.get("salary", "").strip()

        if not name:
            flash("Customer name is required.", "danger")
            return render_template("add_customer.html")

        # Convert salary safely
        try:
            salary_val = float(salary) if salary else None
        except ValueError:
            flash("Invalid salary!", "danger")
            return render_template("add_customer.html")

        new_cust = Customer(
            name=name,
            address=request.form.get("address"),
            email=request.form.get("email"),
            phone=request.form.get("phone"),
            job=request.form.get("job"),
            salary=salary_val
        )
        db.session.add(new_cust)
        db.session.commit()

        flash("Customer added.", "success")
        return redirect(url_for("customers"))

    return render_template("add_customer.html")


@app.route("/customers/edit/<int:c_id>", methods=["GET", "POST"])
@login_required
def edit_customer(c_id):
    cust = Customer.query.get_or_404(c_id)

    if request.method == "POST":
        cust.name = request.form.get("name", cust.name).strip()
        cust.address = request.form.get("address", cust.address)
        cust.email = request.form.get("email", cust.email)
        cust.phone = request.form.get("phone", cust.phone)
        cust.job = request.form.get("job", cust.job)

        salary = request.form.get("salary", "")
        try:
            cust.salary = float(salary) if salary else None
        except ValueError:
            flash("Invalid salary!", "danger")
            return render_template("edit_customer.html", customer=cust)

        db.session.commit()
        flash("Customer updated.", "success")
        return redirect(url_for("customers"))

    return render_template("edit_customer.html", customer=cust)


@app.route("/customers/delete/<int:c_id>", methods=["POST"])
@admin_required
def delete_customer(c_id):
    cust = Customer.query.get_or_404(c_id)
    db.session.delete(cust)
    db.session.commit()
    flash("Customer deleted.", "info")
    return redirect(url_for("customers"))


# ------------------------------------------------------
# RUN APP (FINAL FIXED BLOCK)
# ------------------------------------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("✔ Database ready.")

    app.run(debug=True)
