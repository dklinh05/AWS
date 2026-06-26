# Phần 4: Thay đổi Runlevels / Boot Targets và Shutdown hoặc Khởi động lại Linux (Exam 101)

Tài liệu này hướng dẫn cách kiểm tra và chuyển đổi giữa các Runlevel (trong hệ thống SysV init cũ) và các Target (trong hệ thống Systemd mới), cách tắt/khởi động lại hệ điều hành, cấu hình Default Boot Target, và cách gửi thông báo đến các người dùng đang đăng nhập.

---

## 1. Quản lý Runlevel (Hệ thống SysV init cũ)

Dù hầu hết các hệ điều hành Linux hiện đại sử dụng Systemd, các lệnh quản lý Runlevel cũ vẫn được hỗ trợ và thường xuất hiện trong các bài thi chứng chỉ như LPIC-1.

### Các lệnh sử dụng Runlevel:
- **`runlevel`**: Hiển thị runlevel trước đó và runlevel hiện tại của hệ thống.
- **`telinit`**: Thay đổi tức thời từ runlevel này sang runlevel khác.
  - *Ví dụ:* `telinit 3` (chuyển sang chế độ dòng lệnh) hoặc `telinit 6` (khởi động lại hệ thống).

### Thay đổi Runlevel khi khởi động lại hệ điều hành (GRUB):
Trong trường hợp hệ thống gặp lỗi không thể vào được giao diện đồ họa, ta có thể thay đổi runlevel ngay từ menu khởi động GRUB:
1. Khi máy tính bắt đầu khởi động, nhấn một phím bất kỳ để dừng quá trình tự động boot của GRUB.
2. Tại màn hình menu GRUB, di chuyển vệt sáng chọn dòng Kernel muốn khởi động.
3. Nhấn phím **`a`** (trên GRUB Legacy) hoặc phím **`e`** (trên GRUB 2) để chỉnh sửa dòng lệnh nạp nhân (kernel boot arguments).
4. Thêm đối số vào cuối dòng kernel bằng cách nhập số của runlevel mong muốn (ví dụ: cắm thêm số `1` hoặc `3` hoặc chữ `single`).
5. Nhấn `Enter` hoặc `Ctrl+X` để boot vào hệ thống với runlevel vừa chọn.

---

## 2. Tìm hiểu về Systemd Targets

Trong hệ thống Systemd, khái niệm **Runlevel** được thay thế bằng các **Target Units** (có đuôi là `.target`).

### Mục đích của System Target:
- **Target** là một unit đặc biệt dùng để nhóm và đồng bộ hóa các unit khác (dịch vụ, điểm mount...) khi máy tính khởi động hoặc chuyển đổi trạng thái.
- Target đóng vai trò như một "cột mốc" giúp đưa hệ điều hành về một trạng thái hoạt động mong muốn.
  - *Ví dụ:* Chuyển Linux sang giao diện dòng lệnh dùng `multi-user.target`, chuyển sang giao diện đồ họa dùng `graphical.target`.
- Các dịch vụ (services) sẽ tự động liên kết với một target cụ thể để xác định xem chúng có được chạy trong môi trường đó hay không.

### Các loại Targets phổ biến:
- **`multi-user.target`**: Hệ thống đa người dùng, tương đương với **Runlevel 3** trong SystemV init. Chế độ này cho phép nhiều người dùng đăng nhập đồng thời qua giao diện dòng lệnh (CLI).
- **`graphical.target`**: Hệ thống đa người dùng có hỗ trợ giao diện đồ họa (GUI), tương đương với **Runlevel 5** trong SystemV init.
- **`rescue.target`**: Đưa hệ thống vào chế độ cứu hộ cơ bản (Rescue Shell), đã mount các file system cần thiết và cung cấp shell sửa lỗi cho quản trị viên đăng nhập bằng quyền root.
- **`basic.target`**: Trạng thái cơ bản của hệ thống, được sử dụng làm bước trung gian trong quá trình boot Linux trước khi hệ thống chuyển sang target mặc định.
- **`sysinit.target`**: Chịu trách nhiệm khởi tạo hệ thống (system initialization) như mount các file system ảo, cấu hình bộ mã hóa, kiểm tra ổ đĩa...
- **Tài liệu hướng dẫn tra cứu:**
  - `man 5 systemd.target`: Hướng dẫn chi tiết cách cấu hình và khai báo một target unit.
  - `man 7 systemd.special`: Liệt kê tài liệu và định nghĩa của toàn bộ các target units đặc biệt có sẵn trong hệ thống.

