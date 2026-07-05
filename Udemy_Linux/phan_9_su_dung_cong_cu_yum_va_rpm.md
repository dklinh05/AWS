# Phần 9: Sử dụng công cụ YUM và RPM để quản lý gói phần mềm (RHEL / CentOS)

Tài liệu này hướng dẫn cách quản lý gói phần mềm (packages) trên các hệ điều hành họ Red Hat (như RHEL, CentOS, Fedora đời cũ) bằng công cụ quản lý cấp cao **YUM** và công cụ cấp thấp **RPM**. Ngoài ra, tài liệu còn bao gồm bài thực hành cài đặt và quản lý gói trên Debian/Ubuntu.

---

## 1. Trình quản lý gói cấp cao YUM (Yellowdog Updater, Modified)

**YUM** là trình quản lý gói mặc định trên các bản phân phối Linux như Red Hat Enterprise Linux (RHEL), CentOS, Scientific Linux và các phiên bản Fedora cũ. 

### Đặc điểm và Vai trò của YUM:
*   **Xử lý Dependencies tự động:** Tự động giải quyết và cài đặt các gói phụ thuộc (packages dependencies) từ các kho lưu trữ trực tuyến (repositories).
*   **Quản lý toàn diện:** Thực hiện cài đặt (installs), nâng cấp (upgrades) và gỡ bỏ (removes) các gói phần mềm một cách an toàn.

### Cấu hình hệ thống YUM (Yum Setup):
*   **Tệp cấu hình chính:** `/etc/yum.conf` chứa các thiết lập chung và tùy chọn toàn cục của YUM.
*   **Thư mục chứa kho lưu trữ:** `/etc/yum.repos.d/` chứa các tệp tin cấu hình (`.repo`) định nghĩa thông tin địa chỉ các kho lưu trữ (repository information).
*   **Thư mục bộ đệm (cache):** `/var/cache/yum` lưu trữ các dữ liệu tạm thời và thông tin kho lưu trữ được cập nhật mới nhất giúp tăng tốc độ truy vấn cục bộ.

### Các câu lệnh `yum` thông dụng:

| Câu lệnh | Chức năng | Chi tiết |
| :--- | :--- | :--- |
| **`yum update`** | Cập nhật hệ thống và gói phần mềm | Tìm kiếm các kho trực tuyến để cập nhật/nâng cấp các gói đã cài đặt. |
| **`yum search <từ_khóa>`** | Tìm kiếm gói phần mềm | Tìm gói cụ thể trong các kho lưu trữ trực tuyến dựa trên từ khóa. |
| **`yum info <tên_gói>`** | Hiển thị thông tin chi tiết gói | Xem thông tin mô tả, phiên bản, dung lượng, và nhà phát triển của gói. |
| **`yum list installed`** | Hiển thị các gói đã cài đặt | Liệt kê tất cả các gói phần mềm hiện tại đã cài đặt trên hệ điều hành. |
| **`yum clean all`** | Xóa bộ nhớ đệm (cache) | Xóa toàn bộ tệp bộ đệm của YUM và cơ sở dữ liệu cục bộ để giải phóng đĩa. |
| **`yum install <tên_gói>`** | Cài đặt gói mới | Tải và cài đặt gói phần mềm cùng toàn bộ các gói phụ thuộc (dependencies). |
| **`yum remove <tên_gói>`** | Gỡ bỏ gói phần mềm | Xóa gói được chỉ định ra khỏi hệ thống nhưng vẫn giữ lại các dependencies chung. |
| **`yum autoremove`** | Tự động dọn dẹp hệ thống | Gỡ bỏ gói đã chọn cùng các gói phụ thuộc không còn được ứng dụng nào sử dụng. |
| **`yum whatprovides <tên_file>`** | Tìm gói chứa file cụ thể | Xác định xem tệp tin hoặc đường dẫn cụ thể được cung cấp bởi gói phần mềm nào. |
| **`yum reinstall <tên_gói>`** | Cài đặt lại gói | Khôi phục hoặc cài đặt đè lại một gói phần mềm đang bị lỗi. |

---

## 2. Các công cụ quản lý gói RPM khác

Ngoài YUM, trong hệ sinh thái RPM-based Linux còn có các công cụ quản lý gói khác:

### Zypper
Được sử dụng chủ yếu trên các bản phân phối **SUSE Linux** (như openSUSE, SUSE Linux Enterprise Server).
*   *Xem danh sách kho lưu trữ:*
    ```bash
    zypper repos
    ```
*   *Cài đặt phần mềm (ví dụ: `vim`):*
    ```bash
    zypper install vim
    ```

### DNF (Dandified YUM)
Là thế hệ tiếp theo của YUM, khắc phục những hạn chế về hiệu năng và quản lý bộ nhớ của YUM cũ.
*   Được sử dụng mặc định trong các hệ điều hành **Fedora Linux** và **RHEL 8 / CentOS 8 trở lên**.
*   Trong tương lai và hiện tại, DNF thay thế hoàn toàn YUM trong các hệ thống Enterprise Linux (lệnh `yum` trên CentOS 8+ thực chất chỉ là một liên kết tượng trưng trỏ tới `dnf`).
*   **Cú pháp câu lệnh sử dụng giống hệt `yum`** (Ví dụ: `dnf install <package>`).

