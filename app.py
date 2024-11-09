from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocery.db'
app.config['SECRET_KEY'] = '21f3001344Surya'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    carts = db.relationship('Cart', backref='user', lazy=True)
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    items = db.relationship('CartItem', backref='cart', lazy=True)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)

#Forms
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class EditProductForm(FlaskForm):
    product_name = StringField('Product Name')
    price = FloatField('Price')
    quantity = IntegerField('Quantity')
    submit = SubmitField('Update Product')

#routes
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user is None:
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully. You can now log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already exists. Please choose a different username.', 'danger')
    return render_template('signup.html', form=form)

@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('q')
    
    if search_query:
        # Query products based on the search query
        products = Product.query.filter(Product.name.ilike(f'%{search_query}%')).all()
        return render_template('search_results.html', products=products, search_query=search_query)
    
    flash('Please enter a search query.', 'warning')
    return redirect(url_for('index'))

@app.route('/checkout', methods=['GET'])
@login_required
def checkout():
    # need to implement checkout logic here
    
    flash('Checkout successful!', 'success')
    return redirect(url_for('index'))  # Redirect to the homepage or another appropriate page

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/make_admin/<int:user_id>')
@login_required
def make_admin(user_id):
    if current_user.is_admin:  # Check if the current user is an admin
        user = User.query.get(user_id)
        if user:
            user.is_admin = True
            db.session.commit()
            flash(f'{user.username} is now an admin.', 'success')
        else:
            flash('User not found.', 'danger')
    else:
        flash('You do not have permission to perform this action.', 'danger')
    return redirect(url_for('index'))

@app.route('/admin/users')
@login_required
def admin_users():
    if current_user.is_admin:
        users = User.query.all()
        return render_template('admin_users.html', users=users)
    else:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('index'))

@app.route('/')
@login_required
def index():
    categories = Category.query.all()
    return render_template('index.html', categories=categories)

@app.route('/category/<int:category_id>')
@login_required
def category(category_id):
    category = db.session.get(Category, category_id)
    return render_template('category.html', category=category)

@app.route('/product/<int:product_id>')
@login_required
def product(product_id):
    product = db.session.get(Product, product_id)
    return render_template('product.html', product=product)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    quantity = (request.form.get('quantity'))
    if quantity.isdigit() :
        if product_id is not None :
            quantity = int(request.form.get('quantity'))
            product = Product.query.get(int(product_id))
        #quantity = int(request.form.get('quantity'))
            print("Product ID:", product_id)
            print("Quantity:", quantity)
            if product and quantity > 0 :
                    cart = Cart.query.filter_by(user_id=current_user.id).first()
                    if not cart:
                        cart = Cart(user_id=current_user.id)
                        db.session.add(cart)
                        db.session.commit()
                    cart_item = CartItem(product_id=product.id, quantity=quantity, cart_id=cart.id)
                    db.session.add(cart_item)
                    db.session.commit()
                    flash('Product added to cart successfully.', 'success')
            else:
                flash('Invalid product or quantity.', 'danger')
            return redirect(url_for('cart'))
    else:
        flash('Invalid product ID.', 'danger')
        #return redirect(url_for('index'))
        return redirect(url_for('product', product_id=product_id))

@app.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if cart:
        items = CartItem.query.filter_by(cart_id=cart.id).all()
        products_in_cart = []

        for item in items:
            product = Product.query.get(item.product_id)
            products_in_cart.append((product, item.quantity))

        total_quantity = sum(item.quantity for _, item.quantity in products_in_cart)
        total_amount = sum(product.price * item.quantity for product, item.quantity in products_in_cart)

        return render_template('cart.html', products_in_cart=products_in_cart, total_quantity=total_quantity, total_amount=total_amount)
    else:
        return render_template('cart.html', products_in_cart=[], total_quantity=0, total_amount=0)

@app.route('/remove_from_cart/<int:product_id>', methods=['GET'])
@login_required
def remove_from_cart(product_id):
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if cart: 
        cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
        if cart_item: 
            db.session.delete(cart_item)
            db.session.commit()
            flash('Product removed from cart successfully.')
    return redirect(url_for('cart'))

@app.route('/admin')
@login_required
def admin_index():
    if not current_user.is_admin:
        return redirect(url_for('index'))  # Redirect non-admin users
    categories = Category.query.all()
    return render_template('admin_index.html', categories=categories)

@app.route('/admin/category/<int:category_id>')
@login_required
def admin_category(category_id):
    if not current_user.is_admin:
        return redirect(url_for('index'))  # Redirect non-admin users
    category = db.session.get(Category, category_id)
    return render_template('admin_category.html', category=category)

@app.route('/admin/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    if not current_user.is_admin:
        return redirect(url_for('admin_index'))  # Redirect non-admin users
    
    if request.method == 'POST':
        category_name = request.form.get('category_name')
        if category_name:
            new_category = Category(name=category_name)
            db.session.add(new_category)
            db.session.commit()
            flash('New category added successfully.', 'success')
            return redirect(url_for('admin_index'))
        else:
            flash('Category name is required.', 'danger')
    
    return render_template('add_category.html')  # Remove the category argument


@app.route('/admin/add_product/<int:category_id>', methods=['GET', 'POST'])
@login_required
def add_product(category_id):
    category = Category.query.get_or_404(category_id)
    
    if not current_user.is_admin:
        return redirect(url_for('admin_index'))  # Redirect non-admin users
    
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        price = float(request.form.get('price'))
        quantity = int(request.form.get('quantity'))  # Make sure to convert to int
        
        new_product = Product(name=product_name, price=price, quantity=quantity, category=category)
        db.session.add(new_product)
        db.session.commit()
        flash('New product added successfully.', 'success')
        return redirect(url_for('admin_category', category_id=category.id))
    
    return render_template('add_product.html', category=category)


@app.route('/admin/edit_product/<int:category_id>/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(category_id, product_id):
    category = Category.query.get_or_404(category_id)
    product = Product.query.get_or_404(product_id)

    if not current_user.is_admin:
        return redirect(url_for('admin_index'))  # Redirect non-admin users

    form = EditProductForm()  # Use the EditProductForm class

    if form.validate_on_submit():
        # Update the product details based on the form data
        product.name = form.product_name.data
        product.price = form.price.data
        product.quantity = form.quantity.data
        db.session.commit()
        flash('Product updated successfully.', 'success')
        return redirect(url_for('admin_category', category_id=category.id))

    # Pre-populate the form with the existing product details
    form.product_name.data = product.name
    form.price.data = product.price
    form.quantity.data = product.quantity

    return render_template('edit_product.html', category=category, product=product, form=form)

@app.route('/admin/delete_product/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    db.session.delete(product)
    db.session.commit()
    
    flash('Product deleted successfully', 'success')
    return redirect(url_for('admin_category', category_id=product.category_id))


if __name__ == '__main__':
    app.app_context().push()
    db.create_all()
    app.run(debug=True, use_reloader=False)

