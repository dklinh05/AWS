- ec2 là một dịch vụ cung cấp khả năng tính toán có thể thay đổi dự trên kích thước
- giảm thời gian cần để khởi động => nhanh chóng scale lên và xuống
- trả cho những gì bạn xài

Task 1: launch ec2 instance: 
- enter name, chọn Amazon machine image (AMI - cung cấp thông tin cần để launch instance => template for root volume, launch permission which aws acc can use to launch instance, block device mapping that specifies the volumes to attach to the instance) 
- lots of instance type => phù hợp nhiều use case khác nhau. 
- t3.micro có 2 virtual CPUs và 1GiB memory
- chọn VPC, public subnet và SG (tọa rule traffic cho ec2)
- ec2 store data on a network-attached virtual disk called EBS

Task 2: monitor instance:
- watch system log => show output of the instance => tốt cho problem diagnosis, troubleshoot kernel problems và service configuration issues mà có thể khiến ec2 bị terminate/ unreachable .
- get instance screeshot => xem ec2 instance console như thế nào nếu một screen attach vào nó. Nếu ko thể reach instance qua ssh hoặc rdp, có thể chụp screenshot và xem => hiển thị status của instance => quicker troubleshoot.

Task 3: update SG và access web server. 
- thử truy cập public ipv4 ko dc => edit inbound rule để cho anywhere ipv4

Task 4: resize instance 
- stop instance => vào action chọn change instance type => chọn instance muốn đổi
- resize EBS => chọn và đổi size (GiB) muốn đổi
=> sau đó start instance lại

Test 5: Test termination protection 
- You can delete your instance when you no longer need it => terminating your instance. => cannot connect to or restart an instance after it has been terminated.
- unselect termination protection nếu muốn delete instance

Tổng kết: 
- stop is temporary, terminate is permanent
- enable termination protection if dont want accidentally delete instance





