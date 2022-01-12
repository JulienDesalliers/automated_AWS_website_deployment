* Make sure that your aws credentials are in your ~/.aws folder.
* If you don't have Boto3, install it.
* Make sure that you have a security group that allows HTTP traffic on port 80 and that you know its name.
* Create or reuse an existing key for the EC2 instance.
* Choose a name for your bucket. Please note that the client access will be at the following adress: http:\\bucket_name.s3-website-us-east-1.amazonaws.com
* Change directory to the automation folder
* Launch the deployment with the following command: python3 deploy.py <YOUR_SECURITY_GROUP> <YOUR_KEY_NAME> <YOUR_BUCKET_NAME>