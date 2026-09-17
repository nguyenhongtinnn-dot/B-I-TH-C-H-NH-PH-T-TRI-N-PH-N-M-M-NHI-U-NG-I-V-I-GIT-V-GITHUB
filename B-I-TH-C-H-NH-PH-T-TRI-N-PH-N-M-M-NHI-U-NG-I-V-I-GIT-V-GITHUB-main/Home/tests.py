from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse, resolve


# ==========================================
# 1. TEST URLS (Kiểm tra định tuyến URL)
# ==========================================
class TestUrls(TestCase):

    def test_homepage_url_resolves(self):
        """Kiểm tra URL trang chủ định tuyến đúng"""
        resolver = resolve('/')
        self.assertIsNotNone(resolver.func)

    def test_admin_url_resolves(self):
        """Kiểm tra URL Admin định tuyến đúng"""
        resolver = resolve('/admin/')
        self.assertIsNotNone(resolver.func)


# ==========================================
# 2. TEST VIEWS & CLIENT (Kiểm tra phản hồi trang)
# ==========================================
class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_homepage_status_code_and_template(self):
        """TC-CLI-01: Kiểm tra trang chủ trả về HTTP 200"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_404_page_for_non_existing_url(self):
        """TC-SYS-02: Kiểm tra đường dẫn rác trả về 404"""
        response = self.client.get('/duong-dan-khong-ton-tai-123/')
        self.assertEqual(response.status_code, 404)


# ==========================================
# 3. TEST AUTHENTICATION & ADMIN INTERFACE
# ==========================================
class TestAdminInterface(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = "testadmin"
        self.password = "AdminPass123!"
        self.superuser = User.objects.create_superuser(
            username=self.username,
            email="admin@example.com",
            password=self.password
        )

    def test_superuser_creation(self):
        """TC-SYS-01: Kiểm tra Superuser được khởi tạo trong Database"""
        self.assertEqual(User.objects.count(), 1)
        self.assertTrue(self.superuser.is_superuser)
        self.assertTrue(self.superuser.is_staff)

    def test_admin_login_success(self):
        """TC-ADM-01: Kiểm tra đăng nhập trang Admin thành công"""
        login_success = self.client.login(
            username=self.username, 
            password=self.password
        )
        self.assertTrue(login_success)
        
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

    def test_admin_login_wrong_password(self):
        """Kiểm tra đăng nhập thất bại khi sai mật khẩu"""
        login_failed = self.client.login(
            username=self.username, 
            password="WrongPassword123"
        )
        self.assertFalse(login_failed)

    def test_admin_add_user_page_no_attribute_error(self):
        """TC-ADM-02: Kiểm tra trang thêm User Admin không bị văng lỗi AttributeError (Python 3.14 bug)"""
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/admin/auth/user/add/')
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_user_redirected_from_admin(self):
        """Kiểm tra người dùng chưa đăng nhập truy cập Admin sẽ bị chuyển hướng sang Login"""
        response = self.client.get('/admin/auth/user/')
        self.assertEqual(response.status_code, 302)


# ==========================================
# 4. TEST DATABASE INTEGRITY & CRUD
# ==========================================
class TestUserDatabaseCRUD(TestCase):

    def test_create_normal_user(self):
        """Kiểm tra tạo người dùng thường (Non-staff)"""
        user = User.objects.create_user(
            username="normaluser",
            password="UserPass123!"
        )
        self.assertEqual(User.objects.filter(username="normaluser").count(), 1)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_update_user_profile(self):
        """Kiểm tra cập nhật thông tin người dùng"""
        user = User.objects.create_user(username="testupdate", password="Pass123!")
        user.first_name = "Nguyen"
        user.last_name = "Tin"
        user.save()

        updated_user = User.objects.get(username="testupdate")
        self.assertEqual(updated_user.first_name, "Nguyen")
        self.assertEqual(updated_user.last_name, "Tin")

    def test_delete_user(self):
        """Kiểm tra xóa người dùng khỏi Database"""
        user = User.objects.create_user(username="testdelete", password="Pass123!")
        user.delete()
        self.assertEqual(User.objects.filter(username="testdelete").count(), 0)