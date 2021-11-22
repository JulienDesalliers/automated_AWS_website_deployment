import sys
from ec2_starter import create_ec2_instance
from push_files_to_S3 import replace_ip_address, create_bucket, upload_web_site_folder_to_s3

if __name__ == "__main__":
    security_group = sys.argv[1]
    key_name = sys.argv[2]
    bucket_name = 'test-web-aut-tp3'
    # security_group = 'website-server-sc'
    # key_name = 'dev'
    server_ip_adress = create_ec2_instance("t2.micro", security_group, key_name)
    replace_ip_address(server_ip_adress)
    if(create_bucket(bucket_name, 'us-east-1')):
        upload_web_site_folder_to_s3(bucket_name)
        print("Your website was succesfully deployed. You can check it out here : http://" + bucket_name + ".s3-website-us-east-1.amazonaws.com/")
    else:
        print("There was an error creating the bucket so the upload was aborted")