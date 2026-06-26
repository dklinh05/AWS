# Phần 8: Quản lý Gói phần mềm bằng APT và Dpkg (Debian / Ubuntu)

Tài liệu này hướng dẫn cách quản lý các gói phần mềm (packages) trên các hệ điều hành nhân Debian (như Ubuntu, Debian) bằng công cụ quản lý cấp cao **APT** (Advanced Package Tool) và công cụ cấp thấp **Dpkg** (Debian Package).

---

## 1. Trình quản lý gói cấp cao APT (Advanced Package Tool)

**APT** là công cụ quản lý gói phổ biến và mạnh mẽ nhất trên các hệ thống Debian/Ubuntu. Nó tự động xử lý việc tải xuống, cài đặt các gói phần mềm cùng với toàn bộ các gói phụ thuộc (dependencies) liên quan từ các kho lưu trữ trực tuyến (repositories).

### Cơ chế hoạt động của APT:
1. Đọc tệp cấu hình **`/etc/apt/sources.list`** và các tệp trong thư mục `/etc/apt/sources.list.d/`. Tệp này chứa danh sách các địa chỉ máy chủ (repositories) cung cấp phần mềm.
2. Tải danh sách thông tin phần mềm từ các máy chủ này về lưu ở máy cục bộ (gọi là bộ đệm - cache).
3. Thực hiện cài đặt, nâng cấp hoặc gỡ bỏ phần mềm dựa trên thông tin trong bộ đệm.

### Các câu lệnh `apt-get` & `apt-cache` thông dụng:

| Câu lệnh | Chức năng | Ghi chú |
| :--- | :--- | :--- |
| **`/etc/apt/sources.list`** | *File cấu hình* | Liệt kê danh sách các kho lưu trữ (repositories) chính thức. |
| **`apt-get update`** | Cập nhật bộ đệm (cache) | Tải về danh sách phần mềm mới nhất từ kho lưu trữ. Cần chạy trước khi nâng cấp hoặc cài đặt gói mới. |
| **`apt-get upgrade`** | Nâng cấp phần mềm | Nâng cấp các gói phần mềm đã cài đặt trên hệ thống lên phiên bản mới hơn nếu có. |
| **`apt-get dist-upgrade`** | Nâng cấp hệ thống nâng cao | Nâng cấp thông minh, tự động thêm hoặc xóa bỏ các gói phụ thuộc mới nếu phiên bản mới yêu cầu (khác với `upgrade` thông thường). |
| **`apt-get install <tên_gói>`** | Cài đặt gói mới | Ví dụ: `apt-get install chromium-browser` |
| **`apt-get remove <tên_gói>`** | Gỡ cài đặt gói | Xóa gói phần mềm khỏi hệ thống nhưng **vẫn giữ lại** các tệp cấu hình của nó. |
| **`apt-get purge <tên_gói>`** | Gỡ bỏ hoàn toàn | Xóa sạch gói phần mềm cùng toàn bộ các tệp cấu hình liên quan. |
| **`apt-get download <tên_gói>`** | Tải về gói `.deb` | Chỉ tải file gói cài đặt về thư mục hiện tại mà không thực hiện cài đặt. |
| **`apt-cache search <từ_khóa>`** | Tìm kiếm gói | Tìm kiếm phần mềm trong bộ đệm cục bộ dựa trên từ khóa tên hoặc mô tả. |
| **`apt-cache show <tên_gói>`** | Hiển thị thông tin gói | Xem thông tin mô tả cơ bản, phiên bản, dung lượng và nhà phát triển của gói. |
| **`apt-cache showpkg <tên_gói>`** | Xem thông tin kỹ thuật | Hiển thị chi tiết kỹ thuật sâu hơn của gói bao gồm các mối quan hệ phụ thuộc và các gói xung đột. |

---

## 2. Trình quản lý gói cấp thấp Dpkg (Debian Package)

**Dpkg** là công cụ quản lý gói ở cấp độ thấp hơn. Nó làm việc trực tiếp với các tệp tin gói có đuôi `.deb` tải về máy cục bộ.

### Cấu trúc của một gói cài đặt `.deb`:
Một file `.deb` đóng gói sẵn bao gồm:
*   Mã nguồn đã biên dịch hoặc các file thực thi của ứng dụng/tiện ích.
*   Các file cấu hình mặc định.
*   Kịch bản cài đặt (install scripts) hướng dẫn hệ thống vị trí và cách thức copy các file vào HĐH.
*   Danh sách các gói phụ thuộc cần thiết (dependencies).

### Sự khác biệt quan trọng nhất giữa APT và Dpkg:
> [!IMPORTANT]
> - **APT** có khả năng tự động phân tích và tải về toàn bộ các gói phụ thuộc (dependencies) từ internet khi cài đặt một phần mềm.
> - **Dpkg** chỉ cài đặt gói cục bộ bạn cung cấp và **không** tự động tải dependencies. Nếu thiếu gói phụ thuộc, lệnh cài đặt của `dpkg` sẽ báo lỗi và dừng lại.

### Các câu lệnh `dpkg` thông dụng:

- **`dpkg -i <tên_file.deb>`** (hoặc `--install`): Cài đặt một hoặc nhiều gói `.deb` cụ thể từ máy cục bộ.
- **`dpkg -r <tên_gói>`** (hoặc `--remove`): Gỡ bỏ (xóa) một ứng dụng đã cài đặt nhưng **giữ lại** các file cấu hình.
- **`dpkg -P <tên_gói>`** (hoặc `--purge`): Xóa sạch ứng dụng cùng toàn bộ file cấu hình đã được ghi vào hệ thống.
- **`dpkg -l <chuỗi_tên>`** (hoặc `--list`): Liệt kê các gói phần mềm đã cài đặt trên hệ thống khớp với chuỗi tìm kiếm.
- **`dpkg -L <tên_gói>`** (hoặc `--listfiles`): Liệt kê đường dẫn của tất cả các file đã được cài đặt vào hệ thống bởi gói phần mềm đó.
- **`dpkg -S <tên_file_hoặc_đường_dẫn>`** (hoặc `--search`): Tìm kiếm ngược trong cơ sở dữ liệu để xem một file cụ thể trên đĩa thuộc sở hữu của gói phần mềm nào đã cài đặt.
- **`dpkg --info <tên_file.deb>`**: Xem thông tin mô tả chi tiết của một file `.deb` chưa cài đặt.
- **`dpkg --status <tên_gói>`** (hoặc `-s`): Xem trạng thái hiện tại (đã cài đặt hay chưa, phiên bản nào...) của một gói phần mềm (tương tự `--info` nhưng hiển thị ngắn gọn hơn).
- **`dpkg-reconfigure <tên_gói>`**: Chạy lại trình thiết lập cấu hình ban đầu của gói ứng dụng đó (hữu ích khi muốn thay đổi các tùy chọn thiết lập hệ thống như múi giờ, bàn phím, cấu hình mail server...).
