# Admin Dashboard - Troubleshooting Guide

## Quick Fixes

### Issue 1: Can't Login
**Problem:** "Invalid email or password" even with correct credentials

**Solutions:**
1. Ensure admin user exists:
   ```bash
   python manage.py create_admin
   ```

2. Reset admin password in shell:
   ```bash
   python manage.py shell
   ```
   Then:
   ```python
   from myapp.models import User
   admin = User.objects.get(username='admin')
   admin.set_password('admin123')
   admin.save()
   ```

3. Check username vs email:
   - Login uses **username**, not email
   - Default username: `admin`

### Issue 2: Page Returns 404 (Not Found)

**Problem:** Admin pages show "Page Not Found"

**Solutions:**
1. Check if server is running:
   ```bash
   python manage.py runserver
   ```

2. Verify URLs are in urls.py:
   ```python
   # Should see admin routes imported
   from . import admin_views
   ```

3. Check URL format:
   - `/admin/login/` ✅
   - `/admin_login/` ❌ (wrong)

### Issue 3: Template Not Found

**Problem:** "TemplateDoesNotExist: admin/admin_dashboard.html"

**Solutions:**
1. Verify template files exist:
   ```
   myapp/templates/admin/
   ├── admin_login.html
   ├── admin_dashboard.html
   ├── admin_users.html
   ├── admin_user_detail.html
   ├── admin_orders.html
   ├── admin_order_detail.html
   ├── admin_feedback.html
   ├── admin_feedback_detail.html
   ├── admin_products.html
   ├── admin_add_product.html
   └── admin_edit_product.html
   ```

2. Check TEMPLATES setting in settings.py:
   ```python
   TEMPLATES = [
       {
           'BACKEND': '...',
           'DIRS': [],
           'APP_DIRS': True,  # Must be True
           ...
       }
   ]
   ```

### Issue 4: Access Denied / Redirects to Login

**Problem:** Every admin page redirects to login

**Solutions:**
1. Verify you're logged in:
   - Check browser cookies
   - Try logging out and back in

2. Check session backend in settings.py:
   ```python
   SESSION_ENGINE = 'django.contrib.sessions.backends.db'
   ```

3. Verify is_staff is set:
   ```bash
   python manage.py shell
   ```
   ```python
   from myapp.models import User
   admin = User.objects.get(username='admin')
   print(admin.is_staff)  # Should be True
   ```

### Issue 5: Images Not Uploading

**Problem:** Product image upload fails silently

**Solutions:**
1. Check MEDIA_ROOT and MEDIA_URL in settings.py:
   ```python
   MEDIA_ROOT = BASE_DIR / 'media'
   MEDIA_URL = '/media/'
   ```

2. Verify media directory exists:
   ```bash
   # Should exist:
   crop/media/
   crop/media/products/
   crop/media/category/
   ```

3. Check file permissions:
   ```bash
   # On Windows, ensure folder is writable
   # Right-click folder → Properties → Security → Edit
   ```

4. Verify Django middleware:
   ```python
   # In urls.py for local development
   if settings.DEBUG:
       urlpatterns += static(settings.MEDIA_URL,
                           document_root=settings.MEDIA_ROOT)
   ```

### Issue 6: Search/Filter Not Working

**Problem:** Search returns no results even with matching data

**Solutions:**
1. Check query in URL:
   - Should show: `?search=term`
   - Use form method="GET"

2. Verify model has fields:
   ```python
   # User model must have: name, email, number
   # Product model must have: name, category
   ```

3. Clear cache:
   ```bash
   python manage.py clear_cache
   ```

### Issue 7: Forms Not Submitting

**Problem:** Form submit button doesn't work

**Solutions:**
1. Check CSRF token in form:
   ```html
   <form method="POST">
       {% csrf_token %}  <!-- Must have this -->
       ...
   </form>
   ```

2. Verify form method="POST" for changes:
   ```html
   <!-- For add/edit/delete use POST -->
   <form method="POST">
   
   <!-- For search/filter use GET -->
   <form method="GET">
   ```

3. Check console for JavaScript errors:
   - Open browser DevTools (F12)
   - Check Console tab for errors

### Issue 8: Styles Not Applying

**Problem:** Page looks broken or unstyled

**Solutions:**
1. Clear browser cache:
   - Ctrl+F5 (Windows)
   - Cmd+Shift+R (Mac)

2. Check for CSS errors in console:
   - Open DevTools (F12)
   - Check Network tab for failed CSS loads

3. Verify Django STATIC settings:
   ```python
   STATIC_URL = '/static/'
   STATIC_ROOT = BASE_DIR / 'staticfiles'
   ```

### Issue 9: Slow Admin Pages

**Problem:** Admin pages load slowly