---

## 3. Các lệnh kiểm tra và thay đổi Target trong Systemd

| Câu lệnh | Chức năng |
| :--- | :--- |
| **`systemctl list-unit-files -t target`** | Hiển thị tất cả các unit files dạng target hiện có trong hệ điều hành. |
| **`systemctl list-units -t target`** | Hiển thị tất cả các target units hiện đang được nạp (loaded) và kích hoạt (active). |
| **`systemctl get-default`** | Xem target mặc định (default target) đang được thiết lập khi boot máy. |
| **`systemctl set-default <target>`** | Thay đổi target mặc định của hệ thống sang target khác (Ví dụ: `systemctl set-default multi-user.target`). |
| **`systemctl isolate <target>`** | Thay đổi tức thời trạng thái hệ điều hành sang một target khác mà không cần reboot (tương tự như `telinit`). |
| **`systemctl rescue`** | Đưa hệ thống vào chế độ single-user để sửa lỗi bằng quyền root (tương tự `telinit 1`). |
| **`systemctl reboot`** | Khởi động lại hệ điều hành (bằng cách gọi `reboot.target`). |
| **`systemctl poweroff`** | Tắt nguồn máy tính (bằng cách cô lập hệ thống chuyển đến `poweroff.target`). |

---

## 4. Các lệnh Tắt máy (Shutdown) và Khởi động lại (Reboot)

Linux cung cấp nhiều cách khác nhau để thực hiện tắt máy và khởi động lại, từ các câu lệnh truyền thống cho tới lệnh của Systemd.

### Khởi động lại (Reboot):
Bạn có thể sử dụng một trong các lệnh sau để reboot hệ thống:
- `reboot`
- `telinit 6`
- `shutdown -r now` (Khởi động lại ngay lập tức)
- `systemctl isolate reboot.target` hoặc `systemctl reboot`

### Tắt máy (Shutdown / Poweroff):
Bạn có thể sử dụng một trong các lệnh sau để tắt máy:
- `poweroff`
- `shutdown -h now` hoặc `shutdown -h +1` (Tắt hệ thống sau 1 phút nữa).
- `systemctl isolate poweroff.target` hoặc `systemctl poweroff`

### Gửi thông báo đến người dùng (`wall`):
- Khi chuẩn bị tắt máy hoặc khởi động lại hệ thống máy chủ, bạn nên thông báo cho tất cả các user đang đăng nhập biết để họ lưu lại công việc.
- **Lệnh:** `wall` (write all)
- **Cách dùng:** Nhập lệnh `wall`, sau đó soạn nội dung thông điệp. Khi soạn xong, nhấn tổ hợp phím **`Ctrl + D`** để gửi thông báo đi.
  *Ví dụ:*
  ```bash
  wall
  He thong se bao tri va khoi dong lai sau 5 phut. Vui long luu lai cong viec!
  <Ctrl+D>
  ```

### Trình quản lý nguồn điện `acpid` (Advanced Configuration and Power Interface daemon):
- Là dịch vụ chạy ngầm (daemon) ghi nhận và xử lý các sự kiện liên quan đến nút nguồn vật lý hoặc trạng thái đóng/mở nắp laptop.
- Dựa trên cấu hình, `acpid` sẽ kích hoạt các kịch bản tương ứng (ví dụ: tự động chạy lệnh `poweroff` khi người dùng nhấn nút nguồn vật lý của thùng máy).

---

## 5. Thực hành: Cấu hình Default Boot Target

Để chuẩn bị cho kỳ thi LPIC-1, bạn cần nắm vững cách thay đổi default target cho một hệ điều hành Linux Systemd. Hãy thực hành theo các bước dưới đây:

### Các bước thực hành:

1.  **Kiểm tra default target hiện tại:**
    ```bash
    systemctl get-default
    # Kết quả thông thường: graphical.target (nếu có giao diện đồ họa)
    ```
2.  **Thay đổi mặc định sang chế độ dòng lệnh (CLI):**
    ```bash
    sudo systemctl set-default multi-user.target
    # Hệ thống sẽ tạo liên kết động (symlink) để chuyển hướng default.target
    ```
3.  **Kiểm tra lại xem cấu hình đã thay đổi chưa:**
    ```bash
    systemctl get-default
    # Kết quả sẽ hiển thị: multi-user.target
    ```
4.  **Thay đổi trở lại giao diện đồ họa (GUI) mặc định:**
    ```bash
    sudo systemctl set-default graphical.target
    # Hệ thống khôi phục mặc định ban đầu
    ```
