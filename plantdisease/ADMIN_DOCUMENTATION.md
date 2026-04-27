# Admin Dashboard Documentation

## Overview
A comprehensive admin dashboard system for the Agricultural Marketplace with full user, order, feedback, and product management capabilities.

## Features

### 1. Admin Login & Authentication
- **Secure Login**: Username and password-based authentication
- **Session Management**: Secure session handling for admin sessions
- **Access Control**: Decorator-based protection on all admin views
- **Logout Functionality**: Secure session termination

**Login Credentials (Default):**
- Username: `admin`
- Password: `admin123`

### 2. Dashboard
The main admin dashboard displays key metrics:
- **Total Users**: Count of registered customers
- **Total Orders**: All orders placed
- **Total Products**: Items in inventory
- **Total Feedback**: Customer reviews
- **Total Revenue**: Sum of all order values
- **Pending Orders**: Orders awaiting processing
- **Average Product Rating**: Overall product satisfaction
- **Recent Orders**: Latest 5 orders with status
- **Recent Feedback**: Latest 5 customer reviews

### 3. User Management
#### Features:
- **View All Users**: List of all registered customers
- **Search Users**: Search by name, email, or phone number
- **User Details**: 
  - Complete user information (ID, name, email, phone, registration date)
  - User's order history with status and amounts
  - User's feedback/reviews on products
  - Total orders count and amount spent

### 4. Order Management
#### Features:
- **View All Orders**: List of all customer orders
- **Filter Orders**: 
  - By status (Pending, Processing, Shipped, Delivered, Cancelled)
  - By search query (order ID, customer name, email)
- **Order Details**:
  - Full order information (ID, customer details, address)
  - Order items list with quantity and pricing
  - Current order status
  - Update order status (change status and save)
- **Status Types**: Pending, Processing, Shipped, Delivered, Cancelled

### 5. Feedback & Reviews Management
#### Features:
- **View All Feedback**: List of customer reviews
- **Filter Feedback**:
  - By product
  - By rating (1-5 stars)
  - By search query (user name, product name, comment text)
- **Feedback Details**:
  - User information
  - Product information with image
  - Rating and comment
  - Submission date and time
- **Delete Feedback**: Remove inappropriate or duplicate reviews

### 6. Product Management
#### Features:
- **View All Products**: Grid view of all products with images
- **Search Products**: By product name
- **Filter by Category**: View products in specific categories
- **Add New Product**:
  - Category selection
  - Product name
  - Weight/Size
  - Price
  - Manufacture and expiry dates
  - Stock quantity
  - Product image upload
- **Edit Products**:
  - Update all product information
  - Change product image
  - Modify pricing and stock
  - View current product image before editing
- **Delete Products**: Remove products from inventory

## URL Routes

### Admin Routes
```
/admin/login/                           - Admin login page
/admin/logout/                          - Admin logout
/admin/dashboard/                       - Main dashboard

/admin/users/                           - Users list
/admin/user/<user_id>/                  - User details and orders

/admin/orders/                          - Orders list
/admin/order/<order_id>/                - Order details

/admin/feedback/                        - Feedback list
/admin/feedback/<feedback_id>/          - Feedback details
/admin/feedback/<feedback_id>/delete/   - Delete feedback

/admin/products/                        - Products list
/admin/product/add/                     - Add new product
/admin/product/<product_id>/edit/       - Edit product
/admin/product/<product_id>/delete/     - Delete product
```

## File Structure

### Backend (Python/Django)
```
myapp/
├── admin_views.py                 # All admin view functions
│   ├── admin_login()
│   ├── admin_logout()
│   ├── admin_dashboard()
│   ├── admin_users()
│   ├── admin_user_detail()
│   ├── admin_orders()
│   ├── admin_order_detail()
│   ├── admin_feedback()
│   ├── admin_feedback_detail()
│   ├── admin_delete_feedback()
│   ├── admin_products()
│   ├── admin_add_product()
│   ├── admin_edit_product()
│   └── admin_delete_product()
└── management/
    └── commands/
        └── create_admin.py            # Create admin user command
```

### Frontend (HTML/CSS Templates)
```
templates/admin/
├── admin_login.html                # Login page
├── admin_dashboard.html            # Main dashboard
├── admin_users.html                # Users list
├── admin_user_detail.html          # User details
├── admin_orders.html               # Orders list
├── admin_order_detail.html         # Order details
├── admin_feedback.html             # Feedback list
├── admin_feedback_detail.html      # Feedback details
├── admin_products.html             # Products list
├── admin_add_product.html          # Add product form
└── admin_edit_product.html         # Edit product form
```

