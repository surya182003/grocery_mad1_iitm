# Grocery Store Web Application
by Surya Prakash V - 21f3001344
Welcome to the Grocery Store Web Application! This project is a simple web application for managing a grocery store's inventory and allowing users to add and remove items from their cart.
Created for the submission of MAD - 1 project.

## Table of Contents
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Features](#features)

## Getting Started

### Prerequisites
Before running the application, make sure you have the following tools and software installed:

- Python (3.6 or higher)
- Flask (and its dependencies)
- SQLite or another database system

### Installation
1. Clone this repository to your local machine:
git clone https://github.com/surya182003/grocery_mad1_iitm.git
cd grocery_mad1_iitm

2. Create a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

3. Install the required dependencies:
Flask==2.1.1
Flask-SQLAlchemy==3.0.1
Flask-Login==0.5.0
Flask-WTF==1.0.1
Werkzeug==2.0.1

4. Set up the database:
Open a terminal or command prompt.
Navigate to your project directory, where your app.py files are located.
Run a Python interactive shell or execute the following commands in your terminal:

python
from app import db,app,User, Category, Product, Cart, CartItem
app.app_context().push()
db.create_all()
exit()

5. Run the application:
python app.py
The application should now be running locally at `http://localhost:5000`.

For admin login using this credentials:
URL - `http://localhost:5000/admin`
Username : surya
password: 123

## Usage
- Visit `http://localhost:5000` in your web browser to access the Grocery Store Web Application.
- Explore different categories and products.
- Add items to your cart, remove items, and proceed to checkout.

## Features
- User authentication and authorization (login and registration)
- Browse products by categories
- Add products to the cart
- Remove products from the cart
- Checkout and complete orders (Needs to be done)

- ## Contributing
Contributions to this project are welcome! If you find any issues or have improvements to suggest, feel free to open an issue or submit a pull request.

1. Fork the repository.
2. Create a new branch for your feature: `git checkout -b feature-name`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Open a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
