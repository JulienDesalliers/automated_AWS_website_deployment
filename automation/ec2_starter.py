import boto3
from folder_parser import parse_folder_to_script
def create_ec2_instance(instance_type, name):
    user_data = "#!/bin/bash\nmkdir server\ncd server\nsudo apt update\nsudo apt install nodejs -y\n sudo apt install npm -y\n%s\nsudo npm i\nsudo node app.js\n"%parse_folder_to_script()
    try:
        ressource_ec2 = boto3.client("ec2")
        instances = ressource_ec2.run_instances(
            ImageId="ami-09e67e426f25ce0d7",
            MinCount=1,
            MaxCount=1,
            InstanceType=instance_type,
            KeyName="dev",
            SecurityGroups = ['website-server-sc'],
            UserData = user_data,
        )
        ec2 = boto3.client('ec2')
        instance_id = instances['Instances'][0]['InstanceId']
        ip_address = None
        while ip_address is None:
            try:
                ip_address = ec2.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]['PublicIpAddress']
            except:
                pass
        return ip_address
    except Exception as e:
        print(e)


server_ip_adress = create_ec2_instance("t2.micro", "server")
print(server_ip_adress)

