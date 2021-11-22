import os
import re
import boto3
import json
import datetime
def replace_ip_address(new_ip_address):
    script_js_file = os.path.dirname(os.getcwd()) + '/website/script.js'
    file_read = open(script_js_file, 'rt')
    content = file_read.read()
    result = re.sub(r'(const server_ip =)("*.*.*.*)(")', '\g<1>' + "\"" + new_ip_address + '\g<3>', content, 1)
    file_read.close()
    file_write = open(script_js_file, 'wt')
    file_write.write(result)
    file_write.close()

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    home = os.path.dirname(os.getcwd()) + '/website/home.html'
    script = os.path.dirname(os.getcwd()) + '/website/script.js'
    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(home, bucket, object_name)
        response = s3_client.upload_file(script, bucket, object_name)
    except Exception as e:
        print(e)

def create_bucket(bucket_name, region):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """
    path_to_policy = os.path.dirname(os.getcwd()) + '/automation/policy_template.json'
    file = open(path_to_policy, 'r')
    policy_json = json.load(file)
    policy_json['Statement'][0]['Resource'] = 'arn:aws:s3:::' + bucket_name + '/*'
    file.close()
    policy_string = json.dumps(policy_json)
    # Create bucket
    try:
        print(region)
        s3_client = boto3.client('s3', region_name=region)
        location = {'LocationConstraint': region}
        s3_client.create_bucket(Bucket=bucket_name)
                                # CreateBucketConfiguration=location)
        s3_client.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': False,
                'IgnorePublicAcls': False,
                'BlockPublicPolicy': False,
                'RestrictPublicBuckets': False
            },
        )
        s3_client.put_bucket_policy(Bucket=bucket_name, Policy=policy_string)
    except Exception as e:
        print(e)

create_bucket('test-web-aut-tp3', 'us-east-1')
# print(upload_file('test', 'test-web-aut-tp3'))