# Phần 7: Quản lý Thư viện chia sẻ trong Linux (Shared Libraries)

Tài liệu này trình bày chi tiết về định nghĩa thư viện chia sẻ (shared libraries), sự khác biệt giữa thư viện động và tĩnh, các vị trí lưu trữ thư viện phổ biến, và cách quản lý chúng bằng các câu lệnh, file cấu hình và biến môi trường trong Linux.

---

## 1. Thư viện chia sẻ (Shared Library) là gì?

- **Thư viện chia sẻ** là các tệp chứa các hàm, chức năng được biên dịch sẵn mà các ứng dụng khác nhau có thể tái sử dụng để tránh việc phải viết lại mã nguồn, giúp giảm dung lượng bộ nhớ của chương trình khi cài đặt và vận hành.
- Các file này thường có định dạng đuôi **`.so`** (Shared Object), tương tự như file `.dll` trên hệ điều hành Windows.

### Phân loại file thư viện trong Linux:
- **Thư viện động (Dynamic library - kết thúc bằng `.so`)**: Chương trình chỉ liên kết và nạp thư viện vào bộ nhớ khi nó bắt đầu chạy hoặc đang chạy (run-time). Hầu hết các ứng dụng hiện đại đều dùng cách này.
- **Thư viện liên kết tĩnh (Statically linked library - kết thúc bằng `.a`)**: Thư viện được nhúng trực tiếp toàn bộ vào file thực thi của chương trình lúc biên dịch (compile-time). Chương trình chạy độc lập không phụ thuộc file bên ngoài, nhưng kích thước file sẽ lớn hơn rất nhiều.

### Các thư mục chứa Shared Libraries phổ biến trên hệ thống:
- **`/lib`**: Thư viện hệ thống cốt lõi cần thiết cho quá trình boot và chạy các lệnh trong `/bin`, `/sbin`.
- **`/usr/lib`**: Thư viện cho các ứng dụng hệ thống thông thường (dành cho hệ thống 32-bit).
- **`/usr/lib64`**: Thư viện dành riêng cho hệ thống 64-bit.
- **`/usr/local/lib`**: Chứa các thư viện tự biên dịch từ mã nguồn hoặc cài đặt thủ công ngoài trình quản lý gói của hệ điều hành.
- **`/usr/share`**: Các tài nguyên chia sẻ không phụ thuộc kiến trúc vi xử lý (tài liệu, icon, file cấu hình...).

---

## 2. Quản lý Thư viện chia sẻ trong Linux

Quản trị viên hệ thống có thể quản lý, kiểm tra mối liên kết phụ thuộc và cấu hình đường dẫn thư viện bằng các công cụ sau:

### Lệnh `ldd`
- **Chức năng:** Liệt kê tất cả các thư viện động phụ thuộc (shared library dependencies) mà một chương trình cụ thể cần để có thể khởi chạy.
- **Ví dụ:** Xem các thư viện cần thiết cho lệnh `ls`:
  ```bash
  ldd /bin/ls
  ```

### Lệnh `ldconfig`
- **Chức năng:** Định cấu hình các liên kết thời gian chạy (run-time bindings) cho các thư viện động.
- Lệnh này thực hiện quét qua các thư mục thư viện đã khai báo, cập nhật các liên kết động mới và tạo bộ đệm cache (lưu tại `/etc/ld.so.cache`) để tối ưu hóa tốc độ tìm kiếm thư viện của hệ thống.
- **Xem danh sách lưu trong cache:**
  ```bash
  ldconfig -p
  ```

### File cấu hình `/etc/ld.so.conf`
- Là file cấu hình chính chứa danh sách các thư mục mà trình liên kết động (dynamic linker) sẽ tìm kiếm các file thư viện `.so`.
- Thường thì file này sẽ bao gồm chỉ thị nạp thêm các file cấu hình phụ nằm trong thư mục `/etc/ld.so.conf.d/` để dễ quản lý.
  *Ví dụ nội dung file:*
  ```text
  include /etc/ld.so.conf.d/*.conf
  ```

### Biến môi trường `LD_LIBRARY_PATH`
- Là một biến môi trường kế thừa, trỏ đến một hoặc nhiều thư mục chứa file thư viện động.
- Trình liên kết động của Linux sẽ **ưu tiên tìm kiếm** thư viện trong các đường dẫn của biến này trước khi tìm kiếm trong các thư mục hệ thống mặc định và cache `/etc/ld.so.cache`.
- Thường dùng khi chạy thử nghiệm phần mềm hoặc chạy phần mềm di động (portable) cần dùng phiên bản thư viện riêng.
- **Cách dùng:**
  ```bash
  export LD_LIBRARY_PATH=/opt/my_custom_app/lib:$LD_LIBRARY_PATH
  ```