### URL Configuration
```
urls.py                             # Updated with admin routes
```

## Design System

### Colors
- **Primary Green**: #1a472a, #0d2818 (gradient)
- **Accent Green**: #2e7d32 (buttons, highlights)
- **Background**: #f8f9fa (light gray)
- **Danger Red**: #d32f2f (delete buttons)
- **Text**: #2c3e50 (dark), #666 (secondary)

### Layout
- **Sidebar Navigation**: 280px fixed width on desktop
- **Responsive**: Adjusts for tablet (250px sidebar) and mobile (full-width)
- **Grid System**: CSS Grid for responsive layouts

### Typography
- **Font Family**: Segoe UI, Tahoma, Geneva, Verdana, sans-serif
- **Headings**: 700 font-weight
- **Subheadings**: 600 font-weight
- **Body**: 500 font-weight

## Creating an Admin User

### Method 1: Using Management Command
```bash
python manage.py create_admin
```

### Method 2: Using Django Shell
```bash
python manage.py shell
```

Then execute:
```python
from myapp.models import User
from django.contrib.auth.hashers import make_password

admin = User.objects.create(
    username='admin',
    email='admin@example.com',
    name='Admin Name',
    password=make_password('password123'),
    is_staff=True
)
```

## How to Use

### 1. Login
- Navigate to `/admin/login/`
- Enter username: `admin`
- Enter password: `admin123`
- Click "Login to Dashboard"

### 2. Dashboard Overview
- See key statistics and metrics
- View recent orders and feedback
- Quick access to all management sections

### 3. Managing Users
- Click "Users" in sidebar
- Search for specific users
- Click "View Details" to see complete user profile
- View all orders and feedback from that user

### 4. Managing Orders
- Click "Orders" in sidebar
- Filter by status or search by ID/name
- Click "View Details" to see order items
- Update order status using the dropdown
- Track order progression from Pending → Delivered

### 5. Managing Feedback
- Click "Feedback & Reviews" in sidebar
- Filter by product, rating, or search terms
- Click "View" to see full feedback details with product info
- Delete inappropriate feedback using "Delete" button

### 6. Managing Products
- Click "Products" in sidebar
- Search or filter by category
- Click "Add Product" to create new items
- Click "Edit" to modify existing products
- Click "Delete" to remove products
- View product images in grid layout

## Features & Capabilities

### Search & Filter
- **Global Search**: Search across users, orders, products by name/email/ID
- **Advanced Filtering**: Filter by status, category, rating
- **Clear Filters**: Easy filter reset button

### Data Display
- **Statistics Cards**: Key metrics at a glance
- **Tables**: Sortable data in table format
- **Grid Layout**: Visual product display with images
- **Cards**: Detailed feedback cards with ratings

### User Experience
- **Responsive Design**: Works on desktop, tablet, mobile
- **Professional Styling**: Modern, clean interface
- **Intuitive Navigation**: Sidebar menu with clear sections
- **Action Buttons**: Quick access to common operations
- **Confirmation Dialogs**: Safety confirmation for destructive actions

### Security
- **Session-Based Auth**: Secure admin sessions
- **Access Control**: Decorator protection on all views
- **CSRF Protection**: Django CSRF tokens on all forms
- **Input Validation**: Form validation on add/edit operations

## Database Models Used
- **User**: Admin user with is_staff flag
- **Order**: Customer orders with status tracking
- **OrderItem**: Individual items in orders
- **Product**: Product inventory
- **Feedback**: Customer reviews and ratings
- **Category**: Product categories

## Troubleshooting

### Admin Login Issues
- Ensure admin user exists: `python manage.py create_admin`
- Check username/password are correct
- Clear browser cache if session persists

### Missing Data
- Verify products are added to database
- Check user orders exist before viewing
- Ensure feedback is submitted on products

### Page Not Loading
- Check server is running: `python manage.py runserver`
- Verify URLs are properly configured in urls.py
- Check for template syntax errors in browser console

## Future Enhancements
- Export reports (CSV, PDF)
- Bulk operations (delete, update status)
- Advanced analytics and charts
- Email notifications to customers
- Admin activity logging
- Product image gallery management
- Inventory alerts and stock management
- Customer messaging system
