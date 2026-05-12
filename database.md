# MySQL Database Setup & Queries - Blog 12D

Tài liệu này chứa các câu lệnh SQL thuần để khởi tạo cấu trúc cơ sở dữ liệu và các truy vấn cơ bản. Bạn có thể copy các lệnh này vào MySQL Workbench hoặc Terminal để chạy trực tiếp.

## 1. Khởi tạo Cơ sở dữ liệu

```sql
-- Tạo database mới
CREATE DATABASE IF NOT EXISTS blog12d_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE blog12d_db;
```

## 2. Tạo các bảng dữ liệu (Schema)

*Lưu ý: Nếu bạn sử dụng Django, bạn nên ưu tiên chạy `python manage.py migrate`. Tuy nhiên, đây là mã SQL thuần để tham khảo hoặc khởi tạo thủ công.*

```sql
-- 1. Bảng Thông tin người dùng
CREATE TABLE IF NOT EXISTS blog12d_userprofile (
    uid VARCHAR(255) PRIMARY KEY,
    display_name VARCHAR(255) NOT NULL,
    photo_url VARCHAR(500),
    email VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(20) DEFAULT 'member',
    joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    birthday VARCHAR(10)
);

-- 2. Bảng Bài viết Kỷ niệm
CREATE TABLE IF NOT EXISTS blog12d_memorypost (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    image_url VARCHAR(500),
    image_urls JSON,
    author_uid VARCHAR(255),
    author_name VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    tags JSON,
    is_public BOOLEAN DEFAULT TRUE,
    type VARCHAR(20) DEFAULT 'story',
    event_date VARCHAR(20),
    location VARCHAR(255),
    likes INT DEFAULT 0,
    liked_by JSON,
    comment_count INT DEFAULT 0,
    CONSTRAINT fk_post_author FOREIGN KEY (author_uid) REFERENCES blog12d_userprofile(uid) ON DELETE CASCADE
)

-- 3. Bảng Bình luận
CREATE TABLE IF NOT EXISTS blog12d_comment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT NOT NULL,
    author_uid VARCHAR(255),
    author_name VARCHAR(255) NOT NULL,
    author_photo_url VARCHAR(500),
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    parent_comment_id VARCHAR(255),
    reply_to_name VARCHAR(255),
    CONSTRAINT fk_comment_post FOREIGN KEY (post_id) REFERENCES blog12d_memorypost(id) ON DELETE CASCADE,
    CONSTRAINT fk_comment_author FOREIGN KEY (author_uid) REFERENCES blog12d_userprofile(uid) ON DELETE CASCADE
);

-- 4. Bảng Giao dịch Quỹ lớp
CREATE TABLE IF NOT EXISTS blog12d_fundtransaction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(10) NOT NULL, -- 'thu' hoặc 'chi'
    amount DECIMAL(12, 2) NOT NULL,
    description VARCHAR(500) NOT NULL,
    date DATETIME NOT NULL,
    author_name VARCHAR(255) NOT NULL,
    details JSON
);

-- 5. Bảng Sự kiện Lịch
CREATE TABLE IF NOT EXISTS blog12d_calendarevent (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    type VARCHAR(20) NOT NULL,
    location VARCHAR(255),
    description TEXT
);

-- 6. Bảng Thông báo
CREATE TABLE IF NOT EXISTS blog12d_notification (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recipient_uid VARCHAR(255) NOT NULL,
    sender_name VARCHAR(255) NOT NULL,
    sender_uid VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    target_id VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT FALSE
);
```

## 3. Các truy vấn dữ liệu mẫu (Queries)

Dưới đây là các câu lệnh truy vấn thường dùng để kiểm tra dữ liệu:

### Lấy danh sách bài viết mới nhất
```sql
SELECT title, author_name, created_at 
FROM blog12d_memorypost 
WHERE is_public = TRUE 
ORDER BY created_at DESC;
```

### Tính tổng số dư Quỹ lớp (Thu - Chi)
```sql
SELECT 
    SUM(CASE WHEN type = 'thu' THEN amount ELSE 0 END) AS TongThu,
    SUM(CASE WHEN type = 'chi' THEN amount ELSE 0 END) AS TongChi,
    (SUM(CASE WHEN type = 'thu' THEN amount ELSE 0 END) - SUM(CASE WHEN type = 'chi' THEN amount ELSE 0 END)) AS SoDu
FROM blog12d_fundtransaction;
```

### Lấy tất cả bình luận của một bài viết cụ thể
```sql
SELECT author_name, content, created_at 
FROM blog12d_comment 
WHERE post_id = 1 
ORDER BY created_at ASC;
```

### Kiểm tra thông báo chưa đọc của một User
```sql
SELECT COUNT(*) as UnreadCount 
FROM blog12d_notification 
WHERE recipient_uid = 'UID_CUA_BAN' AND is_read = FALSE;
```

---
**Chú ý:** Khi kết nối ứng dụng Django với server mới, hãy đảm bảo bạn đã cung cấp đúng `HOST`, `USER`, và `PASSWORD` trong file `.env` hoặc `settings.py`.
