# Phần 10: Ảo hóa và Container (Virtualization & Containers)

Tài liệu này cung cấp kiến thức nền tảng về ảo hóa (Virtualization), máy ảo (Virtual Machine), và công nghệ container (Containers) trên Linux, cùng các điểm khác biệt cốt lõi giữa hai công nghệ này.

---

## 1. Máy ảo (Virtual Machine - VM) là gì?
Máy ảo (VM) là một môi trường phần mềm mô phỏng một hệ thống máy tính cụ thể, hoạt động dựa trên kiến trúc và chức năng của một máy tính vật lý thật.

### Đặc điểm của Máy ảo:
*   **Mô phỏng đa dạng:** Có thể liên quan đến phần cứng vật lý, phần mềm chuyên dụng hoặc cả hai.
*   **Hệ điều hành lồng nhau:** Phần mềm ảo hóa cho phép bạn cài đặt một hệ điều hành (Guest OS - hệ điều hành khách) bên trong một hệ điều hành khác (Host OS - hệ điều hành chủ).
*   **Chia sẻ phần cứng:** Máy chủ vật lý và các máy ảo cùng chia sẻ chung một tài nguyên phần cứng vật lý giống nhau.
*   **Cách ly hoàn toàn:** Máy ảo bị cách ly hoàn toàn với phần cứng vật lý của máy chủ. Nó bắt buộc phải giao tiếp với phần cứng vật lý thông qua một lớp phần mềm quản lý gọi là **Hypervisor** (Trình giám sát máy ảo).

### Ví dụ về các Hypervisor phổ biến:
*   **KVM** (Kernel-based Virtual Machine)
*   **QEMU**
*   **VMware** (ESXi, Workstation)
*   **Xen**
*   **VirtualBox**

---

## 2. Căn bản về Máy ảo (Virtual Machine Basics)

### Phân loại ảo hóa (Virtualization Types)
*   **Full Virtualization (Ảo hóa toàn phần):**
    *   Hệ thống khách (Guest OS) hoàn toàn **không nhận biết** nó đang chạy trên một máy ảo.
    *   Hypervisor mô phỏng toàn bộ phần cứng vật lý cần thiết.
*   **Paravirtualization (Cận ảo hóa):**
    *   Hệ thống khách (Guest OS) **nhận biết** đây là một máy ảo.
    *   Guest OS sử dụng các driver đặc biệt (**Guest Drivers** như `virtio` trong KVM/QEMU) để tương tác hiệu quả hơn với Hypervisor.
    *   > [!TIP]
        > Máy ảo thực sự hoạt động tốt hơn và đạt hiệu năng cao hơn rất nhiều khi được cài đặt **guest drivers**.

### Quản lý nhân bản và mẫu (Clones & Templates)
*   Các máy ảo có thể được nhân bản (**cloned**) hoặc được lưu thành các mẫu (**templates**) để nhanh chóng triển khai các hệ thống mới mà không cần cài đặt lại từ đầu.
*   > [!WARNING]
    > Khi nhân bản hoặc sử dụng template, bạn có thể cần phải thay đổi **D-Bus machine ID** của máy ảo mới để đảm bảo tính duy nhất trong hệ thống và mạng.
    *   **Lệnh thực hiện:** `dbus-uuidgen --ensure` hoặc `dbus-uuidgen`
    *   **Mục đích:** Đảm bảo mỗi kernel đang chạy tương tác với một hệ điều hành có ID duy nhất.

---

## 3. Máy ảo trong môi trường Điện toán đám mây (Cloud)
*   Trong môi trường đám mây (AWS, Azure, Google Cloud), các máy ảo (Instance) được cung cấp sẵn từ nhà cung cấp dịch vụ điện toán đám mây.
*   Nếu sử dụng một máy ảo nhân bản (cloned virtual machine), công cụ **cloud-init** sẽ được kích hoạt khi khởi động lần đầu để đảm bảo dữ liệu người dùng (**user data**) được khởi tạo mới hoàn toàn.
*   **Các tác vụ phổ biến của `cloud-init`:**
    *   Tạo SSH keys mới cho các kết nối an sau.
    *   Đặt ngôn ngữ mặc định (Default Locale) của hệ điều hành.
    *   Đặt tên máy (Hostname) mới của hệ điều hành.
    *   Thiết lập các điểm gắn kết ổ đĩa (Mount points).
