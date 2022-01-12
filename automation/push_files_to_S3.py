import os
import re
import boto3
import json

#Je n'avais pas d'address ip statique donc je devais la changer à chaque nouvelle instance EC2.
def replace_ip_address(new_ip_address):
    script_js_file = os.path.dirname(os.getcwd()) + '/website/script.js'
    file_read = open(script_js_file, 'rt')
    content = file_read.read()
    result = re.sub(r'(const server_ip =)("*.*.*.*)(")', '\g<1>' + "\"" + "http://" + new_ip_address + '\g<3>', content, 1)
    file_read.close()
    file_write = open(script_js_file, 'wt')
    file_write.write(result)
    file_write.close()

def upload_file(bucket, file_name, path_to_file):
    s3_client = boto3.client('s3')
    try:
        if str(file_name).endswith('.html'):
            s3_client.upload_file(path_to_file, bucket, file_name, ExtraArgs={'ContentType':'text/html'})
        else:
            s3_client.upload_file(path_to_file, bucket, file_name)
    except Exception as e:
        print(e)

def upload_web_site_folder_to_s3(bucket):
    website_dir = os.path.dirname(os.getcwd()) + '/website'
    for root, dirs, files in os.walk(website_dir):
        for file in files:
            upload_file(bucket, file, os.path.join(root, file))

def create_bucket(bucket_name, region):
    path_to_policy = os.path.dirname(os.getcwd()) + '/automation/policy_template.json'
    file = open(path_to_policy, 'r')
    policy_json = json.load(file)
    policy_json['Statement'][0]['Resource'] = 'arn:aws:s3:::' + bucket_name + '/*'
    file.close()
    policy_string = json.dumps(policy_json)
    try:
        s3_client = boto3.client('s3', region_name=region)
        s3_client.create_bucket(Bucket=bucket_name)
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
        website_configuration = {
            'IndexDocument': {'Suffix': 'home.html'},
        }
        s3_client.put_bucket_website(Bucket=bucket_name,
                                        WebsiteConfiguration=website_configuration)
        return True
    except Exception as e:
        print(e)
        return False