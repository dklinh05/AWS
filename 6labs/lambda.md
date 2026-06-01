- AWS Lambda is a compute service that runs your code in response to events and automatically manages the compute resources, making it easy to build applications that respond quickly to new information.
- AWS Lambda starts running your code within milliseconds of an event such as an image upload, in-app activity, website click, or output from a connected device. 
- AWS Lambda also used to create new back-end services where compute resources are automatically triggered based on custom requests.

task 1: create amazon s3 bucket
- create 2 buckets, 1 for raw bucket and another for processed bucket for resizing
- upload a file to the raw bucket

task 2: create aws lambda function
-create an AWS Lambda function that reads an image from Amazon S3, resizes the image, and then stores the new image in Amazon S3.
- custom execution role for lambda to read and write images
- select SG for lambda SG
- add trigger for lambda: select s3 bucket which is CreateThumbnail => name the handler CreateThumbnail.handler

task 3: test your function
- in the Test tab, create a new event named 'Upload' using the 'S3 Put' template
- update the event JSON:
  - replace both occurrences of 'example-bucket' with the raw images bucket name
  - replace 'test%2Fkey' with the image file name (e.g., 'HappyFace.jpg')
- click Test and check if it succeeds
- go to the resized bucket in S3 and open 'HappyFace.jpg' to verify it has been resized successfully

task 4: monitor and logging
- open the Monitor tab of the Lambda function to check metrics (Invocations, Duration, Errors, etc.)
- click 'View CloudWatch logs' and select the latest log stream
- inspect the log messages to see details like duration, memory usage, request ID, and print statements for debugging