---

## 3. Trình quản lý gói cấp thấp RPM (Red Hat Package Manager)

**RPM** hoạt động ở cấp độ thấp hơn YUM. Nó làm việc trực tiếp với các tệp tin gói định dạng `.rpm`.

### Cấu trúc của một gói cài đặt `.rpm` gồm:
*   Ứng dụng hoặc tiện ích đã được biên dịch.
*   Các tệp tin cấu hình mặc định.
*   Các hướng dẫn cách thức và nơi cài đặt các tệp tin đi kèm vào hệ điều hành.
*   Liệt kê các gói phụ thuộc cần thiết (dependencies) mà gói này yêu cầu để có thể hoạt động.

### Cơ sở dữ liệu RPM (RPM Database):
*   Lưu trữ tại thư mục: `/var/lib/rpm`.
*   > [!TIP]
    > Sử dụng lệnh **`rpm --rebuilddb`** để xây dựng lại và sửa chữa cơ sở dữ liệu RPM trong trường hợp database này bị lỗi hoặc hỏng hóc.

### Sự khác biệt quan trọng về quản lý dependencies giữa YUM và RPM:
> [!IMPORTANT]
> - **YUM** tự động tìm kiếm, tải và cài đặt toàn bộ dependencies cho bạn thông qua internet.
> - **RPM** không tự xử lý dependencies. Khi cài đặt bằng RPM, nếu hệ thống thiếu gói phụ thuộc, RPM sẽ báo lỗi và dừng quá trình cài đặt lại, bắt buộc bạn phải cài thủ công các phụ thuộc trước.

### Các câu lệnh `rpm` thông dụng:

- **`rpm -qpi <file.rpm>`** (Query Package Info): Hiển thị thông tin mô tả chi tiết của một gói `.rpm` (khi tệp tin chưa được cài đặt).
- **`rpm -qpl <file.rpm>`** (Query Package List): Liệt kê danh sách tất cả các đường dẫn tệp tin sẽ được cài đặt từ gói `.rpm` đó.
- **`rpm -qa`** (Query All): Hiển thị toàn bộ danh sách các gói phần mềm đã được cài đặt trong hệ điều hành.
- **`rpm -i <file.rpm>`** (Install): Cài đặt một gói phần mềm cụ thể. Thường kết hợp với các tùy chọn tăng trải nghiệm đầu ra:
  ```bash
  rpm -ivh <file.rpm>  # i: install, v: verbose (chi tiết), h: hash (hiển thị tiến trình dạng dấu #)
  ```
- **`rpm -U <file.rpm>`** (Upgrade): Nâng cấp một gói đã cài đặt lên phiên bản mới nhất (nếu gói chưa có trên hệ thống, lệnh này sẽ cài đặt nó).
- **`rpm -e <tên_gói>`** (Erase/Gỡ bỏ): Xóa một gói phần mềm đã cài đặt khỏi hệ thống.
- **`rpm -Va`** (Verify All): Xác nhận và kiểm tra toàn bộ thuộc tính của tất cả các file của các gói đã cài đặt để phát hiện file nào bị sửa đổi.
- **`rpm2cpio`**: Chuyển đổi một file gói `.rpm` thành luồng lưu trữ định dạng `cpio` (thường dùng để giải nén xem nội dung file mà không cần cài đặt).
  *Ví dụ giải nén gói:*
  ```bash
  rpm2cpio name.rpm | cpio -idmv
  ```

---

## 4. Thực hành: Cài đặt và quản lý Gói trên Debian/Ubuntu

Cài đặt và gỡ bỏ các gói Packages trong Linux distribution là một kỹ năng quan trọng đối với một System Administrator. Trong phần này, chúng ta sẽ thực hành quản lý gói trên hệ điều hành Ubuntu/Debian sử dụng `apt` và `dpkg`.

### Bước 1: Cài đặt Apache Web Server
1. Cập nhật cơ sở dữ liệu gói phần mềm của hệ điều hành để đồng bộ danh sách mới nhất:
   ```bash
   sudo apt update
   ```
2. Thực hiện cài đặt dịch vụ Apache server (`apache2`) và tiện ích tải file (`wget`):
   ```bash
   sudo apt install apache2 wget
   ```

### Bước 2: Xác nhận trạng thái hoạt động của Apache Web Server
1. Sử dụng công cụ `curl` để gửi yêu cầu HTTP cục bộ xem Web Server phản hồi hay chưa:
   ```bash
   curl http://localhost
   ```
2. Tải về trang chủ mặc định của Apache và lưu kết quả vào một tệp tin trong thư mục home:
   *   Sử dụng lệnh `wget` kết hợp tùy chọn chỉ định tên file đầu ra là `local_index.response`:
       ```bash
       wget http://localhost -O local_index.response
       ```
   *   *(Lưu ý: Lệnh trên tương đương với việc chuyển hướng đầu ra tiêu chuẩn của wget nếu lấy nội dung trang web).*
