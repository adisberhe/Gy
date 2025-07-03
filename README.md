# 🛋️ Furniture Online Shop

A modern and user-friendly online furniture store built with Django, offering product browsing, categorized listings, cart management, and a streamlined guest checkout experience with email order confirmation.

---

## 🚀 Features

- 🛍️ Admin dashboard to add/manage products with categories
- 🛒 Customers can add products to cart and place orders without logging in
- 📧 Email confirmation sent to customers after placing an order
- 💡 Clean, responsive frontend using Bootstrap and custom CSS/JS

---

## 🛠️ Built With

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Database:** SQLite (default, can be upgraded)
- **Email:** SMTP-based email notifications

---

## 📦 Installation & Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
2. python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. pip install -r requirements.txt

4. python manage.py migrate
python manage.py runserver



Admin Access
1. python manage.py createsuperuser




Email Configuration:

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yourprovider.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your@email.com'
EMAIL_HOST_PASSWORD = 'yourpassword'
