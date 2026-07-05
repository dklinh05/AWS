# Phần 11: Các lệnh cơ bản trong Linux

Tài liệu này giới thiệu các khái niệm và lệnh cơ bản khi làm việc với môi trường dòng lệnh Linux, đặc biệt là Bash shell. Nội dung bao gồm Linux shell, biến môi trường, hàm Bash, trích dẫn trong Bash, trang hướng dẫn `man`, lệnh `history` và tập tin `.bash_history`.

---

## 1. Làm việc với môi trường Bash Shell

### Linux Shell là gì?

**Shell** là môi trường dòng lệnh cho phép người dùng giao tiếp với hệ điều hành Linux. Thông qua shell, người dùng có thể nhập lệnh để quản lý file, thư mục, tiến trình, phần mềm, cấu hình hệ thống và nhiều tác vụ quản trị khác.

Một số loại shell phổ biến trong Linux:

| Shell | Tên đầy đủ / mô tả | Đặc điểm |
| :--- | :--- | :--- |
| `bash` | Bourne Again Shell | Shell mặc định trên nhiều bản phân phối Linux. |
| `csh` | C Shell | Có cú pháp lập trình gần giống ngôn ngữ C. |
| `ksh` | KornShell | Dựa trên Bourne shell và bổ sung một số tính năng của C shell. |
| `zsh` | Z Shell | Kết hợp nhiều tính năng của Bash shell và Korn shell. |

Trong thực tế, **Bash** là shell được sử dụng phổ biến nhất khi học và quản trị Linux.

---

## 2. Bash Environment

### Môi trường Bash là gì?

Môi trường Bash bao gồm các thiết lập, biến môi trường, hàm, alias và tùy chọn shell được sử dụng trong phiên làm việc dòng lệnh.

Các thiết lập này giúp quy định:

* Đường dẫn tìm kiếm chương trình.
* Vị trí thư mục làm việc.
* Cách shell xử lý lệnh.
* Các biến và hàm tùy chỉnh của người dùng.

---

## 3. Biến môi trường trong Bash

**Biến môi trường** là các biến lưu trữ thông tin cấu hình của shell hoặc hệ thống. Các biến này có thể được sử dụng bởi shell hiện tại hoặc các chương trình được chạy từ shell đó.

### Cú pháp khai báo biến

```bash
VARIABLE=value
```

Trong đó:

* `VARIABLE`: tên biến.
* `value`: giá trị được gán cho biến.

Ví dụ:

```bash
CWD=/home/user/Documents
```

Ví dụ trên tạo biến `CWD` có giá trị là đường dẫn `/home/user/Documents`.

> Lưu ý: Khi gán biến trong Bash, không đặt khoảng trắng trước và sau dấu `=`.

Ví dụ đúng:

```bash
NAME=Linux
```

Ví dụ sai:

```bash
NAME = Linux
```

---

## 4. Bash Function

Người dùng có thể tạo các hàm tùy chỉnh trong Bash để gom nhiều lệnh lại thành một lệnh duy nhất.

### Cú pháp tạo hàm

```bash
function ten_ham()
{
    lenh
}
```

Ví dụ:

```bash
function hello()
{
    echo "Hello World!!"
}
```

Sau khi định nghĩa hàm, có thể gọi hàm bằng tên:

```bash
hello
```

Kết quả:

```bash
Hello World!!
```

Hàm Bash thường được dùng để tự động hóa các thao tác lặp lại nhiều lần.

---

## 5. Các lệnh làm việc với Bash Environment

### Bảng lệnh cơ bản

| Lệnh | Chức năng |
| :--- | :--- |
| `env` | Hiển thị các biến môi trường. |
| `echo` | In nội dung hoặc giá trị của biến ra màn hình. |
| `set` | Hiển thị các thiết lập shell và biến shell trong phiên làm việc hiện tại. |
| `unset` | Xóa một biến hoặc một hàm Bash tùy chỉnh. |
| `shopt` | Hiển thị hoặc thay đổi các tùy chọn của shell. |
| `export` | Xuất biến để shell hiện tại và các shell con có thể sử dụng. |
| `pwd` | Hiển thị đường dẫn đầy đủ của thư mục làm việc hiện tại. |
| `which` | Tìm vị trí file thực thi của một chương trình nằm trong `PATH`. |
| `type` | Xác định một lệnh là alias, function, file thực thi, built-in hay keyword. |

