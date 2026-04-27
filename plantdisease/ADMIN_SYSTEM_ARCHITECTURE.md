# Admin Dashboard - System Architecture & Visual Overview

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    ADMIN PORTAL                             │
│                  (http://127.0.0.1:8000)                    │
└─────────────────────────────────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
        ┌───────▼────────┐      ┌──────▼──────┐
        │   Admin Login  │      │   Dashboard │
        │  (auth check)  │      │ (statistics)│
        └───────┬────────┘      └──────┬──────┘
                │                      │
    ┌───────────┴──────────────────────┼────────────────┐
    │                                  │                │
    ▼                                  ▼                ▼
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│  Users   │  │  Orders  │  │ Feedback │  │ Products │  │ Settings │
│ Module   │  │ Module   │  │ Module   │  │ Module   │  │ (Future) │
└──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘
     │             │              │            │
     ├─ List       ├─ List        ├─ List     ├─ List
     ├─ Search     ├─ Filter      ├─ Filter   ├─ Add
     ├─ Details    ├─ Details     ├─ Details  ├─ Edit
     └─ Stats      └─ Update      └─ Delete   └─ Delete
```

## Database Relationships

```
┌─────────────────────────────────────────────────────────────┐
│                    DATABASES MODELS                          │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐
│    User      │
│ (Admin: T/F) │◄─────┐
└──────┬───────┘      │
       │              │
       │    has many  │
       ▼              │
┌──────────────┐      │
│   Feedback   │      │
└──────┬───────┘      │
       │              │
       │    many      │
       ▼              │
┌──────────────┐      │
│   Product    │      │
└──────┬───────┘      │
       │              │
       │    has many  │
       ▼              │
┌──────────────┐      │
│  Category    │      │
└──────────────┘      │
       ▲              │
       │              │
       └──────────────┘
       
┌──────────────┐
│    Order     │──────────────┐
└──────┬───────┘              │
       │ has many             │
       ▼                      │
┌──────────────┐              │
│  OrderItem   │──references──┼─→ Product
└──────────────┘              │
```

## Authentication Flow

```
┌─────────────────────────────────────────────────────────┐
│              ADMIN AUTHENTICATION FLOW                  │
└─────────────────────────────────────────────────────────┘

1. User navigates to /admin/login/
   ↓
2. Enter username & password
   ↓
3. System verifies:
   - User exists
   - is_staff = True
   - Password correct
   ↓
4a. SUCCESS                    4b. FAILURE
   │                               │
   ├→ Create session          └─→ Show error
   ├→ Set session['admin_id']    redirect to login
   ├→ Set session['is_admin']
   └→ Redirect to dashboard

5. For all admin pages:
   ├→ @check_admin decorator
   ├→ Verify session['admin_id']
   ├→ Verify session['is_admin']
   └→ If not admin → redirect to login
```

## Page Navigation Structure

```
┌────────────────────────────────────────────────────────┐
│                  ADMIN SIDEBAR MENU                     │
├────────────────────────────────────────────────────────┤
│  MAIN                                                   │
│  ► Dashboard                                            │
│                                                         │
│  MANAGEMENT                                             │
│  ► Users                                                │
│    └─ Search & select user                             │
│       └─ View user details                             │
│                                                         │
│  ► Orders                                               │
│    └─ Filter & search orders                           │
│       └─ View order details                            │
│          └─ Update status                              │
│                                                         │
│  ► Feedback & Reviews                                   │
│    └─ Filter & search feedback                         │
│       └─ View feedback detail                          │
│          └─ Delete feedback                            │
│                                                         │
│  ► Products                                             │
│    └─ Search & filter products                         │
│       ├─ Add new product                               │
│       ├─ Edit product                                  │
│       └─ Delete product                                │
│                                                         │
│  [Logout Button]                                        │
└────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

### User Management Flow
```
┌─────────────┐
│ Admin Views │
│ /users/     │
└────┬────────┘
     │
     ├─→ Query: User.objects.filter(is_staff=False)
     │
     ├─→ Apply filters/search
     │
     ├─→ Render admin_users.html template
     │
     └─→ Display: User list with search box
     
     User clicks "View Details"
     │
     ├─→ Query: User.objects.get(id=user_id)
     │
     ├─→ Query: Order.objects.filter(user=user)
     │
     ├─→ Query: Feedback.objects.filter(user=user)
     │
     └─→ Render admin_user_detail.html with all data
```

### Order Management Flow
```
┌──────────────┐
│ Admin Views  │
│ /orders/     │
└────┬─────────┘
     │
     ├─→ Query: Order.objects.all()
     │
     ├─→ Apply status filter (if provided)
     │
     ├─→ Apply search filter (if provided)
     │
     ├─→ Render admin_orders.html template
     │
     └─→ Display: Orders table with filters
     
     User clicks "View Details"
     │
     ├─→ Query: Order.objects.get(id=order_id)
     │
     ├─→ Query: order.items.all()
     │
     └─→ Render admin_order_detail.html with items
     
     User updates status and submits form
     │
     ├─→ POST request to admin_order_detail
     │
     ├─→ Validate new_status input
     │
     ├─→ Update: order.status = new_status
     │
     ├─→ Save to database
     │
     └─→ Redirect with success message
```

### Product Management Flow
```
Add Product Flow:
┌──────────────────┐
│ Click Add Button │
└────┬─────────────┘
     │
     ├─→ Load admin_add_product.html
     │
     ├─→ Display: Form with fields
     │
     ├─→ User fills form & uploads image
     │
     ├─→ POST to admin_add_product
     │
     ├─→ Validate all fields
     │
     ├─→ Create: Product object
     │
     ├─→ Save image to /media/products/
     │
     ├─→ Save to database
     │
     └─→ Redirect to products list
     
Edit Product Flow:
(Similar to Add, but with existing data pre-filled)

Delete Product Flow:
┌──────────────────┐
│ Click Delete     │
└────┬─────────────┘
     │
     ├─→ Confirmation dialog
     │
     ├─→ If confirmed:
     │   ├─→ Delete from database
     │   ├─→ Remove image file
     │   └─→ Redirect to products list
     │
     └─→ If cancelled: Stay on page
```

## Response Status Codes

```
Admin Pages Status Codes:
┌──────────────────────────────┐
│ Route             │ Status   │
├──────────────────────────────┤
│ /admin/login/     │ 200 OK   │
│ /admin/dashboard/ │ 200 OK   │
│ /admin/users/     │ 200 OK   │
│ /admin/user/1/    │ 200 OK   │
│ /admin/orders/    │ 200 OK   │
│ /admin/feedback/  │ 200 OK   │
│ /admin/products/  │ 200 OK   │
│ (Non-admin)       │ 302 RDIR │
│ Invalid user      │ 404 ERR  │
└──────────────────────────────┘
```

## Session Management

```
Login Session Lifecycle:
┌─────────────────────────────────────────────┐
│ 1. User accesses /admin/login/              │
│    ├─ Request.session is empty              │
│    └─ Displays login form                   │
│                                             │
│ 2. User submits credentials                 │
│    ├─ Verify username & password            │
│    ├─ Check is_staff = True                 │
│    └─ SUCCESS → Create session              │
│                                             │
│ 3. Session data stored:                     │
│    ├─ session['admin_id'] = user.id         │
│    ├─ session['admin_name'] = user.name     │
│    └─ session['is_admin'] = True            │
│                                             │
│ 4. @check_admin decorator:                  │
│    ├─ Check session['admin_id'] exists      │
│    ├─ Check session['is_admin'] = True      │
│    ├─ YES → Allow access to view            │
│    └─ NO → Redirect to login                │
│                                             │
│ 5. User clicks logout:                      │
│    ├─ request.session.flush()               │
│    ├─ Clear all session data                │
│    └─ Redirect to login page                │
└─────────────────────────────────────────────┘
```

## File Organization

```
Project Structure:
crop/
│
├── myapp/
│   ├── models.py                 (Database models)
│   ├── views.py                  (User views)
│   ├── admin_views.py ★ NEW      (Admin views - 15 functions)
│   ├── urls.py                   (Routes - updated with admin routes)
│   ├── admin.py
│   ├── apps.py
│   │
│   ├── templates/
│   │   ├── [User templates]
│   │   └── admin/ ★ NEW
│   │       ├── admin_login.html
│   │       ├── admin_dashboard.html
│   │       ├── admin_users.html
│   │       ├── admin_user_detail.html
│   │       ├── admin_orders.html
│   │       ├── admin_order_detail.html
│   │       ├── admin_feedback.html
│   │       ├── admin_feedback_detail.html
│   │       ├── admin_products.html
│   │       ├── admin_add_product.html
│   │       └── admin_edit_product.html
│   │
│   └── management/ ★ NEW
│       └── commands/ ★ NEW
│           └── create_admin.py
│
├── ADMIN_DOCUMENTATION.md ★ NEW
├── ADMIN_SETUP_GUIDE.md ★ NEW
├── ADMIN_IMPLEMENTATION.md ★ NEW
└── ADMIN_SYSTEM_ARCHITECTURE.md (this file) ★ NEW
```

## Performance Considerations

```
Database Queries:
┌─────────────────────────────────────┐
│ View          │ Queries            │
├─────────────────────────────────────┤
│ Dashboard     │ 3-4 (aggregate)    │
│ Users List    │ 1 (with search)    │
│ User Detail   │ 3 (user + orders)  │
│ Orders List   │ 1 (with filters)   │
│ Order Detail  │ 2 (order + items)  │
│ Feedback      │ 1 (with filters)   │
│ Products      │ 1 (with images)    │
└─────────────────────────────────────┘

Optimization Tips:
✓ Use select_related for foreign keys
✓ Use prefetch_related for many-to-many
✓ Implement pagination for large lists
✓ Cache dashboard statistics
✓ Use database indexes on search fields
```

## Security Layers

```
┌────────────────────────────────────────────┐
│        SECURITY IMPLEMENTATION              │
├────────────────────────────────────────────┤
│ Layer 1: Login Authentication               │
│ ├─ Username + Password verification        │
│ ├─ is_staff flag check                      │
│ └─ Password hashing (Django default)        │
│                                             │
│ Layer 2: Session Management                 │
│ ├─ Server-side session storage              │
│ ├─ Session timeout (configurable)           │
│ └─ Secure logout with flush()               │
│                                             │
│ Layer 3: Access Control                     │
│ ├─ @check_admin decorator on all views      │
│ ├─ Session validation per request           │
│ └─ Redirect to login if not admin           │
│                                             │
│ Layer 4: CSRF Protection                    │
│ ├─ Django CSRF tokens on all forms          │
│ ├─ {% csrf_token %} in templates            │
│ └─ CSRF validation on POST requests         │
│                                             │
│ Layer 5: Input Validation                   │
│ ├─ Form field validation                    │
│ ├─ Type checking and sanitization           │
│ └─ Confirmation dialogs for actions         │
└────────────────────────────────────────────┘
```

---

**This architecture provides a scalable, secure, and maintainable admin system for the Agricultural Marketplace platform.** 🏗️
