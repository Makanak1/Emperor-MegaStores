# 🛒 Django E-Commerce REST API

A Django REST Framework-based e-commerce backend featuring JWT authentication, session-based cart management, order processing, and Paystack payment verification.

---

## 📁 Project Structure

```
api/
├── users/                  # User authentication & profiles
│   ├── models.py           # Profile model
│   ├── serializers.py      # RegisterSerializer, ProfileSerializer, UserSerializer
│   ├── views.py            # Register, Login, Logout views
│   ├── urls.py             # Auth routes
│   └── admin.py            # Admin registration
├── stores/                 # Products, Cart & Orders
│   ├── models.py           # Category, Product, Cart, CartProduct, Order
│   ├── serializers.py      # All store serializers
│   ├── views.py            # Store, Cart, Checkout views
│   ├── urls.py             # Store routes
│   └── Paystack.py         # Paystack payment helper class
├── api/
│   └── settings.py         # Project settings
└── manage.py
```

---

## ✨ Features

- **User Auth** — Register, login, and logout with JWT tokens
- **Product Catalog** — Full CRUD for products and categories with image support
- **Cart System** — Session-based cart with add, increase, decrease, and remove
- **Order & Checkout** — Place orders with shipping details; auto-generates a unique payment reference
- **Paystack Integration** — Server-side payment verification via Paystack API
- **Media Uploads** — Product and profile image support via Django's media file handling

---

## ⚙️ Requirements

- Python 3.10+
- Django 4.x+
- djangorestframework
- djangorestframework-simplejwt
- Pillow
- requests
- python-dotenv
- dj-database-url

Install all dependencies:

```bash
pip install django djangorestframework djangorestframework-simplejwt \
  Pillow requests python-dotenv dj-database-url
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your_django_secret_key
PAYSTACK_SECRET_KEY=your_paystack_secret_key
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_app_password
```

---

## 🚀 Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/your-username/your-repo.git
cd your-repo

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env and fill in your values

# 5. Apply migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create a superuser
python manage.py createsuperuser

# 7. Run the development server
python manage.py runserver
```

---

## 📡 API Endpoints

### 🔑 Auth — `/api/users/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register/` | Register a new user |
| POST | `/login/` | Login and receive a JWT access token |
| POST | `/logout/` | Logout the current user |

#### Register — Request Body
```json
{
  "fullname": "John Doe",
  "username": "johndoe",
  "email": "john@example.com",
  "phone": "08012345678",
  "gender": "M",
  "password1": "securepassword",
  "password2": "securepassword"
}
```

#### Login — Response
```json
{
  "users": { "first_name": "John" },
  "token": "<jwt_access_token>"
}
```

---

### 🗂️ Categories — `/api/stores/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/categorys/` | List all categories |
| POST | `/categorys/` | Create a new category |
| GET | `/category/<id>/` | Get a category by ID |
| PUT | `/category/<id>/` | Update a category |
| DELETE | `/category/<id>/` | Delete a category |

---

### 📦 Products — `/api/stores/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/products/` | List all products |
| POST | `/products/` | Create a new product |
| GET | `/product/<id>/` | Get product details |
| PUT | `/product/<id>/` | Update a product |
| DELETE | `/product/<id>/` | Delete a product |

---

### 🛒 Cart — `/api/stores/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/addtocart/<id>/` | Add a product to cart (creates cart if none exists) |
| GET | `/mycart/` | View current session cart |
| POST | `/managecart/<id>/` | Modify a cart item |
| POST | `/checkout/` | Checkout and place an order |

#### ManageCart — Request Body

Pass one of the following actions:

```json
{ "action": "increase" }
```
```json
{ "action": "decrease" }
```
```json
{ "action": "remove" }
```

> **Note:** Decreasing a cart item with a quantity of 1 will automatically remove it from the cart.

---

### 🧾 Checkout — `/api/stores/checkout/`

**Method:** `POST`

#### Request Body
```json
{
  "order_by": "John Doe",
  "shipping_address": "12 Example Street, Lagos",
  "mobile": "08012345678",
  "email": "john@example.com",
  "payment_method": "Paystack"
}
```

#### Response
```json
{
  "Message": "Checkout successful",
  "order_id": 1,
  "ref": "abc123XY"
}
```

The `ref` value is used to initiate and verify payment via Paystack.

---

## 💳 Paystack Payment Flow

1. The client calls `/checkout/` — an `Order` is created with a unique `ref` token.
2. The frontend uses the `ref` and `amount` to initiate a Paystack transaction.
3. After the user completes payment, the backend calls `order.verify_payment()`.
4. This hits the Paystack `transaction/verify/{reference}` endpoint and confirms the amount.
5. On success, `payment_complete` is set to `True` on the order.

---

## 🔑 Authentication

This project uses **JWT (JSON Web Tokens)** via `djangorestframework-simplejwt`.

Include the token in all protected request headers:

```
Authorization: Bearer <access_token>
```

Token lifetimes (configurable in `settings.py`):

| Token | Lifetime |
|-------|----------|
| Access token | 5 minutes |
| Refresh token | 1 day |

---

## 🗄️ Database

Defaults to **SQLite** for development. To switch to PostgreSQL or another database, update `DATABASES` in `settings.py` using `dj-database-url`:

```python
import dj_database_url
DATABASES = {
    'default': dj_database_url.parse(os.getenv('DATABASE_URL'))
}
```

---

## 📸 Media Files

Uploaded images are served from `/image/` and stored in the `image/` directory at the project root.

To serve media files during development, add the following to your root `urls.py`:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 📬 Email Configuration

Configured for Gmail SMTP with SSL on port 465. Set `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` in your `.env` file.

> For Gmail, use an **App Password** rather than your account password. See [Google's App Passwords guide](https://support.google.com/accounts/answer/185833).

---

## 🗂️ Data Models

### Profile
| Field | Type | Notes |
|-------|------|-------|
| user | OneToOneField | Links to Django's built-in User |
| fullname | CharField | |
| phone | CharField | |
| gender | CharField | Choices: M / F |
| image | ImageField | Optional |

### Product
| Field | Type | Notes |
|-------|------|-------|
| title | CharField | |
| price | PositiveBigIntegerField | |
| discount_price | PositiveBigIntegerField | Optional |
| category | ForeignKey | Links to Category |
| product_id | UUIDField | Auto-generated, unique |
| is_available | BooleanField | Default: True |
| in_stock | BigIntegerField | |
| main | ImageField | Primary product image |
| photo1–4 | ImageField | Optional additional images |

### Order
| Field | Type | Notes |
|-------|------|-------|
| cart | ForeignKey | Links to Cart |
| order_by | CharField | Customer name |
| order_status | CharField | Pending / Cancel / Complete |
| payment_method | CharField | Paystack / Paypal / Bank Transfer |
| payment_complete | BooleanField | Updated after Paystack verification |
| ref | CharField | Auto-generated payment reference |
| amount | PositiveBigIntegerField | |
| subtotal | PositiveBigIntegerField | |

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).