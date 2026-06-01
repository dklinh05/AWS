- cloudfront is a content delivery web that intefrate with other AWS products => used to distribute content to end users with low latency, high data transfer
- content is stored in edge location => nearest edge location delivers content to end user
- nếu content ko cache ở edge location => edge location ask for origin server (such as S3); nếu cache thì deliver immediately

task 1: create s3 bucket and store image file
- tạo s3 block public access và up ảnh lên 

task 2: create cloudfront web distribution
- create distribution => pay as you go
- origin domain: choose s3 bucket
- enable security (WAF) => enable hoặc ko

task 3: test the distribution
- tạo html code gán cloudfront vào, thay tên object = tên s3
- thử mở, tắt, mở lại => nhanh hơn vì dc cache ở edge location

