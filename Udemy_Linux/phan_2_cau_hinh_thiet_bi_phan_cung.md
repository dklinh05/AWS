# Phần 2: Cấu hình Thiết bị Phần cứng trên Linux

Tài liệu này tổng hợp các kiến thức cơ bản về cách hệ điều hành Linux quản lý và cấu hình các thiết bị phần cứng, bao gồm hệ thống file ảo (pseudo file system), nhân Linux (kernel), các dịch vụ quản lý thiết bị, và các câu lệnh kiểm tra thông tin phần cứng.


---

## 1. Hệ thống File (File System) & Pseudo File System

Hệ điều hành Linux quản lý mọi thứ (kể cả thiết bị phần cứng) dưới dạng file. Chúng ta phân biệt hai loại hệ thống file chính:

### Hệ thống File bình thường (Regular File System)
- Là phương pháp sắp xếp, lưu trữ và quản lý các file/thư mục trên **ổ cứng vật lý** (HDD, SSD, USB...).
- Là một tập hợp các file và thư mục nằm trên một phân vùng (partition) cụ thể đã được định dạng (format) bằng các định dạng như `ext4`, `xfs`, `btrfs`, v.v.

### Hệ thống File ảo (Pseudo File System)
- **Pseudo** có nghĩa là giả hoặc ảo. Các file này **không tồn tại trên ổ cứng vật lý**.
- Chúng chỉ tồn tại trong bộ nhớ **RAM** khi hệ điều hành đang chạy và sẽ biến mất khi tắt máy.
- Đóng vai trò là cầu nối giúp người dùng và các ứng dụng tương tác trực tiếp với Kernel và phần cứng thông qua các thao tác đọc/ghi file thông thường.

Hai thư mục pseudo quan trọng nhất liên quan đến phần cứng:
- **`/proc`**: Chứa thông tin về các tiến trình (processes) đang chạy trong hệ thống (được liệt kê theo mã tiến trình **PID**). Ngoài ra, nó cũng chứa dữ liệu cấu hình phần cứng và tiến trình của hệ điều hành.
- **`/sys`**: Chứa thông tin chi tiết về phần cứng (devices), driver và các module hạt nhân (kernel modules) của hệ điều hành. Thư mục này **không** chứa thông tin về các tiến trình (process) như `/proc`.

---

## 2. Linux Kernel (Nhân Linux)

Kernel là thành phần cốt lõi (core framework) của hệ điều hành Linux.

### Vai trò của Kernel
- Cung cấp giao diện trung gian cho phép các phần mềm và ứng dụng giao tiếp, điều khiển phần cứng được kết nối với máy tính.
- Linux sử dụng kiến trúc **Monolithic Kernel** (Nhân nguyên khối), nghĩa là tất cả các dịch vụ cốt lõi (quản lý bộ nhớ, tiến trình, hệ thống file, và trình điều khiển thiết bị) đều chạy chung trong một không gian bộ nhớ của nhân (kernel space) để đạt hiệu năng tối đa.

### Kernel Module
- Để tránh việc kernel quá cồng kềnh hoặc phải biên dịch lại mỗi khi có phần cứng mới, Linux sử dụng cơ chế **Kernel Module**.
- Các chức năng bổ sung hoặc trình điều khiển thiết bị (device drivers) có thể được **tải (load) hoặc gỡ bỏ (unload)** động vào kernel khi hệ thống đang chạy.
- Cơ chế này đảm bảo hệ điều hành **không cần phải khởi động lại (reboot)** để áp dụng cấu hình mới hoặc nhận thiết bị mới.
- Hầu hết các trình điều khiển thiết bị (device drivers) từ bên thứ ba đều được đóng gói dưới dạng các Linux kernel modules.

---

## 3. Các lệnh làm việc với Linux Kernel

Dưới đây là các câu lệnh phổ biến dùng để kiểm tra và quản lý nhân Linux cùng các module của nó:

| Câu lệnh | Chức năng | Ví dụ / Ghi chú |
| :--- | :--- | :--- |
| **`uname`** | Hiển thị thông tin về hệ thống và kernel đang chạy. | Sử dụng `uname -r` để xem phiên bản kernel cụ thể. |
| **`lsmod`** | Hiển thị danh sách tất cả các kernel modules hiện đang được tải (load) vào bộ nhớ. | Xuất ra các cột: Module name, Size, và Used by. |
| **`modinfo`** | Hiển thị thông tin chi tiết về một kernel module cụ thể. | Ví dụ: `modinfo <tên_module>` (xem tác giả, bản quyền, mô tả...). |
| **`modprobe`** | Tải (load) hoặc gỡ bỏ (unload) các kernel modules một cách an toàn. | - Để tải module: `modprobe <tên_module>` <br> - Để gỡ module: `modprobe -r <tên_module>` |

---

## 4. Quản lý Thiết bị trong Linux: `/dev`, `udev` và `D-Bus`

Hệ thống Linux tự động nhận diện và quản lý thiết bị thông qua sự phối hợp của ba thành phần sau:

### `/dev` (Devices)
- Thư mục chứa các file thiết bị đại diện cho **tất cả các phần cứng** được kết nối vào hệ thống (ví dụ: ổ cứng `/dev/sda`, chuột, bàn phím, card âm thanh...).
- Các chương trình tương tác với phần cứng bằng cách đọc hoặc ghi vào các file tương ứng trong thư mục này.

### `udev` (Device Manager)
- Là **trình quản lý thiết bị** chạy trong không gian người dùng (user-space) của Linux.
- Khi có một thiết bị phần cứng được kết nối hoặc ngắt kết nối, kernel sẽ gửi thông báo đến `udev`.
- `udev` dựa vào các quy tắc cấu hình (rules) để tự động tạo hoặc xóa các file thiết bị tương ứng trong thư mục `/dev`, đồng thời đặt tên và phân quyền cho chúng.

### `D-Bus` (Desktop Bus)
- Là một hệ thống nhắn tin trung gian (message bus) giúp truyền dữ liệu và thông điệp giữa các ứng dụng và tiến trình khác nhau trong hệ thống.
- **Sự kết hợp:** Khi một phần cứng mới được cắm vào (ví dụ: USB), `udev` nhận diện được và sử dụng `D-Bus` để phát đi một thông điệp rộng rãi. Nhờ đó, giao diện người dùng (như màn hình desktop) hoặc các ứng dụng khác có thể biết ngay lập tức để hiển thị thông báo hoặc tự động mount ổ đĩa USB đó.

---

## 5. Các câu lệnh kiểm tra thông tin phần cứng

Để xem nhanh thông tin chi tiết của từng loại linh kiện phần cứng cụ thể cắm trên máy tính, bạn sử dụng nhóm lệnh sau:

*   **`lspci`**: Hiển thị thông tin về các thiết bị kết nối qua khe cắm **PCI/PCIe** (như card đồ họa VGA, card mạng LAN/Wifi, card âm thanh...).
*   **`lsusb`**: Hiển thị danh sách và thông tin về các thiết bị kết nối qua cổng **USB** (chuột, bàn phím, USB drive, webcam...).
*   **`lscpu`**: Hiển thị chi tiết cấu trúc bộ vi xử lý **CPU** (số nhân, số luồng, kiến trúc x86/ARM, các mức bộ nhớ đệm cache...).
*   **`lsblk`**: Liệt kê thông tin dạng sơ đồ cây về các thiết bị khối (block devices) như **ổ cứng** (HDD, SSD) và các phân vùng hiện có của chúng.