*   **Các nhà cung cấp đám mây phổ biến:**
    *   **AWS** (Amazon Web Services)
    *   **Azure** (Microsoft Azure)
    *   **Google Cloud** (Google Cloud Platform)

---

## 4. Container là gì?
Container là một tập hợp các gói (packages), thư viện (libraries) và/hoặc ứng dụng được đóng gói hoàn toàn tách biệt và hoạt động độc lập với môi trường xung quanh.

### Phân loại Container:
*   **Machine Container (System Container):** Chia sẻ chung một kernel và hệ thống tệp tin (file system) với máy chủ vật lý (host server). Trông giống như một OS độc lập nhưng nhẹ hơn VM rất nhiều (Ví dụ: LXD, systemd-nspawn).
*   **Application Container (Container ứng dụng):** Chia sẻ mọi thứ với hệ điều hành máy chủ trừ các files ứng dụng và các files thư viện phụ thuộc (libraries) mà ứng dụng đó trực tiếp yêu cầu để hoạt động (Ví dụ: Docker).

### Ví dụ về các công nghệ Container phổ biến:
*   **Docker**
*   **systemd-nspawn** (công cụ ảo hóa container gọn nhẹ của systemd)
*   **LXD**
*   **OpenShift**

---

## 5. So sánh Ảo hóa (Virtualization) và Container

| Tiêu chí | Ảo hóa (Virtualization / Virtual Machine) | Container (Docker, LXD, ...) |
| :--- | :--- | :--- |
| **Lớp trừu tượng** | Trừu tượng hóa ở cấp độ phần cứng (Hardware level). | Trừu tượng hóa ở cấp độ hệ điều hành (OS/Kernel level). |
| **Khởi động** | Chậm (mất vài phút vì phải khởi động toàn bộ Guest OS). | Cực nhanh (mất vài giây hoặc mili-giây vì chỉ chạy tiến trình ứng dụng). |
| **Tài nguyên** | Yêu cầu tài nguyên lớn (RAM/CPU) để chạy một OS đầy đủ. | Cực kỳ gọn nhẹ, sử dụng tài nguyên hiệu quả và chi tiết hơn. |
| **Cách ly (Isolation)** | Cách ly tuyệt đối bằng Hypervisor (Bảo vệ một OS khỏi OS khác). | Cách ly bằng Namespaces và Cgroups của Linux Kernel (Độ an toàn ở mức tương đối/cao). |

### Tại sao sự khác biệt này lại quan trọng?

#### Ảo hóa (Virtualization):
*   Phân chia và tách biệt hoàn toàn các máy chủ ảo với nhau.
*   Bảo vệ một hệ điều hành khỏi các lỗi hoặc tấn công từ một hệ điều hành khác trên cùng một phần cứng.
*   Ngăn chặn lãng phí tài nguyên phần cứng lớn của máy chủ vật lý.
*   **Nhược điểm:** Phải sử dụng trình Hypervisor để mô phỏng phần cứng máy ảo nên rất nặng về yêu cầu tài nguyên phần cứng.

#### Containers:
*   Sử dụng chia sẻ hệ điều hành Host, nâng cao tối đa hiệu quả sử dụng tài nguyên hệ thống.
*   Quản lý tài nguyên hệ thống chi tiết và linh hoạt hơn (fine-grained resource management).
*   Chia sẻ hạt nhân (kernel) chung với máy chủ host, giúp giảm đáng kể yêu cầu phần cứng so với ảo hóa.
*   Có thể triển khai, phân phối và chạy các ứng dụng nhanh chóng hơn bao giờ hết (phù hợp với mô hình CI/CD và Microservices).
