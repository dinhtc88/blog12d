from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Seed danh sách users"

    def handle(self, *args, **kwargs):
        users = [
            ("Phan Thanh Miện", "mienpt", "mienpt@local.com", "pas12345", "member"),
            ("Phạm Thị Huyền", "huyenpt", "huyenpt@local.com", "pas12345", "thu_quy"),
            ("Ngô Xuân Giáp", "giapnx", "giapnx@local.com", "pas12345", "member"),
            ("Nguyễn Bình Dương", "duongnb", "duongnb@local.com", "pas12345", "member"),
            ("Nguyễn Thị Nhung", "nhungnt", "nhungnt@local.com", "pas12345", "member"),
            ("Bùi Thị Linh", "linhbt", "linhbt@local.com", "pas12345", "member"),
            ("Nguyễn Văn Hoàng", "hoangnv", "hoangnv@local.com", "pas12345", "member"),
            ("Nguyễn Thị Trang", "trangnt", "trangnt@local.com", "pas12345", "member"),
            ("Đỗ Thị Ngọc Mai", "maidtn", "maidtn@local.com", "pas12345", "member"),
            ("Đồng Thị Nga", "ngadt", "ngadt@local.com", "pas12345", "lop_truong"),
            ("Hoàng Thị Thơ", "thoht", "thoht@local.com", "pas12345", "member"),
            ("Đỗ Ngọc Duy", "duydn", "duydn@local.com", "pas12345", "member"),
            ("Tô Văn Tới", "toitv", "toitv@local.com", "pas12345", "member"),
            ("Nguyễn Hồng Minh", "minhnh", "minhnh@local.com", "pas12345", "member"),
            ("Nguyễn Thị Thắm", "thamnt", "thamnt@local.com", "pas12345", "member"),
            ("Trần Đăng Khoa", "khoatd", "khoatd@local.com", "pas12345", "member"),
            ("Nguyễn Thị Huyền Trang", "trangnth", "trangnth@local.com", "pas12345", "member"),
            ("Vũ Thị Luyên", "luyenvt", "luyenvt@local.com", "pas12345", "member"),
            ("Lê Văn Thao", "thaolv", "thaolv@local.com", "pas12345", "member"),
            ("Bùi Thi Tuyên", "tuyenbt", "tuyenbt@local.com", "pas12345", "member"),
            ("Phạm Văn Giỏi", "gioipv", "gioipv@local.com", "pas12345", "member"),
            ("Phạm Thị Hiền", "hienpt", "hienpt@local.com", "pas12345", "member"),
            ("Trần Thị Lệ", "lett", "lett@local.com", "pas12345", "member"),
            ("Trần Thị Hường", "huongtt", "huongtt@local.com", "pas12345", "member"),
            ("Nguyễn Văn Duy B", "duybnv", "duybnv@local.com", "pas12345", "member"),
            ("Phạm Thị Nga", "ngapt", "ngapt@local.com", "pas12345", "member"),
            ("Nghiêm Văn Huy", "huynv", "huynv@local.com", "pas12345", "member"),
            ("Vũ Văn Thông", "thongvv", "thongvv@local.com", "pas12345", "member"),
            ("Bùi Thị Hiêng", "hiengbt", "hiengbt@local.com", "pas12345", "member"),
            ("Bùi Thu Hường", "huongbt", "huongbt@local.com", "pas12345", "member"),
            ("Bùi Thị Nhung", "nhungbt", "nhungbt@local.com", "pas12345", "member"),
            ("Nguyễn Thị Tiệp", "tiepnt", "tiepnt@local.com", "pas12345", "member"),
            ("Phạm Doanh Thưởng", "thuongpd", "thuongpd@local.com", "pas12345", "member"),
            ("Đỗ Thành Luân", "luandt", "luandt@local.com", "pas12345", "member"),
            ("Trần Ngọc Viễn", "vientn", "vientn@local.com", "pas12345", "member"),
            ("Nguyễn Văn Duy A", "duyanv", "duyanv@local.com", "pas12345", "member"),
            ("Lưu Thị Phượng", "phuonglt", "phuonglt@local.com", "pas12345", "member"),
            ("Bùi Văn Nghĩa", "nghiabv", "nghiabv@local.com", "pas12345", "member"),
            ("Nguyễn Văn Toản", "toanvn", "toanvn@local.com", "pas12345", "member"),
        ]

        for full_name, username, email, password, role in users:
            if User.objects.filter(username=username).exists():
                self.stdout.write(f"⚠️ {username} đã tồn tại")
                continue

            is_superuser = role == "admin"
            is_staff = role in ["admin", "thu_quy", "lop_truong"]

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )

            user.first_name = full_name
            user.is_staff = is_staff
            user.is_superuser = is_superuser

            # nếu bạn có field role trong model thì bật dòng này
            # user.role = role

            user.save()

            self.stdout.write(self.style.SUCCESS(f"✅ Created {username} ({role})"))