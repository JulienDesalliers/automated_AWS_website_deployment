import sys
from ec2_starter import create_ec2_instance
from push_files_to_S3 import replace_ip_address
if __name__ == "__main__":
    security_group = sys.argv[1]
    key_name = sys.argv[2]
    # security_group = 'website-server-sc'
    # key_name = 'dev'
    server_ip_adress = create_ec2_instance("t2.micro", security_group, key_name)
    replace_ip_address(server_ip_adress)