**Solutions:**
1. Check database queries:
   ```bash
   # Use Django Debug Toolbar
   pip install django-debug-toolbar
   ```

2. Optimize common queries:
   - Use select_related for ForeignKey
   - Use prefetch_related for M2M
   - Add database indexes

3. Reduce dashboard aggregations:
   - Cache statistics
   - Use database aggregation

4. Optimize images:
   - Compress before upload
   - Use appropriate formats (JPG, PNG)

### Issue 10: Delete Confirmation Not Working

**Problem:** Clicking delete skips confirmation

**Solutions:**
1. Verify JavaScript onclick attribute:
   ```html
   <a href="..." onclick="return confirm('Sure?');">Delete</a>
   ```

2. Check if JavaScript is disabled:
   - Enable JavaScript in browser

3. Alternative: Server-side confirmation:
   ```python
   # Show confirmation page before deleting
   ```

## Common Error Messages

### "TemplateDoesNotExist"
→ Check template file exists in correct directory

### "No reverse match"
→ Check URL name in urls.py matches template link

### "DatabaseError"
→ Run migrations: `python manage.py migrate`

### "ModuleNotFoundError"
→ Check imports in admin_views.py

### "403 Forbidden"
→ Check CSRF token in form

### "500 Server Error"
→ Check server console for full error

## Server Issues

### Server Won't Start
```bash
# Check port in use
lsof -i :8000  # Mac/Linux

# Use different port
python manage.py runserver 8001
```

### Database Locked
```bash
# Check if another process is using DB
# Stop all Django instances
# Delete .sqlite3-journal file if exists
```

### Import Errors
```bash
# Ensure all modules are installed
pip install -r requirements.txt

# Check PYTHONPATH
export PYTHONPATH=$PWD
```

## Testing Checklist

Before reporting issues, verify:
- ✅ Server is running on port 8000
- ✅ Admin user exists (username: admin)
- ✅ Session backend is configured
- ✅ Templates directory is correct
- ✅ Media directory exists
- ✅ Static files are configured
- ✅ Browser cache is cleared
- ✅ JavaScript is enabled
- ✅ Cookies are allowed
- ✅ CSRF token is present

## Debug Mode

### Enable Debug in settings.py
```python
DEBUG = True  # Already enabled for development

# To add more logging:
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
```

### Check Django Version
```bash
python --version
python -m django --version
# Should be Django 5.1.14
```

### Test Admin Login Directly
```python
# shell: python manage.py shell
from myapp.models import User
from django.contrib.auth.hashers import check_password

admin = User.objects.get(username='admin')
print(admin.email)
print(check_password('admin123', admin.password))
print(admin.is_staff)
```

## Getting Help

If issue persists:

1. **Check Logs:**
   - View full error in server console
   - Check Django error message completely

2. **Verify Installation:**
   - All 11 templates exist in admin folder
   - admin_views.py has all 15 functions
   - urls.py has admin routes imported

3. **Test Minimally:**
   - Test just login first
   - Then test one feature at a time

4. **Check Documentation:**
   - ADMIN_DOCUMENTATION.md
   - ADMIN_SETUP_GUIDE.md
   - ADMIN_SYSTEM_ARCHITECTURE.md

5. **Common Files to Check:**
   - `myapp/admin_views.py`
   - `myapp/urls.py`
   - `myapp/templates/admin/*.html`
   - `mysite/settings.py`
   - `manage.py` file

## Quick Reset

If everything is broken, try:

```bash
# 1. Backup current state
# cp myapp/templates/admin myapp/templates/admin_backup

# 2. Reset database
# rm db.sqlite3

# 3. Recreate database
python manage.py migrate

# 4. Create admin user
python manage.py create_admin

# 5. Restart server
python manage.py runserver
```

## Performance Optimization

### For Slow Dashboards
```python
# Add caching in admin_dashboard view:
from django.views.decorators.cache import cache_page

@cache_page(60)  # Cache for 60 seconds
@check_admin
def admin_dashboard(request):
    ...
```

### For Slow Searches
```python
# Add database indexes in models.py:
class User(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    email = models.EmailField(db_index=True)
```

### For Large Product Lists
```python
# Implement pagination:
from django.core.paginator import Paginator

products = Product.objects.all()
paginator = Paginator(products, 20)  # 20 per page
page_obj = paginator.get_page(request.GET.get('page'))
```

---

## Still Having Issues?

1. Check all 4 documentation files
2. Verify all files were created correctly
3. Ensure no typos in file names
4. Check Django version compatibility
5. Review server console output completely
6. Test with fresh browser in private/incognito mode

**Most issues are resolved by:**
- Restarting Django server
- Clearing browser cache
- Verifying admin user exists
- Checking template file paths