### Ví dụ sử dụng

Hiển thị biến môi trường:

```bash
env
```

In giá trị của biến `PATH`:

```bash
echo $PATH
```

Hiển thị thư mục hiện tại:

```bash
pwd
```

Tìm vị trí của lệnh `ls`:

```bash
which ls
```

Kiểm tra loại của một lệnh:

```bash
type type
```

Kết quả có thể cho biết `type` là một lệnh tích hợp sẵn của shell.

Xuất một biến môi trường:

```bash
export COURSE=Linux
```

Xóa biến:

```bash
unset COURSE
```

---

## 6. Biến PATH trong Linux

`PATH` là một biến môi trường rất quan trọng. Biến này chứa danh sách các thư mục mà shell sẽ tìm kiếm khi người dùng nhập một lệnh.

Ví dụ:

```bash
echo $PATH
```

Kết quả có thể giống như sau:

```bash
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

Các thư mục trong `PATH` được phân cách bằng dấu hai chấm `:`.

Khi người dùng nhập lệnh:

```bash
ls
```

Shell sẽ tìm file thực thi `ls` trong các thư mục được liệt kê trong biến `PATH`.

---

## 7. Trích dẫn trong Bash

Trong Bash, trích dẫn ảnh hưởng đến cách shell xử lý biến và các ký tự đặc biệt.

### Trích dẫn yếu

Trích dẫn yếu sử dụng dấu ngoặc kép `" "`.

Bên trong dấu ngoặc kép:

* Biến vẫn được mở rộng.
* Một số ký tự đặc biệt dùng cho thay thế đường dẫn hoặc so khớp mẫu sẽ không được mở rộng theo cách thông thường.

Ví dụ:

```bash
echo "$PATH"
```

Lệnh trên sẽ in ra giá trị thật của biến `PATH`.

Ví dụ khác:

```bash
ls "*"
```

Lệnh này không liệt kê toàn bộ file trong thư mục hiện tại. Thay vào đó, `ls` sẽ tìm một file có tên chính xác là `*`.

### Trích dẫn mạnh

Trích dẫn mạnh sử dụng dấu ngoặc đơn `' '`.

Bên trong dấu ngoặc đơn:

* Biến không được mở rộng.
* Lệnh không được thực thi.
* Nội dung được giữ nguyên.

Ví dụ:

```bash
echo '$PATH'
```

Kết quả:

```bash
$PATH
```

Điểm khác biệt quan trọng:

| Câu lệnh | Kết quả |
| :--- | :--- |
| `echo "$PATH"` | In giá trị của biến `PATH`. |
| `echo '$PATH'` | In nguyên văn chuỗi `$PATH`. |

---

## 8. Trang hướng dẫn man page trong Linux

Linux cung cấp hệ thống tài liệu hướng dẫn tích hợp sẵn gọi là **manual page**, thường được gọi ngắn gọn là **man page**.

Man page dùng để tra cứu:

* Cách sử dụng lệnh.
* Ý nghĩa các tùy chọn của lệnh.
* File cấu hình.
* System calls.
* Library calls.
* Các tác vụ quản trị hệ thống.

### Cú pháp sử dụng

```bash
man ten_lenh
```

Ví dụ:

```bash
man ls
```

Lệnh trên mở trang hướng dẫn của lệnh `ls`.

---

## 9. Các phần trong man page

Trang hướng dẫn trong Linux được chia thành nhiều phần khác nhau.

| Phần | Nội dung |
| :--- | :--- |
| 1 | Các chương trình thực thi hoặc lệnh dòng lệnh. |
| 2 | System calls, tức các hàm được cung cấp bởi kernel. |
| 3 | Library calls, tức các hàm trong thư viện chương trình. |
| 4 | Special files, thường nằm trong thư mục `/dev`. |
| 5 | Định dạng và quy ước file, ví dụ `/etc/passwd`. |
| 6 | Trò chơi. |
| 7 | Các mục và quy ước đa dạng, ví dụ `man(7)`, `regex(7)`. |
| 8 | Các lệnh quản trị hệ thống, thường dành cho `root`. |
| 9 | Các thủ tục kernel, không chuẩn trên mọi hệ thống. |

### Mở một phần cụ thể của man page

Cú pháp:

```bash
man section ten_lenh
```

Ví dụ:

```bash
man 5 passwd
```

Lệnh trên mở phần 5 của man page liên quan đến định dạng file `passwd`.

---

## 10. Các lệnh tìm kiếm man page

### Lệnh `man`

Dùng để mở trang hướng dẫn cho một lệnh cụ thể.

```bash
man pwd
```

### Lệnh `man -k`

Dùng để tìm kiếm các trang hướng dẫn theo từ khóa.

```bash
man -k passwd
```

### Lệnh `apropos`

`apropos` có chức năng tương tự `man -k`, dùng để tìm các trang hướng dẫn liên quan đến một từ khóa.

```bash
apropos passwd
```

### Mở man page theo số chương

```bash
man 1 passwd
man 5 passwd
```

Trong đó:

* `man 1 passwd` thường nói về lệnh `passwd`.
* `man 5 passwd` thường nói về định dạng file cấu hình liên quan đến `passwd`.

---

## 11. Lệnh history

`history` là lệnh tích hợp sẵn trong Bash shell, dùng để hiển thị danh sách các lệnh đã được thực thi trước đó.

Ví dụ:

```bash
history
```

Theo mặc định, Bash thường hiển thị khoảng 500 lệnh gần đây nhất trong phiên làm việc terminal hiện tại. Giá trị này có thể thay đổi tùy cấu hình hệ thống.

### Chạy lại lệnh trong history

Chạy lại lệnh theo số thứ tự:

```bash
!25
```

Chạy lại lệnh gần nhất:

```bash
!!
```

Tìm các lệnh đã chạy có chứa từ khóa:

```bash
history | grep ssh
```

---

## 12. Tập tin `.bash_history`

`.bash_history` là tập tin văn bản nằm trong thư mục home của người dùng. Tập tin này lưu trữ lịch sử các lệnh đã được thực thi trong các phiên làm việc terminal.

Đường dẫn thường gặp:

```bash
~/.bash_history
```

Xem nội dung file:

```bash
cat ~/.bash_history
```

Tập tin này thường được cập nhật khi người dùng kết thúc phiên terminal hoặc khi Bash ghi lịch sử lệnh xuống file.

---

## 13. Biến HISTFILESIZE

`HISTFILESIZE` là biến môi trường xác định số lượng dòng lệnh tối đa có thể được lưu trong file `.bash_history`.

Kiểm tra giá trị hiện tại:

```bash
echo $HISTFILESIZE
```

Ví dụ đặt lại giá trị:

```bash
HISTFILESIZE=1000
```

Để thiết lập lâu dài, có thể thêm dòng cấu hình vào file `~/.bashrc` hoặc `~/.bash_profile`:

```bash
export HISTFILESIZE=1000
```

Sau đó nạp lại file cấu hình:

```bash
source ~/.bashrc
```

---

## 14. Bài thực hành nhanh

Thực hiện các lệnh sau trong terminal Linux:

```bash
pwd
echo $PATH
env
which bash
type cd
type ls
man pwd
man -k passwd
apropos history
history
echo "$PATH"
echo '$PATH'
```

Quan sát sự khác nhau giữa:

```bash
echo "$PATH"
```

và:

```bash
echo '$PATH'
```

---

## 15. Tổng kết

Trong phần này, bạn đã học các nội dung cơ bản sau:

* Shell là môi trường dòng lệnh để làm việc với hệ điều hành Linux.
* Bash là shell phổ biến và thường được dùng mặc định.
* Biến môi trường lưu trữ các thiết lập quan trọng của shell và hệ thống.
* Có thể tạo hàm tùy chỉnh trong Bash để tự động hóa thao tác.
* Các lệnh `env`, `echo`, `set`, `unset`, `shopt`, `export`, `pwd`, `which`, `type` giúp kiểm tra và quản lý môi trường Bash.
* Dấu ngoặc kép `" "` cho phép mở rộng biến, còn dấu ngoặc đơn `' '` giữ nguyên nội dung.
* `man`, `man -k` và `apropos` dùng để tra cứu tài liệu hướng dẫn trong Linux.
* `history` hiển thị lịch sử lệnh đã dùng.
* `.bash_history` lưu lịch sử lệnh trong thư mục home của người dùng.
* `HISTFILESIZE` quy định số dòng lệnh tối đa được lưu trong `.bash_history`.
